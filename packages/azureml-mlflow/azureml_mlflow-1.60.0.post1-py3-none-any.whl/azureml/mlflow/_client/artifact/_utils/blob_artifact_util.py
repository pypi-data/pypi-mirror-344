# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import re
import os
import time
from typing import Optional, Dict
import uuid
import azure.core
from azure.storage.blob import (
    BlobClient,
    BlobServiceClient,
    ContainerClient,
    BlobProperties,
)
from azureml.mlflow._client.artifact._utils.file_utils import (
    makedirs_for_file_path,
)
from azureml.mlflow._client.artifact._utils.asset_utils import (
    upload_directory,
    _build_metadata_dict,
    MAX_CONCURRENCY,
)
from azureml.mlflow._common._cloud.cloud import _get_cloud_or_default
from pathlib import Path, PurePosixPath
import requests.exceptions

module_logger = logging.getLogger(__name__)

ARTIFACT_ORIGIN = "LocalUpload"
LEGACY_ARTIFACT_DIRECTORY = "az-ml-artifacts"
BLOB_DATASTORE_IS_HDI_FOLDER_KEY = "hdi_isfolder"
FILE_SIZE_WARNING = (
    "Your file exceeds 100 MB. If you experience low speeds, latency, or broken connections, we recommend using "  # noqa: E501
    "the AzCopyv10 tool for this file transfer.\n\nExample: azcopy copy '{source}' '{destination}' "  # noqa: E501
    "\n\nSee https://docs.microsoft.com/azure/storage/common/storage-use-azcopy-v10 for more information."  # noqa: E501
)
STORAGE_URI_REGEX = r"(https:\/\/([a-zA-Z0-9@:%_\\\-+~#?&=]+)[a-zA-Z0-9@:%._\\\-+~#?&=]+\.?)\/([a-zA-Z0-9@:%._\\\-+~#?&=]+)\/(.*)"  # noqa: E501


class BlobStorageClient:
    def __init__(
        self,
        credential: str,
        account_url: str,
        container_name: Optional[str] = None,
    ):
        self.account_name = account_url.split(".")[0].split("://")[1]
        self.service_client = BlobServiceClient(
            account_url=account_url, credential=credential
        )
        self.upload_to_root_container = None
        if container_name:
            self.container_client = self.service_client.get_container_client(
                container=container_name
            )
        else:
            self.container_client = ContainerClient.from_container_url(
                account_url
            )
            self.upload_to_root_container = True
        self.container = self.container_client.container_name
        self.total_file_count = 1
        self.uploaded_file_count = 0
        self.overwrite = False
        self.indicator_file = None
        self.legacy = False
        self.name = None
        self.version = None

    def download(
        self,
        starts_with: str,
        destination: str,
        max_concurrency: int = MAX_CONCURRENCY,
    ) -> None:
        """Downloads all blobs inside a specified container to the destination folder.

        :param starts_with: Indicates the blob name starts with to search.
        :param destination: Indicates path to download in local
        :param max_concurrency: Indicates concurrent connections to download a blob.
        """
        try:
            my_list = list(
                self.container_client.list_blobs(
                    name_starts_with=starts_with, include="metadata"
                )
            )
            download_size_in_mb = 0
            for item in my_list:
                blob_name = (
                    item.name[len(starts_with) :].lstrip("/")
                    or Path(starts_with).name
                )
                target_path = Path(destination, blob_name).resolve()

                if _blob_is_hdi_folder(item):
                    target_path.mkdir(parents=True, exist_ok=True)
                    continue

                blob_content = self.container_client.download_blob(item)

                # check if total size of download has exceeded 100 MB
                # make sure proper cloud endpoint is used
                # cloud = _get_cloud_details()
                # cloud_endpoint = cloud["storage_endpoint"]
                full_storage_url = f"https://{self.account_name}.blob.cloud_endpoint/{self.container}/{starts_with}"
                download_size_in_mb += blob_content.size / 10**6
                if download_size_in_mb > 100:
                    module_logger.warning(
                        FILE_SIZE_WARNING.format(
                            source=full_storage_url, destination=destination
                        )
                    )

                blob_content = blob_content.content_as_bytes(max_concurrency)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with target_path.open("wb") as file:
                    file.write(blob_content)
        except OSError as ex:
            raise ex
        except Exception as e:
            msg = "Saving blob with prefix {} was unsuccessful. exception={}"
            raise Exception(
                message=msg.format(starts_with, e),
            )

    def upload(
        self,
        source: str,
        name: str,
        version: str,
        asset_hash: Optional[str] = None,
        show_progress: bool = True,
    ) -> Dict[str, str]:
        """Upload a file or directory to a path inside the container."""
        if name and version is None:
            version = str(
                uuid.uuid4()
            )  # placeholder for auto-increment artifacts

        asset_id = (
            generate_asset_id(asset_hash, include_directory=True)
            if not self.upload_to_root_container
            else ""
        )
        source_name = Path(source).name
        dest = str(PurePosixPath(asset_id, source_name))

        try:
            self.indicator_file = dest
            container_path = upload_directory(
                storage_client=self,
                source=source,
                dest=dest,
                msg="Uploading...",
                show_progress=show_progress,
            )

            # upload must be completed before we try to generate confirmation file
            while self.uploaded_file_count < self.total_file_count:
                time.sleep(0.5)
            self._set_confirmation_metadata(name, version)
        except Exception as ex:  # noqa: F841
            name = self.name
            version = self.version
            if self.legacy:
                dest = dest.replace(ARTIFACT_ORIGIN, LEGACY_ARTIFACT_DIRECTORY)

        artifact_info = {
            "remote path": dest,
            "name": name,
            "version": version,
            "container path": container_path,
            "indicator file": self.indicator_file,
        }

        return artifact_info

    def _set_confirmation_metadata(self, name: str, version: str) -> None:
        blob_client = self.container_client.get_blob_client(
            blob=self.indicator_file
        )
        metadata_dict = _build_metadata_dict(name, version)
        blob_client.set_blob_metadata(metadata_dict)


def is_source_uri_matches_storage_blob(source_uri, **kwargs):
    """
    Regex matches the source_uri with azure storage blob url
    :param source_uri: The name of the file to normalize (may or may not contain the file extension).
    :type source_uri: str
    :return: true if regex matches successfully
    :rtype: bool
    """
    cloud = kwargs.pop("cloud", None)
    storage_endpoint = (
        cloud.suffixes.storage_endpoint
        if cloud
        else _get_cloud_or_default().suffixes.storage_endpoint
    )
    pattern = "^{}(.*){}(.*){}(.*){}(.*)".format(
        re.escape("https://"),
        re.escape(".blob.{}/".format(storage_endpoint)),
        re.escape("/"),
        re.escape("?"),
    )
    return re.match(pattern, source_uri) is not None


def download_file(source_uri, path=None, **kwargs):
    module_logger.debug("downloading file to {path}".format(path=path))
    cloud = kwargs.pop("cloud", None)

    if path is None:
        module_logger.debug(
            "Output file path is {}, the file was not downloaded.".format(path)
        )
        return

    if is_source_uri_matches_storage_blob(source_uri, cloud=cloud):
        blob_client = BlobClient.from_blob_url(source_uri)

        makedirs_for_file_path(path)

        if not os.path.isdir(path):
            with open(path, "wb") as file:
                blob_client.download_blob().readinto(file)
        else:
            module_logger.warning(f"path {path} is a directory")


def upload_blob_from_stream(stream, artifact_uri):
    blob_client = BlobClient.from_blob_url(artifact_uri)
    module_logger.debug(f"Uploading stream to container {blob_client.container_name}")

    try:
        blob_client.upload_blob(stream)
    except azure.core.exceptions.ServiceResponseError as e:
        inner = e.inner_exception
        if not isinstance(inner, requests.exceptions.ConnectionError) and isinstance(inner.args[1], TimeoutError):
            raise e

        module_logger.debug("Upload timed out. Trying again with smaller request chunk size.")

        # Blob client defaults to 64MB chunks for upload requests, which can sometimes timeout in different
        # network conditions. Using a smaller chunk size can resolve this.
        blob_client = BlobClient.from_blob_url(artifact_uri, max_single_put_size=32 * 1024 * 1024)
        blob_client.upload_blob(stream)


def _blob_is_hdi_folder(blob: "BlobProperties") -> bool:
    """Checks if a given blob actually represents a folder.

    Blob datastores do not natively have any conception of a folder. Instead,
    empty blobs with the same name as a "folder" can have additional metadata
    specifying that it is actually a folder.

    :param BlobProperties blob: Blob to check
    :return bool: True if blob represents a folder, False otherwise
    """

    # Metadata isn't always a populated field, and may need to be explicitly
    # requested from whatever function generates the blobproperties object
    #
    # e.g self.container_client.list_blobs(..., include='metadata')
    return bool(
        blob.metadata
        and blob.metadata.get(BLOB_DATASTORE_IS_HDI_FOLDER_KEY, None)
    )


def generate_asset_id(asset_hash: str, include_directory=True) -> str:
    asset_id = asset_hash or str(uuid.uuid4())
    if include_directory:
        asset_id = "/".join((ARTIFACT_ORIGIN, asset_id))
    return asset_id
