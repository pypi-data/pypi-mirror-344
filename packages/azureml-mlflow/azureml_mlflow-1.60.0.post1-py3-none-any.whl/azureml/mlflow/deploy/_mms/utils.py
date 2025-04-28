# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from copy import deepcopy
import json
import logging
import os
import tempfile
from urllib.parse import urljoin

from azure.core.polling import LROPoller
from azureml.mlflow._restclient.mms.models import ModelEnvironmentDefinition, ModelPythonSection,\
    DockerImagePlatform, ModelDockerSection
from azureml.mlflow.deploy._mms.polling.mms_poller import MMSOperationResourcePolling, MMSPolling
from azureml.mlflow.deploy._util import load_pyfunc_conf, get_deployments_import_error
from mlflow.exceptions import MlflowException
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
from mlflow.utils.file_utils import _copy_file_or_tree


_logger = logging.getLogger(__name__)


DEFAULT_CONDA_FILE = """
name: project_environment
dependencies:
  # The python interpreter version.
  # Currently Azure ML only supports 3.5.2 and later.
  - python=3.6.2

  - pip:
    # Required packages for AzureML execution, history, and data preparation.
    - azureml-defaults

channels:
  - anaconda
  - conda-forge
"""


INFERENCE_REQUIRED_PACKAGE_LIST = ["azureml-inference-server-http~=0.6.1"]


def _base_images_current_tags():
    images = {}
    current_base_images_file = os.path.join(os.path.dirname(__file__), "azureml_base_images.json")
    if os.path.exists(current_base_images_file):
        try:
            with open(current_base_images_file) as file:
                images = json.loads(file.read())
        except Exception:
            pass
    return images


def _get_tagged_image(image_name, default_tag=None):
    """
    Return tagged image from azureml_base_images.json, pin to default_tag if missing, else as is
    """
    images = _base_images_current_tags()
    tag = images.get(image_name, None)
    if tag:
        return image_name + ":" + tag
    else:
        return image_name + ((":" + default_tag) if default_tag else "")


def get_default_base_image():
    return _get_tagged_image("mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04")


def wrap_execution_script(execution_script):
    """
    Wrap the user's execution script in our own in order to provide schema validation.
    :param execution_script: str path to execution script
    :param schema_file: str path to schema file
    :param dependencies: list of str paths to dependencies
    :return: str path to wrapped execution script
    """
    new_script_loc = tempfile.mkstemp(suffix='.py')[1]

    execution_script = os.path.join(execution_script).replace(os.sep, '/')

    return generate_main(execution_script, new_script_loc)


def generate_main(user_file, main_file_name, source_directory=None):
    """
    :param user_file: str path to user file with init() and run()
    :param main_file_name: str full path of file to create
    :return: str filepath to generated file
    """

    data_directory = os.path.join(os.path.dirname(__file__), '_template')
    source_directory_import = ''
    if source_directory:
        source_directory_import = "sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), {}))" \
            .format(repr(source_directory))
    main_template_path = os.path.join(data_directory, 'main_template.txt')

    with open(main_template_path) as template_file:
        main_src = template_file.read()

    main_src = main_src.replace('<user_script>', user_file) \
        .replace('<source_directory_import>', source_directory_import)
    with open(main_file_name, 'w') as main_file:
        main_file.write(main_src)
    return main_file_name


def create_inference_env_and_entry_script(tmp_dir, model_name, model_version, service_name):
    """
    Create the InferenceConfig object which will be used to deploy.

    :param tmp_dir:
    :type tmp_dir:
    :param model_name:
    :type model_name:
    :param model_version:
    :type model_version:
    :param service_name:
    :type service_name:
    :return:
    :rtype:
    """
    try:
        from mlflow import pyfunc
        from mlflow.models import Model

        from mlflow.models.model import MLMODEL_FILE_NAME
    except ImportError as exception:
        raise get_deployments_import_error(exception)

    try:
        import pandas
    except ImportError:
        _logger.warning("Unable to import pandas")

    try:
        import numpy as np
    except ImportError:
        _logger.warning("Unable to import numpy")

    absolute_model_path = _download_artifact_from_uri('models:/{}/{}'.format(model_name, model_version))
    model_folder = absolute_model_path.split(os.path.sep)[-1]
    model_directory_path = tmp_dir.path("model")
    tmp_model_path = os.path.join(
        model_directory_path,
        _copy_file_or_tree(src=absolute_model_path, dst=model_directory_path),
    )

    # Create environment
    env_name = service_name + "-env"
    env_name = env_name[:32]
    mlflow_model = Model.load(os.path.join(absolute_model_path, MLMODEL_FILE_NAME))

    model_pyfunc_conf = load_pyfunc_conf(mlflow_model)
    if pyfunc.ENV in model_pyfunc_conf:
        if isinstance(model_pyfunc_conf[pyfunc.ENV], dict) and 'conda' in model_pyfunc_conf[pyfunc.ENV]:
            env_file_path = model_pyfunc_conf[pyfunc.ENV]['conda']
        else:
            env_file_path = model_pyfunc_conf[pyfunc.ENV]

        environment = create_environment_from_conda_file(
            env_name,
            os.path.join(tmp_model_path, env_file_path)
        )
    else:
        raise MlflowException('Error, no environment information provided with model')

    sample_input = None
    sample_output = None
    input_sample_json = None

    model_folder = absolute_model_path.split(os.path.sep)[-1]
    # If a sample input is provided, load this input and use this as the sample input to create the
    # scoring script and inference-schema decorators instead of creating a sample based on just the
    # signature information
    try:
        if mlflow_model.saved_input_example_info:
            sample_input_file_path = os.path.join(absolute_model_path,
                                                  mlflow_model.saved_input_example_info['artifact_path'])
            with open(sample_input_file_path, 'r') as sample_input_file:
                input_sample_json = json.load(sample_input_file)
                input_example_type = mlflow_model.saved_input_example_info["type"]
                if input_example_type == "ndarray":
                    input_sample_json = input_sample_json["inputs"]
                if input_example_type != "dataframe":
                    _logger.info('Sample model input must be of type "dataframe" or "ndarray"')
    except Exception:
        _logger.info(
            "Unable to read sample input. Creating sample input based on model signature."
            "For more information, please see: https://aka.ms/aml-mlflow-deploy."
        )

    def create_tensor_spec_sample_io(model_signature_io, input_sample_json=None):
        # Create a sample numpy.ndarray based on shape/type of the tensor info of the model
        io = model_signature_io.inputs
        if not model_signature_io.has_input_names():
            sample_io = np.array([])
            # If the input is not a named tensor, the sample io value that we create will just be a numpy.ndarray
            if input_sample_json is not None:
                # If sample input is provided, create a numpy array from it with the typing information
                # found in the model's input signature
                dtype = io[0].type
                if dtype.name == 'str':
                    # String types in numpy are saved with an exact character length. Change to an object
                    # type to not truncate strings when doing type conversion in InferenceSchema
                    dtype = np.dtype('object')
                sample_io = np.asarray(input_sample_json, dtype=dtype)
            else:
                shape = io[0].shape
                if shape:
                    shape = list(deepcopy(shape))
                    variable_dims = False
                    for index, dim in enumerate(shape):
                        # -1 for a dimensions means that the size of the data can vary.
                        # For the sake of swagger handling we'll set these dimensions to 1
                        if dim == -1:
                            variable_dims = True
                            shape[index] = 1
                    dtype = io[0].type
                    if variable_dims or dtype.name == 'str':
                        dtype = np.dtype('object')
                    sample_io = np.zeros(tuple(shape), dtype=dtype)
        else:
            # otherwise, the input is a named tensor, so the sample io value that we create will be
            # Dict[str, numpy.ndarray], which maps input name to a numpy.ndarray of the corresponding size
            sample_io = {}
            for io_val in io:
                if input_sample_json is not None:
                    dtype = io_val.type
                    if dtype.name == 'str':
                        # String types in numpy are saved with an exact character length. Change to an object
                        # type to not truncate strings when doing type conversion in InferenceSchema
                        dtype = np.dtype('object')
                    sample_io[io_val.name] = np.asarray(input_sample_json[io_val.name], dtype=dtype)
                else:
                    shape = io_val.shape
                    if shape:
                        shape = list(deepcopy(shape))
                        variable_dims = False
                        for index, dim in enumerate(shape):
                            # -1 for a dimensions means that the size of the data can vary.
                            # For the sake of swagger handling we'll set these dimensions to 1
                            if dim == -1:
                                variable_dims = True
                                shape[index] = 1
                        dtype = io_val.type
                        if variable_dims or dtype.name == 'str':
                            dtype = np.dtype('object')
                        sample_io[io_val.name] = np.zeros(tuple(shape), dtype=dtype)
        return sample_io

    def create_col_spec_sample_io(model_signature_io, input_sample_json=None):
        try:
            columns = model_signature_io.input_names()
        except AttributeError:  # MLflow < 1.24.0
            columns = model_signature_io.column_names()
        types = model_signature_io.pandas_types()
        schema = {}
        for c, t in zip(columns, types):
            schema[c] = t

        # Create a sample pandas.DataFrame based on shape/type of the tensor info of the model
        if input_sample_json is not None:
            # If sample input is provided, create a pandas.Dataframe from it with the typing information
            # found in the model's input signature using mlflow's parser
            df = pandas.read_json(
                json.dumps(input_sample_json),
                orient=mlflow_model.saved_input_example_info['pandas_orient'],
                dtype=False
            )
        else:
            df = pandas.DataFrame(columns=columns)

        return df.astype(dtype=schema)

    model_signature = mlflow_model.signature
    if mlflow_model.signature:
        # If a signature is provided, use it to create sample inputs/outputs
        # with the input/output typing information. If a sample input is provided,
        # it will be parsed into either a numpy.ndarray or pandas.Dataframe, and the
        # signature will be used for setting the correct type(s) of the ndarray/Dataframe.
        model_signature_inputs = model_signature.inputs
        model_signature_outputs = model_signature.outputs
        if model_signature_inputs:
            if model_signature_inputs.is_tensor_spec():
                sample_input = create_tensor_spec_sample_io(
                    model_signature_inputs,
                    input_sample_json=input_sample_json
                )
            else:
                sample_input = create_col_spec_sample_io(
                    model_signature_inputs,
                    input_sample_json=input_sample_json
                )

        if model_signature_outputs and sample_output is None:
            if model_signature_outputs.is_tensor_spec():
                sample_output = create_tensor_spec_sample_io(model_signature_outputs)
            else:
                sample_output = create_col_spec_sample_io(model_signature_outputs)
    else:
        # If no signature is provided, we don't know the typing of the inputs/outputs, so we cannot
        # create a swagger for the model. Even if a sample input is provided, we cannot use it
        # without signature information as the default type inferred from the json may not match
        # what the model is expecting.
        _logger.warning(
            "No signature information provided for model. "
            "The deployment's swagger will not include input and output schema and typing information."
            "For more information, please see: https://aka.ms/aml-mlflow-deploy."
        )

    # Create execution script
    execution_script_path = tmp_dir.path("execution_script.py")
    create_execution_script(execution_script_path, model_folder, sample_input, sample_output)

    # Setting entry script related env vars
    if environment.environment_variables is None:
        environment.environment_variables = {}
    environment.environment_variables['AZUREML_ENTRY_SCRIPT'] = \
        os.path.join(execution_script_path).replace(os.sep, '/')

    # Create InferenceConfig
    # inference_config = InferenceConfig(entry_script=execution_script_path, environment=environment)

    return execution_script_path, environment


def create_environment_from_conda_file(name, conda_file_path=None):
    import yaml

    conda_file_contents = None
    if conda_file_path:
        with open(conda_file_path, "r") as f:
            conda_file_contents = yaml.safe_load(f)

    environment = _create_base_environment(name)
    if conda_file_contents is None:
        conda_file_contents = yaml.safe_load(DEFAULT_CONDA_FILE)

    # Add Inference dependencies
    conda_file_contents = _add_pip_packages(conda_file_contents, INFERENCE_REQUIRED_PACKAGE_LIST)
    # TODO: Add check if mlflow exists do not add it. It is causing env build failure
    # conda_file_contents = _add_pip_packages(conda_file_contents, ["mlflow=={}".format(mlflow_version)])

    environment.python.conda_dependencies = conda_file_contents

    return environment


def _add_pip_packages(conda_dependencies, pip_packages):
    dependencies = conda_dependencies["dependencies"]
    pip_found = False
    for dep in dependencies:
        if "pip" in dep and isinstance(dep, dict):
            dep["pip"].extend(pip_packages)
            pip_found = True
    if not pip_found:
        dependencies.append({"pip": pip_packages})
    return conda_dependencies


def _create_base_environment(name):
    environment = ModelEnvironmentDefinition(name=name)

    # Creating python section
    interpreter_path = "python"
    user_managed_dependencies = False
    conda_dependencies = None
    base_conda_environment = None  # TODO: Check if this is set in Environment Image Request for v1 deployment

    environment.python = ModelPythonSection(
        interpreter_path=interpreter_path,
        user_managed_dependencies=user_managed_dependencies,
        conda_dependencies=conda_dependencies,
        base_conda_environment=base_conda_environment
    )

    # Creating docker section
    # TODO : AML SDK adds tag to pick a specific version. Tags are updated with each release. Need to check how to
    # reconcile it or okay to use default tag

    base_image = None
    platform = DockerImagePlatform(os="Linux", architecture="amd64")
    base_dockerfile = """\
FROM {base_image}
ENV AZUREML_INFERENCE_SERVER_HTTP_ENABLED=true
""".format(base_image=get_default_base_image())

    base_image_registry = None

    environment.docker = ModelDockerSection(
        base_image=base_image,
        platform=platform,
        base_dockerfile=base_dockerfile,
        base_image_registry=base_image_registry
    )

    return environment


def create_execution_script(output_path, model_folder, sample_input, sample_output):
    """
    Create the execution script which will be used to deploy.

    Creates an Azure-compatible execution script (entry point) for a model server backed by
    the specified model. This script is created as a temporary file in the current working
    directory.

    :param output_path: The path where the execution script will be written.
    :param model_folder: The folder containing the model files
    :param model_version: The version of the model to load for inference
    :param sample_input: A sample input dataframe, numpy.ndarray, or Dict[str, numpy.ndarray],
        if we could parse one from the MLFlow Model object
    :param sample_output: A sample output dataframe, numpy.ndarray, or Dict[str, numpy.ndarray],
        if we could parse one from the MLFlow Model object
    :return: A reference to the temporary file containing the execution script.
    """
    try:
        import numpy as np
        from numpy import dtype
        from pandas import StringDtype
        string_d_type_imported = True
    except ImportError:
        string_d_type_imported = False
    INIT_SRC = """\
import json
import os
import pandas as pd
import numpy as np
from numpy import dtype

from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.standard_py_parameter_type import StandardPythonParameterType
from inference_schema.schema_decorators import input_schema, output_schema
from mlflow.pyfunc import load_model
from mlflow.pyfunc.scoring_server import _get_jsonable_obj

def init():
    global model

    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), '{model_folder}')
    model = load_model(model_path)
""".format(model_folder=model_folder)
    RUN_WITH_INFERENCE_SCHEMA_SRC = """\
def run(input_data):
    return _get_jsonable_obj(model.predict(input_data), pandas_orient="records")
"""
    RUN_WITHOUT_INFERENCE_SCHEMA_SRC = """\
def run(input_data):
    input_data = json.loads(input_data)
    input_data = input_data['input_data']
    if isinstance(input_data, list):
        # if a list, assume the input is a numpy array
        input = np.asarray(input_data)
    elif isinstance(input_data, dict) and "columns" in input_data and "index" in input_data and "data" in input_data:
        # if the dictionary follows pandas split column format, deserialize into a pandas Dataframe
        input = pd.read_json(json.dumps(input_data), orient="split", dtype=False)
    else:
        # otherwise, assume input is a named tensor, and deserialize into a dict[str, numpy.ndarray]
        input = {input_name: np.asarray(input_value) for input_name, input_value in input_data.items()}
    return _get_jsonable_obj(model.predict(input), pandas_orient="records")
"""
    INPUT_DECORATOR_PANDAS_STR = \
        "@input_schema('input_data', PandasParameterType(sample_input, orient='split', enforce_shape=False))"
    OUTPUT_DECORATOR_PANDAS_STR = \
        "@output_schema(PandasParameterType(sample_output, orient='records', enforce_shape=False))"
    TENSOR_PARAMETER_TYPE = "NumpyParameterType({sample_io}, enforce_shape=False)"
    STANDARD_PY_PARAMETER_TYPE = "StandardPythonParameterType({sample_io})"
    INPUT_DECORATOR_TENSOR_STR = "@input_schema('input_data', {tensor_input})"
    OUTPUT_DECORATOR_TENSOR_STR = "@output_schema({tensor_output})"
    SAMPLE_PANDAS_INPUT_STR = \
        "sample_input = pd.read_json('{input_format_str}', orient='split', dtype={input_df_dtypes})"
    SAMPLE_PANDAS_OUTPUT_STR = \
        "sample_output = pd.read_json('{output_format_str}', orient='records', dtype={output_df_dtypes})"
    SAMPLE_NUMPY_INPUT_OUTPUT_STR = "np.array(json.loads('{input_format_str}'), dtype='{input_dtype}')"

    if sample_output is not None:
        # Create and write sample output handling, which uses inference-schema, to the scoring script
        if isinstance(sample_output, np.ndarray):
            # Write the sample numpy array into the scoring script and create the output
            # inference-schema decorator using NumpyParameterType
            sample_output_str = SAMPLE_NUMPY_INPUT_OUTPUT_STR.format(
                input_format_str=json.dumps(sample_output.tolist()),
                input_dtype=sample_output.dtype)
            output_parameter_str = TENSOR_PARAMETER_TYPE.format(sample_io=sample_output_str)
            output_decorator_str = OUTPUT_DECORATOR_TENSOR_STR.format(tensor_output=output_parameter_str)
        else:
            # Write the sample output into the scoring script and create the
            # inference-schema decorator using PandasParameterType
            sample_output_dtypes_dict = sample_output.dtypes.to_dict()
            # Pandas has added an extension dtype for strings.
            # However, the string repr for them can't be used in a format, and read_json still
            # handles it as a dtype object anyway. So doing this conversion loses nothing.
            if string_d_type_imported:
                for column_name, column_type in sample_output_dtypes_dict.items():
                    if type(column_type) is StringDtype:
                        sample_output_dtypes_dict[column_name] = dtype('O')

            # Append the sample output to init and prepend the output decorator to the run function
            sample_output_str = SAMPLE_PANDAS_OUTPUT_STR.format(
                output_format_str=sample_output.to_json(orient='records'),
                output_df_dtypes=sample_output_dtypes_dict)
            output_decorator_str = OUTPUT_DECORATOR_PANDAS_STR
            INIT_SRC = INIT_SRC + "\n" + sample_output_str
        RUN_WITH_INFERENCE_SCHEMA_SRC = output_decorator_str + "\n" + RUN_WITH_INFERENCE_SCHEMA_SRC

    if sample_input is not None:
        # Create and write sample input handling, which uses inference-schema, to the scoring script
        if isinstance(sample_input, np.ndarray):
            # Write the sample input into the scoring script and create the
            # inference-schema input decorator using NumpyParameterType.
            sample_input_str = SAMPLE_NUMPY_INPUT_OUTPUT_STR.format(
                input_format_str=json.dumps(sample_input.tolist()),
                input_dtype=sample_input.dtype)
            input_parameter_str = TENSOR_PARAMETER_TYPE.format(sample_io=sample_input_str)
            input_decorator_str = INPUT_DECORATOR_TENSOR_STR.format(tensor_input=input_parameter_str)
        elif isinstance(sample_input, dict):
            # Write the sample input into the scoring script and create the
            # input inference-schema decorator using StandardPyParameter
            # StandardPyPameter will nest a dictionary mapping str to NumpyParameterType
            sample_input_str = "{"
            for key, value in sample_input.items():
                tensor_input_str = SAMPLE_NUMPY_INPUT_OUTPUT_STR.format(
                    input_format_str=json.dumps(value.tolist()),
                    input_dtype=value.dtype)
                tensor_paramter_str = TENSOR_PARAMETER_TYPE.format(sample_io=tensor_input_str)
                sample_input_str += \
                    "'{key}': {tensor_parameter_str},".format(key=key, tensor_parameter_str=tensor_paramter_str)
            sample_input_str += "}"
            input_parameter_str = STANDARD_PY_PARAMETER_TYPE.format(sample_io=sample_input_str)
            input_decorator_str = INPUT_DECORATOR_TENSOR_STR.format(tensor_input=input_parameter_str)
        else:
            # Write the sample input into the scoring script and create the
            # input inference-schema decorator using PandasParameterType
            sample_input_dtypes_dict = sample_input.dtypes.to_dict()
            # Pandas has added an extension dtype for strings.
            # However, the string repr for them can't be used in a format
            # string, and read_json still handles it as a dtype object anyway. So doing this conversion loses nothing.
            if string_d_type_imported:
                for column_name, column_type in sample_input_dtypes_dict.items():
                    if type(column_type) is StringDtype:
                        sample_input_dtypes_dict[column_name] = dtype('O')

            # Append the sample input to init and prepend the input decorator to the run function
            sample_input_str = SAMPLE_PANDAS_INPUT_STR.format(input_format_str=sample_input.to_json(orient='split'),
                                                              input_df_dtypes=sample_input_dtypes_dict)
            input_decorator_str = INPUT_DECORATOR_PANDAS_STR
            INIT_SRC = INIT_SRC + "\n" + sample_input_str
        RUN_WITH_INFERENCE_SCHEMA_SRC = input_decorator_str + "\n" + RUN_WITH_INFERENCE_SCHEMA_SRC

    if sample_input is not None or sample_output is not None:
        # Combine the init which contains appended sample line/s to the run function with prepended decorator/s
        execution_script_text = INIT_SRC + "\n\n" + RUN_WITH_INFERENCE_SCHEMA_SRC
    else:
        # No fancy handling, just our basic init and run without samples/decorators
        execution_script_text = INIT_SRC + "\n" + RUN_WITHOUT_INFERENCE_SCHEMA_SRC

    with open(output_path, "w") as f:
        f.write(execution_script_text)


def _get_poller(client, initial_response, deserialization_callback, service_context, show_output=False):
    polling_method = MMSPolling(
        show_output=show_output,
        lro_algorithms=[MMSOperationResourcePolling(service_context)]
    )

    poller = LROPoller(client, initial_response, deserialization_callback, polling_method)
    return poller


def _get_polling_url(operation_location, service_context):
    url_path = "modelmanagement/v1.0/{0}/operations/{1}".format(
        service_context._get_workspace_scope(),
        operation_location.split('/')[-1]
    )
    return urljoin(service_context.host_url, url_path)
