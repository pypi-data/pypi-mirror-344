# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import uuid
from urllib.parse import urlparse
from azureml.mlflow._restclient.mms._azure_machine_learning_workspaces import \
    AzureMachineLearningWorkspaces as RestMmsClient
from azureml.mlflow._restclient.mms.models import EnvironmentImageRequest, ImageAsset
from azureml.mlflow.deploy._mms.utils import create_inference_env_and_entry_script, \
    wrap_execution_script, _get_poller, _get_polling_url
from azureml.mlflow.deploy._mms.webservice.aci.aci import AciWebservice
from azureml.mlflow.deploy._mms.webservice.aks.aks import AksWebservice
from azureml.mlflow.deploy._mms._constants import ACI_WEBSERVICE_TYPE, AKS_WEBSERVICE_TYPE
from mlflow.utils.file_utils import TempDir


class MmsDeploymentClient(object):

    def __init__(self, service_context):
        self._client = RestMmsClient(
            credential=service_context.auth,
            base_url=service_context.host_url,
            credential_scopes=[service_context.cloud._get_default_scope()],
            logging_enable=os.environ.get("AZUREML_LOG_NETWORK_TRACES", False)
        )
        self._service_context = service_context

    def create_service(self, name, model_name, model_version, deploy_config, **kwargs):
        no_wait = kwargs.pop("no_wait", False)
        # TODO: Replace TempDir use since its coming from MLflow
        with TempDir(chdr=True) as tmp_dir:
            execution_script_path, environment = create_inference_env_and_entry_script(
                tmp_dir, model_name, model_version, name)

            environment_image_request = self._create_environment_image_request(
                environment, execution_script_path, ['{}:{}'.format(model_name, model_version)])

        service_create_request = deploy_config._to_service_create_request(
            name=name,
            environment_image_request=environment_image_request
        )
        service_create_request.environment_image_request = environment_image_request

        initial_response = self._client.services.create(
            subscription_id=self._service_context.subscription_id,
            resource_group=self._service_context.resource_group_name,
            workspace=self._service_context.workspace_name,
            body=service_create_request,
            cls=lambda x, y, z: (x),
        )

        poller = self._get_poller(initial_response=initial_response, show_output=not no_wait)

        if no_wait is False:
            poller.result()

        return self.get_service(name=name)

    def get_service(self, name):
        response = self._client.services.query_by_id(
            id=name,
            subscription_id=self._service_context.subscription_id,
            resource_group=self._service_context.resource_group_name,
            workspace=self._service_context.workspace_name,
            expand=True
        )
        if response.compute_type == AKS_WEBSERVICE_TYPE:
            webservice_object = AksWebservice._from_service_response(response, service_context=self._service_context)
        if response.compute_type == ACI_WEBSERVICE_TYPE:
            webservice_object = AciWebservice._from_service_response(response, service_context=self._service_context)

        return webservice_object

    def update_service(self, name, model_name=None, model_version=None, deploy_config=None, **kwargs):
        no_wait = kwargs.pop("no_wait", False)
        environment_image_request = None
        # TODO: Replace TempDir use since its coming from MLflow
        if model_name is not None and model_version is not None:
            with TempDir(chdr=True) as tmp_dir:
                execution_script_path, environment = create_inference_env_and_entry_script(
                    tmp_dir, model_name, model_version, name)

                environment_image_request = self._create_environment_image_request(
                    environment, execution_script_path, ['{}:{}'.format(model_name, model_version)])

        service_update_request = deploy_config._to_service_update_request(
            environment_image_request=environment_image_request)

        initial_response = self._client.services.patch(
            id=name,
            subscription_id=self._service_context.subscription_id,
            resource_group=self._service_context.resource_group_name,
            workspace=self._service_context.workspace_name,
            body=service_update_request,
            cls=lambda x, y, z: (x),
        )

        poller = self._get_poller(initial_response=initial_response, show_output=not no_wait)

        if no_wait is False:
            poller.result(timeout=720)

        return self.get_service(name=name)

    def delete_service(self, name):
        pipeline_response, deserialized_response = self._client.services.delete(
            subscription_id=self._service_context.subscription_id,
            resource_group=self._service_context.resource_group_name,
            workspace=self._service_context.workspace_name,
            id=name,
            cls=lambda x, y, z: (x, y),
        )

        if pipeline_response.http_response.status_code == 202:
            poller = self._get_poller(initial_response=pipeline_response, show_output=True)
            poller.result(timeout=720)
        elif pipeline_response.http_response.status_code == 204:
            print('No service with name {} found to delete.'.format(name))

    def list_services(self, **kwargs):
        compute_type = kwargs.pop("compute_type", None)
        service_list = []

        rest_service_list = self._client.services.list_query(
            compute_type=compute_type,
            expand=True,
            subscription_id=self._service_context.subscription_id,
            resource_group=self._service_context.resource_group_name,
            workspace=self._service_context.workspace_name,
        )

        for rest_service in rest_service_list:
            webservice_object = None
            if rest_service.compute_type == AKS_WEBSERVICE_TYPE:
                webservice_object = AksWebservice._from_service_response(rest_service,
                                                                         service_context=self._service_context)
            if rest_service.compute_type == ACI_WEBSERVICE_TYPE:
                webservice_object = AciWebservice._from_service_response(rest_service,
                                                                         service_context=self._service_context)
            if webservice_object:
                service_list.append(webservice_object)

        return service_list

    def list_service_keys(self, name):
        auth_keys = self._client.services.list_service_keys(
            subscription_id=self._service_context.subscription_id,
            resource_group=self._service_context.resource_group_name,
            workspace=self._service_context.workspace_name,
            id=name
        )

        return auth_keys

    def get_service_token(self, name):
        service_token = self._client.services.get_service_token(
            subscription_id=self._service_context.subscription_id,
            resource_group=self._service_context.resource_group_name,
            workspace=self._service_context.workspace_name,
            id=name
        )

        return service_token

    def _create_environment_image_request(self, environment, execution_script_path, model_ids):
        environment_image_request = EnvironmentImageRequest()
        if model_ids:
            environment_image_request.model_ids = model_ids

        image_assets, wrapped_driver_program_id = self._create_entry_script_assets(execution_script_path)
        environment_image_request.driver_program = wrapped_driver_program_id
        environment_image_request.assets = image_assets
        environment_image_request.environment = environment

        return environment_image_request

    def _create_entry_script_assets(self, execution_script_path):
        # # TODO: Replace TempDir use since its coming from MLflow
        # with TempDir(chdr=True) as tmp_dir:
        #     execution_script_path, environment = create_inference_env_and_entry_script(
        #         tmp_dir, model_name, model_version, service_name)

        wrapped_execution_script = wrap_execution_script(execution_script_path)

        (driver_package_location, _) = self._upload_dependency(wrapped_execution_script)
        wrapped_driver_program_id = os.path.basename(wrapped_execution_script)

        (artifact_url, artifact_id) = self._upload_dependency(execution_script_path)

        image_assets = []

        driver_image_asset = ImageAsset(
            id=wrapped_driver_program_id,
            url=driver_package_location,
            mime_type='application/x-python'
        )
        entry_script_asset = ImageAsset(
            id=artifact_id,
            url=artifact_url,
            mime_type='application/octet-stream'
        )
        image_assets.append(driver_image_asset)
        image_assets.append(entry_script_asset)
        return image_assets, wrapped_driver_program_id

    def _upload_dependency(self, dependency):
        """
        :param workspace: AzureML workspace
        :type workspace: workspace: azureml.core.workspace.Workspace
        :param dependency: path (local, http[s], or wasb[s]) to dependency
        :type dependency: str
        :param create_tar: tar creation flag. Defaults to False
        :type create_tar: bool
        :param arcname: arcname to use for tar
        :type arcname: str
        :param show_output: Indicates whether to display the progress of service deployment.
        :type show_output: bool
        :return: (str, str): uploaded_location, dependency_name
        """
        # from azureml._restclient.artifacts_client import ArtifactsClient
        if dependency.startswith('http') or dependency.startswith('wasb'):
            return dependency, urlparse(dependency).path.split('/')[-1]
        if not os.path.exists(dependency):
            raise Exception('Error resolving dependency: '
                            'no such file or directory {}'.format(dependency))

        dependency = dependency.rstrip(os.sep)
        dependency_name = os.path.basename(dependency)
        dependency_path = dependency

        origin = 'LocalUpload'
        container = '{}'.format(str(uuid.uuid4())[:8])

        from azureml.mlflow._client.artifact.local_artifact_client import LocalArtifactClient
        artifact_client = LocalArtifactClient(self._service_context, origin, container, None)

        # result = artifact_client.up(dependency_path, origin, container, dependency_name)
        result = artifact_client.upload_file(local_path=dependency_path, artifact_path=dependency_name)

        artifact_content = result.artifacts[dependency_name]
        dependency_name = artifact_content.path
        uploaded_location = "aml://artifact/" + artifact_content.artifact_id
        return uploaded_location, dependency_name

    def _get_poller(self, initial_response, show_output=None):

        polling_url = _get_polling_url(initial_response.http_response.headers.get('Operation-Location'),
                                       self._service_context)

        initial_response.http_response.headers['Operation-Location'] = polling_url

        poller = _get_poller(
            client=self._client.services._client,
            initial_response=initial_response,
            deserialization_callback=lambda x: x,
            service_context=self._service_context,
            show_output=show_output
        )

        return poller
