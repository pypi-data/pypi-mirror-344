# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import re

from azureml.mlflow._restclient.mms.models import Model, ModelEnvironmentDefinition, AKSServiceCreateRequest, \
    ModelDataCollection, AutoScaler as RestAutoScalar, \
    ContainerResourceRequirements as RestContainerResourceRequirements, \
    LivenessProbeRequirements as RestLivenessProbeRequirements, JsonPatchOperation
from azureml.mlflow.deploy._mms._constants import AKS_WEBSERVICE_TYPE, WEBSERVICE_SWAGGER_PATH, NAMESPACE_REGEX
from azureml.mlflow.deploy._mms.webservice.webservice import Webservice, WebserviceDeploymentConfiguration


class AutoScaler(object):
    """Defines details for autoscaling configuration of a AksWebservice.

    AutoScaler configuration values are specified using the ``deploy_configuration`` or ``update`` methods
    of the :class:`azureml.core.webservice.aks.AksWebservice` class.

    :var autoscale_enabled: Indicates whether the AutoScaler is enabled or disabled.
    :vartype autoscale_enabled: bool
    :var max_replicas: The maximum number of containers for the AutoScaler to use.
    :vartype max_replicas: int
    :var min_replicas: The minimum number of containers for the AutoScaler to use
    :vartype min_replicas: int
    :var refresh_period_seconds: How often the AutoScaler should attempt to scale the Webservice.
    :vartype refresh_period_seconds: int
    :var target_utilization: The target utilization (in percent out of 100) the AutoScaler should
        attempt to maintain for the Webservice.
    :vartype target_utilization: int

    :param autoscale_enabled: Indicates whether the AutoScaler is enabled or disabled.
    :type autoscale_enabled: bool
    :param max_replicas: The maximum number of containers for the AutoScaler to use.
    :type max_replicas: int
    :param min_replicas: The minimum number of containers for the AutoScaler to use
    :type min_replicas: int
    :param refresh_period_seconds: How often the AutoScaler should attempt to scale the Webservice.
    :type refresh_period_seconds: int
    :param target_utilization: The target utilization (in percent out of 100) the AutoScaler should
        attempt to maintain for the Webservice.
    :type target_utilization: int
    """

    _expected_payload_keys = ['autoscaleEnabled', 'maxReplicas', 'minReplicas', 'refreshPeriodInSeconds',
                              'targetUtilization']

    def __init__(self, autoscale_enabled, max_replicas, min_replicas, refresh_period_seconds, target_utilization):
        """Initialize the AKS AutoScaler.

        :param autoscale_enabled: Indicates whether the AutoScaler is enabled or disabled.
        :type autoscale_enabled: bool
        :param max_replicas: The maximum number of containers for the AutoScaler to use.
        :type max_replicas: int
        :param min_replicas: The minimum number of containers for the AutoScaler to use
        :type min_replicas: int
        :param refresh_period_seconds: How often the AutoScaler should attempt to scale the Webservice.
        :type refresh_period_seconds: int
        :param target_utilization: The target utilization (in percent out of 100) the AutoScaler should
            attempt to maintain for the Webservice.
        :type target_utilization: int
        """
        self.autoscale_enabled = autoscale_enabled
        self.max_replicas = max_replicas
        self.min_replicas = min_replicas
        self.refresh_period_seconds = refresh_period_seconds
        self.target_utilization = target_utilization

    def serialize(self):
        """Convert this AutoScaler object into a JSON serialized dictionary.

        :return: The JSON representation of this AutoScaler object.
        :rtype: dict
        """
        return {'autoscaleEnabled': self.autoscale_enabled, 'minReplicas': self.min_replicas,
                'maxReplicas': self.max_replicas, 'refreshPeriodInSeconds': self.refresh_period_seconds,
                'targetUtilization': self.target_utilization}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a JSON object into a AutoScaler object.

        :param payload_obj: A JSON object to convert to a AutoScaler object.
        :type payload_obj: dict
        :return: The AutoScaler representation of the provided JSON object.
        :rtype: azureml.core.webservice.aks.AutoScaler
        """
        for payload_key in AutoScaler._expected_payload_keys:
            if payload_key not in payload_obj:
                raise Exception('Invalid webservice payload, missing {} for autoScaler:\n'
                                '{}'.format(payload_key, payload_obj))

        return AutoScaler(payload_obj['autoscaleEnabled'], payload_obj['maxReplicas'], payload_obj['minReplicas'],
                          payload_obj['refreshPeriodInSeconds'], payload_obj['targetUtilization'])


class ContainerResourceRequirements(object):
    """Defines the resource requirements for a container used by the Webservice.

    ContainerResourceRequirement values are specified when deploying or updating a Webervice. For example, use the
    ``deploy_configuration`` or ``update`` methods of the :class:`azureml.core.webservice.aks.AksWebservice` class, or
    the ``create_version``, ``deploy_configuration``, or ``update_version`` methods of
    :class:`azureml.core.webservice.aks.AksEndpoint` class.

    :var cpu: The number of CPU cores to allocate for this Webservice. Can be a decimal.
    :vartype cpu: float
    :var memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
    :vartype memory_in_gb: float
    :var cpu_limit: The max number of CPU cores this Webservice is allowed to use. Can be a decimal.
    :vartype cpu_limit: float
    :var memory_in_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use. Can be a decimal.
    :vartype memory_in_gb_limit: float

    :param cpu: The number of CPU cores to allocate for this Webservice. Can be a decimal.
    :type cpu: float
    :param memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
    :type memory_in_gb: float
    :param cpu_limit: The max number of CPU cores this Webservice is allowed to use. Can be a decimal.
    :type cpu_limit: float
    :param memory_in_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use. Can be a decimal.
    :type memory_in_gb_limit: float
    """

    _expected_payload_keys = ['cpu', 'cpuLimit', 'memoryInGB', 'memoryInGBLimit', 'gpu']

    def __init__(self, cpu, memory_in_gb, gpu=None, cpu_limit=None, memory_in_gb_limit=None):
        """Initialize the container resource requirements.

        :param cpu: The number of CPU cores to allocate for this Webservice. Can be a decimal.
        :type cpu: float
        :param memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        :type memory_in_gb: float
        :param cpu_limit: The max number of CPU cores this Webservice is allowed to use. Can be a decimal.
        :type cpu_limit: float
        :param memory_in_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use.
                                    Can be a decimal.
        :type memory_in_gb_limit: float
        """
        self.cpu = cpu
        self.cpu_limit = cpu_limit
        self.memory_in_gb = memory_in_gb
        self.memory_in_gb_limit = memory_in_gb_limit
        self.gpu = gpu

    def serialize(self):
        """Convert this ContainerResourceRequirements object into a JSON serialized dictionary.

        :return: The JSON representation of this ContainerResourceRequirements.
        :rtype: dict
        """
        return {'cpu': self.cpu, 'cpuLimit': self.cpu_limit,
                'memoryInGB': self.memory_in_gb, 'memoryInGBLimit': self.memory_in_gb_limit,
                'gpu': self.gpu}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a JSON object into a ContainerResourceRequirements object.

        :param payload_obj: A JSON object to convert to a ContainerResourceRequirements object.
        :type payload_obj: dict
        :return: The ContainerResourceRequirements representation of the provided JSON object.
        :rtype: azureml.core.webservice.aks.ContainerResourceRequirements
        """
        for payload_key in ContainerResourceRequirements._expected_payload_keys:
            if payload_key not in payload_obj:
                raise Exception('Invalid webservice payload, missing {} for ContainerResourceRequirements:\n'
                                '{}'.format(payload_key, payload_obj))

        return ContainerResourceRequirements(cpu=payload_obj['cpu'], memory_in_gb=payload_obj['memoryInGB'],
                                             gpu=payload_obj['gpu'], cpu_limit=payload_obj['cpuLimit'],
                                             memory_in_gb_limit=payload_obj['memoryInGBLimit'])


class LivenessProbeRequirements(object):
    """Defines liveness probe time requirements for deployments of the Webservice.

    LivenessProbeRequirements configuration values values are specified when deploying or updating a Webervice.
    For example, use the ``deploy_configuration`` or ``update`` methods of the
    :class:`azureml.core.webservice.aks.AksWebservice` class, or the ``create_version``, ``deploy_configuration``,
    or ``update_version`` methods of the :class:`azureml.core.webservice.aks.AksEndpoint` class.

    :var period_seconds: How often (in seconds) to perform the liveness probe. Defaults to 10 seconds.
        Minimum value is 1.
    :vartype period_seconds: int
    :var initial_delay_seconds: The number of seconds after the container has started before liveness probes are
        initiated.
    :vartype initial_delay_seconds: int
    :var timeout_seconds: The number of seconds after which the liveness probe times out. Defaults to 1 second.
        Minimum value is 1.
    :vartype timeout_seconds: int
    :var failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try
        ``failureThreshold`` times before giving up. Defaults to 3. Minimum value is 1.
    :vartype failure_threshold: int
    :var success_threshold: The minimum consecutive successes for the liveness probe to be considered successful
        after having failed. Defaults to 1. Minimum value is 1.
    :vartype success_threshold: int

    :param period_seconds: How often (in seconds) to perform the liveness probe. Defaults to 10 seconds.
        Minimum value is 1.
    :type period_seconds: int
    :param initial_delay_seconds: The number of seconds after the container has started before liveness probes are
        initiated.
    :type initial_delay_seconds: int
    :param timeout_seconds: The number of seconds after which the liveness probe times out. Defaults to 1 second.
        Minimum value is 1.
    :type timeout_seconds: int
    :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try
        ``failureThreshold`` times before giving up. Defaults to 3. Minimum value is 1.
    :type failure_threshold: int
    :param success_threshold: The minimum consecutive successes for the liveness probe to be considered successful
        after having failed. Defaults to 1. Minimum value is 1.
    :type success_threshold: int
    """

    _expected_payload_keys = ['periodSeconds', 'initialDelaySeconds', 'timeoutSeconds',
                              'failureThreshold', 'successThreshold']

    def __init__(self, period_seconds, initial_delay_seconds, timeout_seconds, success_threshold, failure_threshold):
        """Initialize the container resource requirements.

        :param period_seconds: How often (in seconds) to perform the liveness probe. Defaults to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: The number of seconds after the container has started before liveness probes are
            initiated.
        :type initial_delay_seconds: int
        :param timeout_seconds: The number of seconds after which the liveness probe times out. Defaults to 1 second.
            Minimum value is 1.
        :type timeout_seconds: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try
            ``failureThreshold`` times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int
        :param success_threshold: The minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        """
        self.period_seconds = period_seconds
        self.timeout_seconds = timeout_seconds
        self.initial_delay_seconds = initial_delay_seconds
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold

    def serialize(self):
        """Convert this LivenessProbeRequirements object into a JSON serialized dictionary.

        :return: The JSON representation of this LivenessProbeRequirements object.
        :rtype: dict
        """
        return {'periodSeconds': self.period_seconds, 'initialDelaySeconds': self.initial_delay_seconds,
                'timeoutSeconds': self.timeout_seconds, 'successThreshold': self.success_threshold,
                'failureThreshold': self.failure_threshold}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a JSON object into a LivenessProbeRequirements object.

        :param payload_obj: A JSON object to convert to a LivenessProbeRequirements object.
        :type payload_obj: dict
        :return: The LivenessProbeRequirements representation of the provided JSON object.
        :rtype: azureml.core.webservice.aks.LivenessProbeRequirements
        """
        if payload_obj is None:
            return LivenessProbeRequirements(period_seconds=10, initial_delay_seconds=310, timeout_seconds=1,
                                             success_threshold=1, failure_threshold=3)
        for payload_key in LivenessProbeRequirements._expected_payload_keys:
            if payload_key not in payload_obj:
                raise Exception('Invalid webservice payload, missing {} for LivenessProbeRequirements:\n'
                                '{}'.format(payload_key, payload_obj))

        return LivenessProbeRequirements(payload_obj['periodSeconds'], payload_obj['initialDelaySeconds'],
                                         payload_obj['timeoutSeconds'], payload_obj['successThreshold'],
                                         payload_obj['failureThreshold'])


class DataCollection(object):
    """Defines data collection configuration for an :class:`azureml.core.webservice.aks.AksWebservice`.

    :var event_hub_enabled: Indicates whether event hub is enabled for the Webservice.
    :vartype event_hub_enabled: bool
    :var storage_enabled: Indicates whether data collection storage is enabled for the Webservice.
    :vartype storage_enabled: bool

    :param event_hub_enabled: Indicates whether event hub is enabled for the Webservice.
    :type event_hub_enabled: bool
    :param storage_enabled: Indicates whether data collection storage is enabled for the Webservice.
    :type storage_enabled: bool
    """

    _expected_payload_keys = ['eventHubEnabled', 'storageEnabled']

    def __init__(self, event_hub_enabled, storage_enabled):
        """Intialize the DataCollection object.

        :param event_hub_enabled: Indicates whether event hub is enabled for the Webservice.
        :type event_hub_enabled: bool
        :param storage_enabled: Indicates whether data collection storage is enabled for the Webservice.
        :type storage_enabled: bool
        """
        self.event_hub_enabled = event_hub_enabled
        self.storage_enabled = storage_enabled

    def serialize(self):
        """Convert this DataCollection into a JSON serialized dictionary.

        :return: The JSON representation of this DataCollection object.
        :rtype: dict
        """
        return {'eventHubEnabled': self.event_hub_enabled, 'storageEnabled': self.storage_enabled}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a JSON object into a DataCollection object.

        :param payload_obj: A JSON object to convert to a DataCollection object.
        :type payload_obj: dict
        :return: The DataCollection representation of the provided JSON object.
        :rtype: azureml.core.webservice.aks.DataCollection
        """
        for payload_key in DataCollection._expected_payload_keys:
            if payload_key not in payload_obj:
                raise Exception('Invalid webservice payload, missing {} for DataCollection:\n'
                                '{}'.format(payload_key, payload_obj))

        return DataCollection(payload_obj['eventHubEnabled'], payload_obj['storageEnabled'])


class AksWebservice(Webservice):
    """Represents a machine learning model deployed as a web service endpoint on Azure Kubernetes Service.

    A deployed service is created from a model, script, and associated files. The resulting web
    service is a load-balanced, HTTP endpoint with a REST API. You can send data to this API and
    receive the prediction returned by the model.

    AksWebservice deploys a single service to one endpoint. To deploy multiple services to one endpoint, use the
    :class:`azureml.core.webservice.AksEndpoint` class.

    For more information, see `Deploy a model to an Azure Kubernetes Service
    cluster <https://docs.microsoft.com/azure/machine-learning/how-to-deploy-azure-kubernetes-service>`_.

    .. remarks::

        The recommended deployment pattern is to create a deployment configuration object with the
        ``deploy_configuration`` method and then use it with the ``deploy`` method of the
        :class:`azureml.core.model.Model` class as shown below.

        .. code-block:: inject notebooks/how-to-use-azureml/deployment/production-deploy-to-aks
        /production-deploy-to-aks.ipynb#sample-deploy-to-aks

        There are a number of ways to deploy a model as a webservice, including with the:

        * ``deploy`` method of the :class:`azureml.core.model.Model` for models already registered in the workspace.

        * ``deploy_from_image`` method of :class:`azureml.core.webservice.Webservice`.

        * ``deploy_from_model`` method of :class:`azureml.core.webservice.Webservice` for models already registered
          in the workspace. This method will create an image.

        * ``deploy`` method of the :class:`azureml.core.webservice.Webservice`, which will register a model and
          create an image.

        For information on working with webservices, see

        * `Consume an Azure Machine Learning model deployed
          as a web service <https://docs.microsoft.com/azure/machine-learning/how-to-consume-web-service>`_

        * `Monitor and collect data from ML web service
          endpoints <https://docs.microsoft.com/azure/machine-learning/how-to-enable-app-insights>`_

        * `Troubleshooting
          deployment <https://docs.microsoft.com/azure/machine-learning/how-to-troubleshoot-deployment>`_

        The *Variables* section lists attributes of a local representation of the cloud AksWebservice object. These
        variables should be considered read-only. Changing their values will not be reflected in the corresponding
        cloud object.

    :var enable_app_insights: Whether or not AppInsights logging is enabled for the Webservice.
    :vartype enable_app_insights: bool
    :var autoscaler: The Autoscaler object for the Webservice.
    :vartype autoscaler: azureml.core.webservice.webservice.AutoScaler
    :var compute_name: The name of the ComputeTarget that the Webservice is deployed to.
    :vartype compute_name: str
    :var container_resource_requirements: The container resource requirements for the Webservice.
    :vartype container_resource_requirements: azureml.core.webservice.aks.ContainerResourceRequirements
    :var liveness_probe_requirements: The liveness probe requirements for the Webservice.
    :vartype liveness_probe_requirements: azureml.core.webservice.aks.LivenessProbeRequirements
    :var data_collection: The DataCollection object for the Webservice.
    :vartype data_collection: azureml.core.webservice.aks.DataCollection
    :var max_concurrent_requests_per_container: The maximum number of concurrent requests per container for
        the Webservice.
    :vartype max_concurrent_requests_per_container: int
    :var max_request_wait_time: The maximum request wait time for the Webservice, in milliseconds.
    :vartype max_request_wait_time: int
    :var num_replicas: The number of replicas for the Webservice. Each replica corresponds to an AKS pod.
    :vartype num_replicas: int
    :var scoring_timeout_ms: The scoring timeout for the Webservice, in milliseconds.
    :vartype scoring_timeout_ms: int
    :var azureml.core.webservice.AksWebservice.scoring_uri: The scoring endpoint for the Webservice
    :vartype azureml.core.webservice.AksWebservice.scoring_uri: str
    :var is_default: If the Webservice is the default version for the parent AksEndpoint.
    :vartype is_default: bool
    :var traffic_percentile: What percentage of traffic to route to the Webservice in the parent AksEndpoint.
    :vartype traffic_percentile: int
    :var version_type: The version type for the Webservice in the parent AksEndpoint.
    :vartype version_type: azureml.core.webservice.aks.AksEndpoint.VersionType
    :var token_auth_enabled: Whether or not token auth is enabled for the Webservice.
    :vartype token_auth_enabled: bool
    :var environment: The Environment object that was used to create the Webservice.
    :vartype environment: azureml.core.Environment
    :var azureml.core.webservice.AksWebservice.models: A list of Models deployed to the Webservice.
    :vartype azureml.core.webservice.AksWebservice.models: builtin.list[azureml.core.Model]
    :var deployment_status: The deployment status of the Webservice.
    :vartype deployment_status: str
    :var namespace: The AKS namespace of the Webservice.
    :vartype namespace: str
    :var azureml.core.webservice.AksWebservice.swagger_uri: The swagger endpoint for the Webservice.
    :vartype azureml.core.webservice.AksWebservice.swagger_uri: str
    """

    _expected_payload_keys = Webservice._expected_payload_keys + ['appInsightsEnabled', 'authEnabled',
                                                                  'autoScaler', 'computeName',
                                                                  'containerResourceRequirements', 'dataCollection',
                                                                  'maxConcurrentRequestsPerContainer',
                                                                  'maxQueueWaitMs', 'numReplicas', 'scoringTimeoutMs',
                                                                  'scoringUri', 'livenessProbeRequirements',
                                                                  'aadAuthEnabled']
    _webservice_type = AKS_WEBSERVICE_TYPE

    def __init__(self, obj_dict):
        """Initialize the Webservice instance.

        This is used because the constructor is used as a getter.

        :param workspace: The workspace that contains the model to deploy.
        :type workspace: azureml.core.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        # Validate obj_dict with _expected_payload_keys
        # AksWebservice._validate_get_payload(obj_dict)

        # Initialize common Webservice attributes
        super(AksWebservice, self).__init__(obj_dict)

        # Initialize expected AksWebservice specific attributes
        self.enable_app_insights = obj_dict.get('appInsightsEnabled')
        self.autoscaler = AutoScaler.deserialize(obj_dict.get('autoScaler')) if "autoScaler" in obj_dict else None
        self.compute_name = obj_dict.get('computeName')
        self.container_resource_requirements = \
            ContainerResourceRequirements.deserialize(
                obj_dict.get('containerResourceRequirements')) if "containerResourceRequirements" in obj_dict else None
        self.liveness_probe_requirements = \
            LivenessProbeRequirements.deserialize(
                obj_dict.get('livenessProbeRequirements')) if "livenessProbeRequirements" in obj_dict else None
        self.data_collection = DataCollection.deserialize(
            obj_dict.get('dataCollection')) if "dataCollection" in obj_dict else None
        self.max_concurrent_requests_per_container = obj_dict.get(
            'maxConcurrentRequestsPerContainer') if "maxConcurrentRequestsPerContainer" in obj_dict else None
        self.max_request_wait_time = obj_dict.get('maxQueueWaitMs')
        self.num_replicas = obj_dict.get('numReplicas')
        self.scoring_timeout_ms = obj_dict.get('scoringTimeoutMs')
        self.scoring_uri = obj_dict.get('scoringUri')
        self.is_default = obj_dict.get('isDefault')
        self.traffic_percentile = obj_dict.get('trafficPercentile')
        self.version_type = obj_dict.get('type')

        self.token_auth_enabled = obj_dict.get('aadAuthEnabled')
        env_image_request = obj_dict.get('environmentImageRequest')
        env_dict = env_image_request.get('environment') if env_image_request else None
        # self.environment = Environment._deserialize_and_add_to_object(env_dict) if env_dict else None
        self.environment = ModelEnvironmentDefinition(**env_dict) if env_dict else None
        models = obj_dict.get('models')
        # self.models = [Model.deserialize(workspace, model_payload) for model_payload in models] if models else []
        self.models = [Model(**model) for model in models] if models else []

        # Initialize other AKS utility attributes
        self.deployment_status = obj_dict.get('deploymentStatus')
        self.namespace = obj_dict.get('namespace')
        self.swagger_uri = '/'.join(self.scoring_uri.split('/')[:-1]) + WEBSERVICE_SWAGGER_PATH \
            if self.scoring_uri else None
        self._model_config_map = obj_dict.get('modelConfigMap')
        self._refresh_token_time = None

    def __repr__(self):
        """Return the string representation of the AksWebservice object.

        :return: String representation of the AksWebservice object
        :rtype: str
        """
        return super().__repr__()

    @staticmethod
    def _from_service_response(service_response, **kwargs):
        if service_response.compute_type != AKS_WEBSERVICE_TYPE:
            raise Exception("Invalid input provided for AKSService")
        aks_webservice = AksWebservice({})
        aks_webservice.compute_type = AKS_WEBSERVICE_TYPE
        aks_webservice.name = service_response.name
        aks_webservice.description = service_response.description
        aks_webservice.tags = service_response.kv_tags
        aks_webservice.properties = service_response.properties
        aks_webservice.state = service_response.state
        aks_webservice.created_time = service_response.created_time
        aks_webservice.updated_time = service_response.updated_time
        aks_webservice.error = service_response.error
        aks_webservice.created_by = service_response.created_by
        aks_webservice.is_default = service_response.is_default
        aks_webservice.traffic_percentile = service_response.traffic_percentile
        aks_webservice.image_id = service_response.image_id
        aks_webservice.image_digest = service_response.image_digest
        aks_webservice.models = service_response.models
        aks_webservice.container_resource_requirements = service_response.container_resource_requirements
        aks_webservice.max_concurrent_requests_per_container = service_response.max_concurrent_requests_per_container
        aks_webservice.max_request_wait_time = service_response.max_queue_wait_ms
        aks_webservice.compute_name = service_response.compute_name
        aks_webservice.namespace = service_response.namespace
        aks_webservice.num_replicas = service_response.num_replicas
        aks_webservice.data_collection = service_response.data_collection
        aks_webservice.enable_app_insights = service_response.app_insights_enabled
        aks_webservice.autoscaler = service_response.auto_scaler
        aks_webservice.scoring_uri = service_response.scoring_uri
        aks_webservice.deployment_status = service_response.deployment_status
        aks_webservice.scoring_timeout_ms = service_response.scoring_timeout_ms
        aks_webservice.liveness_probe_requirements = service_response.liveness_probe_requirements
        # TODO : Check for readiness_probe_requirements
        aks_webservice.auth_enabled = service_response.auth_enabled
        aks_webservice.token_auth_enabled = service_response.aad_auth_enabled
        # TODO : storage_init_enabled
        aks_webservice.swagger_uri = service_response.swagger_uri
        aks_webservice._model_config_map = service_response.model_config_map
        aks_webservice.environment = service_response.environment_image_request.environment
        # TODO : environment_variables
        # TODO : instance_type
        aks_webservice.version_type = service_response.type
        aks_webservice.service_context = kwargs.pop("service_context", None)

        return aks_webservice

    def _create_update_service_request(self, deploy_config=None, image=None, autoscale_enabled=None,
                                       autoscale_min_replicas=None,
                                       autoscale_max_replicas=None,
                                       autoscale_refresh_seconds=None, autoscale_target_utilization=None,
                                       collect_model_data=None,
                                       auth_enabled=None, cpu_cores=None, memory_gb=None,
                                       enable_app_insights=None, scoring_timeout_ms=None,
                                       replica_max_concurrent_requests=None,
                                       max_request_wait_time=None, num_replicas=None, tags=None,
                                       properties=None, description=None, models=None, inference_config=None,
                                       gpu_cores=None,
                                       period_seconds=None, initial_delay_seconds=None, timeout_seconds=None,
                                       success_threshold=None,
                                       failure_threshold=None, namespace=None, token_auth_enabled=None,
                                       cpu_cores_limit=None,
                                       memory_gb_limit=None, **kwargs):
        """Update the Webservice with provided properties.

        Values left as None will remain unchanged in this Webservice.

        :param image: A new Image to deploy to the Webservice
        :type image: azureml.core.Image
        :param autoscale_enabled: Enable or disable autoscaling of this Webservice
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice
        :type autoscale_target_utilization: int
        :param collect_model_data: Enable or disable model data collection for this Webservice
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable auth for this Webservice
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per replica to allow for this
            Webservice.
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this Webservice
        :type num_replicas: int
        :param tags: Dictionary of key value tags to give this Webservice. Will replace existing tags.
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to add to existing properties dictionary
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :param models: A list of Model objects to package with the updated service
        :type models: builtin.list[azureml.core.Model]
        :param inference_config: An InferenceConfig object used to provide the required model deployment properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param gpu_cores: The number of gpu cores to allocate for this Webservice
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated.
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 1 second.
            Minimum value is 1.
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int
        :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
            ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
        :type namespace: str
        :param token_auth_enabled: Whether or not to enable Token auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :param cpu_cores_limit: The max number of cpu cores this Webservice is allowed to use. Can be a decimal.
        :type cpu_cores_limit: float
        :param memory_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use. Can be a decimal.
        :type memory_gb_limit: float
        :param kwargs: include params to support migrating AKS web service to Kubernetes online endpoint and
            deployment. is_migration=True|False, compute_target=<compute target with AzureML extension installed to
            host migrated Kubernetes online endpoint and deployment>.
        :type kwargs: varies
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        # Image usage has been deprecated only environments are supported

        autoscale_enabled = deploy_config.autoscale_enabled
        autoscale_min_replicas = deploy_config.autoscale_min_replicas
        autoscale_max_replicas = deploy_config.autoscale_max_replicas
        autoscale_refresh_seconds = deploy_config.autoscale_refresh_seconds
        autoscale_target_utilization = deploy_config.autoscale_target_utilization
        collect_model_data = deploy_config.collect_model_data
        auth_enabled = deploy_config.auth_enabled
        cpu_cores = deploy_config

        if not image and autoscale_enabled is None and not autoscale_min_replicas and not autoscale_max_replicas \
                and not autoscale_refresh_seconds and not autoscale_target_utilization and collect_model_data is None \
                and auth_enabled is None and not cpu_cores and not memory_gb and not gpu_cores \
                and enable_app_insights is None and not scoring_timeout_ms and not replica_max_concurrent_requests \
                and not max_request_wait_time and not num_replicas and tags is None and properties is None \
                and not description and not period_seconds and not initial_delay_seconds and not timeout_seconds \
                and models is None and inference_config is None and not failure_threshold and not success_threshold \
                and not namespace and token_auth_enabled is None and cpu_cores_limit is None \
                and memory_gb_limit is None:
            raise Exception('No parameters provided to update.', )

        self._validate_update(image, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                              autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                              memory_gb, enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests,
                              max_request_wait_time, num_replicas, tags, properties, description, models,
                              inference_config, gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                              success_threshold, failure_threshold, namespace, auth_enabled, token_auth_enabled,
                              cpu_cores_limit, memory_gb_limit)

        patch_list = []

        if not models:
            models = self.models if self.models else None

        environment_image_request = kwargs.pop("environment_image_request")

        patch_list.append({'op': 'replace', 'path': '/environmentImageRequest',
                           'value': environment_image_request})

        properties = properties or {}

        if self.autoscaler.autoscale_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/autoscaleEnabled', 'value': autoscale_enabled})
        if autoscale_min_replicas:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/minReplicas', 'value': autoscale_min_replicas})
        if autoscale_max_replicas:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/maxReplicas', 'value': autoscale_max_replicas})
        if autoscale_refresh_seconds:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/refreshPeriodInSeconds',
                               'value': autoscale_refresh_seconds})
        if autoscale_target_utilization:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/targetUtilization',
                               'value': autoscale_target_utilization})
        if collect_model_data is not None:
            patch_list.append({'op': 'replace', 'path': '/dataCollection/storageEnabled', 'value': collect_model_data})

        if auth_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/authEnabled', 'value': auth_enabled})
        if token_auth_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/aadAuthEnabled', 'value': token_auth_enabled})

        if cpu_cores:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/cpu', 'value': cpu_cores})
        if cpu_cores_limit:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/cpuLimit',
                               'value': cpu_cores_limit})
        if memory_gb:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/memoryInGB',
                               'value': memory_gb})
        if memory_gb_limit:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/memoryInGBLimit',
                               'value': memory_gb_limit})

        if gpu_cores:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/gpu', 'value': gpu_cores})
        if enable_app_insights is not None:
            patch_list.append({'op': 'replace', 'path': '/appInsightsEnabled', 'value': enable_app_insights})
        if scoring_timeout_ms:
            patch_list.append({'op': 'replace', 'path': '/scoringTimeoutMs', 'value': scoring_timeout_ms})
        if replica_max_concurrent_requests:
            patch_list.append({'op': 'replace', 'path': '/maxConcurrentRequestsPerContainer',
                               'value': replica_max_concurrent_requests})
        if max_request_wait_time:
            patch_list.append({'op': 'replace', 'path': '/maxQueueWaitMs',
                               'value': max_request_wait_time})
        if num_replicas:
            patch_list.append({'op': 'replace', 'path': '/numReplicas', 'value': num_replicas})
        if period_seconds:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/periodSeconds',
                               'value': period_seconds})
        if initial_delay_seconds:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/initialDelaySeconds',
                               'value': initial_delay_seconds})
        if timeout_seconds:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/timeoutSeconds',
                               'value': timeout_seconds})
        if success_threshold:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/successThreshold',
                               'value': success_threshold})
        if failure_threshold:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/failureThreshold',
                               'value': failure_threshold})
        if namespace:
            patch_list.append({'op': 'replace', 'path': '/namespace', 'value': namespace})
        if tags is not None:
            patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': tags})
        if properties is not None:
            for key in properties:
                patch_list.append({'op': 'add', 'path': '/properties/{}'.format(key), 'value': properties[key]})
        if description:
            patch_list.append({'op': 'replace', 'path': '/description', 'value': description})

        patch_operation_list = [JsonPatchOperation(**patch) for patch in patch_list]

        return patch_operation_list

    def _validate_update(self, image, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                         autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                         memory_gb, enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests,
                         max_request_wait_time, num_replicas, tags, properties, description, models,
                         inference_config, gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                         success_threshold, failure_threshold, namespace, auth_enabled, token_auth_enabled,
                         cpu_cores_limit, memory_gb_limit):
        """Validate the values provided to update the webservice.

        :param image:
        :type image: azureml.core.Image
        :param autoscale_enabled:
        :type autoscale_enabled: bool
        :param autoscale_min_replicas:
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas:
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds:
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization:
        :type autoscale_target_utilization: int
        :param collect_model_data:
        :type collect_model_data: bool
        :param cpu_cores:
        :type cpu_cores: float
        :param memory_gb:
        :type memory_gb: float
        :param enable_app_insights:
        :type enable_app_insights: bool
        :param scoring_timeout_ms:
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests:
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error
        :type max_request_wait_time: int
        :param num_replicas:
        :type num_replicas: int
        :param tags:
        :type tags: dict[str, str]
        :param properties:
        :type properties: dict[str, str]
        :param description:
        :type description: str
        :param models: A list of Model objects to package with this image. Can be an empty list
        :type models: :class:`list[azureml.core.Model]`
        :param inference_config: An InferenceConfig object used to determine required model properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param: gpu_cores
        :type: int
        :param period_seconds:
        :type period_seconds: int
        :param initial_delay_seconds:
        :type initial_delay_seconds: int
        :param timeout_seconds:
        :type timeout_seconds: int
        :param success_threshold:
        :type success_threshold: int
        :param failure_threshold:
        :type failure_threshold: int
        :param namespace:
        :type namespace: str
        :param auth_enabled: If Key auth is enabled.
        :type auth_enabled: bool
        :param token_auth_enabled: Whether or not to enable Token auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :param cpu_cores_limit: The max number of cpu cores this Webservice is allowed to use. Can be a decimal.
        :type cpu_cores_limit: float
        :param memory_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use. Can be a decimal.
        :type memory_gb_limit: float
        """
        error = ""
        if image and self.environment:
            error += 'Error, unable to use Image object to update Webservice created with Environment object.\n'
        # if inference_config and inference_config.environment and self.image:
        #     error += 'Error, unable to use Environment object to update Webservice created with Image object.\n'
        # if image and inference_config:
        #     error += 'Error, unable to pass both an Image object and an InferenceConfig object to update.\n'
        if cpu_cores is not None:
            if cpu_cores <= 0:
                error += 'Error, cpu_cores must be greater than zero.\n'
            if self.container_resource_requirements is not None and \
                    self.container_resource_requirements.cpu_limit is not None \
                    and cpu_cores > self.container_resource_requirements.cpu_limit:
                error += 'Error, cpu_cores must be ' \
                         'less than or equal to container_resource_requirements.cpu_limit.\n'
        if cpu_cores_limit is not None:
            if cpu_cores_limit <= 0:
                error += 'Error, cpu_cores_limit must be greater than zero.\n'
            if cpu_cores is not None and cpu_cores_limit < cpu_cores:
                error += 'Error, cpu_cores_limit must be greater than or equal to cpu_cores.\n'
            if self.container_resource_requirements is not None and \
                    self.container_resource_requirements.cpu is not None \
                    and cpu_cores_limit < self.container_resource_requirements.cpu:
                error += 'Error, cpu_cores_limit must be ' \
                         'greater than or equal to container_resource_requirements.cpu.\n'
        if memory_gb is not None:
            if memory_gb <= 0:
                error += 'Error, memory_gb must be greater than zero.\n'
            if self.container_resource_requirements and self.container_resource_requirements.memory_in_gb_limit \
                    and memory_gb > self.container_resource_requirements.memory_in_gb_limit:
                error += 'Error, memory_gb must be ' \
                         'less than or equal to container_resource_requirements.memory_in_gb_limit.\n'
        if memory_gb_limit is not None:
            if memory_gb_limit <= 0:
                error += 'Error, memory_gb_limit must be greater than zero.\n'
            elif memory_gb and memory_gb_limit < memory_gb:
                error += 'Error, memory_gb_limit must be greater than or equal to memory_gb.\n'
            elif self.container_resource_requirements and self.container_resource_requirements.memory_in_gb \
                    and memory_gb_limit < self.container_resource_requirements.memory_in_gb:
                error += 'Error, memory_gb_limit must be ' \
                         'greater than or equal to container_resource_requirements.memory_in_gb.\n'
        if gpu_cores is not None and gpu_cores < 0:
            error += 'Error, gpu_cores must be greater than or equal to zero.\n'
        if scoring_timeout_ms is not None and scoring_timeout_ms <= 0:
            error += 'Error, scoring_timeout_ms must be greater than zero.\n'
        if replica_max_concurrent_requests is not None and replica_max_concurrent_requests <= 0:
            error += 'Error, replica_max_concurrent_requests must be greater than zero.\n'
        if max_request_wait_time is not None and max_request_wait_time <= 0:
            error += 'Error, max_request_wait_time must be greater than zero.\n'
        if num_replicas is not None and num_replicas <= 0:
            error += 'Error, num_replicas must be greater than zero.\n'
        if period_seconds is not None and period_seconds <= 0:
            error += 'Error, period_seconds must be greater than zero.\n'
        if timeout_seconds is not None and timeout_seconds <= 0:
            error += 'Error, timeout_seconds must be greater than zero.\n'
        if initial_delay_seconds is not None and initial_delay_seconds <= 0:
            error += 'Error, initial_delay_seconds must be greater than zero.\n'
        if success_threshold is not None and success_threshold <= 0:
            error += 'Error, success_threshold must be greater than zero.\n'
        if failure_threshold is not None and failure_threshold <= 0:
            error += 'Error, failure_threshold must be greater than zero.\n'
        if namespace and not re.match(NAMESPACE_REGEX, namespace):
            error += 'Error, namespace must be a valid Kubernetes namespace. ' \
                     'Regex for validation is ' + NAMESPACE_REGEX + '\n'
        if autoscale_enabled:
            if num_replicas:
                error += 'Error, autoscale enabled and num_replicas provided.\n'
            if autoscale_min_replicas is not None and autoscale_min_replicas <= 0:
                error += 'Error, autoscale_min_replicas must be greater than zero.\n'
            if autoscale_max_replicas is not None and autoscale_max_replicas <= 0:
                error += 'Error, autoscale_max_replicas must be greater than zero.\n'
            if autoscale_min_replicas and autoscale_max_replicas and \
                    autoscale_min_replicas > autoscale_max_replicas:
                error += 'Error, autoscale_min_replicas cannot be greater than autoscale_max_replicas.\n'
            if autoscale_refresh_seconds is not None and autoscale_refresh_seconds <= 0:
                error += 'Error, autoscale_refresh_seconds must be greater than zero.\n'
            if autoscale_target_utilization is not None and autoscale_target_utilization <= 0:
                error += 'Error, autoscale_target_utilization must be greater than zero.\n'
        else:
            if autoscale_enabled is False and not num_replicas:
                error += 'Error, autoscale disabled but num_replicas not provided.\n'
            if autoscale_min_replicas:
                error += 'Error, autoscale_min_replicas provided without enabling autoscaling.\n'
            if autoscale_max_replicas:
                error += 'Error, autoscale_max_replicas provided without enabling autoscaling.\n'
            if autoscale_refresh_seconds:
                error += 'Error, autoscale_refresh_seconds provided without enabling autoscaling.\n'
            if autoscale_target_utilization:
                error += 'Error, autoscale_target_utilization provided without enabling autoscaling.\n'
        if token_auth_enabled and auth_enabled:
            error += 'Error, cannot set both token_auth_enabled and auth_enabled.\n'
        elif token_auth_enabled and (self.auth_enabled and auth_enabled is not False):
            error += 'Error, cannot set token_auth_enabled without disabling key auth (set auth_enabled to False).\n'
        elif auth_enabled and (self.token_auth_enabled and token_auth_enabled is not False):
            error += 'Error, cannot set token_auth_enabled without disabling key auth (set auth_enabled to False).\n'

        if error:
            raise Exception(error)

    def serialize(self):
        """Convert this Webservice into a JSON serialized dictionary.

        :return: The JSON representation of this Webservice.
        :rtype: dict
        """

        properties = super(AksWebservice, self).serialize()
        # TODO: Check if we need mapping for autoscler, container_resource_requirements, liveness_probe_requirements,
        # data_collection
        # and if it warrants use of v1 like class
        # autoscaler = self.autoscaler.serialize() if self.autoscaler else None
        autoscaler = self.autoscaler.as_dict(key_transformer=self._attribute_transformer) if self.autoscaler else None
        container_resource_requirements = self.container_resource_requirements.as_dict(
            key_transformer=self._attribute_transformer) \
            if self.container_resource_requirements else None
        liveness_probe_requirements = self.liveness_probe_requirements.as_dict(
            key_transformer=self._attribute_transformer) \
            if self.liveness_probe_requirements else None
        data_collection = self.data_collection.as_dict(
            key_transformer=self._attribute_transformer) if self.data_collection else None
        # env_details = Environment._serialize_to_dict(self.environment) if self.environment else None
        env_details = self.environment.as_dict(
            key_transformer=self._attribute_transformer) if self.environment else None
        model_details = [model.as_dict(key_transformer=self._attribute_transformer) for model in
                         self.models] if self.models else None

        deployment_status = self.deployment_status.as_dict(
            key_transformer=self._attribute_transformer) if self.deployment_status else None

        aks_properties = {'appInsightsEnabled': self.enable_app_insights, 'authEnabled': self.auth_enabled,
                          'autoScaler': autoscaler, 'computeName': self.compute_name,
                          'containerResourceRequirements': container_resource_requirements,
                          'dataCollection': data_collection, 'imageId': self.image_id,
                          'maxConcurrentRequestsPerContainer': self.max_concurrent_requests_per_container,
                          'maxQueueWaitMs': self.max_request_wait_time,
                          'livenessProbeRequirements': liveness_probe_requirements,
                          'numReplicas': self.num_replicas, 'deploymentStatus': deployment_status,
                          'scoringTimeoutMs': self.scoring_timeout_ms, 'scoringUri': self.scoring_uri,
                          'aadAuthEnabled': self.token_auth_enabled, 'environmentDetails': env_details,
                          'modelDetails': model_details, 'isDefault': self.is_default,
                          'trafficPercentile': self.traffic_percentile, 'versionType': self.version_type}
        properties.update(aks_properties)
        return properties


class AksServiceDeploymentConfiguration(WebserviceDeploymentConfiguration):
    """Represents a deployment configuration information for a service deployed on Azure Kubernetes Service.

    Create an AksServiceDeploymentConfiguration object using the ``deploy_configuration`` method of the
    :class:`azureml.core.webservice.aks.AksWebservice` class.

    :var autoscale_enabled: Indicates whether to enable autoscaling for this Webservice.
        Defaults to True if ``num_replicas`` is None.
    :vartype autoscale_enabled: bool
    :var autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice.
        Defaults to 1.
    :vartype autoscale_min_replicas: int
    :var autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice.
        Defaults to 10
    :vartype autoscale_max_replicas: int
    :var autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice.
        Defaults to 1.
    :vartype autoscale_refresh_seconds: int
    :var autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
        attempt to maintain for this Webservice. Defaults to 70.
    :vartype autoscale_target_utilization: int
    :var collect_model_data: Whether or not to enable model data collection for this Webservice.
        Defaults to False.
    :vartype collect_model_data: bool
    :var auth_enabled: Whether or not to enable auth for this Webservice. Defaults to True.
    :vartype auth_enabled: bool
    :var cpu_cores: The number of CPU cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
    :vartype cpu_cores: float
    :var memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        Defaults to 0.5
    :vartype memory_gb: float
    :var enable_app_insights: Whether or not to enable Application Insights logging for this Webservice.
        Defaults to False
    :vartype enable_app_insights: bool
    :var scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice. Defaults to 60000.
    :vartype scoring_timeout_ms: int
    :var replica_max_concurrent_requests: The number of maximum concurrent requests per replica to allow for this
        Webservice. Defaults to 1. **Do not change this setting from the default value of 1 unless instructed by
        Microsoft Technical Support or a member of Azure Machine Learning team.**
    :vartype replica_max_concurrent_requests: int
    :var max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
        before returning a 503 error. Defaults to 500.
    :vartype max_request_wait_time: int
    :var num_replicas: The number of containers to allocate for this Webservice. No default, if this parameter
        is not set then the autoscaler is enabled by default.
    :vartype num_replicas: int
    :var primary_key: A primary auth key to use for this Webservice.
    :vartype primary_key: str
    :var secondary_key: A secondary auth key to use for this Webservice.
    :vartype secondary_key: str
    :var azureml.core.webservice.AksServiceDeploymentConfiguration.tags: Dictionary of key value tags to give this
        Webservice.
    :vartype tags: dict[str, str]
    :var azureml.core.webservice.AksServiceDeploymentConfiguration.properties: Dictionary of key value properties to
        give this Webservice. These properties cannot be changed after deployment, however new key value pairs can
        be added.
    :vartype properties: dict[str, str]
    :var azureml.core.webservice.AksServiceDeploymentConfiguration.description: A description to give this Webservice.
    :vartype description: str
    :var gpu_cores: The number of GPU cores to allocate for this Webservice. Defaults to 0.
    :vartype gpu_cores: int
    :var period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
        Minimum value is 1.
    :vartype period_seconds: int
    :var initial_delay_seconds: Number of seconds after the container has started before liveness probes are
        initiated. Defaults to 310.
    :vartype initial_delay_seconds: int
    :var timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
        Minimum value is 1.
    :vartype timeout_seconds: int
    :var success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
        after having failed. Defaults to 1. Minimum value is 1.
    :vartype success_threshold: int
    :var failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try ``failureThreshold``
        times before giving up. Defaults to 3. Minimum value is 1.
    :vartype failure_threshold: int
    :var azureml.core.webservice.AksServiceDeploymentConfiguration.namespace: The Kubernetes namespace in which to
        deploy this Webservice: up to 63 lowercase alphanumeric ('a'-'z', '0'-'9') and hyphen ('-') characters. The
        first and last characters cannot be hyphens.
    :vartype namespace: str
    :var token_auth_enabled: Whether or not to enable Azure Active Directory auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False.
    :vartype token_auth_enabled: bool
    :param cpu_cores_limit: The max number of cpu cores this Webservice is allowed to use. Can be a decimal.
    :vartype cpu_cores_limit: float
    :param memory_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use. Can be a decimal.
    :vartype memory_gb_limit: float

    :param autoscale_enabled: Indicates whether to enable autoscaling for this Webservice.
        Defaults to True if ``num_replicas`` is None.
    :type autoscale_enabled: bool
    :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice.
        Defaults to 1.
    :type autoscale_min_replicas: int
    :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice.
        Defaults to 10
    :type autoscale_max_replicas: int
    :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice.
        Defaults to 1.
    :type autoscale_refresh_seconds: int
    :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
        attempt to maintain for this Webservice. Defaults to 70.
    :type autoscale_target_utilization: int
    :param collect_model_data: Whether or not to enable model data collection for this Webservice.
        Defaults to False.
    :type collect_model_data: bool
    :param auth_enabled: Whether or not to enable auth for this Webservice. Defaults to True.
    :type auth_enabled: bool
    :param cpu_cores: The number of CPU cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
    :type cpu_cores: float
    :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        Defaults to 0.5
    :type memory_gb: float
    :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice.
        Defaults to False
    :type enable_app_insights: bool
    :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice. Defaults to 60000.
    :type scoring_timeout_ms: int
    :param replica_max_concurrent_requests: The number of maximum concurrent requests per replica to allow for this
        Webservice. Defaults to 1. **Do not change this setting from the default value of 1 unless instructed by
        Microsoft Technical Support or a member of Azure Machine Learning team.**
    :type replica_max_concurrent_requests: int
    :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
        before returning a 503 error. Defaults to 500.
    :type max_request_wait_time: int
    :param num_replicas: The number of containers to allocate for this Webservice. No default, if this parameter
        is not set then the autoscaler is enabled by default.
    :type num_replicas: int
    :param primary_key: A primary auth key to use for this Webservice.
    :type primary_key: str
    :param secondary_key: A secondary auth key to use for this Webservice.
    :type secondary_key: str
    :param tags: Dictionary of key value tags to give this Webservice.
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
        be changed after deployment, however new key value pairs can be added.
    :type properties: dict[str, str]
    :param description: A description to give this Webservice.
    :type description: str
    :param gpu_cores: The number of GPU cores to allocate for this Webservice. Defaults to 0.
    :type gpu_cores: int
    :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
        Minimum value is 1.
    :type period_seconds: int
    :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
        initiated. Defaults to 310.
    :type initial_delay_seconds: int
    :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
        Minimum value is 1.
    :type timeout_seconds: int
    :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
        after having failed. Defaults to 1. Minimum value is 1.
    :type success_threshold: int
    :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try
        ``failureThreshold`` times before giving up. Defaults to 3. Minimum value is 1.
    :type failure_threshold: int
    :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
        ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
    :type namespace: str
    :param token_auth_enabled: Whether or not to enable Azure Active Directory auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False.
    :type token_auth_enabled: bool
    :param cpu_cores_limit: The max number of cpu cores this Webservice is allowed to use. Can be a decimal.
    :vartype cpu_cores_limit: float
    :param memory_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use. Can be a decimal.
    :vartype memory_gb_limit: float
    """

    def __init__(self, autoscale_enabled=None, autoscale_min_replicas=None, autoscale_max_replicas=None,
                 autoscale_refresh_seconds=None,
                 autoscale_target_utilization=None, collect_model_data=None, auth_enabled=None, cpu_cores=None,
                 memory_gb=None, enable_app_insights=None, scoring_timeout_ms=None,
                 replica_max_concurrent_requests=None, max_request_wait_time=None, num_replicas=None,
                 primary_key=None, secondary_key=None, tags=None, properties=None, description=None,
                 gpu_cores=None, period_seconds=None, initial_delay_seconds=None, timeout_seconds=None,
                 success_threshold=None, failure_threshold=None, namespace=None, token_auth_enabled=None,
                 compute_target_name=None, cpu_cores_limit=None, memory_gb_limit=None):
        """Initialize a configuration object for deploying to an AKS compute target.

        :param autoscale_enabled: Indicates whether to enable autoscaling for this Webservice.
            Defaults to True if ``num_replicas`` is None.
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice.
            Defaults to 1.
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice.
            Defaults to 10
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice.
            Defaults to 1.
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice. Defaults to 70.
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this Webservice.
            Defaults to False.
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable auth for this Webservice. Defaults to True.
        :type auth_enabled: bool
        :param cpu_cores: The number of CPU cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
            Defaults to 0.5
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice.
            Defaults to False
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice. Defaults to 60000.
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per replica to allow for this
            Webservice. Defaults to 1. **Do not change this setting from the default value of 1 unless instructed by
            Microsoft Technical Support or a member of Azure Machine Learning team.**
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error. Defaults to 500.
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this Webservice. No default, if this parameter
            is not set then the autoscaler is enabled by default.
        :type num_replicas: int
        :param primary_key: A primary auth key to use for this Webservice.
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Webservice.
        :type secondary_key: str
        :param tags: Dictionary of key value tags to give this Webservice.
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added.
        :type properties: dict[str, str]
        :param description: A description to give this Webservice.
        :type description: str
        :param gpu_cores: The number of GPU cores to allocate for this Webservice. Defaults to 0.
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated. Defaults to 310.
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
            Minimum value is 1.
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try
            ``failureThreshold`` times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int
        :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
            ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
        :type namespace: str
        :param token_auth_enabled: Whether or not to enable Azure Active Directory auth for this Webservice. If this is
                enabled, users can access this Webservice by fetching access token using their Azure Active Directory
                credentials. Defaults to False.
        :type token_auth_enabled: bool
        :param compute_target_name: The name of the compute target to deploy to
        :type compute_target_name: str
        :param cpu_cores_limit: The max number of cpu cores this Webservice is allowed to use. Can be a decimal.
        :type cpu_cores_limit: float
        :param memory_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use. Can be a decimal.
        :type memory_gb_limit: float
        :return: A configuration object to use when deploying a Webservice object.
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        super(AksServiceDeploymentConfiguration, self).__init__(AksWebservice, description, tags, properties,
                                                                primary_key, secondary_key)
        self.autoscale_enabled = autoscale_enabled
        self.autoscale_min_replicas = autoscale_min_replicas
        self.autoscale_max_replicas = autoscale_max_replicas
        self.autoscale_refresh_seconds = autoscale_refresh_seconds
        self.autoscale_target_utilization = autoscale_target_utilization
        self.collect_model_data = collect_model_data
        self.auth_enabled = auth_enabled
        self.cpu_cores = cpu_cores
        self.cpu_cores_limit = cpu_cores_limit
        self.memory_gb = memory_gb
        self.memory_gb_limit = memory_gb_limit
        self.gpu_cores = gpu_cores
        self.enable_app_insights = enable_app_insights
        self.scoring_timeout_ms = scoring_timeout_ms
        self.replica_max_concurrent_requests = replica_max_concurrent_requests
        self.max_request_wait_time = max_request_wait_time
        self.num_replicas = num_replicas
        self.period_seconds = period_seconds
        self.initial_delay_seconds = initial_delay_seconds
        self.timeout_seconds = timeout_seconds
        self.success_threshold = success_threshold
        self.failure_threshold = failure_threshold
        self.namespace = namespace
        self.token_auth_enabled = token_auth_enabled
        self.compute_target_name = compute_target_name
        self.validate_configuration()

    def validate_configuration(self):
        """Check that the specified configuration values are valid.

        Will raise a WebserviceException if validation fails.

        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        error = ""
        if self.cpu_cores is not None and self.cpu_cores <= 0:
            error += 'Invalid configuration, cpu_cores must be greater than zero.\n'
        if self.cpu_cores is not None and self.cpu_cores_limit is not None and self.cpu_cores_limit < self.cpu_cores:
            error += 'Invalid configuration, cpu_cores_limit must be greater than or equal to cpu_cores.\n'
        if self.memory_gb is not None and self.memory_gb <= 0:
            error += 'Invalid configuration, memory_gb must be greater than zero.\n'
        if self.memory_gb is not None and self.memory_gb_limit is not None and self.memory_gb_limit < self.memory_gb:
            error += 'Invalid configuration, memory_gb_limit must be greater than or equal to memory_gb.\n'
        if self.gpu_cores is not None and self.gpu_cores < 0:
            error += 'Invalid configuration, gpu_cores must be greater than or equal to zero.\n'
        if self.period_seconds is not None and self.period_seconds <= 0:
            error += 'Invalid configuration, period_seconds must be greater than zero.\n'
        if self.initial_delay_seconds is not None and self.initial_delay_seconds <= 0:
            error += 'Invalid configuration, initial_delay_seconds must be greater than zero.\n'
        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            error += 'Invalid configuration, timeout_seconds must be greater than zero.\n'
        if self.success_threshold is not None and self.success_threshold <= 0:
            error += 'Invalid configuration, success_threshold must be greater than zero.\n'
        if self.failure_threshold is not None and self.failure_threshold <= 0:
            error += 'Invalid configuration, failure_threshold must be greater than zero.\n'
        if self.namespace and not re.match(NAMESPACE_REGEX, self.namespace):
            error += 'Invalid configuration, namespace must be a valid Kubernetes namespace. ' \
                     'Regex for validation is ' + NAMESPACE_REGEX + '\n'
        if self.scoring_timeout_ms is not None and self.scoring_timeout_ms <= 0:
            error += 'Invalid configuration, scoring_timeout_ms must be greater than zero.\n'
        if self.replica_max_concurrent_requests is not None and self.replica_max_concurrent_requests <= 0:
            error += 'Invalid configuration, replica_max_concurrent_requests must be greater than zero.\n'
        if self.max_request_wait_time is not None and self.max_request_wait_time <= 0:
            error += 'Invalid configuration, max_request_wait_time must be greater than zero.\n'
        if self.num_replicas is not None and self.num_replicas <= 0:
            error += 'Invalid configuration, num_replicas must be greater than zero.\n'
        if self.autoscale_enabled:
            if self.num_replicas:
                error += 'Invalid configuration, autoscale enabled and num_replicas provided.\n'
            if self.autoscale_min_replicas is not None and self.autoscale_min_replicas <= 0:
                error += 'Invalid configuration, autoscale_min_replicas must be greater than zero.\n'
            if self.autoscale_max_replicas is not None and self.autoscale_max_replicas <= 0:
                error += 'Invalid configuration, autoscale_max_replicas must be greater than zero.\n'
            if self.autoscale_min_replicas and self.autoscale_max_replicas and \
                    self.autoscale_min_replicas > self.autoscale_max_replicas:
                error += 'Invalid configuration, autoscale_min_replicas cannot be greater than ' \
                         'autoscale_max_replicas.\n'
            if self.autoscale_refresh_seconds is not None and self.autoscale_refresh_seconds <= 0:
                error += 'Invalid configuration, autoscale_refresh_seconds must be greater than zero.\n'
            if self.autoscale_target_utilization is not None and self.autoscale_target_utilization <= 0:
                error += 'Invalid configuration, autoscale_target_utilization must be greater than zero.\n'
        else:
            if self.autoscale_enabled is False and not self.num_replicas:
                error += 'Invalid configuration, autoscale disabled but num_replicas not provided.\n'
            if self.autoscale_min_replicas:
                error += 'Invalid configuration, autoscale_min_replicas provided without enabling autoscaling.\n'
            if self.autoscale_max_replicas:
                error += 'Invalid configuration, autoscale_max_replicas provided without enabling autoscaling.\n'
            if self.autoscale_refresh_seconds:
                error += 'Invalid configuration, autoscale_refresh_seconds provided without enabling autoscaling.\n'
            if self.autoscale_target_utilization:
                error += 'Invalid configuration, autoscale_target_utilization provided without enabling autoscaling.\n'
        if self.token_auth_enabled and self.auth_enabled:
            error += "Invalid configuration, auth_enabled and token_auth_enabled cannot both be true.\n"

        if error:
            raise Exception(error)

    def print_deploy_configuration(self):
        """Print the deployment configuration."""
        deploy_config = []
        if self.cpu_cores:
            deploy_config.append('CPU requirement: {}'.format(self.cpu_cores))
        if self.gpu_cores:
            deploy_config.append('GPU requirement: {}'.format(self.gpu_cores))
        if self.memory_gb:
            deploy_config.append('Memory requirement: {}GB'.format(self.memory_gb))
        if self.num_replicas:
            deploy_config.append('Number of replica: {}'.format(self.num_replicas))

        if len(deploy_config) > 0:
            print(', '.join(deploy_config))

    def _to_service_create_request(self, name, environment_image_request, overwrite=False):
        service_create_request = AKSServiceCreateRequest(
            num_replicas=self.num_replicas,
            data_collection=ModelDataCollection(
                storage_enabled=self.collect_model_data
            ),
            app_insights_enabled=self.enable_app_insights,
            auto_scaler=RestAutoScalar(
                autoscale_enabled=self.autoscale_enabled,
                min_replicas=self.autoscale_min_replicas,
                max_replicas=self.autoscale_max_replicas,
                target_utilization=self.autoscale_target_utilization,
                refresh_period_in_seconds=self.autoscale_refresh_seconds
            ),
            container_resource_requirements=RestContainerResourceRequirements(
                cpu=self.cpu_cores,
                cpu_limit=self.cpu_cores_limit,
                memory_in_gb=self.memory_gb,
                memory_in_gb_limit=self.memory_gb_limit,
                gpu=self.gpu_cores,
            ),
            max_concurrent_requests_per_container=self.replica_max_concurrent_requests,
            max_queue_wait_ms=self.max_request_wait_time,
            namespace=self.namespace,
            scoring_timeout_ms=self.scoring_timeout_ms,
            auth_enabled=self.auth_enabled,
            aad_auth_enabled=self.token_auth_enabled,
            liveness_probe_requirements=RestLivenessProbeRequirements(
                period_seconds=self.period_seconds,
                initial_delay_seconds=self.initial_delay_seconds,
                timeout_seconds=self.timeout_seconds,
                failure_threshold=self.failure_threshold,
                success_threshold=self.success_threshold
            ),
            overwrite=overwrite,
            compute_name=self.compute_target_name,
            environment_image_request=environment_image_request,
            name=name
        )

        return service_create_request

    def _to_service_update_request(self, environment_image_request=None, overwrite=False):
        if self.autoscale_enabled is None and not self.autoscale_min_replicas and not self.autoscale_max_replicas \
                and not self.autoscale_refresh_seconds and not self.autoscale_target_utilization \
                and self.collect_model_data is None \
                and self.auth_enabled is None and not self.cpu_cores and not self.memory_gb and not self.gpu_cores \
                and self.enable_app_insights is None and not self.scoring_timeout_ms \
                and not self.replica_max_concurrent_requests \
                and not self.max_request_wait_time and not self.num_replicas and self.tags is None \
                and self.properties is None \
                and not self.description and not self.period_seconds and not self.initial_delay_seconds \
                and not self.timeout_seconds \
                and not self.failure_threshold and not self.success_threshold \
                and not self.namespace and self.token_auth_enabled is None and self.cpu_cores_limit is None \
                and self.memory_gb_limit is None:
            raise Exception('No parameters provided to update.')

        self._validate_update(self.autoscale_enabled, self.autoscale_min_replicas, self.autoscale_max_replicas,
                              self.autoscale_refresh_seconds, self.autoscale_target_utilization,
                              self.collect_model_data, self.cpu_cores,
                              self.memory_gb, self.enable_app_insights, self.scoring_timeout_ms,
                              self.replica_max_concurrent_requests,
                              self.max_request_wait_time, self.num_replicas, self.tags, self.properties,
                              self.description, None, None,
                              self.gpu_cores, self.period_seconds, self.initial_delay_seconds, self.timeout_seconds,
                              self.success_threshold, self.failure_threshold, self.namespace, self.auth_enabled,
                              self.token_auth_enabled,
                              self.cpu_cores_limit, self.memory_gb_limit)

        patch_list = []

        if environment_image_request is not None:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/environmentImageRequest', value=environment_image_request))
        if self.autoscale_enabled is not None:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/autoScaler/autoscaleEnabled', value=self.autoscale_enabled))
        if self.autoscale_min_replicas:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/autoScaler/minReplicas', value=self.autoscale_min_replicas))
        if self.autoscale_max_replicas:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/autoScaler/maxReplicas', value=self.autoscale_max_replicas))
        if self.autoscale_refresh_seconds:
            patch_list.append(JsonPatchOperation(op='replace', path='/autoScaler/refreshPeriodInSeconds',
                                                 value=self.autoscale_refresh_seconds))
        if self.autoscale_target_utilization:
            patch_list.append(JsonPatchOperation(op='replace', path='/autoScaler/targetUtilization',
                                                 value=self.autoscale_target_utilization))
        if self.collect_model_data is not None:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/dataCollection/storageEnabled', value=self.collect_model_data))

        if self.auth_enabled is not None:
            patch_list.append(JsonPatchOperation(op='replace', path='/authEnabled', value=self.auth_enabled))
        if self.token_auth_enabled is not None:
            patch_list.append(JsonPatchOperation(op='replace', path='/aadAuthEnabled', value=self.token_auth_enabled))

        if self.cpu_cores:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/containerResourceRequirements/cpu', value=self.cpu_cores))
        if self.cpu_cores_limit:
            patch_list.append(JsonPatchOperation(op='replace', path='/containerResourceRequirements/cpuLimit',
                                                 value=self.cpu_cores_limit))
        if self.memory_gb:
            patch_list.append(JsonPatchOperation(op='replace', path='/containerResourceRequirements/memoryInGB',
                                                 value=self.memory_gb))
        if self.memory_gb_limit:
            patch_list.append(JsonPatchOperation(op='replace', path='/containerResourceRequirements/memoryInGBLimit',
                                                 value=self.memory_gb_limit))

        if self.gpu_cores:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/containerResourceRequirements/gpu', value=self.gpu_cores))
        if self.enable_app_insights is not None:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/appInsightsEnabled', value=self.enable_app_insights))
        if self.scoring_timeout_ms:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/scoringTimeoutMs', value=self.scoring_timeout_ms))
        if self.replica_max_concurrent_requests:
            patch_list.append(JsonPatchOperation(op='replace', path='/maxConcurrentRequestsPerContainer',
                                                 value=self.replica_max_concurrent_requests))
        if self.max_request_wait_time:
            patch_list.append(JsonPatchOperation(op='replace', path='/maxQueueWaitMs',
                                                 value=self.max_request_wait_time))
        if self.num_replicas:
            patch_list.append(JsonPatchOperation(op='replace', path='/numReplicas', value=self.num_replicas))
        if self.period_seconds:
            patch_list.append(JsonPatchOperation(op='replace', path='/livenessProbeRequirements/periodSeconds',
                                                 value=self.period_seconds))
        if self.initial_delay_seconds:
            patch_list.append(JsonPatchOperation(op='replace', path='/livenessProbeRequirements/initialDelaySeconds',
                                                 value=self.initial_delay_seconds))
        if self.timeout_seconds:
            patch_list.append(JsonPatchOperation(op='replace', path='/livenessProbeRequirements/timeoutSeconds',
                                                 value=self.timeout_seconds))
        if self.success_threshold:
            patch_list.append(JsonPatchOperation(op='replace', path='/livenessProbeRequirements/successThreshold',
                                                 value=self.success_threshold))
        if self.failure_threshold:
            patch_list.append(JsonPatchOperation(op='replace', path='/livenessProbeRequirements/failureThreshold',
                                                 value=self.failure_threshold))
        if self.namespace:
            patch_list.append(JsonPatchOperation(op='replace', path='/namespace', value=self.namespace))
        if self.tags is not None:
            patch_list.append(JsonPatchOperation(op='replace', path='/kvTags', value=self.tags))
        if self.properties is not None:
            for key in self.properties:
                patch_list.append(
                    JsonPatchOperation(op='add', path='/properties/{}'.format(key), value=self.properties[key]))
        if self.description:
            patch_list.append(JsonPatchOperation(op='replace', path='/description', value=self.description))

        return patch_list

    def _validate_update(self, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                         autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                         memory_gb, enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests,
                         max_request_wait_time, num_replicas, tags, properties, description, models,
                         inference_config, gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                         success_threshold, failure_threshold, namespace, auth_enabled, token_auth_enabled,
                         cpu_cores_limit, memory_gb_limit):
        """Validate the values provided to update the webservice.

        :param image:
        :type image: azureml.core.Image
        :param autoscale_enabled:
        :type autoscale_enabled: bool
        :param autoscale_min_replicas:
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas:
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds:
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization:
        :type autoscale_target_utilization: int
        :param collect_model_data:
        :type collect_model_data: bool
        :param cpu_cores:
        :type cpu_cores: float
        :param memory_gb:
        :type memory_gb: float
        :param enable_app_insights:
        :type enable_app_insights: bool
        :param scoring_timeout_ms:
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests:
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error
        :type max_request_wait_time: int
        :param num_replicas:
        :type num_replicas: int
        :param tags:
        :type tags: dict[str, str]
        :param properties:
        :type properties: dict[str, str]
        :param description:
        :type description: str
        :param models: A list of Model objects to package with this image. Can be an empty list
        :type models: :class:`list[azureml.core.Model]`
        :param inference_config: An InferenceConfig object used to determine required model properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param: gpu_cores
        :type: int
        :param period_seconds:
        :type period_seconds: int
        :param initial_delay_seconds:
        :type initial_delay_seconds: int
        :param timeout_seconds:
        :type timeout_seconds: int
        :param success_threshold:
        :type success_threshold: int
        :param failure_threshold:
        :type failure_threshold: int
        :param namespace:
        :type namespace: str
        :param auth_enabled: If Key auth is enabled.
        :type auth_enabled: bool
        :param token_auth_enabled: Whether or not to enable Token auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :param cpu_cores_limit: The max number of cpu cores this Webservice is allowed to use. Can be a decimal.
        :type cpu_cores_limit: float
        :param memory_gb_limit: The max amount of memory (in GB) this Webservice is allowed to use. Can be a decimal.
        :type memory_gb_limit: float
        """
        error = ""
        if cpu_cores is not None:
            if cpu_cores <= 0:
                error += 'Error, cpu_cores must be greater than zero.\n'
            if self.container_resource_requirements is not None and \
                    self.container_resource_requirements.cpu_limit is not None \
                    and cpu_cores > self.container_resource_requirements.cpu_limit:
                error += 'Error, cpu_cores must be ' \
                         'less than or equal to container_resource_requirements.cpu_limit.\n'
        if cpu_cores_limit is not None:
            if cpu_cores_limit <= 0:
                error += 'Error, cpu_cores_limit must be greater than zero.\n'
            if cpu_cores is not None and cpu_cores_limit < cpu_cores:
                error += 'Error, cpu_cores_limit must be greater than or equal to cpu_cores.\n'
            if self.container_resource_requirements is not None and \
                    self.container_resource_requirements.cpu is not None \
                    and cpu_cores_limit < self.container_resource_requirements.cpu:
                error += 'Error, cpu_cores_limit must be ' \
                         'greater than or equal to container_resource_requirements.cpu.\n'
        if memory_gb is not None:
            if memory_gb <= 0:
                error += 'Error, memory_gb must be greater than zero.\n'
            if self.container_resource_requirements and self.container_resource_requirements.memory_in_gb_limit \
                    and memory_gb > self.container_resource_requirements.memory_in_gb_limit:
                error += 'Error, memory_gb must be ' \
                         'less than or equal to container_resource_requirements.memory_in_gb_limit.\n'
        if memory_gb_limit is not None:
            if memory_gb_limit <= 0:
                error += 'Error, memory_gb_limit must be greater than zero.\n'
            elif memory_gb and memory_gb_limit < memory_gb:
                error += 'Error, memory_gb_limit must be greater than or equal to memory_gb.\n'
            elif self.container_resource_requirements and self.container_resource_requirements.memory_in_gb \
                    and memory_gb_limit < self.container_resource_requirements.memory_in_gb:
                error += 'Error, memory_gb_limit must be ' \
                         'greater than or equal to container_resource_requirements.memory_in_gb.\n'
        if gpu_cores is not None and gpu_cores < 0:
            error += 'Error, gpu_cores must be greater than or equal to zero.\n'
        if scoring_timeout_ms is not None and scoring_timeout_ms <= 0:
            error += 'Error, scoring_timeout_ms must be greater than zero.\n'
        if replica_max_concurrent_requests is not None and replica_max_concurrent_requests <= 0:
            error += 'Error, replica_max_concurrent_requests must be greater than zero.\n'
        if max_request_wait_time is not None and max_request_wait_time <= 0:
            error += 'Error, max_request_wait_time must be greater than zero.\n'
        if num_replicas is not None and num_replicas <= 0:
            error += 'Error, num_replicas must be greater than zero.\n'
        if period_seconds is not None and period_seconds <= 0:
            error += 'Error, period_seconds must be greater than zero.\n'
        if timeout_seconds is not None and timeout_seconds <= 0:
            error += 'Error, timeout_seconds must be greater than zero.\n'
        if initial_delay_seconds is not None and initial_delay_seconds <= 0:
            error += 'Error, initial_delay_seconds must be greater than zero.\n'
        if success_threshold is not None and success_threshold <= 0:
            error += 'Error, success_threshold must be greater than zero.\n'
        if failure_threshold is not None and failure_threshold <= 0:
            error += 'Error, failure_threshold must be greater than zero.\n'
        if namespace and not re.match(NAMESPACE_REGEX, namespace):
            error += 'Error, namespace must be a valid Kubernetes namespace. ' \
                     'Regex for validation is ' + NAMESPACE_REGEX + '\n'
        if autoscale_enabled:
            if num_replicas:
                error += 'Error, autoscale enabled and num_replicas provided.\n'
            if autoscale_min_replicas is not None and autoscale_min_replicas <= 0:
                error += 'Error, autoscale_min_replicas must be greater than zero.\n'
            if autoscale_max_replicas is not None and autoscale_max_replicas <= 0:
                error += 'Error, autoscale_max_replicas must be greater than zero.\n'
            if autoscale_min_replicas and autoscale_max_replicas and \
                    autoscale_min_replicas > autoscale_max_replicas:
                error += 'Error, autoscale_min_replicas cannot be greater than autoscale_max_replicas.\n'
            if autoscale_refresh_seconds is not None and autoscale_refresh_seconds <= 0:
                error += 'Error, autoscale_refresh_seconds must be greater than zero.\n'
            if autoscale_target_utilization is not None and autoscale_target_utilization <= 0:
                error += 'Error, autoscale_target_utilization must be greater than zero.\n'
        else:
            if autoscale_enabled is False and not num_replicas:
                error += 'Error, autoscale disabled but num_replicas not provided.\n'
            if autoscale_min_replicas:
                error += 'Error, autoscale_min_replicas provided without enabling autoscaling.\n'
            if autoscale_max_replicas:
                error += 'Error, autoscale_max_replicas provided without enabling autoscaling.\n'
            if autoscale_refresh_seconds:
                error += 'Error, autoscale_refresh_seconds provided without enabling autoscaling.\n'
            if autoscale_target_utilization:
                error += 'Error, autoscale_target_utilization provided without enabling autoscaling.\n'
        if token_auth_enabled and auth_enabled:
            error += 'Error, cannot set both token_auth_enabled and auth_enabled.\n'
        elif token_auth_enabled and (self.auth_enabled and auth_enabled is not False):
            error += 'Error, cannot set token_auth_enabled without disabling key auth (set auth_enabled to False).\n'
        elif auth_enabled and (self.token_auth_enabled and token_auth_enabled is not False):
            error += 'Error, cannot set token_auth_enabled without disabling key auth (set auth_enabled to False).\n'

        if error:
            raise Exception(error)

    def _build_create_payload(self, name, environment_image_request, deployment_target=None, overwrite=False):
        import copy
        from azureml._model_management._util import aks_specific_service_create_payload_template
        json_payload = copy.deepcopy(aks_specific_service_create_payload_template)
        base_payload = super(AksServiceDeploymentConfiguration,
                             self)._build_base_create_payload(name, environment_image_request)

        json_payload['numReplicas'] = self.num_replicas
        if self.collect_model_data:
            json_payload['dataCollection']['storageEnabled'] = self.collect_model_data
        else:
            del (json_payload['dataCollection'])
        if self.enable_app_insights is not None:
            json_payload['appInsightsEnabled'] = self.enable_app_insights
        else:
            del (json_payload['appInsightsEnabled'])
        if self.autoscale_enabled is not None:
            json_payload['autoScaler']['autoscaleEnabled'] = self.autoscale_enabled
            json_payload['autoScaler']['minReplicas'] = self.autoscale_min_replicas
            json_payload['autoScaler']['maxReplicas'] = self.autoscale_max_replicas
            json_payload['autoScaler']['targetUtilization'] = self.autoscale_target_utilization
            json_payload['autoScaler']['refreshPeriodInSeconds'] = self.autoscale_refresh_seconds
        else:
            del (json_payload['autoScaler'])
        json_payload['containerResourceRequirements']['cpu'] = self.cpu_cores
        json_payload['containerResourceRequirements']['cpuLimit'] = self.cpu_cores_limit
        json_payload['containerResourceRequirements']['memoryInGB'] = self.memory_gb
        json_payload['containerResourceRequirements']['memoryInGBLimit'] = self.memory_gb_limit
        json_payload['containerResourceRequirements']['gpu'] = self.gpu_cores
        json_payload['maxConcurrentRequestsPerContainer'] = self.replica_max_concurrent_requests
        json_payload['maxQueueWaitMs'] = self.max_request_wait_time
        json_payload['namespace'] = self.namespace
        json_payload['scoringTimeoutMs'] = self.scoring_timeout_ms
        if self.auth_enabled is not None:
            json_payload['authEnabled'] = self.auth_enabled
        else:
            del (json_payload['authEnabled'])
        if self.token_auth_enabled is not None:
            json_payload['aadAuthEnabled'] = self.token_auth_enabled
        else:
            del (json_payload['aadAuthEnabled'])
        json_payload['livenessProbeRequirements']['periodSeconds'] = self.period_seconds
        json_payload['livenessProbeRequirements']['initialDelaySeconds'] = self.initial_delay_seconds
        json_payload['livenessProbeRequirements']['timeoutSeconds'] = self.timeout_seconds
        json_payload['livenessProbeRequirements']['failureThreshold'] = self.failure_threshold
        json_payload['livenessProbeRequirements']['successThreshold'] = self.success_threshold

        if overwrite:
            json_payload['overwrite'] = overwrite
        else:
            del (json_payload['overwrite'])

        if deployment_target is not None:
            json_payload['computeName'] = deployment_target.name

        json_payload.update(base_payload)

        return json_payload

    @staticmethod
    def _create_deploy_config_from_dict(deploy_config_dict):
        deploy_config = AksServiceDeploymentConfiguration(
            autoscale_enabled=deploy_config_dict.get('autoScaler', {}).get('autoscaleEnabled'),
            autoscale_min_replicas=deploy_config_dict.get('autoScaler', {}).get('minReplicas'),
            autoscale_max_replicas=deploy_config_dict.get('autoScaler', {}).get('maxReplicas'),
            autoscale_refresh_seconds=deploy_config_dict.get('autoScaler', {}).get('refreshPeriodInSeconds'),
            autoscale_target_utilization=deploy_config_dict.get('autoScaler', {}).get('targetUtilization'),
            collect_model_data=deploy_config_dict.get('dataCollection', {}).get('storageEnabled'),
            auth_enabled=deploy_config_dict.get('authEnabled'),
            cpu_cores=deploy_config_dict.get('containerResourceRequirements', {}).get('cpu'),
            memory_gb=deploy_config_dict.get('containerResourceRequirements', {}).get('memoryInGB'),
            enable_app_insights=deploy_config_dict.get('appInsightsEnabled'),
            scoring_timeout_ms=deploy_config_dict.get('scoringTimeoutMs'),
            replica_max_concurrent_requests=deploy_config_dict.get('maxConcurrentRequestsPerContainer'),
            max_request_wait_time=deploy_config_dict.get('maxQueueWaitMs'),
            num_replicas=deploy_config_dict.get('numReplicas'),
            primary_key=deploy_config_dict.get('keys', {}).get('primaryKey'),
            secondary_key=deploy_config_dict.get('keys', {}).get('secondaryKey'),
            tags=deploy_config_dict.get('tags'),
            properties=deploy_config_dict.get('properties'),
            description=deploy_config_dict.get('description'),
            gpu_cores=deploy_config_dict.get('gpuCores'),
            period_seconds=deploy_config_dict.get('livenessProbeRequirements', {}).get('periodSeconds'),
            initial_delay_seconds=deploy_config_dict.get('livenessProbeRequirements',
                                                         {}).get('initialDelaySeconds'),
            timeout_seconds=deploy_config_dict.get('livenessProbeRequirements', {}).get('timeoutSeconds'),
            success_threshold=deploy_config_dict.get('livenessProbeRequirements', {}).get('successThreshold'),
            failure_threshold=deploy_config_dict.get('livenessProbeRequirements', {}).get('failureThreshold'),
            namespace=deploy_config_dict.get('namespace'),
            token_auth_enabled=deploy_config_dict.get("tokenAuthEnabled"),
            compute_target_name=deploy_config_dict.get("computeTargetName"),
            cpu_cores_limit=deploy_config_dict.get('containerResourceRequirements', {}).get('cpuLimit'),
            memory_gb_limit=deploy_config_dict.get('containerResourceRequirements', {}).get('memoryInGBLimit')
        )

        return deploy_config

    def __eq__(self, other):
        return (
            self.autoscale_enabled == other.autoscale_enabled
            and self.autoscale_min_replicas == other.autoscale_min_replicas
            and self.autoscale_max_replicas == other.autoscale_max_replicas
            and self.autoscale_refresh_seconds == other.autoscale_refresh_seconds
            and self.autoscale_target_utilization == other.autoscale_target_utilization
            and self.collect_model_data == other.collect_model_data
            and self.auth_enabled == other.auth_enabled
            and self.cpu_cores == other.cpu_cores
            and self.memory_gb == other.memory_gb
            and self.enable_app_insights == other.enable_app_insights
            and self.scoring_timeout_ms == other.scoring_timeout_ms
            and self.replica_max_concurrent_requests == other.replica_max_concurrent_requests
            and self.max_request_wait_time == other.max_request_wait_time
            and self.num_replicas == other.num_replicas
            and self.primary_key == other.primary_key
            and self.secondary_key == other.secondary_key
            and self.tags == other.tags
            and self.properties == other.properties
            and self.description == other.description
            and self.gpu_cores == other.gpu_cores
            and self.period_seconds == other.period_seconds
            and self.initial_delay_seconds == other.initial_delay_seconds
            and self.timeout_seconds == other.timeout_seconds
            and self.success_threshold == other.success_threshold
            and self.failure_threshold == other.failure_threshold
            and self.namespace == other.namespace
            and self.token_auth_enabled == other.token_auth_enabled
            and self.compute_target_name == other.compute_target_name
            and self.cpu_cores_limit == other.cpu_cores_limit
            and self.memory_gb_limit == other.memory_gb_limit
        )
