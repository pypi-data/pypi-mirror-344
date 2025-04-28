# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import os

from azureml.mlflow.deploy._mir._util import \
    _get_default_online_endpoint_config, _attribute_transformer_snake_to_camel_case
from azureml.mlflow.deploy._mir.polling._azureml_polling import AzureMLPolling
from azureml.mlflow._restclient.mfe_v2022_02_01_preview._azure_machine_learning_workspaces import \
    AzureMachineLearningWorkspaces as RestMirClient

from azureml.mlflow._restclient.mfe_v2022_02_01_preview.models import \
    ManagedOnlineDeployment, \
    OnlineDeploymentData, Sku, PartialOnlineEndpointPartialTrackedResource, PartialOnlineEndpoint
from azureml.mlflow.deploy._mir._util import convert_v2_deploy_config_to_rest_config

_logger = logging.getLogger(__name__)


class MirDeploymentClient(object):

    def __init__(self, service_context):
        self._client = RestMirClient(
            credential=service_context.auth,
            base_url=service_context.cloud.endpoints.resource_manager,
            subscription_id=service_context.subscription_id,
            credential_scopes=[service_context.cloud._get_default_scope()],
            logging_enable=os.environ.get("AZUREML_LOG_NETWORK_TRACES", False)
        )
        self._service_context = service_context

    def create_online_endpoint(self, endpoint_name, config=None, **kwargs):
        no_wait = kwargs.pop("no_wait", False)

        if config is None:
            config = _get_default_online_endpoint_config()

        ws = self._get_aml_workspace()

        if config.location is None:
            config.location = ws.location

        poller = self._client.online_endpoints.begin_create_or_update(
            endpoint_name=endpoint_name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            polling=not no_wait,
            body=config._to_rest())

        if no_wait is False:
            return poller.result(timeout=720)
        else:
            return poller

    def update_online_endpoint(self, endpoint_name, config=None, **kwargs):
        no_wait = kwargs.pop("no_wait", False)

        ws = self._get_aml_workspace()
        if config.location is None:
            config.location = ws.location

        partial_online_endpoint_resource = config._to_rest_update_config()

        poller = self._client.online_endpoints.begin_update(
            endpoint_name=endpoint_name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            body=partial_online_endpoint_resource
        )

        if no_wait is False:
            return poller.result(timeout=720)
        else:
            return poller

    def update_endpoint_traffic(self, endpoint_name, deployment_name):
        endpoint_update_config = PartialOnlineEndpoint(traffic={deployment_name: 100})
        endpoint_update_body = PartialOnlineEndpointPartialTrackedResource(
            properties=endpoint_update_config
        )
        update_endpoint = self._client.online_endpoints.begin_update(
            endpoint_name=endpoint_name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            body=endpoint_update_body
        )

        return update_endpoint

    def create_online_deployment(
            self, deployment_config, deployment_name, endpoint_name, model_name, model_version, **kwargs):
        no_wait = kwargs.pop("no_wait", False)

        deploy_config_converted = convert_v2_deploy_config_to_rest_config(deployment_config)
        managed_deployment = ManagedOnlineDeployment(**deploy_config_converted)

        capacity = 1
        if 'instance_count' in deployment_config:
            capacity = deployment_config.get('instance_count')

        sku = Sku(name="Default", capacity=capacity)
        ws = self._get_aml_workspace()
        location = ws.location

        path_format_arguments = {
            "endpointName": deployment_name,
            "resourceGroupName": self._service_context.resource_group_name,
            "workspaceName": self._service_context.workspace_name,
        }

        poller = self._client.online_deployments.begin_create_or_update(
            endpoint_name=endpoint_name,
            deployment_name=deployment_name,
            body=OnlineDeploymentData(
                location=location, properties=managed_deployment, sku=sku
            ),
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            polling=AzureMLPolling(
                5,
                path_format_arguments=path_format_arguments,
                # **self._init_kwargs,
            )
            if not no_wait
            else False,
        )

        if no_wait is False:
            _logger.info("Creating deployment {}".format(deployment_name))
            poller.result(timeout=3600)

    def update_online_deployment(
            self, deployment_config, deployment_name, endpoint_name,
            model_name, model_version, existing_deployment=None, **kwargs):
        no_wait = kwargs.pop("no_wait", False)

        existing_deployment = existing_deployment if existing_deployment else\
            self._client.online_deployments.get(
                deployment_name=deployment_name,
                endpoint_name=endpoint_name,
                resource_group_name=self._service_context.resource_group_name,
                workspace_name=self._service_context.workspace_name
            )

        deploy_config_converted = convert_v2_deploy_config_to_rest_config(
            deployment_config, existing_deployment=existing_deployment
        )
        managed_deployment = ManagedOnlineDeployment(**deploy_config_converted)
        workspace_scope = self._service_context._get_workspace_scope()
        managed_deployment.model = '{0}/models/{1}/versions/{2}' \
            .format(workspace_scope, model_name, model_version)

        capacity = 1
        if 'instance_count' in deployment_config:
            capacity = deployment_config.get('instance_count')

        sku = Sku(name="Default", capacity=capacity)
        ws = self._get_aml_workspace()
        location = ws.location

        path_format_arguments = {
            "endpointName": deployment_name,
            "resourceGroupName": self._service_context.resource_group_name,
            "workspaceName": self._service_context.workspace_name,
        }

        poller = self._client.online_deployments.begin_update(
            endpoint_name=endpoint_name,
            deployment_name=deployment_name,
            body=OnlineDeploymentData(
                location=location, properties=managed_deployment, sku=sku
            ),
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            polling=AzureMLPolling(
                5,
                path_format_arguments=path_format_arguments,
                # **self._init_kwargs,
            )
            if not no_wait
            else False,
        )

        if no_wait is False:
            _logger.info("Creating deployment {}".format(deployment_name))
            poller.result(timeout=720)

    def get_endpoint(self, name):
        endpoint = self._client.online_endpoints.get(
            endpoint_name=name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
        )

        return endpoint.as_dict(key_transformer=_attribute_transformer_snake_to_camel_case)

    def get_deployment(self, name, endpoint_name):
        deployment = self._get_deployment(name=name, endpoint_name=endpoint_name)

        return deployment.as_dict(key_transformer=_attribute_transformer_snake_to_camel_case)

    def list_endpoints(self):
        endpoints_list = self._client.online_endpoints.list(
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name
        )

        json_endpoints_list = []
        for endpoint in endpoints_list:
            # TODO: Check if we should transform to camel case from snake case
            json_endpoints_list.append(endpoint.as_dict(key_transformer=_attribute_transformer_snake_to_camel_case))

        return json_endpoints_list

    def list_deployments(self, endpoint_name):
        deployment_list = self._client.online_deployments.list(
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            endpoint_name=endpoint_name
        )

        json_deployment_list = []
        for deployment in deployment_list:
            json_deployment_list.append(deployment.as_dict(key_transformer=_attribute_transformer_snake_to_camel_case))

        return json_deployment_list

    def delete_endpoint(self, name):
        # deleting endpoint also deletes deployments associated to it.
        response = self._client.online_endpoints.begin_delete(
            endpoint_name=name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name
        )
        # TODO : Add timeout for all long running operations
        return response.result(720)

    def delete_deployment(self, deployment_name, endpoint_name):
        response = self._client.online_deployments.begin_delete(
            deployment_name=deployment_name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            endpoint_name=endpoint_name
        )

        return response.result(720)

    def _get_deployment(self, name, endpoint_name):
        deployment = self._client.online_deployments.get(
            deployment_name=name,
            endpoint_name=endpoint_name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name
        )

        return deployment

    def _get_token(self, endpoint_name):
        response = self._client.online_endpoints.get_token(
            endpoint_name=endpoint_name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name
        )

        return response.access_token

    def _list_keys(self, endpoint_name):
        response = self._client.online_endpoints.list_keys(
            endpoint_name=endpoint_name,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name
        )

        return response

    def _get_aml_workspace(self):
        ws = self._client.workspaces.get(
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
        )

        return ws
