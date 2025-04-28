# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""mlflow helper functions."""

import logging
import os
import re
from pathlib import Path

from azureml.mlflow._common._authentication.azureml_token_authentication import (
    AzureMLTokenAuthentication,
)
from azureml.mlflow._common._cloud.cloud import _get_cloud_or_default
from azure.identity import (
    DefaultAzureCredential,
    ChainedTokenCredential,
    DeviceCodeCredential,
    InteractiveBrowserCredential,
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
from azureml.mlflow._client.artifact.registry_artifact_client import (
    RegistryArtifactClient,
)
from azureml.mlflow._internal.utils import (
    ServiceContext,
    RegistryServiceContext,
)

from six.moves.urllib import parse

_IS_REMOTE = "is-remote"
_REGION = "region"
_SUB_ID = "sub-id"
_RES_GRP = "res-grp"
_WS_NAME = "ws-name"
_EXP_NAME = "experiment"
_RUN_ID = "runid"
_ORIGIN = "origin"
_CONTAINER = "container"

_REG_NAME = "reg-name"
_MODEL_NAME = "model-name"
_MODEL_VERSION = "model-version"
_STORAGE = "storage"
_PATH = "path"
_PATH_PREFIX = "path-prefix"

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

_ARTIFACT_URI_REGEX = (
    _WORKSPACE_INFO_REGEX + r"/experiments/([^/]+)/runs/([^/]+)(/artifacts.*)?"
)

_REGISTRY_URI_REGEX = (
    r"azureml://(.+)/mlflow/v2.0/registries/(.+)/models/(.+)"
    r"/versions/(.+)/storage/(.+)/paths/(.+)/(.+)"
)

VERSION_WARNING = (
    "Could not import {}. Please upgrade to Mlflow 1.4.0 or higher."
)


def tracking_uri_decomp(tracking_uri):
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

    pattern = re.compile(_WORKSPACE_INFO_REGEX)
    mo = pattern.match(parsed_url_path)

    ret = {}
    ret[_SUB_ID] = mo.group(1)
    ret[_RES_GRP] = mo.group(2)
    ret[_WS_NAME] = mo.group(3)
    logger.info(
        "Tracking uri {} has sub id {}, resource group {}, and workspace {}".format(
            tracking_uri, ret[_SUB_ID], ret[_RES_GRP], ret[_WS_NAME]
        )
    )

    return ret


def get_run_info(parsed_url_path):
    """
    Parses artifact uri into a dictionary.

    Artifact uri contains experiment and run info.

    :param parsed_url_path: The tracking_uri to parse.
    :type parsed_url_path: str
    """
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
        parsed_artifact_uri = parsed_url_path[1:].split("/", 3)
        artifact_info_dict[_ORIGIN] = parsed_artifact_uri[0]
        artifact_info_dict[_CONTAINER] = parsed_artifact_uri[1]
        artifact_path = Path(*parsed_artifact_uri[2:]).as_posix()
        artifact_info_dict[_ARTIFACT_PATH] = (
            artifact_path
            if not artifact_path.startswith("/")
            else artifact_path[1:]
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
    workspace_name = parsed_artifacts_path[_WS_NAME]
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
        workspace_name=workspace_name,
    )

    return ServiceContext(
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
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
    parsed_path = tracking_uri_decomp(parsed_url.path)
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

    auth = DefaultAzureCredential(
        exclude_interactive_browser_credential=False,
        exclude_managed_identity_credential=True,
        exclude_environment_credential=True,
    )

    service_context = ServiceContext(
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
        auth=auth,
        host_url="https://" + parsed_url.netloc,
    )
    # TODO Create host url from tracking URL select scheme based on dev mode or no

    return service_context


def get_service_context_from_tracking_url_mlflow_env_vars(parsed_url):
    parsed_path = tracking_uri_decomp(parsed_url.path)
    subscription_id = parsed_path[_SUB_ID]
    resource_group_name = parsed_path[_RES_GRP]
    workspace_name = parsed_path[_WS_NAME]
    token = os.environ["MLFLOW_TRACKING_TOKEN"]
    experiment_name = os.environ.get("MLFLOW_EXPERIMENT_NAME", None)
    experiment_id = os.environ.get("MLFLOW_EXPERIMENT_ID", None)
    run_id = os.environ["MLFLOW_RUN_ID"]
    host_url = "https://{0}".format(parsed_url.netloc)

    auth = AzureMLTokenAuthentication(
        token,
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
    service_context = ServiceContext(
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        workspace_name=workspace_name,
        auth=auth,
        host_url=host_url,
    )
    # TODO Create host url from tracking URL select scheme based on dev mode or no

    return service_context

    # return ws.service_context


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


def get_registry_uri_decomp(parsed_artifacts_url):
    mo = re.compile(_REGISTRY_URI_REGEX).match(parsed_artifacts_url)

    ret = {}
    ret[_REG_NAME] = mo.group(2)
    ret[_MODEL_NAME] = mo.group(3)
    ret[_MODEL_VERSION] = mo.group(4)
    ret[_STORAGE] = mo.group(5)
    ret[_PATH] = mo.group(6)
    ret[_PATH_PREFIX] = mo.group(7)

    return ret


def get_registry_service_context(parsed_artifact_path):
    registry_name = parsed_artifact_path[_REG_NAME]
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
        subscription_id=None,
        resource_group_name=None,
        host_url=None,
        auth=auth,
        registry_name=registry_name,
        cloud=cloud,
    )

    return service_context


def get_artifact_repository_client(artifact_uri):
    logger.debug("Initializing the AzureMLflowArtifactRepository")
    parsed_artifacts_url = parse.urlparse(artifact_uri)

    pattern = re.compile(_REGISTRY_URI_REGEX)
    if pattern.search(artifact_uri):
        registry_dict = get_registry_uri_decomp(artifact_uri)
        reg_service_context = get_registry_service_context(registry_dict)
        artifacts_client = RegistryArtifactClient(
            reg_service_context, parsed_artifacts_url.path[1:]
        )
        return artifacts_client

    service_context = get_service_context(parsed_artifacts_url)
    parsed_artifacts_path = artifact_uri_decomp(artifact_uri)

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
            service_context, experiment_name, run_id, path
        )
    else:
        origin = parsed_artifacts_path[_ORIGIN]
        container = parsed_artifacts_path[_CONTAINER]
        path = parsed_artifacts_path[_ARTIFACT_PATH]
        artifacts_client = LocalArtifactClient(
            service_context, origin, container, path
        )
    return artifacts_client
