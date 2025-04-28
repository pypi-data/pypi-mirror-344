# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""mlflow helper functions."""

import logging
import os
import re

from azureml.mlflow._common._authentication.azureml_token_authentication import (
    AzureMLTokenAuthentication,
)
from azureml.mlflow._common._authentication.databricks_cluster_authentication import (
    _DatabricksClusterAuthentication,
)
from azureml.mlflow._common._authentication.arcadia_authentication import (
    _ArcadiaAuthentication,
)
from azureml.mlflow._client.artifact.run_artifact_client import (
    RunArtifactsClient,
)
from azureml.mlflow._client.artifact.local_artifact_client import (
    LocalArtifactClient,
)
from azure.identity import (
    DefaultAzureCredential,
    ChainedTokenCredential,
    DeviceCodeCredential,
    InteractiveBrowserCredential,
)
from azureml.mlflow._common._cloud.cloud import _get_cloud_or_default

from six.moves.urllib import parse

_IS_REMOTE = "is-remote"
_REGION = "region"
_SUB_ID = "sub-id"
_RES_GRP = "res-grp"
_WS_NAME = "ws-name"
_REG_NAME = "reg-name"
_EXP_NAME = "experiment"
_RUN_ID = "runid"
_ORIGIN = "origin"
_CONTAINER = "container"

_AUTH_HEAD = "auth"
_AUTH_TYPE = "auth-type"
_CLOUD_TYPE = "cloud-type"
_TRUE_QUERY_VALUE = "True"

_TOKEN_PREFIX = "Bearer "
_TOKEN_QUERY_NAME = "token"

_ARTIFACT_PATH = "artifact_path"

logger = logging.getLogger(__name__)

_ARTIFACT_URI_EXP_RUN_REGEX = r".*/([^/]+)/runs/([^/]+)(/artifacts.*)?"

_WORKSPACE_INFO_REGEX = (
    r".*/subscriptions/(.+)/resourceGroups/(.+)"
    r"/providers/Microsoft.MachineLearningServices/workspaces/([^/]+)"
)

_REGISTRY_INFO_REGEX = (
    r".*/subscriptions/(.+)/resourceGroups/(.+)"
    r"/providers/Microsoft.MachineLearningServices/registries/([^/]+)"
)

_ARTIFACT_URI_REGEX = (
    _WORKSPACE_INFO_REGEX + r"/experiments/([^/]+)/runs/([^/]+)(/artifacts.*)?"
)

VERSION_WARNING = (
    "Could not import {}. Please upgrade to Mlflow 1.4.0 or higher."
)


class ServiceContextBase(object):
    def __init__(
        self, subscription_id, resource_group_name, auth, host_url, cloud
    ):
        self._subscription_id = subscription_id
        self._resource_group_name = resource_group_name
        self._auth = auth
        self._host_url = host_url
        self._cloud = cloud

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def resource_group_name(self):
        return self._resource_group_name

    @property
    def auth(self):
        return self._auth

    @property
    def host_url(self):
        return self._host_url

    @property
    def cloud(self):
        if self._cloud is None:
            self._cloud = _get_cloud_or_default()
        return self._cloud


class ServiceContext(ServiceContextBase):
    def __init__(
        self,
        host_url,
        subscription_id,
        workspace_name,
        resource_group_name,
        auth,
        location=None,
        cloud=None,
    ):
        super().__init__(
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            auth=auth,
            host_url=host_url,
            cloud=cloud,
        )

        self._workspace_name = workspace_name
        self._location = location

    @property
    def workspace_name(self):
        return self._workspace_name

    @property
    def location(self):
        return self._location

    def _get_workspace_scope(self):
        """
        For all pre-existing code that access the get_workspace_scope() method

        Return the scope information for the workspace.

        :param workspace_object: The workspace object.
        :type workspace_object: azureml.core.workspace.Workspace
        :return: The scope information for the workspace.
        :rtype: str
        """
        return (
            "/subscriptions/{}/resourceGroups/{}/providers"
            "/Microsoft.MachineLearningServices"
            "/workspaces/{}"
        ).format(
            self._subscription_id,
            self._resource_group_name,
            self._workspace_name,
        )

    def _get_scope(self):
        """
        Return the scope information for the workspace.

        :param workspace_object: The workspace object.
        :type workspace_object: azureml.core.workspace.Workspace
        :return: The scope information for the workspace.
        :rtype: str
        """
        return (
            "/subscriptions/{}/resourceGroups/{}/providers"
            "/Microsoft.MachineLearningServices"
            "/workspaces/{}"
        ).format(
            self._subscription_id,
            self._resource_group_name,
            self._workspace_name,
        )


class RegistryServiceContext(ServiceContextBase):
    def __init__(
        self,
        subscription_id,
        resource_group_name,
        registry_name,
        auth,
        host_url,
        cloud,
    ):
        super().__init__(
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            auth=auth,
            host_url=host_url,
            cloud=cloud,
        )
        self._registry_name = registry_name

    @property
    def registry_name(self):
        return self._registry_name

    def _get_scope(self):
        """
        Return the scope information for the registry.
        """
        return (
            "/subscriptions/{}/resourceGroups/{}/providers"
            "/Microsoft.MachineLearningServices"
            "/registries/{}"
        ).format(
            self._subscription_id,
            self._resource_group_name,
            self._registry_name,
        )


def tracking_uri_decomp(tracking_uri, is_registry):
    """
    Parse the tracking URI into a dictionary.

    The tracking URI contains the scope information for the workspace.

    :param tracking_uri: The tracking_uri to parse.
    :type tracking_uri: str
    :return: Dictionary of the parsed workspace information
    :rtype: dict[str, str]
    """

    logger.info("Parsing tracking uri {}".format(tracking_uri))
    parsed_url_path = parse.urlparse(tracking_uri).path

    pattern = (
        re.compile(_REGISTRY_INFO_REGEX)
        if is_registry
        else re.compile(_WORKSPACE_INFO_REGEX)
    )
    mo = pattern.match(parsed_url_path)

    ret = {}
    ret[_SUB_ID] = mo.group(1)
    ret[_RES_GRP] = mo.group(2)
    if is_registry:
        ret[_REG_NAME] = mo.group(3)
        logger.info(
            "Tracking uri {} has sub id {}, resource group {}, and workspace {}".format(
                tracking_uri, ret[_SUB_ID], ret[_RES_GRP], ret[_REG_NAME]
            )
        )
    else:
        ret[_WS_NAME] = mo.group(3)
        logger.info(
            "Tracking uri {} has sub id {}, resource group {}, and workspace {}".format(
                tracking_uri, ret[_SUB_ID], ret[_RES_GRP], ret[_WS_NAME]
            )
        )

    return ret


def get_run_info(parsed_url_path):
    run_info_dict = {}
    try:
        mo = re.compile(_ARTIFACT_URI_REGEX).match(parsed_url_path)
        run_info_dict[_SUB_ID] = mo.group(1)
        run_info_dict[_RES_GRP] = mo.group(2)
        run_info_dict[_WS_NAME] = mo.group(3)
        run_info_dict[_EXP_NAME] = mo.group(4)
        run_info_dict[_RUN_ID] = mo.group(5)
        path_match = mo.group(7)
    except Exception:
        try:
            mo = re.compile(_ARTIFACT_URI_EXP_RUN_REGEX).match(parsed_url_path)
            run_info_dict[_EXP_NAME] = mo.group(1)
            run_info_dict[_RUN_ID] = mo.group(2)
            path_match = mo.group(3)
        except Exception:
            return

    if path_match is not None and path_match != "/artifacts":
        path = path_match[len("/artifacts") :]
        run_info_dict[_ARTIFACT_PATH] = (
            path if not path.startswith("/") else path[1:]
        )
    return run_info_dict


def artifact_uri_decomp(artifact_uri):
    """
    Parse the artifact URI into a dictionary.

    The artifact URI contains the scope information for the workspace, the experiment and the run_id.

    :param artifact_uri: The artifact_uri to parse.
    :type artifact_uri: str
    :return: Dictionary of the parsed experiment name, and run id and workspace information if available.
    :rtype: dict[str, str]
    """

    logger.info("Parsing artifact uri {}".format(artifact_uri))
    parsed_url_path = parse.urlparse(artifact_uri).path
    artifact_info_dict = get_run_info(parsed_url_path) or {}

    if not artifact_info_dict:
        # Remove the starting "/"
        origin, container, path = parsed_url_path[1:].split("/", 3)
        artifact_info_dict[_ORIGIN] = origin
        artifact_info_dict[_CONTAINER] = container
        artifact_info_dict[_ARTIFACT_PATH] = (
            path if not path.startswith("/") else path[1:]
        )

    logger.info(
        "Artifact uri {} info: {}".format(artifact_uri, artifact_info_dict)
    )
    return artifact_info_dict


def get_service_context_from_artifact_url(parsed_url):
    from mlflow.exceptions import MlflowException  # Avoiding circular import

    parsed_artifacts_path = artifact_uri_decomp(parsed_url.path)
    logger.debug("Creating service context from the artifact uri")
    subscription_id = parsed_artifacts_path[_SUB_ID]
    resource_group_name = parsed_artifacts_path[_RES_GRP]
    workspace_name = parsed_artifacts_path.get(_WS_NAME, None)  # noqa: F841
    registry_name = parsed_artifacts_path.get(_REG_NAME, None)
    queries = dict(parse.parse_qsl(parsed_url.query))
    if _TOKEN_QUERY_NAME not in queries:
        raise MlflowException(
            "An authorization token was not set in the artifact uri"
        )

    auth = AzureMLTokenAuthentication(
        queries[_TOKEN_QUERY_NAME],
        host=parsed_url.netloc,
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        workspace_name=workspace_name
    )

    return ServiceContext(
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
        registry_name=registry_name,
        workspace_id=None,
        workspace_discovery_url=None,
        authentication=auth,
    )


def get_service_context_from_tracking_url_default_auth(parsed_url):
    """Create a Service Context object out of a parsed URL."""
    logger.debug(
        "Creating a Service Context object from the tracking uri using default authentication"
        " : InteractiveLoginAuthentication"
    )
    parsed_path = tracking_uri_decomp(parsed_url.path, False)
    subscription_id = parsed_path[_SUB_ID]
    resource_group_name = parsed_path[_RES_GRP]
    workspace_name = parsed_path[_WS_NAME]
    queries = dict(parse.parse_qsl(parsed_url.query))

    if _AUTH_HEAD in queries or _AUTH_TYPE in queries:
        logger.warning(
            "Use of {}, {} query parameters in tracking URI is deprecated."
            " InteractiveLoginAuthentication will be used by default."
            " Please use 'azureml.core.workspace.Workspace.get_mlflow_tracking_uri'"
            " to use authentication associated with workspace".format(
                _AUTH_TYPE, _AUTH_HEAD
            )
        )

    """
    Using InteractiveLoginAuthentication poses an issue if customer uses a subscription not belonging to its default
    tenant. In that case customer needs to provide tenantId as a param to InteractiveLoginAuthentication which is
    not possible currently in this flow. In this case customer needs to create workspace object with auth param

        from azureml.core.authentication import InteractiveLoginAuthentication

        interactive_auth = InteractiveLoginAuthentication(tenant_id="my-tenant-id")

        ws = Workspace(subscription_id="my-subscription-id",
                       resource_group="my-ml-rg",
                       workspace_name="my-ml-workspace",
                       auth=interactive_auth)

        ws.get_mlflow_tracking_uri()
    """
    cloud = _get_cloud_or_default()
    tenant_id = os.getenv("AZURE_TENANT_ID", None)
    default_auth = DefaultAzureCredential(authority=cloud._get_authority())
    auth = ChainedTokenCredential(
        *default_auth.credentials,
        _ArcadiaAuthentication(),
        _DatabricksClusterAuthentication(),
        InteractiveBrowserCredential(
            authority=cloud._get_authority(), tenant_id=tenant_id
        ),
        DeviceCodeCredential(
            authority=cloud._get_authority(), tenant_id=tenant_id
        )
    )
    service_context = ServiceContext(
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
        auth=auth,
        host_url="https://" + parsed_url.netloc,
        cloud=cloud,
    )
    # TODO Create host url from tracking URL select scheme based on dev mode or no

    return service_context


def get_service_context_from_tracking_url_mlflow_env_vars(parsed_url):
    parsed_path = tracking_uri_decomp(parsed_url.path, False)
    subscription_id = parsed_path[_SUB_ID]
    resource_group_name = parsed_path[_RES_GRP]
    workspace_name = parsed_path[_WS_NAME]
    token = os.environ["MLFLOW_TRACKING_TOKEN"]
    experiment_name = os.environ.get("MLFLOW_EXPERIMENT_NAME", None)
    experiment_id = os.environ.get("MLFLOW_EXPERIMENT_ID", None)
    run_id = os.environ["MLFLOW_RUN_ID"]
    host_url = "https://{0}".format(parsed_url.netloc)

    auth = AzureMLTokenAuthentication.create(
        azureml_access_token=token,
        expiry_time=None,
        host=host_url,
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
        experiment_name=experiment_name,
        experiment_id=experiment_id,
        run_id=run_id,
    )

    # This adds dependecny on these 2 env vars
    # AZUREML_SERVICE_ENDPOINT, AZUREML_WORKSPACE_ID
    # and they are set for remote runs by backend service
    # Needs this so that discovery url is set correctly for Private Link (PL) and non PL workspace
    # Now since we are using tracking uri and using that for host url it should handle PL workspace.
    cloud = _get_cloud_or_default()
    service_context = ServiceContext(
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
        auth=auth,
        host_url=host_url,
        cloud=cloud,
    )
    # TODO Create host url from tracking URL select scheme based on dev mode or no

    return service_context


def get_aml_experiment_name(exp_name):
    """Extract the actual experiment name from the adb experiment name format."""
    regex = "(.+)\\/(.+)"
    mo = re.compile(regex).match(exp_name)
    if mo is not None:
        logger.info(
            "Parsing experiment name from {} to {}".format(
                exp_name, mo.group(2)
            )
        )
        return mo.group(2)
    else:
        logger.debug(
            "The given experiment name {} does not match regex {}".format(
                exp_name, regex
            )
        )
        return exp_name


def handle_exception(operation, store, e):
    from mlflow.exceptions import MlflowException  # Avoiding circular import

    msg = "Failed to {} from the {} store with exception {}".format(
        operation, store.__class__.__name__, e
    )
    raise MlflowException(msg)


def execute_func(func, stores, operation, *args, **kwargs):
    """
    :param func: func to call with store as first param
    :type func: function with store as the first param and inputs to the
        store func as the rest
    :param operation: Identifier for the operation
    :type operation: str
    :param args: arguments for func after store
    :param kwargs: kwargs for func
    :return: list of store returns of func per store
    :rtype: list[< - func]
    """
    store = stores[0]
    try:
        out = func(store, *args, **kwargs)
    except Exception as e:
        handle_exception(operation, store, e)
    for other_store in stores[1:]:
        try:
            func(other_store, *args, **kwargs)
        except Exception as e:
            handle_exception(operation, other_store, e)
    return out


def get_service_context(parsed_artifacts_url):
    from mlflow.tracking.client import MlflowClient
    from azureml.mlflow._store.tracking.store import AzureMLRestStore

    try:
        store = MlflowClient()._tracking_client.store
    except Exception:
        logger.warning(
            VERSION_WARNING.format("MlflowClient()._tracking_client.store")
        )
        store = MlflowClient().store
    if isinstance(store, AzureMLRestStore):
        logger.debug(
            "Using the service context from the {} store".format(
                store.__class__.__name__
            )
        )
        return store.service_context
    else:
        return get_service_context_from_artifact_url(parsed_artifacts_url)


def get_artifact_repository_client(artifact_uri):
    logger.debug("Initializing the AzureMLflowArtifactRepository")
    parsed_artifacts_url = parse.urlparse(artifact_uri)
    service_context = get_service_context(parsed_artifacts_url)

    parsed_artifacts_path = artifact_uri_decomp(artifact_uri, False)

    # else if statement for when artifact_uri from registry
    # We need to check what the uri contains to determine if its enough info to get sas uri

    if _EXP_NAME in parsed_artifacts_path and _RUN_ID in parsed_artifacts_path:
        experiment_name = parsed_artifacts_path[_EXP_NAME]
        logger.debug(
            "AzureMLflowArtifactRepository for experiment {}".format(
                experiment_name
            )
        )
        run_id = parsed_artifacts_path[_RUN_ID]
        logger.debug(
            "AzureMLflowArtifactRepository for run id {}".format(run_id)
        )
        path = parsed_artifacts_path.get(_ARTIFACT_PATH)
        logger.debug("AzureMLflowArtifactRepository for path {}".format(path))
        artifacts_client = RunArtifactsClient(
            get_v2_service_context(service_context),
            experiment_name,
            run_id,
            path,
        )
    else:
        origin = parsed_artifacts_path[_ORIGIN]
        container = parsed_artifacts_path[_CONTAINER]
        path = parsed_artifacts_path[_ARTIFACT_PATH]
        artifacts_client = LocalArtifactClient(
            get_v2_service_context(service_context), origin, container, path
        )
    return artifacts_client


def get_v2_service_context(service_context):
    return ServiceContext(
        subscription_id=service_context.subscription_id,
        workspace_name=service_context.workspace_name,
        resource_group_name=service_context.resource_group_name,
        auth=service_context.get_auth(),
        host_url=service_context._get_mlflow_url(),
        cloud=_get_cloud_or_default(
            service_context.get_auth()._cloud_type.name
        ),
    )


def _get_cloud_from_tracking_uri(tracking_uri):
    parse.urlparse(tracking_uri)


def get_service_context_from_registry_url_mlflow_env_vars(parsed_url):
    parsed_path = tracking_uri_decomp(parsed_url.path, True)
    subscription_id = parsed_path[_SUB_ID]
    resource_group_name = parsed_path[_RES_GRP]
    registry_name = parsed_path.get(_REG_NAME, None)
    token = os.environ["MLFLOW_TRACKING_TOKEN"]
    experiment_name = os.environ.get("MLFLOW_EXPERIMENT_NAME", None)
    experiment_id = os.environ.get("MLFLOW_EXPERIMENT_ID", None)
    run_id = os.environ["MLFLOW_RUN_ID"]
    host_url = "https://{0}".format(parsed_url.netloc)

    auth = AzureMLTokenAuthentication.create(
        azureml_access_token=token,
        expiry_time=None,
        host=host_url,
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        workspace_name=None,
        experiment_name=experiment_name,
        experiment_id=experiment_id,
        run_id=run_id,
    )

    # This adds dependecny on these 2 env vars
    # AZUREML_SERVICE_ENDPOINT, AZUREML_WORKSPACE_ID
    # and they are set for remote runs by backend service
    # Needs this so that discovery url is set correctly for Private Link (PL) and non PL workspace
    # Now since we are using tracking uri and using that for host url it should handle PL workspace.
    cloud = _get_cloud_or_default()
    service_context = RegistryServiceContext(
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        auth=auth,
        host_url=host_url,
        cloud=cloud,
    )

    return service_context


def get_service_context_from_registry_url_default_auth(parsed_url):
    """Create a Service Context object out of a parsed URL."""
    logger.debug(
        "Creating a Service Context object from the tracking uri using default authentication"
        " : InteractiveLoginAuthentication"
    )
    parsed_path = tracking_uri_decomp(parsed_url.path, True)
    subscription_id = parsed_path[_SUB_ID]
    resource_group_name = parsed_path[_RES_GRP]
    registry_name = parsed_path.get(_REG_NAME, None)

    queries = dict(parse.parse_qsl(parsed_url.query))

    if _AUTH_HEAD in queries or _AUTH_TYPE in queries:
        logger.warning(
            "Use of {}, {} query parameters in tracking URI is deprecated."
            " InteractiveLoginAuthentication will be used by default."
            " Please use 'azureml.core.workspace.Workspace.get_mlflow_tracking_uri'"
            " to use authentication associated with workspace".format(
                _AUTH_TYPE, _AUTH_HEAD
            )
        )

    """
    Using InteractiveLoginAuthentication poses an issue if customer uses a subscription not belonging to its default
    tenant. In that case customer needs to provide tenantId as a param to InteractiveLoginAuthentication which is
    not possible currently in this flow. In this case customer needs to create workspace object with auth param

        from azureml.core.authentication import InteractiveLoginAuthentication

        interactive_auth = InteractiveLoginAuthentication(tenant_id="my-tenant-id")

        ws = Workspace(subscription_id="my-subscription-id",
                       resource_group="my-ml-rg",
                       workspace_name="my-ml-workspace",
                       auth=interactive_auth)

        ws.get_mlflow_tracking_uri()
    """
    cloud = _get_cloud_or_default()
    tenant_id = os.getenv("AZURE_TENANT_ID", None)
    default_auth = DefaultAzureCredential(authority=cloud._get_authority())
    auth = ChainedTokenCredential(
        *default_auth.credentials,
        _ArcadiaAuthentication(),
        _DatabricksClusterAuthentication(),
        InteractiveBrowserCredential(
            authority=cloud._get_authority(), tenant_id=tenant_id
        ),
        DeviceCodeCredential(
            authority=cloud._get_authority(), tenant_id=tenant_id
        )
    )

    service_context = RegistryServiceContext(
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        registry_name=registry_name,
        auth=auth,
        host_url="https://" + parsed_url.netloc,
        cloud=cloud,
    )

    return service_context


def convertToServiceContext(subscription_id, workspace_name, resource_group, auth, host_url):
    return ServiceContext(
        subscription_id=subscription_id,
        workspace_name=workspace_name,
        resource_group_name=resource_group,
        auth=auth,
        host_url=host_url
    )
