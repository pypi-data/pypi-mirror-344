# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
from pprint import pformat
from urllib import parse

import requests

logger = logging.getLogger(__name__)

AZUREML_CLOUD_ENV_NAME = "AZUREML_CURRENT_CLOUD"
ARM_CLOUD_METADATA_URL = "ARM_CLOUD_METADATA_URL"
DEFAULT_TIMEOUT = 30
KNOWN_METADATA_URL_LIST = [
    "https://management.azure.com/metadata/endpoints?api-version=2019-05-01"
]


class CloudEndpointNotSetException(Exception):
    pass


class CloudSuffixNotSetException(Exception):
    pass


class Cloud:  # pylint: disable=too-few-public-methods
    """ Represents an Azure Cloud instance """

    def __init__(self,
                 name,
                 endpoints=None,
                 suffixes=None,
                 profile=None,
                 is_active=False):
        self.name = name
        self.endpoints = endpoints or CloudEndpoints()
        self.suffixes = suffixes or CloudSuffixes()
        self.profile = profile
        self.is_active = is_active

    def __str__(self):
        o = {
            'profile': self.profile,
            'name': self.name,
            'is_active': self.is_active,
            'endpoints': vars(self.endpoints),
            'suffixes': vars(self.suffixes),
        }
        return pformat(o)

    def to_json(self):
        return {'name': self.name, "endpoints": self.endpoints.__dict__, "suffixes": self.suffixes.__dict__}

    @classmethod
    def from_json(cls, json_str):
        return cls(json_str['name'],
                   endpoints=CloudEndpoints(**json_str['endpoints']),
                   suffixes=CloudSuffixes(**json_str['suffixes']))

    def _get_default_scope(self):
        return "{}/{}".format(self.endpoints.resource_manager.rstrip("/"), ".default")

    def _get_authority(self):
        return parse.urlparse(self.endpoints.active_directory).netloc
    
    def _get_storage_endpoint(self):
        return self.suffixes.storage_endpoint


class CloudEndpoints:  # pylint: disable=too-few-public-methods,too-many-instance-attributes

    def __init__(self,  # pylint: disable=unused-argument
                 management=None,
                 resource_manager=None,
                 sql_management=None,
                 batch_resource_id=None,
                 gallery=None,
                 active_directory=None,
                 active_directory_resource_id=None,
                 active_directory_graph_resource_id=None,
                 microsoft_graph_resource_id=None,
                 active_directory_data_lake_resource_id=None,
                 vm_image_alias_doc=None,
                 media_resource_id=None,
                 ossrdbms_resource_id=None,
                 log_analytics_resource_id=None,
                 app_insights_resource_id=None,
                 app_insights_telemetry_channel_resource_id=None,
                 synapse_analytics_resource_id=None,
                 attestation_resource_id=None,
                 portal=None,
                 azmirror_storage_account_resource_id=None,
                 **kwargs):  # To support init with __dict__ for deserialization
        # Attribute names are significant. They are used when storing/retrieving clouds from config
        self.management = management
        self.resource_manager = resource_manager
        self.sql_management = sql_management
        self.batch_resource_id = batch_resource_id
        self.gallery = gallery
        self.active_directory = active_directory
        self.active_directory_resource_id = active_directory_resource_id
        self.active_directory_graph_resource_id = active_directory_graph_resource_id
        self.microsoft_graph_resource_id = microsoft_graph_resource_id
        self.active_directory_data_lake_resource_id = active_directory_data_lake_resource_id
        self.vm_image_alias_doc = vm_image_alias_doc
        self.media_resource_id = media_resource_id
        self.ossrdbms_resource_id = ossrdbms_resource_id
        self.log_analytics_resource_id = log_analytics_resource_id
        self.app_insights_resource_id = app_insights_resource_id
        self.app_insights_telemetry_channel_resource_id = app_insights_telemetry_channel_resource_id
        self.synapse_analytics_resource_id = synapse_analytics_resource_id
        self.attestation_resource_id = attestation_resource_id
        self.portal = portal
        self.azmirror_storage_account_resource_id = azmirror_storage_account_resource_id

    def has_endpoint_set(self, endpoint_name):
        try:
            # Can't simply use hasattr here as we override __getattribute__ below.
            # Python 3 hasattr() only returns False if an AttributeError is raised but we raise
            # CloudEndpointNotSetException. This exception is not a subclass of AttributeError.
            getattr(self, endpoint_name)
            return True
        except Exception:  # pylint: disable=broad-except
            return False

    def __getattribute__(self, name):
        val = object.__getattribute__(self, name)
        if val is None:
            raise CloudEndpointNotSetException("The endpoint '{}' for this cloud "
                                               "is not set but is used.\n"
                                               "may be corrupt or invalid.\nResolve the error or delete this file "
                                               "and try again.".format(name))
        return val


class CloudSuffixes:  # pylint: disable=too-few-public-methods,too-many-instance-attributes

    def __init__(self,  # pylint: disable=unused-argument
                 storage_endpoint=None,
                 storage_sync_endpoint=None,
                 keyvault_dns=None,
                 mhsm_dns=None,
                 sql_server_hostname=None,
                 azure_datalake_store_file_system_endpoint=None,
                 azure_datalake_analytics_catalog_and_job_endpoint=None,
                 acr_login_server_endpoint=None,
                 mysql_server_endpoint=None,
                 postgresql_server_endpoint=None,
                 mariadb_server_endpoint=None,
                 synapse_analytics_endpoint=None,
                 attestation_endpoint=None,
                 **kwargs):  # To support init with __dict__ for deserialization
        # Attribute names are significant. They are used when storing/retrieving clouds from config
        self.storage_endpoint = storage_endpoint
        self.storage_sync_endpoint = storage_sync_endpoint
        self.keyvault_dns = keyvault_dns
        self.mhsm_dns = mhsm_dns
        self.sql_server_hostname = sql_server_hostname
        self.mysql_server_endpoint = mysql_server_endpoint
        self.postgresql_server_endpoint = postgresql_server_endpoint
        self.mariadb_server_endpoint = mariadb_server_endpoint
        self.azure_datalake_store_file_system_endpoint = azure_datalake_store_file_system_endpoint
        self.azure_datalake_analytics_catalog_and_job_endpoint = azure_datalake_analytics_catalog_and_job_endpoint
        self.acr_login_server_endpoint = acr_login_server_endpoint
        self.synapse_analytics_endpoint = synapse_analytics_endpoint
        self.attestation_endpoint = attestation_endpoint

    def __getattribute__(self, name):
        val = object.__getattribute__(self, name)
        if val is None:
            raise CloudSuffixNotSetException("The suffix '{}' for this cloud "
                                             "is not set but is used.\n"
                                             "may be corrupt or invalid.\nResolve the error or delete this file "
                                             "and try again.".format(name))
        return val


AZURE_PUBLIC_CLOUD = Cloud(
    'AzureCloud',
    endpoints=CloudEndpoints(
        management='https://management.core.windows.net/',
        resource_manager='https://management.azure.com/',
        sql_management='https://management.core.windows.net:8443/',
        batch_resource_id='https://batch.core.windows.net/',
        gallery='https://gallery.azure.com/',
        active_directory='https://login.microsoftonline.com',
        active_directory_resource_id='https://management.core.windows.net/',
        active_directory_graph_resource_id='https://graph.windows.net/',
        microsoft_graph_resource_id='https://graph.microsoft.com/',
        active_directory_data_lake_resource_id='https://datalake.azure.net/',
        vm_image_alias_doc='https://raw.githubusercontent.com/Azure/azure-rest-api-specs/master/arm-compute/quickstart-templates/aliases.json',
        media_resource_id='https://rest.media.azure.net',
        ossrdbms_resource_id='https://ossrdbms-aad.database.windows.net',
        app_insights_resource_id='https://api.applicationinsights.io',
        log_analytics_resource_id='https://api.loganalytics.io',
        app_insights_telemetry_channel_resource_id='https://dc.applicationinsights.azure.com/v2/track',
        synapse_analytics_resource_id='https://dev.azuresynapse.net',
        attestation_resource_id='https://attest.azure.net',
        portal='https://portal.azure.com'),
    suffixes=CloudSuffixes(
        storage_endpoint='core.windows.net',
        storage_sync_endpoint='afs.azure.net',
        keyvault_dns='.vault.azure.net',
        mhsm_dns='.managedhsm.azure.net',
        sql_server_hostname='.database.windows.net',
        mysql_server_endpoint='.mysql.database.azure.com',
        postgresql_server_endpoint='.postgres.database.azure.com',
        mariadb_server_endpoint='.mariadb.database.azure.com',
        azure_datalake_store_file_system_endpoint='azuredatalakestore.net',
        azure_datalake_analytics_catalog_and_job_endpoint='azuredatalakeanalytics.net',
        acr_login_server_endpoint='.azurecr.io',
        synapse_analytics_endpoint='.dev.azuresynapse.net',
        attestation_endpoint='.attest.azure.net'))

AZURE_CHINA_CLOUD = Cloud(
    'AzureChinaCloud',
    endpoints=CloudEndpoints(
        management='https://management.core.chinacloudapi.cn/',
        resource_manager='https://management.chinacloudapi.cn',
        sql_management='https://management.core.chinacloudapi.cn:8443/',
        batch_resource_id='https://batch.chinacloudapi.cn/',
        gallery='https://gallery.chinacloudapi.cn/',
        active_directory='https://login.chinacloudapi.cn',
        active_directory_resource_id='https://management.core.chinacloudapi.cn/',
        active_directory_graph_resource_id='https://graph.chinacloudapi.cn/',
        microsoft_graph_resource_id='https://microsoftgraph.chinacloudapi.cn',
        vm_image_alias_doc='https://raw.githubusercontent.com/Azure/azure-rest-api-specs/master/arm-compute/quickstart-templates/aliases.json',
        media_resource_id='https://rest.media.chinacloudapi.cn',
        ossrdbms_resource_id='https://ossrdbms-aad.database.chinacloudapi.cn',
        app_insights_resource_id='https://api.applicationinsights.azure.cn',
        log_analytics_resource_id='https://api.loganalytics.azure.cn',
        app_insights_telemetry_channel_resource_id='https://dc.applicationinsights.azure.cn/v2/track',
        synapse_analytics_resource_id='https://dev.azuresynapse.azure.cn',
        portal='https://portal.azure.cn'),
    suffixes=CloudSuffixes(
        storage_endpoint='core.chinacloudapi.cn',
        keyvault_dns='.vault.azure.cn',
        mhsm_dns='.managedhsm.azure.cn',
        sql_server_hostname='.database.chinacloudapi.cn',
        mysql_server_endpoint='.mysql.database.chinacloudapi.cn',
        postgresql_server_endpoint='.postgres.database.chinacloudapi.cn',
        mariadb_server_endpoint='.mariadb.database.chinacloudapi.cn',
        acr_login_server_endpoint='.azurecr.cn',
        synapse_analytics_endpoint='.dev.azuresynapse.azure.cn'))

AZURE_US_GOV_CLOUD = Cloud(
    'AzureUSGovernment',
    endpoints=CloudEndpoints(
        management='https://management.core.usgovcloudapi.net/',
        resource_manager='https://management.usgovcloudapi.net/',
        sql_management='https://management.core.usgovcloudapi.net:8443/',
        batch_resource_id='https://batch.core.usgovcloudapi.net/',
        gallery='https://gallery.usgovcloudapi.net/',
        active_directory='https://login.microsoftonline.us',
        active_directory_resource_id='https://management.core.usgovcloudapi.net/',
        active_directory_graph_resource_id='https://graph.windows.net/',
        microsoft_graph_resource_id='https://graph.microsoft.us/',
        vm_image_alias_doc='https://raw.githubusercontent.com/Azure/azure-rest-api-specs/master/arm-compute/quickstart-templates/aliases.json',
        media_resource_id='https://rest.media.usgovcloudapi.net',
        ossrdbms_resource_id='https://ossrdbms-aad.database.usgovcloudapi.net',
        app_insights_resource_id='https://api.applicationinsights.us',
        log_analytics_resource_id='https://api.loganalytics.us',
        app_insights_telemetry_channel_resource_id='https://dc.applicationinsights.us/v2/track',
        synapse_analytics_resource_id='https://dev.azuresynapse.usgovcloudapi.net',
        portal='https://portal.azure.us'),
    suffixes=CloudSuffixes(
        storage_endpoint='core.usgovcloudapi.net',
        storage_sync_endpoint='afs.azure.us',
        keyvault_dns='.vault.usgovcloudapi.net',
        mhsm_dns='.managedhsm.usgovcloudapi.net',
        sql_server_hostname='.database.usgovcloudapi.net',
        mysql_server_endpoint='.mysql.database.usgovcloudapi.net',
        postgresql_server_endpoint='.postgres.database.usgovcloudapi.net',
        mariadb_server_endpoint='.mariadb.database.usgovcloudapi.net',
        acr_login_server_endpoint='.azurecr.us',
        synapse_analytics_endpoint='.dev.azuresynapse.usgovcloudapi.net'))

AZURE_GERMAN_CLOUD = Cloud(
    'AzureGermanCloud',
    endpoints=CloudEndpoints(
        management='https://management.core.cloudapi.de/',
        resource_manager='https://management.microsoftazure.de',
        sql_management='https://management.core.cloudapi.de:8443/',
        batch_resource_id='https://batch.cloudapi.de/',
        gallery='https://gallery.cloudapi.de/',
        active_directory='https://login.microsoftonline.de',
        active_directory_resource_id='https://management.core.cloudapi.de/',
        active_directory_graph_resource_id='https://graph.cloudapi.de/',
        microsoft_graph_resource_id='https://graph.microsoft.de',
        vm_image_alias_doc='https://raw.githubusercontent.com/Azure/azure-rest-api-specs/master/arm-compute/quickstart-templates/aliases.json',
        media_resource_id='https://rest.media.cloudapi.de',
        ossrdbms_resource_id='https://ossrdbms-aad.database.cloudapi.de',
        portal='https://portal.microsoftazure.de'),
    suffixes=CloudSuffixes(
        storage_endpoint='core.cloudapi.de',
        keyvault_dns='.vault.microsoftazure.de',
        mhsm_dns='.managedhsm.microsoftazure.de',
        sql_server_hostname='.database.cloudapi.de',
        mysql_server_endpoint='.mysql.database.cloudapi.de',
        postgresql_server_endpoint='.postgres.database.cloudapi.de',
        mariadb_server_endpoint='.mariadb.database.cloudapi.de'))


def _add_starting_dot(suffix):
    return suffix if not suffix or suffix.startswith('.') else '.' + suffix


def _get_arm_endpoint(arm_dict, is_suffix=False):
    def _get_processed_arm_endpoint(name, add_dot=False, fallback_value=None):
        if is_suffix:
            return (_add_starting_dot(arm_dict['suffixes'][name]) if add_dot else arm_dict['suffixes'][name]) if name in \
                                                                                                                 arm_dict[
                                                                                                                     'suffixes'] else fallback_value
        return arm_dict[name] if name in arm_dict else fallback_value

    return _get_processed_arm_endpoint


def _get_database_server_endpoint(sql_server_hostname, cloud_name):
    def _concat_db_server_endpoint(db_prefix):
        if cloud_name == 'AzureCloud':
            return db_prefix + '.database.azure.com'
        if not sql_server_hostname:
            return None
        return db_prefix + sql_server_hostname

    return _concat_db_server_endpoint


def _get_endpoint_fallback_value(cloud_name):
    def _get_cloud_endpoint_fallback_value(endpoint_name):
        endpoint_mapper = {c.name: c.endpoints.__dict__.get(endpoint_name, None) for c in HARD_CODED_CLOUD_LIST}
        return endpoint_mapper.get(cloud_name, None)

    return _get_cloud_endpoint_fallback_value


def _get_suffix_fallback_value(cloud_name):
    def _get_cloud_suffix_fallback_value(suffix_name):
        suffix_mapper = {c.name: c.suffixes.__dict__.get(suffix_name, None) for c in HARD_CODED_CLOUD_LIST}
        return suffix_mapper.get(cloud_name, None)

    return _get_cloud_suffix_fallback_value


def _arm_to_cli_mapper(arm_dict):
    get_endpoint = _get_arm_endpoint(arm_dict)
    get_suffix = _get_arm_endpoint(arm_dict, is_suffix=True)

    sql_server_hostname = get_suffix('sqlServerHostname', add_dot=True)
    get_db_server_endpoint = _get_database_server_endpoint(sql_server_hostname, arm_dict['name'])

    get_suffix_fallback_value = _get_suffix_fallback_value(arm_dict['name'])
    get_endpoint_fallback_value = _get_endpoint_fallback_value(arm_dict['name'])

    return Cloud(
        arm_dict['name'],
        endpoints=CloudEndpoints(
            # please add fallback_value if the endpoint is not added to https://management.azure.com/metadata/endpoints?api-version=2019-05-01 yet
            management=arm_dict['authentication']['audiences'][0],
            resource_manager=get_endpoint('resourceManager'),
            sql_management=get_endpoint('sqlManagement'),
            batch_resource_id=get_endpoint('batch'),
            gallery=get_endpoint('gallery'),
            active_directory=arm_dict['authentication']['loginEndpoint'],
            active_directory_resource_id=arm_dict['authentication']['audiences'][0],
            active_directory_graph_resource_id=get_endpoint('graphAudience'),
            microsoft_graph_resource_id=get_endpoint('microsoftGraphResourceId',
                                                     fallback_value=get_endpoint_fallback_value(
                                                         'microsoft_graph_resource_id')),
            # change once microsoft_graph_resource_id is fixed in ARM
            vm_image_alias_doc=get_endpoint('vmImageAliasDoc'),
            media_resource_id=get_endpoint('media'),
            ossrdbms_resource_id=get_endpoint('ossrdbmsResourceId',
                                              fallback_value=get_endpoint_fallback_value('ossrdbms_resource_id')),
            # change once ossrdbms_resource_id is available via ARM
            active_directory_data_lake_resource_id=get_endpoint('activeDirectoryDataLake'),
            app_insights_resource_id=get_endpoint('appInsightsResourceId', fallback_value=get_endpoint_fallback_value(
                'app_insights_resource_id')),
            log_analytics_resource_id=get_endpoint('logAnalyticsResourceId', fallback_value=get_endpoint_fallback_value(
                'log_analytics_resource_id')),
            synapse_analytics_resource_id=get_endpoint('synapseAnalyticsResourceId',
                                                       fallback_value=get_endpoint_fallback_value(
                                                           'synapse_analytics_resource_id')),
            app_insights_telemetry_channel_resource_id=get_endpoint('appInsightsTelemetryChannelResourceId',
                                                                    fallback_value=get_endpoint_fallback_value(
                                                                        'app_insights_telemetry_channel_resource_id')),
            attestation_resource_id=get_endpoint('attestationResourceId',
                                                 fallback_value=get_endpoint_fallback_value('attestation_resource_id')),
            portal=get_endpoint('portal'),
            azmirror_storage_account_resource_id=get_endpoint('azmirrorStorageAccountResourceId')),
        suffixes=CloudSuffixes(
            storage_endpoint=get_suffix('storage'),
            storage_sync_endpoint=get_suffix('storageSyncEndpointSuffix',
                                             fallback_value=get_suffix_fallback_value('storage_sync_endpoint')),
            keyvault_dns=get_suffix('keyVaultDns', add_dot=True),
            mhsm_dns=get_suffix('mhsmDns', add_dot=True, fallback_value=get_suffix_fallback_value('mhsm_dns')),
            sql_server_hostname=sql_server_hostname,
            mysql_server_endpoint=get_suffix('mysqlServerEndpoint', add_dot=True,
                                             fallback_value=get_db_server_endpoint('.mysql')),
            postgresql_server_endpoint=get_suffix('postgresqlServerEndpoint', add_dot=True,
                                                  fallback_value=get_db_server_endpoint('.postgres')),
            mariadb_server_endpoint=get_suffix('mariadbServerEndpoint', add_dot=True,
                                               fallback_value=get_db_server_endpoint('.mariadb')),
            azure_datalake_store_file_system_endpoint=get_suffix('azureDataLakeStoreFileSystem'),
            azure_datalake_analytics_catalog_and_job_endpoint=get_suffix('azureDataLakeAnalyticsCatalogAndJob'),
            synapse_analytics_endpoint=get_suffix('synapseAnalytics', add_dot=True,
                                                  fallback_value=get_suffix_fallback_value(
                                                      'synapse_analytics_endpoint')),
            acr_login_server_endpoint=get_suffix('acrLoginServer', add_dot=True),
            attestation_endpoint=get_suffix('attestationEndpoint', add_dot=True,
                                            fallback_value=get_suffix_fallback_value('attestation_endpoint'))))


def _convert_arm_to_cli(arm_cloud_metadata_dict):
    cli_cloud_metadata_dict = {}
    for cloud in arm_cloud_metadata_dict:
        cli_cloud_metadata_dict[cloud['name']] = _arm_to_cli_mapper(cloud)
        # Strip trailing slash at end of active directory endpoints
        for cloud in cli_cloud_metadata_dict.keys():
            logger.debug('Active directory endpoint loaded from {0} metadata is {1}'.format(cloud,
                                                                                            cli_cloud_metadata_dict[
                                                                                                cloud].endpoints.active_directory))
            cli_cloud_metadata_dict[cloud].endpoints.active_directory = cli_cloud_metadata_dict[
                cloud].endpoints.active_directory.rstrip('/')
            logger.debug('Active directory endpoint for cloud {0} set to {1}'.format(cloud, cli_cloud_metadata_dict[
                cloud].endpoints.active_directory))
    return cli_cloud_metadata_dict


HARD_CODED_CLOUD_LIST = [AZURE_PUBLIC_CLOUD, AZURE_CHINA_CLOUD, AZURE_US_GOV_CLOUD, AZURE_GERMAN_CLOUD]


def get_known_clouds():
    if 'ARM_CLOUD_METADATA_URL' in os.environ:
        try:
            arm_cloud_dict = None
            with requests.get(os.getenv('ARM_CLOUD_METADATA_URL'), timeout=DEFAULT_TIMEOUT) as meta_response:
                arm_cloud_dict = meta_response.json()
            cli_cloud_dict = _convert_arm_to_cli(arm_cloud_dict)
            logger.info("Cloud endpoints loaded from ARM_CLOUD_METADATA_URL: %s", os.getenv('ARM_CLOUD_METADATA_URL'))
        except Exception as ex:  # pylint: disable=broad-except
            logger.warning('Failed to load cloud metadata from the url specified by ARM_CLOUD_METADATA_URL')
            raise ex

        if not cli_cloud_dict:
            raise Exception("No clouds available. Please ensure ARM_CLOUD_METADATA_URL is valid.")
        return cli_cloud_dict
    return {cloud.name: cloud for cloud in HARD_CODED_CLOUD_LIST}


KNOWN_CLOUDS = get_known_clouds()


def _get_cloud_or_default(cloud_name=None):
    if not cloud_name:
        cloud_name = os.getenv(AZUREML_CLOUD_ENV_NAME)
        if cloud_name:
            logger.info("Fetched cloud name from environment variable {}".format(AZUREML_CLOUD_ENV_NAME))

    if cloud_name in KNOWN_CLOUDS.keys():
        return KNOWN_CLOUDS[cloud_name]

    clouds = _get_cloud_metadata_from_known_urls()
    if clouds:
        logger.info("Cloud was fetched from known metadataurls")
        for name, cloud in clouds.items():
            if name not in KNOWN_CLOUDS.keys():
                KNOWN_CLOUDS.update({name: cloud})
    else:
        logger.info("Cloud could not be fetched from known metadataurls falling back to known clouds")
        clouds = KNOWN_CLOUDS

    if cloud_name in KNOWN_CLOUDS.keys():
        return KNOWN_CLOUDS[cloud_name]
    else:
        if cloud_name is None:
            logger.info("Cloud metadata not found so falling back to {} as default".format(list(clouds.values())[0].name))
            return list(clouds.values())[0]

    raise Exception("{} cloud metadata could not be fetched or found".format(cloud_name))


def _get_clouds_by_metadata_url(metadata_url, timeout=DEFAULT_TIMEOUT):
    """Get all the clouds by the specified metadata url

        :return: list of the clouds
        :rtype: list[azureml._vendor.azure_cli_core.Cloud]
    """
    try:
        import requests
        logger.debug('Start : Loading cloud metatdata from the url specified by {0}'.format(metadata_url))
        with requests.get(metadata_url, timeout=timeout) as meta_response:
            arm_cloud_dict = meta_response.json()
            cli_cloud_dict = _convert_arm_to_cli(arm_cloud_dict)
            # Strip trailing slash at end of active directory endpoints
            for cloud in cli_cloud_dict.keys():
                logger.debug('Active directory endpoint loaded from {0} metadata is {1}'.format(cloud, cli_cloud_dict[
                    cloud].endpoints.active_directory))
                cli_cloud_dict[cloud].endpoints.active_directory = cli_cloud_dict[
                    cloud].endpoints.active_directory.rstrip('/')
                logger.debug('Active directory endpoint for cloud {0} set to {1}'.format(cloud, cli_cloud_dict[
                    cloud].endpoints.active_directory))
            logger.debug('Finish : Loading cloud metatdata from the url specified by {0}'.format(metadata_url))
            return cli_cloud_dict
    except Exception as ex:  # pylint: disable=broad-except
        logger.warning("Error: Azure ML was unable to load cloud metadata from the url specified by {0}. {1}. "
                       "This may be due to a misconfiguration of networking controls. Azure Machine Learning Python SDK "
                       "requires outbound access to Azure Resource Manager. Please contact your networking team to configure "
                       "outbound access to Azure Resource Manager on both Network Security Group and Firewall. "
                       "For more details on required configurations, see "
                       "https://docs.microsoft.com/azure/machine-learning/how-to-access-azureml-behind-firewall."
                       .format(metadata_url, ex))


def _get_cloud_metadata_from_known_urls():
    logger.info("Fetching cloud metadata from known urls")
    for metadata_url in KNOWN_METADATA_URL_LIST:
        logger.debug('Start : Loading cloud metatdata from url {}'.format(metadata_url))
        clouds = _get_clouds_by_metadata_url(metadata_url, DEFAULT_TIMEOUT)
        if clouds:
            logger.debug('Finish : Loading cloud metatdata')
            return clouds

        logger.debug('Finish : Loading cloud metatdata')
