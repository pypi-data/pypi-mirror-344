# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains utilities for use by the deployment client"""
import json
import logging
import os
from copy import deepcopy

import requests
import yaml
from azure.core.exceptions import HttpResponseError
from azureml.mlflow._internal.service_context_loader import _AzureMLServiceContextLoader
from mlflow import get_tracking_uri, get_registry_uri
from mlflow import register_model as mlflow_register_model
from mlflow.exceptions import MlflowException
from mlflow.tracking import MlflowClient
from mlflow.version import VERSION as mlflow_version

VERSION_WARNING = "Could not import {}. Please upgrade to Mlflow 1.4.0 or higher."

_logger = logging.getLogger(__name__)


def file_stream_to_object(file_stream):
    """
    Take a YAML or JSON file_stream and return the dictionary object.

    :param file_stream: File stream from with open(file) as file_stream
    :type file_stream:
    :return: File dictionary
    :rtype: dict
    """
    file_data = file_stream.read()

    try:
        return yaml.safe_load(file_data)
    except Exception:
        pass

    try:
        return json.loads(file_data)
    except Exception as ex:
        raise Exception('Error while parsing file. Must be valid JSON or YAML file.') from ex


def handle_model_uri(model_uri, service_name):
    """
    Handle the various types of model uris we could receive.

    :param model_uri:
    :type model_uri: str
    :param service_name:
    :type service_name: str
    :return:
    :rtype:
    """
    client = MlflowClient()

    if model_uri.startswith("models:/"):
        model_name = model_uri.split("/")[-2]
        model_stage_or_version = model_uri.split("/")[-1]
        if model_stage_or_version in client.get_model_version_stages(None, None):
            # TODO: Add exception handling for no models found with specified stage
            model_version = client.get_latest_versions(model_name, [model_stage_or_version])[0].version
        else:
            model_version = model_stage_or_version
    elif (model_uri.startswith("runs:/") or model_uri.startswith("file://")) \
            and get_tracking_uri().startswith("azureml") and get_registry_uri().startswith("azureml"):
        # We will register the model for the user
        model_name = service_name + "-model"
        mlflow_model = mlflow_register_model(model_uri, model_name)
        model_version = mlflow_model.version

        _logger.info(
            "Registered an Azure Model with name: `%s` and version: `%s`",
            mlflow_model.name,
            mlflow_model.version,
        )
    else:
        raise MlflowException("Unsupported model uri provided, or tracking or registry uris are not set to "
                              "an AzureML uri.")

    return model_name, model_version


# This method is only used for local deployment right now and will be removed in future release.
# DO NOT take a dependency on it
def create_inference_config(tmp_dir, mlflow_model, environment, absolute_model_path):
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
        import pandas
    except ImportError:
        _logger.warning("Unable to import pandas")

    try:
        import numpy as np
    except ImportError:
        _logger.warning("Unable to import numpy")

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
            # If the input is not a named tensor, the sample io value that we create will just be a numpy.ndarray
            if input_sample_json is not None:
                # If sample input is provided, create a numpy array from it with the typing information
                # found in the model's input signature
                sample_io = np.asarray(input_sample_json, dtype=io[0].type)
            else:
                shape = io[0].shape
                if shape and shape[0] == -1:
                    # -1 for first dimension means the input data is batched
                    # Create a numpy array with the first dimension of shape as 1 so that inference-schema
                    # can correctly generate the swagger sample for the input
                    shape = list(deepcopy(shape))
                    shape[0] = 1
                sample_io = np.zeros(tuple(shape), dtype=io[0].type)
        else:
            # otherwise, the input is a named tensor, so the sample io value that we create will be
            # Dict[str, numpy.ndarray], which maps input name to a numpy.ndarray of the corresponding size
            sample_io = {}
            for io_val in io:
                if input_sample_json is not None:
                    sample_io[io_val.name] = np.asarray(input_sample_json[io_val.name], dtype=io_val.type)
                else:
                    shape = io_val.shape
                    if shape and shape[0] == -1:
                        # -1 for first dimension means the input data is batched
                        # Create a numpy array with the first dimension of shape as 1 so that inference-schema
                        # can correctly generate the swagger sample for the input
                        shape = list(deepcopy(shape))
                        shape[0] = 1
                        sample_io[io_val.name] = np.zeros(tuple(shape), dtype=io_val.type)
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

    # Add inference dependencies
    environment.python.conda_dependencies.add_pip_package("mlflow=={}".format(mlflow_version))
    environment.python.conda_dependencies.add_pip_package("azureml-inference-server-http~=0.6.1")

    environment.docker.base_dockerfile = _create_base_dockerfile()

    # Create InferenceConfig
    from azureml.core.model import InferenceConfig
    inference_config = InferenceConfig(entry_script=execution_script_path, environment=environment)

    return inference_config


# This method is only used for local deployment right now and will be removed in future release.
# DO NOT take a dependency on it
def _create_base_dockerfile():
    from azureml.core.environment import DEFAULT_CPU_IMAGE
    return """\
FROM {base_image}
ENV AZUREML_INFERENCE_SERVER_HTTP_ENABLED=true
""".format(base_image=DEFAULT_CPU_IMAGE)


# This method is only used for local deployment right now and will be removed in future release.
# DO NOT take a dependency on it
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


def load_pyfunc_conf(model):
    """
    Load the pyfunc flavor configuration for the passed in model.

    Loads the `python_function` flavor configuration for the specified model or throws an exception
    if the model does not contain the `python_function` flavor.

    :param model_path: The MLFlow Model object to retrieve the pyfunc conf from
    :return: The model's `python_function` flavor configuration.
    """
    try:
        from mlflow import pyfunc
    except ImportError as exception:
        raise get_deployments_import_error(exception)

    if pyfunc.FLAVOR_NAME not in model.flavors:
        raise MlflowException(
            message=(
                "The specified model does not contain the `python_function` flavor. This "
                "flavor is currently required for model deployment."
            )
        )
    return model.flavors[pyfunc.FLAVOR_NAME]


def get_deployments_import_error(import_error):
    deployments_suffix = (". pandas numpy and flask are needed for"
                          "full mlflow.deployments support with the azureml backend.")
    return ImportError(import_error.msg + deployments_suffix)


def post_and_validate_response(url, data=None, json=None, headers=None, **kwargs) -> requests.Response:
    r"""Sends a POST request and validate the response.
    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    response = requests.post(url=url, data=data, json=json, headers=headers, **kwargs)
    r_json = {}

    if response.status_code not in [200, 201]:
        # We need to check for an empty response body or catch the exception raised.
        # It is possible the server responded with a 204 No Content response, and json parsing fails.
        if response.status_code != 204:
            try:
                r_json = response.json()
            except ValueError:
                # exception is not in the json format
                raise Exception(response.content.decode("utf-8"))
        failure_msg = r_json.get("error", {}).get("message", response)
        raise HttpResponseError(response=response, message=failure_msg)

    return response


def get_and_validate_response(url, data=None, json=None, headers=None, **kwargs) -> requests.Response:
    r"""Sends a POST request and validate the response.
    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    # error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}

    response = requests.Session().get(url=url, data=data, json=json, headers=headers, **kwargs)

    if response.status_code not in [200, 201]:
        # map_error(status_code=response.status_code, response=response, error_map=error_map)
        raise HttpResponseError(response=response, message=response.content.decode("utf-8"))

    return response


def get_registry_model_uri(registry_uri, model_name, model_version):
    registry_name = _AzureMLServiceContextLoader.get_registry_name(registry_uri)
    model_uri = 'azureml://registries/{registry_name}/models/{model_name}/versions/{model_version}'\
        .format(registry_name=registry_name, model_name=model_name, model_version=model_version)
    return model_uri


def is_registry_uri(registry_uri, target_uri):
    if registry_uri != target_uri and 'registries' in registry_uri:
        return True
    return False


def load_azure_workspace():
    """
    Load existing Azure Workspace from Tracking Store
    :rtype: AzureML Workspace object
    """
    from azureml.mlflow._store.tracking.store import AzureMLRestStore
    from mlflow.exceptions import ExecutionException
    from mlflow.tracking.client import MlflowClient
    from azureml.core import Workspace

    try:
        def_store = MlflowClient()._tracking_client.store
    except ExecutionException:
        _logger.warning(VERSION_WARNING.format("MlflowClient()._tracking_client.store"))
        def_store = MlflowClient().store
    if isinstance(def_store, AzureMLRestStore):
        # workspace = Workspace._from_service_context(service_context, _location=def_store.service_context.location)
        # TODO: This will use Interactive auth. Check if it causes issue for remote scenarios
        workspace = Workspace(
            subscription_id=def_store.service_context.subscription_id,
            resource_group=def_store.service_context.resource_group_name,
            workspace_name=def_store.service_context.workspace_name,
        )
        return workspace
    else:
        raise ExecutionException("Workspace not found, please set the tracking URI in your script to AzureML.")
