# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality for deploying models to AzureML through MLFlow."""

import json
import logging
import tempfile
from azure.core.exceptions import HttpResponseError
from azureml.mlflow._internal.constants import NUMPY_SWAGGER_FORMAT
from azureml.mlflow._internal.service_context_loader import _AzureMLServiceContextLoader
from azureml.mlflow.deploy._mir.mir import OnlineEndpointConfiguration
from azureml.mlflow.deploy._mms._constants import COMPUTE_TYPE_KEY, ACI_WEBSERVICE_TYPE, AKS_WEBSERVICE_TYPE
from azureml.mlflow.deploy._mms.mms_client import MmsDeploymentClient
from azureml.mlflow.deploy._mir.mir_deployment_client import MirDeploymentClient
from azureml.mlflow.deploy._mms.webservice.aci.aci import AciServiceDeploymentConfiguration
from azureml.mlflow.deploy._mms.webservice.aks.aks import AksServiceDeploymentConfiguration
from mlflow.deployments import BaseDeploymentClient
from mlflow.tracking._model_registry.utils import get_registry_uri
from mlflow.exceptions import MlflowException
from mlflow.utils.annotations import experimental
from ._util import (file_stream_to_object, handle_model_uri, get_deployments_import_error,
                    post_and_validate_response, get_and_validate_response, get_registry_model_uri,
                    is_registry_uri)

_logger = logging.getLogger(__name__)


class AzureMLDeploymentClient(BaseDeploymentClient):
    """Client object used to deploy MLFlow models to AzureML."""

    def __init__(self, target_uri):
        """
        Initialize the deployment client with the MLFlow target uri.

        :param target_uri: AzureML workspace specific target uri.
        :type target_uri: str
        """
        super(AzureMLDeploymentClient, self).__init__(target_uri)
        self.service_context = _AzureMLServiceContextLoader.load_service_context(target_uri)
        self._mms_client = MmsDeploymentClient(service_context=self.service_context)
        self._mir_client = MirDeploymentClient(service_context=self.service_context)

    @experimental
    def create_deployment(self, name, model_uri, flavor=None, config=None, endpoint=None):
        """
        Deploy a model to the specified target.

        Deploy a model to the specified target. By default, this method should block until
        deployment completes (i.e. until it's possible to perform inference with the deployment).
        In the case of conflicts (e.g. if it's not possible to create the specified deployment
        without due to conflict with an existing deployment), raises a
        :py:class:`mlflow.exceptions.MlflowException`. See target-specific plugin documentation
        for additional detail on support for asynchronous deployment and other configuration.

        :param name: Unique name to use for deployment. If another deployment exists with the same
                     name, raises a :py:class:`mlflow.exceptions.MlflowException`
        :param model_uri: URI of model to deploy. AzureML supports deployments of 'models', 'runs', and 'file' uris.
        :param flavor: (optional) Model flavor to deploy. If unspecified, a default flavor
                       will be chosen.
        :param config: (optional) Dict containing updated target-specific configuration for the
                       deployment
        :param endpoint: (optional) Endpoint to create the deployment under
        :return: Dict corresponding to created deployment, which must contain the 'name' key.
        """
        if flavor and flavor != 'python_function':
            raise MlflowException('Unable to use {} model flavor, '
                                  'AML currently only supports python_function.'.format(flavor))

        model_name, model_version = handle_model_uri(model_uri, name)

        v1_deploy_config = None
        v2_deploy_config = None
        no_wait = False

        # Convert passed in file to deployment config
        if config and 'deploy-config-file' in config:
            with open(config['deploy-config-file'], 'r') as deploy_file_stream:
                deploy_config_obj = file_stream_to_object(deploy_file_stream)
                no_wait = deploy_config_obj.get("async", False)
                try:
                    if COMPUTE_TYPE_KEY in deploy_config_obj:
                        deploy_compute_type = deploy_config_obj[COMPUTE_TYPE_KEY].lower()

                        if deploy_compute_type == AKS_WEBSERVICE_TYPE.lower():
                            v1_deploy_config = AksServiceDeploymentConfiguration._create_deploy_config_from_dict(
                                deploy_config_dict=deploy_config_obj
                            )
                        elif deploy_compute_type == ACI_WEBSERVICE_TYPE.lower():
                            v1_deploy_config = AciServiceDeploymentConfiguration._create_deploy_config_from_dict(
                                deploy_config_dict=deploy_config_obj
                            )
                        else:
                            raise Exception("unknown deployment type: {}".format(deploy_compute_type))

                    else:
                        if 'type' in deploy_config_obj and deploy_config_obj['type'].lower() != 'managed':
                            raise MlflowException('Unable to deploy MLFlow model to {} compute, currently only '
                                                  'supports Managed '
                                                  'compute.'.format(deploy_config_obj['endpointComputeType']))
                        if 'model' in deploy_config_obj:
                            raise MlflowException('Unable to provide model information in the deployment config file '
                                                  'when deploying through MLFlow. Please use the `model_uri` '
                                                  'parameter.')
                        else:
                            registry_uri = get_registry_uri()
                            if is_registry_uri(registry_uri, self.target_uri):
                                deploy_config_obj['model'] = get_registry_model_uri(registry_uri, model_name,
                                                                                    model_version)
                            else:
                                deploy_config_obj['model'] = \
                                    '/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/' \
                                    'Microsoft.MachineLearningServices/workspaces/{workspace_name}' \
                                    '/models/{model_name}/versions/{model_version}'.format(
                                        subscription_id=self.service_context.subscription_id,
                                        resource_group=self.service_context.resource_group_name,
                                        workspace_name=self.service_context.workspace_name,
                                        model_name=model_name, model_version=model_version)
                        if 'code_configuration' in deploy_config_obj or 'environment' in deploy_config_obj or \
                                'endpoint_name' in deploy_config_obj:
                            raise MlflowException(
                                'code_configuration, environment, and endpoint_name are not used with '
                                'MLFlow deployments. Please remove from the deployment config and '
                                'try again.')
                        v2_deploy_config = deploy_config_obj
                except Exception as e:
                    raise MlflowException('Failed to parse provided configuration file') from e
        else:
            if not endpoint:
                v1_deploy_config = AciServiceDeploymentConfiguration()

        if v1_deploy_config:
            deployment = self._v1_create_deployment(name, model_name, model_version, config,
                                                    v1_deploy_config, no_wait)
        else:
            deployment = self._v2_create_deployment_new(name, model_name, model_version, v2_deploy_config, endpoint)

        if 'flavor' not in deployment:
            deployment['flavor'] = flavor if flavor else 'python_function'
        return deployment

    @experimental
    def update_deployment(self, name, model_uri=None, flavor=None, config=None, endpoint=None):
        """
        Update the deployment specified by name.

        Update the deployment with the specified name. You can update the URI of the model, the
        flavor of the deployed model (in which case the model URI must also be specified), and/or
        any target-specific attributes of the deployment (via `config`). By default, this method
        should block until deployment completes (i.e. until it's possible to perform inference
        with the updated deployment). See target-specific plugin documentation for additional
        detail on support for asynchronous deployment and other configuration.

        :param name: Unique name of deployment to update
        :param model_uri: URI of a new model to deploy.
        :param flavor: (optional) new model flavor to use for deployment. If provided,
                       ``model_uri`` must also be specified. If ``flavor`` is unspecified but
                       ``model_uri`` is specified, a default flavor will be chosen and the
                       deployment will be updated using that flavor.
        :param config: (optional) dict containing updated target-specific configuration for the
                       deployment
        :param endpoint: (optional) Endpoint containing the deployment to update.
        :return: None
        """
        endpoint_name = endpoint if endpoint is not None else name
        endpoint = self._get_endpoint(endpoint_name)

        if endpoint:
            deployment = self.get_deployment(name, endpoint_name)
            if deployment:
                self._v2_deployment_update(name, endpoint_name, model_uri, flavor, config)
            else:
                raise MlflowException('No deployment with name {} found to update'.format(name))
        else:
            service = self._get_v1_service(name)
            if service:
                self._v1_deployment_update(service, name, model_uri, flavor, config)
            else:
                raise MlflowException('No deployment with name {} found to update'.format(name))

    @experimental
    def delete_deployment(self, name, endpoint=None, **kwargs):
        """
        Delete the deployment with name ``name``.

        :param name: Name of deployment to delete
        :param endpoint: (optional) Endpoint containing the deployment to delete.
        :return: None
        """
        endpoint_name = endpoint if endpoint is not None else name
        endpoint_obj = self._get_endpoint(endpoint_name)

        if endpoint_obj:
            traffic = endpoint_obj['properties']['traffic']
            if name in traffic:
                del (traffic[name])

            traffic_update_config_file_path = tempfile.mkstemp(suffix='.json')[1]
            traffic_update_config = {
                "traffic": traffic
            }
            with open(traffic_update_config_file_path, 'w') as traffic_update_config_file:
                json.dump(traffic_update_config, traffic_update_config_file)
            test_config = {'endpoint-config-file': traffic_update_config_file_path}
            self.update_endpoint(endpoint_name, test_config)

            self._mir_client.delete_deployment(deployment_name=name, endpoint_name=endpoint_name)

            if 'delete_empty_endpoint' in kwargs and kwargs['delete_empty_endpoint'] is True:
                self.delete_endpoint(endpoint_name)
        else:
            service = self._get_v1_service(name=name)
            if service:
                try:
                    self._mms_client.delete_service(name=name)
                except Exception as e:
                    raise MlflowException('There was an error deleting the deployment: \n{}'.format(e)) from e
            else:
                _logger.info('No deployment with name {} found to delete'.format(name))

    @experimental
    def list_deployments(self, endpoint=None):
        """
        List deployments.

        If no endpoint is provided, will list all deployments. If an endpoint is provided,
        will list all deployments under that endpoint.

        :param endpoint: (optional) List deployments in the specified endpoint.
        :return: A list of dicts corresponding to deployments.
        """
        try:
            if endpoint:
                _logger.info('Retrieving all deployments under endpoint {}'.format(endpoint))
                deployment_list = self._mir_client.list_deployments(endpoint_name=endpoint)
                return deployment_list

            else:
                _logger.info('Retrieving all ACI/AKS deployments')
                service_list = []
                services = self._mms_client.list_services(compute_type='ACI')
                services += self._mms_client.list_services(compute_type='AKS')
                for service in services:
                    service_list.append(service.serialize())

                endpoints = self.list_endpoints()
                for endpoint in endpoints:
                    try:
                        deployments = self.list_deployments(endpoint['name'])
                        for deployment in deployments:
                            deployment['endpointName'] = endpoint['name']
                            deployment['scoringUri'] = endpoint['properties']['scoringUri']
                            deployment['swaggerUri'] = endpoint['properties']['swaggerUri']
                        service_list += deployments
                    except MlflowException as ex:
                        if "Code: NoSuchEndpoint" not in ex.message:
                            raise ex

                return service_list
        except Exception as e:
            raise MlflowException('There was an error listing deployments') from e

    @experimental
    def get_deployment(self, name, endpoint=None):
        """
        Retrieve details for the specified deployment.

        Returns a dictionary describing the specified deployment. The dict is guaranteed to contain an 'name' key
        containing the deployment name.

        :param name: Name of deployment to retrieve
        :param endpoint: (optional) Endpoint containing the deployment to get
        """
        endpoint_name = endpoint if endpoint is not None else name

        deployment = self._get_v2_deployment(name, endpoint_name)

        if not deployment:
            service = self._get_v1_service(name)
            if service:
                deployment = service.serialize()

        if not deployment:
            raise MlflowException('No deployment with name {} found'.format(name))

        if 'flavor' not in deployment:
            deployment['flavor'] = 'python_function'

        return deployment

    @experimental
    def predict(self, deployment_name=None, df=None, endpoint=None):
        """
        Predict on the specified deployment using the provided dataframe.

        Compute predictions on the ``df`` using the specified deployment.
        Note that the input/output types of this method matches that of `mlflow pyfunc predict`
        (we accept a pandas.DataFrame, numpy.ndarray, or Dict[str, numpy.ndarray] as input and return
        either a pandas.DataFrame, pandas.Series, or numpy.ndarray as output).

        :param deployment_name: Name of deployment to predict against
        :param df: pandas.DataFrame, numpy.ndarray, or Dict[str, numpy.ndarray] to use for inference
        :param endpoint: Endpoint to predict against
        :return: A pandas.DataFrame, pandas.Series, or numpy.ndarray
        """
        try:
            from mlflow.pyfunc.scoring_server import _get_jsonable_obj
            import numpy as np
        except ImportError as exception:
            raise get_deployments_import_error(exception)

        if not deployment_name and not endpoint:
            raise MlflowException('Error, must provide one of deployment_name or endpoint')

        # Take in DF, parse to json using split orient
        if isinstance(df, dict):
            input_data = {key: _get_jsonable_obj(value, pandas_orient='split') for key, value in df.items()}
        else:
            input_data = _get_jsonable_obj(df, pandas_orient='split')

        if endpoint:
            endpoint_obj = self._get_endpoint(endpoint)
            if deployment_name:
                # Predict against a specific deployment in an endpoint
                _logger.info('Issuing prediction against deployment {} in endpoint '
                             '{}'.format(deployment_name, endpoint))
                scoring_resp, output_format = self._v2_predict(endpoint_obj, input_data, deployment_name)
            else:
                # Predict against endpoint and rely on traffic management
                _logger.info('Issuing prediction against endpoint {}'.format(endpoint))
                scoring_resp, output_format = self._v2_predict(endpoint_obj, input_data)
        else:
            # Try to get implicitly created endpoint
            endpoint_obj = self._get_endpoint(deployment_name)
            if endpoint_obj:
                # Predict against implicitly created endpoint and rely on traffic management
                _logger.info('Issuing prediction against endpoint {}'.format(deployment_name))
                scoring_resp, output_format = self._v2_predict(endpoint_obj, input_data)
            else:
                service = self._get_v1_service(deployment_name)
                if service:
                    # Predict against v1 webservice
                    _logger.info('Issuing prediction against deployment {}'.format(service.name))
                    scoring_resp, output_format = self._v1_predict(service, input_data)
                else:
                    raise MlflowException('No deployment with name {} '
                                          'found to predict against'.format(deployment_name))

        if scoring_resp:
            if output_format == NUMPY_SWAGGER_FORMAT:
                return np.array(scoring_resp.json())

            try:
                import pandas as pd
                return pd.read_json(json.dumps(scoring_resp.json()), orient="records", dtype=False)
            except ImportError:
                raise MlflowException('Prediction response is pandas format, but unable to import pandas')
        else:
            raise MlflowException('Failure during prediction:\n'
                                  'Response Code: {}\n'
                                  'Headers: {}\n'
                                  'Content: {}'.format(scoring_resp.status_code, scoring_resp.headers,
                                                       scoring_resp.content))

    @experimental
    def create_endpoint(self, name, config=None):
        """
        Create an endpoint with the specified target.

        By default, this method should block until creation completes (i.e. until it's possible
        to create a deployment within the endpoint). In the case of conflicts (e.g. if it's not
        possible to create the specified endpoint due to conflict with an existing endpoint),
        raises a :py:class:`mlflow.exceptions.MlflowException`. See target-specific plugin
        documentation for additional detail on support for asynchronous creation and other
        configuration.

        :param name: Unique name to use for endpoint. If another endpoint exists with the same
                     name, raises a :py:class:`mlflow.exceptions.MlflowException`.
        :param config: (optional) Dict containing target-specific configuration for the
                       endpoint.
        :return: Dict corresponding to created endpoint, which must contain the 'name' key.
        """
        endpoint_config_obj = {}
        endpoint_config = None
        if config:
            if 'endpoint-config-file' in config:
                with open(config['endpoint-config-file'], 'r') as deploy_file_stream:
                    endpoint_config_obj = file_stream_to_object(deploy_file_stream)
                    endpoint_config = OnlineEndpointConfiguration._from_dict_config(endpoint_config_obj)

        no_wait = endpoint_config_obj.get('async', False) if config else False
        self._mir_client.create_online_endpoint(endpoint_name=name, config=endpoint_config, no_wait=no_wait)

        return self._mir_client.get_endpoint(name=name)

    @experimental
    def get_endpoint(self, endpoint):
        """
        Retrieve the details of the specified endpoint.

        Returns a dictionary describing the specified endpoint, throwing a
        py:class:`mlflow.exception.MlflowException` if no endpoint exists with the provided
        name.
        The dict is guaranteed to contain an 'name' key containing the endpoint name.
        The other fields of the returned dictionary and their types may vary across targets.

        :param endpoint: Name of endpoint to fetch
        :return: A dict corresponding to the retrieved endpoint. The dict is guaranteed to
                 contain a 'name' key corresponding to the endpoint name. The other fields of
                 the returned dictionary and their types may vary across targets.
        """
        _logger.info('Starting endpoint get request')
        return self._mir_client.get_endpoint(name=endpoint)

    @experimental
    def delete_endpoint(self, endpoint):
        """
        Delete the endpoint from the specified target.

        Deletion should be idempotent (i.e. deletion should not fail if retried on a non-existent
        deployment).

        :param endpoint: Name of endpoint to delete
        :return: None
        """
        endpoint_obj = self._get_endpoint(endpoint)

        if endpoint_obj:
            self._mir_client.delete_endpoint(name=endpoint)
        else:
            _logger.info('No endpoint with name {} found to delete'.format(endpoint))

    @experimental
    def update_endpoint(self, endpoint, config=None):
        """
        Update the endpoint with the specified name.

        You can update any target-specific attributes of the endpoint (via `config`). By default,
        this method should block until the update completes (i.e. until it's possible to create a
        deployment within the endpoint). See target-specific plugin documentation for additional
        detail on support for asynchronous update and other configuration.

        :param endpoint: Unique name of endpoint to update
        :param config: (optional) dict containing target-specific configuration for the
                       endpoint
        :return: None
        """
        endpoint_obj = self.get_endpoint(endpoint)

        if not endpoint_obj:
            raise MlflowException('No endpoint with name {} found to update'.format(endpoint))

        endpoint_config_obj = {}
        if config:
            if 'endpoint-config-file' in config:
                with open(config['endpoint-config-file'], 'r') as deploy_file_stream:
                    endpoint_config_obj = file_stream_to_object(deploy_file_stream)

        no_wait = endpoint_config_obj.get('async', False) if config else False
        endpoint_config = OnlineEndpointConfiguration._from_dict_config(endpoint_config_obj)

        self._mir_client.update_online_endpoint(endpoint_name=endpoint, config=endpoint_config, no_wait=no_wait)

        return self.get_endpoint(endpoint)

    @experimental
    def list_endpoints(self):
        """
        List endpoints in the specified target.

        This method is expected to return an unpaginated list of all endpoints (an alternative
        would be to return a dict with an 'endpoints' field containing the actual endpoints,
        with plugins able to specify other fields, e.g. a next_page_token field, in the
        returned dictionary for pagination, and to accept a `pagination_args` argument to this
        method for passing pagination-related args).

        :return: A list of dicts corresponding to endpoints. Each dict is guaranteed to
                 contain a 'name' key containing the endpoint name. The other fields of
                 the returned dictionary and their types may vary across targets.
        """
        _logger.info('Starting endpoint list request')
        endpoint_list = self._mir_client.list_endpoints()

        return endpoint_list

    def _get_endpoint(self, endpoint_name):
        try:
            endpoint = self.get_endpoint(endpoint_name)
        except HttpResponseError as ex:
            if ex.response.status_code == 404:
                return None
            else:
                raise ex
        return endpoint

    def _v1_create_deployment(self, name, model_name, model_version, create_deployment_config,
                              v1_deploy_config, no_wait=False):

        try:
            deployment = self._mms_client.create_service(
                name=name, model_name=model_name, model_version=model_version, deploy_config=v1_deploy_config,
                no_wait=no_wait
            )

            if no_wait:
                _logger.info('AzureML deployment in progress, you can use get_deployment to check on the '
                             'current deployment status.')

        except Exception as e:
            raise MlflowException('Error while creating deployment') from e

        return deployment.serialize()

    def _v2_create_deployment_new(self, name, model_name, model_version, v2_deploy_config, endpoint=None):
        if not endpoint:
            _logger.info('Creating endpoint with name {} to create deployment under')
            self.create_endpoint(name, None)

        # Create Deployment using v2_deploy_config
        endpoint_name = endpoint if endpoint else name
        self._mir_client.create_online_deployment(deployment_config=v2_deploy_config,
                                                  deployment_name=name,
                                                  endpoint_name=endpoint_name, model_name=model_name,
                                                  model_version=model_version)

        if not endpoint:
            _logger.info('Updating endpoint to serve 100 percent traffic to deployment {}'.format(name))
            endpoint_update_poller = self._mir_client.update_endpoint_traffic(endpoint_name=name, deployment_name=name)
            endpoint_update_poller.result()
        else:
            _logger.info('Deployment created. Be sure to update your endpoint with desired traffic settings.')

        return self._mir_client.get_deployment(name, endpoint_name=endpoint_name)

    def _v1_deployment_update(self, service, name, model_uri=None, flavor=None, config=None):
        no_wait = False

        deploy_config = None
        if config and 'deploy-config-file' in config:
            try:
                with open(config['deploy-config-file'], 'r') as deploy_file_stream:
                    deploy_config_obj = file_stream_to_object(deploy_file_stream)

                    no_wait = deploy_config_obj.get("async", False)

                    deploy_compute_type = deploy_config_obj[
                        "computeType"] if "computeType" in deploy_config_obj else None
                    deploy_config = None
                    if deploy_compute_type == AKS_WEBSERVICE_TYPE.lower():
                        deploy_config = AksServiceDeploymentConfiguration._create_deploy_config_from_dict(
                            deploy_config_dict=deploy_config_obj)
                    elif deploy_compute_type == ACI_WEBSERVICE_TYPE.lower():
                        deploy_config = AciServiceDeploymentConfiguration._create_deploy_config_from_dict(
                            deploy_config_dict=deploy_config_obj)
                    else:
                        raise Exception("unknown deployment type: {}".format(deploy_compute_type))

            except Exception as e:
                raise MlflowException('Failed to parse provided deployment config file') from e

        model_name = None
        model_version = None
        if model_uri is not None:
            model_name, model_version = handle_model_uri(model_uri, name)

        try:
            deployment = self._mms_client.update_service(
                name=name, model_name=model_name, model_version=model_version, deploy_config=deploy_config,
                no_wait=no_wait
            )

            if no_wait:
                _logger.info('AzureML deployment in progress, you can use get_deployment to check on the current '
                             'deployment status.')

        except Exception as e:
            raise MlflowException('Error while updating deployment') from e

        return deployment.serialize()

    def _v2_deployment_update(self, name, endpoint_name, model_uri=None, flavor=None, config=None):
        try:
            resp = self._mir_client._get_deployment(name, endpoint_name)
        except MlflowException as e:
            raise MlflowException('Failure retrieving the deployment to update') from e

        existing_deployment = resp

        v2_deploy_config = {}
        if model_uri:
            model_name, model_version = handle_model_uri(model_uri, name)
        else:
            model_parts_list = existing_deployment.properties.model.split('/')
            model_name = model_parts_list[-3]
            model_version = model_parts_list[-1]

        if config and 'deploy-config-file' in config:
            with open(config['deploy-config-file'], 'r') as deploy_file_stream:
                deploy_config_obj = file_stream_to_object(deploy_file_stream)
                if 'code_configuration' in deploy_config_obj or 'environment' in deploy_config_obj or \
                        'endpoint_name' in deploy_config_obj:
                    raise MlflowException('code_configuration, environment, and endpoint_name are not used with '
                                          'MLFlow deployments. Please remove from the deployment config and '
                                          'try again.')
                v2_deploy_config = deploy_config_obj

        _logger.info('Starting update request')
        no_wait = v2_deploy_config.get('async', False) if config else False
        self._mir_client.update_online_deployment(
            v2_deploy_config, name, endpoint_name, model_name, model_version,
            existing_deployment=existing_deployment, no_wait=no_wait)
        _logger.info('Completed update request')

    def _get_v1_service(self, name):
        try:
            deployment = self._mms_client.get_service(name=name)
            return deployment
        except Exception as e:
            if 'NoSuchService' in e.message:
                return None
            raise MlflowException('There was an error retrieving the deployment: \n{}'.format(e.message)) from e

    def _get_v2_deployment(self, name, endpoint_name):
        try:
            deployment = self._mir_client.get_deployment(name, endpoint_name)
        except HttpResponseError as ex:
            if ex.response.status_code == 404:
                return None
            else:
                raise ex

        return deployment

    def _v1_predict(self, service, input_data):
        if not service.scoring_uri:
            raise MlflowException('Error attempting to call deployment, scoring_uri unavailable. '
                                  'This could be due to a failed deployment, or the service is not ready yet.\n'
                                  'Current State: {}\n'
                                  'Errors: {}'.format(service.state, service.error))

        # Pass split orient json to webservice
        # Take records orient json from webservice

        json_data = {'input_data': input_data}
        headers = dict({'Content-Type': 'application/json', 'Accept': 'application/json'})

        try:
            if service.auth_enabled is False:
                token = None
            elif service.auth_enabled:
                token = self._mms_client.list_service_keys(service.name).primary_key
            elif service.token_auth_enabled:
                token = self._mms_client.get_service_token(name=service.name).access_token
        except Exception as e:
            raise MlflowException('Received bad response attempting to retrieve deployment auth token') from e

        if token:
            headers.update({'Authorization': 'Bearer ' + token})

        response = post_and_validate_response(service.scoring_uri,
                                              json=json_data, headers=headers)

        output_format = self._get_output_format_from_swagger(service.swagger_uri, service.name, headers)

        return response, output_format

    def _v2_predict(self, endpoint, input_data, deployment_name=None):

        auth_mode = endpoint.get('properties').get('authMode', None) if endpoint.get('properties', None) else None

        try:
            if auth_mode == "Key":
                token = self._mir_client._list_keys(endpoint['name']).primary_key
            else:
                token = self._mir_client._get_token(endpoint['name'])
        except Exception as e:
            raise MlflowException('Received bad response attempting to retrieve deployment auth token') from e

        scoring_uri = endpoint['properties']['scoringUri']
        common_request_headers = {'Content-Type': 'application/json',
                                  'Authorization': 'Bearer {}'.format(token)}

        endpoint_request_headers = common_request_headers
        if deployment_name:
            endpoint_request_headers.update({'azureml-model-deployment': deployment_name})

        scoring_resp = post_and_validate_response(scoring_uri, json={'input_data': input_data},
                                                  headers=endpoint_request_headers)
        output_format = self._get_output_format_from_swagger(endpoint['properties']['swaggerUri'], endpoint["name"],
                                                             common_request_headers)

        return scoring_resp, output_format

    @staticmethod
    def _get_output_format_from_swagger(swagger_uri, endpoint_name, request_headers):
        swagger_params = {"version": 3}
        output_format = None

        try:
            swagger_response = get_and_validate_response(swagger_uri, params=swagger_params, headers=request_headers)
            swagger = swagger_response.json()
            output_format = swagger.get("components", {}) \
                .get("schemas", {}) \
                .get("ServiceOutput", {}) \
                .get("format", None)
        except Exception:
            _logger.warning(
                f'Unable to fetch swagger for deployment {endpoint_name}. '
                f'Proceeding with default output handling.'
            )

        return output_format
