# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains package references for AzureML deployment handling via MLFlow."""

import logging
from azureml.mlflow.deploy.deployment_client import AzureMLDeploymentClient


_logger = logging.getLogger(__name__)


def run_local(name, model_uri, flavor=None, config=None):
    """
    Deploy the specified model locally.

    :param name:  Unique name to use for deployment. If another deployment exists with the same
                     name, create_deployment will raise a
                     :py:class:`mlflow.exceptions.MlflowException`
    :param model_uri: URI of model to deploy
    :param flavor: (optional) Model flavor to deploy. If unspecified, default flavor is chosen.
    :param config: (optional) Dict containing updated target-specific config for the deployment
    :return: None
    """
    from azureml.mlflow.deploy._util import file_stream_to_object, handle_model_uri, create_inference_config
    from azureml.mlflow.deploy._util import load_azure_workspace
    from mlflow.exceptions import MlflowException
    from mlflow.utils.file_utils import TempDir

    try:
        from azureml.core.webservice.local import LocalWebservice, LocalWebserviceDeploymentConfiguration
        from azureml.core import Model
        from azureml._model_management._util import deploy_config_dict_to_obj
    except ImportError:
        raise Exception("Please install azureml.core to use create local deployments with AML")

    try:
        workspace = load_azure_workspace()
    except Exception as e:
        raise MlflowException("Failed to retrieve AzureML Workspace") from e

    model_name, model_version = handle_model_uri(model_uri, name)

    try:
        aml_model = Model(workspace, id='{}:{}'.format(model_name, model_version))
    except Exception as e:
        raise MlflowException('Failed to retrieve model to deploy') from e

    # Convert passed in file to deployment config
    if config and 'deploy-config-file' in config:
        try:
            # TODO: Tags, properties, and description are not in the config file for some reason?
            with open(config['deploy-config-file'], 'r') as deploy_file_stream:
                deploy_config_obj = file_stream_to_object(deploy_file_stream)
                deploy_config = deploy_config_dict_to_obj(deploy_config_obj, None, None, None)
        except Exception as e:
            raise MlflowException('Failed to parse provided deployment config file') from e
    else:
        deploy_config = LocalWebserviceDeploymentConfiguration()

    if not isinstance(deploy_config, LocalWebserviceDeploymentConfiguration):
        raise MlflowException('Provided deployment configuration information must correspond to a local deploy config')

    with TempDir(chdr=True) as tmp_dir:
        inference_config = create_inference_config(tmp_dir, model_name, model_version, name)

        try:
            _logger.info("Creating an AzureML deployment with name: `%s`", name)

            wait = True if not config else 'async' not in config or not config['async']

            # Deploy
            LocalWebservice._deploy(
                workspace=workspace,
                name=name,
                models=[aml_model],
                deployment_config=deploy_config,
                wait=wait,
                inference_config=inference_config
            )
        except Exception as e:
            raise MlflowException('Error while creating deployment') from e


def target_help():
    """
    Provide help information for the AzureML deployment client.

    :return:
    :rtype: str
    """
    help_str = """For the AzureML deployment plugin, the `target_uri` to provide to `get_deployment_client` is the
    same as the tracking uri, and is retrievable via the AzureML Workspace using
    `<workspace>.get_mlflow_tracking_uri()`.

    For `create_deployment` and `update_deployment` configuration, AzureML accepts a single key, 'deploy-config-file',
    the value of which is a path to a yaml or json file containing full configuration options. If this key is not
    provided deployment will be made using a default ACI configuration. More details about full configuration and
    how to construct the expected file can be found here: https://aka.ms/aml-deploy-configuration-options"""
    return help_str


__all__ = ["run_local", "target_help", "AzureMLDeploymentClient"]
