# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains functionality for deploying machine learning models as web service endpoints on Azure Container Instances.

Azure Container Instances (ACI) is recommended for scenarios that can operate in isolated containers,
including simple applications, task automation, and build jobs. For more information about when to use ACI,
see [Deploy a model to Azure Container
Instances](https://docs.microsoft.com/azure/machine-learning/how-to-deploy-azure-container-instance).
"""

import logging
import os

from azureml.mlflow.deploy._mms.webservice.webservice import WebserviceDeploymentConfiguration
from azureml.mlflow._restclient.mms.models import ACIServiceCreateRequest, ModelDataCollection, \
    ContainerResourceRequirements as RestContainerResourceRequirements, \
    EncryptionProperties as RestEncryptionProperties, \
    VnetConfiguration as RestVnetConfiguration, AuthKeys, JsonPatchOperation
from azureml.mlflow.deploy._mms._constants import ACI_WEBSERVICE_TYPE
from azureml.mlflow.deploy._mms.webservice.webservice import Webservice

module_logger = logging.getLogger(__name__)


class AciWebservice(Webservice):
    """Represents a machine learning model deployed as a web service endpoint on Azure Container Instances.

    A deployed service is created from a model, script, and associated files. The resulting web service
    is a load-balanced, HTTP endpoint with a REST API. You can send data to this API and receive the
    prediction returned by the model.

    For more information, see `Deploy a model to Azure Container
    Instances <https://docs.microsoft.com/azure/machine-learning/how-to-deploy-azure-container-instance>`__.

    .. remarks::

        The recommended deployment pattern is to create a deployment configuration object with the
        ``deploy_configuration`` method and then use it with the ``deploy`` method of the
        :class:`azureml.core.model.Model` class as shown below.

        .. code-block:: inject notebooks/how-to-use-azureml/deployment/deploy-to-cloud
        /model-register-and-deploy.ipynb#sample-aciwebservice-deploy-config

        There are a number of ways to deploy a model as a webservice,
        including with the:

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

        The *Variables* section lists attributes of a local representation of the cloud AciWebservice object. These
        variables should be considered read-only. Changing their values will not be reflected in the corresponding
        cloud object.

    :var enable_app_insights: Whether or not AppInsights logging is enabled for the Webservice.
    :vartype enable_app_insights: bool
    :var cname: The cname for the Webservice.
    :vartype cname: str
    :var container_resource_requirements: The container resource requirements for the Webservice.
    :vartype container_resource_requirements: azureml.core.webservice.aci.ContainerResourceRequirements
    :var encryption_properties: The encryption properties for the Webservice.
    :vartype encryption_properties: azureml.core.webservice.aci.EncryptionProperties
    :var vnet_configuration: The virtual network properties for the Webservice, configuration should be
                            created and provided by user.
    :vartype vnet_configuration: azureml.core.webservice.aci.VnetConfiguration
    :var azureml.core.webservice.AciWebservice.location: The location the Webservice is deployed to.
    :vartype azureml.core.webservice.AciWebservice.location: str
    :var public_ip: The public ip address of the Webservice.
    :vartype public_ip: str
    :var azureml.core.webservice.AciWebservice.scoring_uri: The scoring endpoint for the Webservice
    :vartype azureml.core.webservice.AciWebservice.scoring_uri: str
    :var ssl_enabled: Whether or not SSL is enabled for the Webservice
    :vartype ssl_enabled: bool
    :var public_fqdn: The public FQDN for the Webservice
    :vartype public_fqdn: str
    :var environment: The Environment object that was used to create the Webservice
    :vartype environment: azureml.core.Environment
    :var azureml.core.webservice.AciWebservice.models: A list of Models deployed to the Webservice
    :vartype azureml.core.webservice.AciWebservice.models: builtin.list[azureml.core.Model]
    :var azureml.core.webservice.AciWebservice.swagger_uri: The swagger endpoint for the Webservice
    :vartype azureml.core.webservice.AciWebservice.swagger_uri: str
    """

    _expected_payload_keys = Webservice._expected_payload_keys + \
        ['appInsightsEnabled', 'authEnabled', 'cname', 'containerResourceRequirements',
         'location', 'publicIp', 'scoringUri', 'sslCertificate', 'sslEnabled', 'sslKey']
    _webservice_type = ACI_WEBSERVICE_TYPE

    def __repr__(self):
        """Return the string representation of the AciWebservice object.

        :return: String representation of the AciWebservice object
        :rtype: str
        """
        return super().__repr__()

    @staticmethod
    def _from_service_response(service_response, **kwargs):
        if service_response.compute_type != ACI_WEBSERVICE_TYPE:
            raise Exception("Invalid input provided for AKSService")
        aci_webservice = AciWebservice({})
        aci_webservice.compute_type = ACI_WEBSERVICE_TYPE
        aci_webservice.name = service_response.name

        # common attributes
        aci_webservice.description = service_response.description
        aci_webservice.tags = service_response.kv_tags
        aci_webservice.properties = service_response.properties
        aci_webservice.auth_enabled = service_response.auth_enabled
        aci_webservice.created_time = service_response.created_time
        aci_webservice.created_by = service_response.created_by
        # TODO: Check if image is valid for ACI
        # TODO: Check if ImageDetails are needed
        # aci_webservice.image = service_response.image if service_response.image else None
        aci_webservice.image_id = service_response.image_id
        aci_webservice.image_digest = service_response.image_digest
        aci_webservice.state = service_response.state
        aci_webservice.updated_time = service_response.updated_time
        aci_webservice.error = service_response.error
        aci_webservice.scoring_uri = service_response.scoring_uri
        aci_webservice.enable_app_insights = service_response.app_insights_enabled

        aci_webservice.cname = service_response.cname
        if service_response.encryption_properties:
            aci_webservice.encryption_properties = EncryptionProperties(
                cmk_vault_base_url=service_response.encryption_properties.vault_base_url,
                cmk_key_version=service_response.encryption_properties.key_version,
                cmk_key_name=service_response.encryption_properties.key_name
            )
        else:
            aci_webservice.encryption_properties = None

        if service_response.vnet_configuration:
            aci_webservice.vnet_configuration = VnetConfiguration(
                vnet_name=service_response.vnet_configuration.vnet_name,
                subnet_name=service_response.vnet_configuration.subnet_name,
            )
        else:
            aci_webservice.vnet_configuration = None

        if service_response.container_resource_requirements:
            aci_webservice.container_resource_requirements = ContainerResourceRequirements(
                cpu=service_response.container_resource_requirements.cpu,
                memory_in_gb=service_response.container_resource_requirements.memory_in_gb
            )
        else:
            aci_webservice.container_resource_requirements = None

        aci_webservice.location = service_response.location
        aci_webservice.public_ip = service_response.public_ip
        aci_webservice.public_fqdn = service_response.public_fqdn
        aci_webservice.swagger_uri = service_response.swagger_uri
        aci_webservice.ssl_enabled = service_response.ssl_enabled
        aci_webservice.ssl_certificate = service_response.ssl_certificate
        aci_webservice.ssl_key = service_response.ssl_key
        aci_webservice.environment = service_response.environment_image_request.environment
        aci_webservice.models = service_response.models
        aci_webservice._model_config_map = service_response.model_config_map
        aci_webservice.service_context = kwargs.pop("service_context", None)

        return aci_webservice

    def add_tags(self, tags):
        """Add key value pairs to this Webservice's tags dictionary.

        :param tags: The dictionary of tags to add.
        :type tags: dict[str, str]
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        updated_tags = self._add_tags(tags)
        self.tags = updated_tags
        self.update(tags=updated_tags)

        print('Webservice tag add operation complete.')

    def remove_tags(self, tags):
        """Remove the specified keys from this Webservice's dictionary of tags.

        :param tags: The list of keys to remove.
        :type tags: builtin.list[str]
        """
        updated_tags = self._remove_tags(tags)
        self.tags = updated_tags
        self.update(tags=updated_tags)

        print('Webservice tag remove operation complete.')

    def add_properties(self, properties):
        """Add key value pairs to this Webservice's properties dictionary.

        :param properties: The dictionary of properties to add.
        :type properties: dict[str, str]
        """
        updated_properties = self._add_properties(properties)
        self.properties = updated_properties
        self.update(properties=updated_properties)

        print('Webservice add properties operation complete.')

    def serialize(self):
        """Convert this Webservice into a JSON serialized dictionary.

        :return: The JSON representation of this Webservice object.
        :rtype: dict
        """
        properties = super(AciWebservice, self).serialize()
        container_resource_requirements = self.container_resource_requirements.serialize() \
            if self.container_resource_requirements else None
        encryption_properties = self.encryption_properties.serialize() \
            if self.encryption_properties else None
        vnet_configuration = self.vnet_configuration.serialize() \
            if self.vnet_configuration else None
        # env_details = Environment._serialize_to_dict(self.environment) if self.environment else None
        env_details = self.environment.as_dict(
            key_transformer=self._attribute_transformer) if self.environment else None

        # model_details = [model.serialize() for model in self.models] if self.models else None

        model_details = [model.as_dict(key_transformer=self._attribute_transformer) for model in
                         self.models] if self.models else None

        aci_properties = {'containerResourceRequirements': container_resource_requirements, 'imageId': self.image_id,
                          'scoringUri': self.scoring_uri, 'location': self.location,
                          'authEnabled': self.auth_enabled, 'sslEnabled': self.ssl_enabled,
                          'appInsightsEnabled': self.enable_app_insights, 'sslCertificate': self.ssl_certificate,
                          'sslKey': self.ssl_key, 'cname': self.cname, 'publicIp': self.public_ip,
                          'publicFqdn': self.public_fqdn, 'environmentDetails': env_details,
                          'modelDetails': model_details, 'encryptionProperties': encryption_properties,
                          'vnetConfiguration': vnet_configuration}
        properties.update(aci_properties)
        return properties

    def get_token(self):
        """
        Retrieve auth token for this Webservice, scoped to the current user.

        .. note::
            Not implemented.

        :return: The auth token for this Webservice and when it should be refreshed after.
        :rtype: str, datetime
        :raises: azureml.exceptions.NotImplementedError
        """
        raise NotImplementedError("ACI webservices do not support Token Authentication.")


class ContainerResourceRequirements(object):
    """Defines the resource requirements for a container used by the Webservice.

    To specify ContainerResourceRequirements values, you will typically use the ``deploy_configuration`` method of the
    :class:`azureml.core.webservice.aci.AciWebservice` class.

    :var cpu: The number of CPU cores to allocate for this Webservice. Can be a decimal.
    :vartype cpu: float
    :var memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
    :vartype memory_in_gb: float

    :param cpu: The number of CPU cores to allocate for this Webservice. Can be a decimal.
    :type cpu: float
    :param memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
    :type memory_in_gb: float
    """

    _expected_payload_keys = ['cpu', 'memoryInGB']

    def __init__(self, cpu, memory_in_gb):
        """Initialize the container resource requirements.

        :param cpu: The number of CPU cores to allocate for this Webservice. Can be a decimal.
        :type cpu: float
        :param memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        :type memory_in_gb: float
        """
        self.cpu = cpu
        self.memory_in_gb = memory_in_gb

    def serialize(self):
        """Convert this ContainerResourceRequirements object into a JSON serialized dictionary.

        :return: The JSON representation of this ContainerResourceRequirements object.
        :rtype: dict
        """
        return {'cpu': self.cpu, 'memoryInGB': self.memory_in_gb}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a JSON object into a ContainerResourceRequirements object.

        :param payload_obj: A JSON object to convert to a ContainerResourceRequirements object.
        :type payload_obj: dict
        :return: The ContainerResourceRequirements representation of the provided JSON object.
        :rtype: azureml.core.webservice.aci.ContainerResourceRequirements
        """
        for payload_key in ContainerResourceRequirements._expected_payload_keys:
            if payload_key not in payload_obj:
                raise Exception('Invalid webservice payload, missing {} for containerResourceReservation:\n'
                                '{}'.format(payload_key, payload_obj))

        return ContainerResourceRequirements(payload_obj['cpu'], payload_obj['memoryInGB'])


class EncryptionProperties(object):
    """Defines the encryption properties for a container used by the Webservice.

    To specify EncryptionProperties values, you will typically use the ``deploy_configuration`` method
    of the :class:`azureml.core.webservice.aci.AciWebservice` class.

    :var cmk_vault_base_url: Customer managed key vault base url.
    :vartype cmk_vault_base_url: str
    :var cmk_key_name: Customer managed key name.
    :vartype cmk_key_name: str
    :var cmk_key_version: Customer managed key version.
    :vartype cmk_key_version: str
    """

    _expected_payload_keys = ['vaultBaseUrl', 'keyName', 'keyVersion']

    def __init__(self, cmk_vault_base_url, cmk_key_name, cmk_key_version):
        """Initialize encryption properties.

        :param cmk_vault_base_url: customer managed key vault base url.
        :type cmk_vault_base_url: str
        :param cmk_key_name: customer managed key name.
        :type cmk_key_name: str
        :param cmk_key_version: customer managed key version.
        :type cmk_key_version: str
        """
        self.cmk_vault_base_url = cmk_vault_base_url
        self.cmk_key_name = cmk_key_name
        self.cmk_key_version = cmk_key_version

    def serialize(self):
        """Convert this EncryptionProperties object into a JSON serialized dictionary.

        :return: The JSON representation of this EncryptionProperties object.
        :rtype: dict
        """
        return {'vaultBaseUrl': self.cmk_vault_base_url,
                'keyName': self.cmk_key_name,
                'keyVersion': self.cmk_key_version}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a JSON object into a EncryptionProperties object.

        :param payload_obj: A JSON object to convert to a EncryptionProperties object.
        :type payload_obj: dict
        :return: The EncryptionProperties representation of the provided JSON object.
        :rtype: azureml.core.webservice.aci.EncryptionProperties
        """
        if payload_obj is None:
            return None
        for payload_key in EncryptionProperties._expected_payload_keys:
            if payload_key not in payload_obj:
                raise Exception('Invalid webservice payload, missing {} for EncryptionProperties:\n'
                                '{}'.format(payload_key, payload_obj))

        return EncryptionProperties(payload_obj['vaultBaseUrl'], payload_obj['keyName'], payload_obj['keyVersion'])


class VnetConfiguration(object):
    """Defines the Virtual network configuration for a container used by the Webservice.

    To specify VnetConfiguration values, you will typically use the ``deploy_configuration`` method
    of the :class:`azureml.core.webservice.aci.AciWebservice` class.

    :var vnet_name: Virtual network name.
    :vartype vnet_name: str
    :var subnet_name: Subnet name within virtual network.
    :vartype subnet_name: str
    """

    _expected_payload_keys = ['vnetName', 'subnetName']

    def __init__(self, vnet_name, subnet_name):
        """Initialize encryption properties.

        :param vnet_name: Virtual network name.
        :type vnet_name: str
        :param subnet_name: Subnet name within virtual network.
        :type subnet_name: str
        """
        self.vnet_name = vnet_name
        self.subnet_name = subnet_name

    def serialize(self):
        """Convert this VnetConfiguration object into a JSON serialized dictionary.

        :return: The JSON representation of this VnetConfiguration object.
        :rtype: dict
        """
        return {'vnetName': self.vnet_name,
                'subnetName': self.subnet_name}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a JSON object into a VnetConfiguration object.

        :param payload_obj: A JSON object to convert to a VnetConfiguration object.
        :type payload_obj: dict
        :return: The VnetConfiguration representation of the provided JSON object.
        :rtype: azureml.core.webservice.aci.VnetConfiguration
        """
        if payload_obj is None:
            return None
        for payload_key in VnetConfiguration._expected_payload_keys:
            if payload_key not in payload_obj:
                raise Exception('Invalid webservice payload, missing {} for VnetConfiguration:\n'
                                '{}'.format(payload_key, payload_obj))

        return VnetConfiguration(payload_obj['vnetName'], payload_obj['subnetName'])


class AciServiceDeploymentConfiguration(WebserviceDeploymentConfiguration):
    """Represents deployment configuration information for a service deployed on Azure Container Instances.

    Create an AciServiceDeploymentConfiguration object using the ``deploy_configuration`` method of the
    :class:`azureml.core.webservice.aci.AciWebservice` class.

    :var cpu_cores: The number of CPU cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
    :vartype cpu_cores: float
    :var memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        Defaults to 0.5
    :vartype memory_gb: float
    :var azureml.core.webservice.AciServiceDeploymentConfiguration.tags: A dictionary of key value tags to give this
        Webservice.
    :vartype tags: dict[str, str]
    :var azureml.core.webservice.AciServiceDeploymentConfiguration.properties: A dictionary of key value properties
        to give this Webservice. These properties cannot be changed after deployment, however new key value pairs
        can be added.
    :vartype properties: dict[str, str]
    :var azureml.core.webservice.AciServiceDeploymentConfiguration.description: A description to give this Webservice.
    :vartype description: str
    :var azureml.core.webservice.AciServiceDeploymentConfiguration.location: The Azure region to deploy this
        Webservice to. If not specified, the Workspace location will be used. For more details on available regions,
        see `Products by region
        <https://azure.microsoft.com/global-infrastructure/services/?products=container-instances>`_.
    :vartype location: str
    :var auth_enabled: Whether or not to enable auth for this Webservice. Defaults to False.
    :vartype auth_enabled: bool
    :var ssl_enabled: Whether or not to enable SSL for this Webservice. Defaults to False.
    :vartype ssl_enabled: bool
    :var enable_app_insights: Whether or not to enable AppInsights for this Webservice. Defaults to False.
    :vartype enable_app_insights: bool
    :var ssl_cert_pem_file: The cert file needed if SSL is enabled.
    :vartype ssl_cert_pem_file: str
    :var ssl_key_pem_file: The key file needed if SSL is enabled.
    :vartype ssl_key_pem_file: str
    :var ssl_cname: The cname for if SSL is enabled.
    :vartype ssl_cname: str
    :var dns_name_label: The DNS name label for the scoring endpoint.
        If not specified a unique DNS name label will be generated for the scoring endpoint.
    :vartype dns_name_label: str
    :var primary_key: A primary auth key to use for this Webservice.
    :vartype primary_key: str
    :var secondary_key: A secondary auth key to use for this Webservice.
    :vartype secondary_key: str
    :var collect_model_data: Whether or not to enabled model data collection for the Webservice.
    :vartype collect_model_data: bool

    :param cpu_cores: The number of CPU cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
    :type cpu_cores: float
    :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        Defaults to 0.5
    :type memory_gb: float
    :param tags: A dictionary of key value tags to give this Webservice.
    :type tags: dict[str, str]
    :param properties: A dictionary of key value properties to give this Webservice. These properties cannot
        be changed after deployment, however new key value pairs can be added.
    :type properties: dict[str, str]
    :param description: A description to give this Webservice.
    :type description: str
    :param location: The Azure region to deploy this Webservice to. If not specified, the Workspace location will
        be used. For more details on available regions, see `Products by
        region <https://azure.microsoft.com/global-infrastructure/services/?products=container-instances>`__.
    :type location: str
    :param auth_enabled: Whether or not to enable auth for this Webservice. Defaults to False.
    :type auth_enabled: bool
    :param ssl_enabled: Whether or not to enable SSL for this Webservice. Defaults to False.
    :type ssl_enabled: bool
    :param enable_app_insights: Whether or not to enable AppInsights for this Webservice. Defaults to False.
    :type enable_app_insights: bool
    :param ssl_cert_pem_file: The cert file needed if SSL is enabled.
    :type ssl_cert_pem_file: str
    :param ssl_key_pem_file: The key file needed if SSL is enabled.
    :type ssl_key_pem_file: str
    :param ssl_cname: The cname for if SSL is enabled.
    :type ssl_cname: str
    :param dns_name_label: The DNS name label for the scoring endpoint.
        If not specified a unique DNS name label will be generated for the scoring endpoint.
    :type dns_name_label: str
    :param primary_key: A primary auth key to use for this Webservice.
    :type primary_key: str
    :param secondary_key: A secondary auth key to use for this Webservice.
    :type secondary_key: str
    :param collect_model_data: Whether or not to enable model data collection for this Webservice.
        Defaults to False
    :type collect_model_data: bool
    :param cmk_vault_base_url: customer managed key vault base url
    :type cmk_vault_base_url: str
    :param cmk_key_name: customer managed key name.
    :type cmk_key_name: str
    :param cmk_key_version: customer managed key version.
    :type cmk_key_version: str
    :param vnet_name: virtual network name.
    :type vnet_name: str
    :param subnet_name: subnet name within virtual network.
    :type subnet_name: str
    """

    _webservice_type = AciWebservice

    def __init__(self, cpu_cores=None, memory_gb=None, tags=None, properties=None, description=None, location=None,
                 auth_enabled=None, ssl_enabled=None, enable_app_insights=None, ssl_cert_pem_file=None,
                 ssl_key_pem_file=None, ssl_cname=None, dns_name_label=None,
                 primary_key=None, secondary_key=None, collect_model_data=None,
                 cmk_vault_base_url=None, cmk_key_name=None, cmk_key_version=None,
                 vnet_name=None, subnet_name=None):
        """Create a configuration object for deploying an ACI Webservice.

        :param cpu_cores: The number of CPU cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
            Defaults to 0.5
        :type memory_gb: float
        :param tags: A dictionary of key value tags to give this Webservice.
        :type tags: dict[str, str]
        :param properties: A dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added.
        :type properties: dict[str, str]
        :param description: A description to give this Webservice.
        :type description: str
        :param location: The Azure region to deploy this Webservice to. If not specified, the Workspace location will
            be used. For more details on available regions, see `Products by
            region <https://azure.microsoft.com/global-infrastructure/services/?products=container-instances>`__.
        :type location: str
        :param auth_enabled: Whether or not to enable auth for this Webservice. Defaults to False.
        :type auth_enabled: bool
        :param ssl_enabled: Whether or not to enable SSL for this Webservice. Defaults to False.
        :type ssl_enabled: bool
        :param enable_app_insights: Whether or not to enable AppInsights for this Webservice. Defaults to False.
        :type enable_app_insights: bool
        :param ssl_cert_pem_file: The cert file needed if SSL is enabled.
        :type ssl_cert_pem_file: str
        :param ssl_key_pem_file: The key file needed if SSL is enabled.
        :type ssl_key_pem_file: str
        :param ssl_cname: The cname for if SSL is enabled.
        :type ssl_cname: str
        :param dns_name_label: The DNS name label for the scoring endpoint.
            If not specified a unique DNS name label will be generated for the scoring endpoint.
        :type dns_name_label: str
        :param primary_key: A primary auth key to use for this Webservice.
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Webservice.
        :type secondary_key: str
        :param collect_model_data: Whether or not to enable model data collection for this Webservice.
            Defaults to False
        :type collect_model_data: bool
        :param cmk_vault_base_url: customer managed key vault base url
        :type cmk_vault_base_url: str
        :param cmk_key_name: customer managed key name.
        :type cmk_key_name: str
        :param cmk_key_version: customer managed key version.
        :type cmk_key_version: str
        :param vnet_name: virtual network name.
        :type vnet_name: str
        :param subnet_name: subnet name within virtual network.
        :type subnet_name: str
        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        super(AciServiceDeploymentConfiguration, self).__init__(AciWebservice, description, tags, properties,
                                                                primary_key, secondary_key, location)
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.auth_enabled = auth_enabled
        self.ssl_enabled = ssl_enabled
        self.enable_app_insights = enable_app_insights
        self.ssl_cert_pem_file = ssl_cert_pem_file
        self.ssl_key_pem_file = ssl_key_pem_file
        self.ssl_cname = ssl_cname
        self.dns_name_label = dns_name_label
        self.collect_model_data = collect_model_data
        self.cmk_vault_base_url = cmk_vault_base_url
        self.cmk_key_name = cmk_key_name
        self.cmk_key_version = cmk_key_version
        self.vnet_name = vnet_name
        self.subnet_name = subnet_name
        self.validate_configuration()

    def validate_configuration(self):
        """Check that the specified configuration values are valid.

        Will raise a :class:`azureml.exceptions.WebserviceException` if validation fails.

        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        if self.cpu_cores is not None and self.cpu_cores <= 0:
            raise Exception('Invalid configuration, cpu_cores must be positive.')
        if self.memory_gb is not None and self.memory_gb <= 0:
            raise Exception('Invalid configuration, memory_gb must be positive.')
        if self.ssl_enabled:
            if not self.ssl_cert_pem_file or not self.ssl_key_pem_file or not self.ssl_cname:
                raise Exception('SSL is enabled, you must provide a SSL certificate, key, and cname.')
            if not os.path.exists(self.ssl_cert_pem_file):
                raise Exception('Error, unable to find SSL cert pem file provided paths:\n'
                                '{}'.format(self.ssl_cert_pem_file))
            if not os.path.exists(self.ssl_key_pem_file):
                raise Exception('Error, unable to find SSL key pem file provided paths:\n'
                                '{}'.format(self.ssl_key_pem_file))
        if not ((self.cmk_vault_base_url and self.cmk_key_name and self.cmk_key_version)
                or (not self.cmk_vault_base_url and not self.cmk_key_name and not self.cmk_key_version)):
            raise Exception('customer managed key vault_base_url, key_name and key_version must all have values or \
                                      all are empty/null')
        if (self.vnet_name and not self.subnet_name) or (not self.vnet_name and self.subnet_name):
            raise Exception('vnet_name and subnet_name must all have values or both are empty/null')

    def print_deploy_configuration(self):
        """Print the deployment configuration."""
        deploy_config = []
        if self.cpu_cores:
            deploy_config.append('CPU requirement: {}'.format(self.cpu_cores))
        if self.memory_gb:
            deploy_config.append('Memory requirement: {}GB'.format(self.memory_gb))

        if len(deploy_config) > 0:
            print(', '.join(deploy_config))

    def _to_service_update_request(self, environment_image_request=None, overwrite=False):
        if self.tags is None and self.properties is None and not self.description and self.auth_enabled is None \
                and self.ssl_enabled is None and not self.ssl_cert_pem_file and not self.ssl_key_pem_file\
                and not self.ssl_cname and self.enable_app_insights is None and environment_image_request is None:
            raise Exception('No parameters provided to update.')

        self._validate_update(self.ssl_enabled, self.ssl_cert_pem_file, self.ssl_key_pem_file)

        cert_data = ""
        key_data = ""
        if self.ssl_cert_pem_file:
            try:
                with open(self.ssl_cert_pem_file, 'r') as cert_file:
                    cert_data = cert_file.read()
            except (IOError, OSError) as exc:
                raise Exception("Error while reading ssl information:\n{}".format(exc))
        if self.ssl_key_pem_file:
            try:
                with open(self.ssl_key_pem_file, 'r') as key_file:
                    key_data = key_file.read()
            except (IOError, OSError) as exc:
                raise Exception("Error while reading ssl information:\n{}".format(exc))

        patch_list = []

        if environment_image_request is not None:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/environmentImageRequest', value=environment_image_request))
        if self.auth_enabled is not None:
            patch_list.append(JsonPatchOperation(op='replace', path='/authEnabled', value=self.auth_enabled))
        if self.ssl_enabled is not None:
            patch_list.append(JsonPatchOperation(op='replace', path='/sslEnabled', value=self.ssl_enabled))
        if self.ssl_cert_pem_file:
            patch_list.append(JsonPatchOperation(op='replace', path='/sslCertificate', value=cert_data))
        if self.ssl_key_pem_file:
            patch_list.append(JsonPatchOperation(op='replace', path='/sslKey', value=key_data))
        if self.ssl_cname:
            patch_list.append(JsonPatchOperation(op='replace', path='/cname', value=self.ssl_cname))
        if self.enable_app_insights is not None:
            patch_list.append(
                JsonPatchOperation(op='replace', path='/appInsightsEnabled', value=self.enable_app_insights))
        if self.tags is not None:
            patch_list.append(JsonPatchOperation(op='replace', path='/kvTags', value=self.tags))
        if self.properties is not None:
            for key in self.properties:
                patch_list.append(
                    JsonPatchOperation(op='add', path='/properties/{}'.format(key), value=self.properties[key]))
        if self.description:
            patch_list.append(JsonPatchOperation(op='replace', path='/description', value=self.description))

        return patch_list

    def _validate_update(self, ssl_enabled, ssl_cert_pem_file, ssl_key_pem_file):
        error = ""
        if (ssl_cert_pem_file or ssl_key_pem_file) and not ssl_enabled and not self.ssl_enabled:
            error += 'Error, SSL must be enabled in order to update SSL cert/key.\n'
        if ssl_cert_pem_file and not os.path.exists(ssl_cert_pem_file):
            error += 'Error, unable to find ssl_cert_pem_file at provided path: {}\n'.format(ssl_cert_pem_file)
        if ssl_key_pem_file and not os.path.exists(ssl_key_pem_file):
            error += 'Error, unable to find ssl_key_pem_file at provided path: {}\n'.format(ssl_key_pem_file)

        if error:
            raise Exception(error, logger=module_logger)

    def _to_service_create_request(self, name, environment_image_request, overwrite=False):
        vnet_configuration = None
        if self.vnet_name and self.subnet_name:
            vnet_configuration = RestVnetConfiguration(
                vnet_name=self.vnet_name,
                subnet_name=self.subnet_name
            )

        encryption_properties = None
        if self.cmk_key_name and self.cmk_key_version and self.cmk_vault_base_url:
            encryption_properties = RestEncryptionProperties(
                key_name=self.cmk_key_name,
                key_version=self.cmk_key_version,
                vault_base_url=self.cmk_vault_base_url
            )

        data_collection = None
        if self.collect_model_data:
            data_collection = ModelDataCollection(
                storage_enabled=self.collect_model_data
            )

        keys = None
        if self.primary_key:
            keys = AuthKeys(
                primary_key=self.primary_key,
                secondary_key=self.secondary_key
            )

        service_create_request = ACIServiceCreateRequest(
            name=name,
            description=self.description,
            kv_tags=self.tags,
            properties=self.properties,
            auth_enabled=self.auth_enabled,
            ssl_enabled=self.ssl_enabled,
            app_insights_enabled=self.enable_app_insights,
            data_collection=data_collection,
            cname=self.ssl_cname,
            dns_name_label=self.dns_name_label,
            vnet_configuration=vnet_configuration,
            encryption_properties=encryption_properties,
            container_resource_requirements=RestContainerResourceRequirements(
                cpu=self.cpu_cores,
                memory_in_gb=self.memory_gb
            ),
            environment_image_request=environment_image_request,
            overwrite=overwrite,
            keys=keys,
        )

        if self.ssl_enabled:
            try:
                with open(self.ssl_cert_pem_file, 'r') as cert_file:
                    cert_data = cert_file.read()
                service_create_request.ssl_certificate = cert_data
            except Exception as e:
                raise Exception('Error occurred attempting to read SSL cert pem file:\n{}'.format(e))
            try:
                with open(self.ssl_key_pem_file, 'r') as key_file:
                    key_data = key_file.read()
                service_create_request.ssl_key = key_data
            except Exception as e:
                raise Exception('Error occurred attempting to read SSL key pem file:\n{}'.format(e))

        return service_create_request

    # def _build_create_payload(self, name, environment_image_request, overwrite=False):
    #     import copy
    #     from azureml._model_management._util import aci_specific_service_create_payload_template
    #     json_payload = copy.deepcopy(aci_specific_service_create_payload_template)
    #     base_payload = super(AciServiceDeploymentConfiguration,
    #                          self)._build_base_create_payload(name, environment_image_request)
    #
    #     json_payload['containerResourceRequirements']['cpu'] = self.cpu_cores
    #     json_payload['containerResourceRequirements']['memoryInGB'] = self.memory_gb
    #     if self.auth_enabled is not None:
    #         json_payload['authEnabled'] = self.auth_enabled
    #     else:
    #         del (json_payload['authEnabled'])
    #     if self.enable_app_insights is not None:
    #         json_payload['appInsightsEnabled'] = self.enable_app_insights
    #     else:
    #         del (json_payload['appInsightsEnabled'])
    #     if self.collect_model_data:
    #         json_payload['dataCollection']['storageEnabled'] = self.collect_model_data
    #     else:
    #         del (json_payload['dataCollection'])
    #
    #     if self.ssl_enabled is not None:
    #         json_payload['sslEnabled'] = self.ssl_enabled
    #         if self.ssl_enabled:
    #             try:
    #                 with open(self.ssl_cert_pem_file, 'r') as cert_file:
    #                     cert_data = cert_file.read()
    #                 json_payload['sslCertificate'] = cert_data
    #             except Exception as e:
    #                 raise Exception('Error occurred attempting to read SSL cert pem file:\n{}'.format(e))
    #             try:
    #                 with open(self.ssl_key_pem_file, 'r') as key_file:
    #                     key_data = key_file.read()
    #                 json_payload['sslKey'] = key_data
    #             except Exception as e:
    #                 raise Exception('Error occurred attempting to read SSL key pem file:\n{}'.format(e))
    #     else:
    #         del (json_payload['sslEnabled'])
    #         del (json_payload['sslCertificate'])
    #         del (json_payload['sslKey'])
    #
    #     json_payload['cname'] = self.ssl_cname
    #     json_payload['dnsNameLabel'] = self.dns_name_label
    #
    #     encryption_properties = {}
    #     vnet_configuration = {}
    #
    #     # All 3 propertis will either be all null or all valid
    #     # validation is done in aciDeploymentConfiguration
    #     if self.cmk_vault_base_url:
    #         encryption_properties['vaultBaseUrl'] = self.cmk_vault_base_url
    #         encryption_properties['keyName'] = self.cmk_key_name
    #         encryption_properties['keyVersion'] = self.cmk_key_version
    #         json_payload['encryptionProperties'] = encryption_properties
    #
    #     if self.vnet_name:
    #         vnet_configuration['vnetName'] = self.vnet_name
    #         vnet_configuration['subnetName'] = self.subnet_name
    #         json_payload['vnetConfiguration'] = vnet_configuration
    #
    #     if overwrite:
    #         json_payload['overwrite'] = overwrite
    #     else:
    #         del (json_payload['overwrite'])
    #
    #     json_payload.update(base_payload)
    #
    #     return json_payload

    @staticmethod
    def _create_deploy_config_from_dict(deploy_config_dict):
        # aci deployment
        deploy_config = AciServiceDeploymentConfiguration(
            cpu_cores=deploy_config_dict.get('containerResourceRequirements', {}).get('cpu'),
            memory_gb=deploy_config_dict.get('containerResourceRequirements', {}).get('memoryInGB'),
            tags=deploy_config_dict.get('tags'),
            properties=deploy_config_dict.get('properties'),
            description=deploy_config_dict.get('description'),
            location=deploy_config_dict.get('location'),
            auth_enabled=deploy_config_dict.get('authEnabled'),
            ssl_enabled=deploy_config_dict.get('sslEnabled'),
            enable_app_insights=deploy_config_dict.get('appInsightsEnabled'),
            ssl_cert_pem_file=deploy_config_dict.get('sslCertificate'),
            ssl_key_pem_file=deploy_config_dict.get('sslKey'),
            ssl_cname=deploy_config_dict.get('cname'),
            dns_name_label=deploy_config_dict.get('dnsNameLabel'),
            cmk_vault_base_url=deploy_config_dict.get('vaultBaseUrl'),
            cmk_key_name=deploy_config_dict.get('keyName'),
            cmk_key_version=deploy_config_dict.get('keyVersion'),
            vnet_name=deploy_config_dict.get('vnetName'),
            subnet_name=deploy_config_dict.get('subnetName'),
            primary_key=deploy_config_dict.get('keys', {}).get('primaryKey'),
            secondary_key=deploy_config_dict.get('keys', {}).get('secondaryKey'),
        )

        return deploy_config

    def __eq__(self, other):
        return (
            self.cpu_cores == other.cpu_cores
            and self.memory_gb == other.memory_gb
            and self.tags == other.tags
            and self.properties == other.properties
            and self.description == other.description
            and self.location == other.location
            and self.auth_enabled == other.auth_enabled
            and self.ssl_enabled == other.ssl_enabled
            and self.enable_app_insights == other.enable_app_insights
            and self.ssl_cert_pem_file == other.ssl_cert_pem_file
            and self.ssl_key_pem_file == other.ssl_key_pem_file
            and self.ssl_cname == other.ssl_cname
            and self.dns_name_label == other.dns_name_label
            and self.primary_key == other.primary_key
            and self.secondary_key == other.secondary_key
            and self.collect_model_data == other.collect_model_data
            and self.cmk_vault_base_url == other.cmk_vault_base_url
            and self.cmk_key_name == other.cmk_key_name
            and self.cmk_key_version == other.cmk_key_version
            and self.vnet_name == other.vnet_name
            and self.subnet_name == other.subnet_name
        )
