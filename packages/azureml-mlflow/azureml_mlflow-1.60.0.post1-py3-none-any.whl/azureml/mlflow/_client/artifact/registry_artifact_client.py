# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Access run artifacts extension client."""
import logging
import os
import re

from azureml.mlflow._client.artifact.base_artifact_client import (
    BaseArtifactsClient,
)
from azureml.mlflow._client.artifact.registry_client import (
    get_registry_client,
    get_storage_details_for_registry_assets,
    _get_next_version_from_container,
    get_asset_body_for_registry_storage,
    get_sas_uri_for_registry_asset,
)
from azureml.mlflow._client.artifact._utils.blob_artifact_util import (
    BlobStorageClient,
)

module_logger = logging.getLogger(__name__)

ASSET_TYPE = "models"
ARTIFACTS_BATCH_SIZE_ENV_VAR = "AZUREML_ARTIFACT_BATCH_SIZE"
ARTIFACTS_BATCH_SIZE_DEFAULT = 50
AZUREML_ARTIFACTS_TIMEOUT_ENV_VAR = "AZUREML_ARTIFACTS_DEFAULT_TIMEOUT"
AZUREML_ARTIFACTS_MIN_TIMEOUT = 300
REMOTE_PATH_REG = (
    r".*/models/([^/]+)/versions/([^/]+)/storage/([^/]+)/paths/([^/]+)/(.*)"
)


class RegistryArtifactClient(BaseArtifactsClient):
    """Registry Artifact Repository client class."""

    def __init__(self, service_context, path):
        self._client, self._rg_name, self._sub_id = get_registry_client(
            registry_name=service_context.registry_name,
            auth=service_context.auth,
        )
        self._reg_name = service_context.registry_name
        self.cloud = service_context.cloud
        self.path = path

    def download_artifact(self, remote_path, local_path):
        """download artifact"""
        remote_decomp = parse_remote_path(remote_path)
        endpoint = self.cloud._get_storage_endpoint()
        model_uri = (
            f"https://{remote_decomp.get('storage')}.blob.{endpoint}/"
            f"{remote_decomp.get('container')}/{remote_decomp.get('path')}"
        )

        try:
            sas_uri, auth_type = get_storage_details_for_registry_assets(
                service_client=self._client,
                asset_name=remote_decomp.get("model_name"),
                asset_version=remote_decomp.get("model_version"),
                reg_name=self._reg_name,
                asset_type=ASSET_TYPE,
                rg_name=self._rg_name,
                uri=model_uri,
            )

            if auth_type != "SAS":
                raise Exception(
                    "Only SAS auth is supported for downloading artifacts from registry"
                )
        except Exception as ex:
            raise Exception(
                "Failed to get storage details for registry assets"
            ) from ex

        blob_client = BlobStorageClient(
            credential=None, container_name=None, account_url=sas_uri
        )

        blob_client.download(
            starts_with=remote_decomp.get("path"), destination=local_path
        )

    def upload_dir(self, local_dir, model_name):
        local_dir = os.path.abspath(local_dir)

        model_version = _get_next_version_from_container(
            name=model_name,
            container_operation=self._client.model_containers,
            resource_group_name=self._rg_name,
            workspace_name=None,
            registry_name=self._reg_name,
        )

        sas_uri, blob_uri = get_sas_uri_for_registry_asset(
            service_client=self._client,
            name=model_name,
            version=model_version,
            resource_group=self._rg_name,
            registry=self._reg_name,
            body=get_asset_body_for_registry_storage(
                self._reg_name, "models", model_name, model_version
            ),
        )

        blob_client = BlobStorageClient(
            credential=None, container_name=None, account_url=sas_uri
        )
        artifact_info = blob_client.upload(
            local_dir, model_name, model_version
        )

        return blob_uri + "/" + artifact_info.get("container path")

    def get_file_paths(self):
        return []


def parse_remote_path(path: str):
    mo = re.compile(REMOTE_PATH_REG).match(path)

    ret = {}
    ret["model_name"] = mo.group(1)
    ret["model_version"] = mo.group(2)
    ret["storage"] = mo.group(3)
    ret["container"] = mo.group(4)
    ret["path"] = mo.group(5)

    return ret
