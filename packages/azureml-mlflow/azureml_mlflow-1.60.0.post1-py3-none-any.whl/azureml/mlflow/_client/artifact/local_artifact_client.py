# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Access run artifacts extension client."""
import logging
import os
import posixpath

from azure.core.exceptions import HttpResponseError
from azureml.mlflow._client.artifact.base_artifact_client import BaseArtifactsClient
from azureml.mlflow._restclient.artifact._azure_machine_learning_workspaces import \
    AzureMachineLearningWorkspaces as RestArtifactsClient
# from azureml._restclient.artifacts_client import ArtifactsClient as RestArtifactsClient
from azureml.mlflow._client.artifact._utils.blob_artifact_util import download_file, upload_blob_from_stream
from azureml.mlflow._restclient.artifact.models import ArtifactPathList, ArtifactPath

module_logger = logging.getLogger(__name__)


class LocalArtifactClient(BaseArtifactsClient):
    """Local Artifact Repository client class."""

    def __init__(self, service_context, origin, container, path):
        self._client = RestArtifactsClient(
            credential=service_context.auth,
            base_url=service_context.host_url,
            credential_scopes=[service_context.cloud._get_default_scope()],
            logging_enable=os.environ.get("AZUREML_LOG_NETWORK_TRACES", False),
        )
        self._service_context = service_context
        self._origin = origin
        self._container = container
        self.path = path

    def download_artifact(self, remote_path, local_path):
        """download artifact"""
        try:
            content_info = self._client.artifacts.get_content_information(
                subscription_id=self._service_context.subscription_id,
                resource_group_name=self._service_context.resource_group_name,
                workspace_name=self._service_context.workspace_name,
                origin=self._origin,
                container=self._container,
                path=remote_path
            )

            if not content_info:
                raise Exception("Cannot find the artifact '{0}' in container '{1}'".format(
                    remote_path, self._container))
            uri = content_info.content_uri
        except HttpResponseError as operation_error:
            if operation_error.response.status_code == 404:
                existing_files = self.get_file_paths()
                raise Exception("File with path {0} was not found,\n"
                                "available files include: "
                                "{1}.".format(remote_path, ",".join(existing_files)))
            else:
                raise

        download_file(uri, local_path)

    def upload_artifact(self, local_path, remote_path, empty_artifact_content_info):
        module_logger.debug(
            "Uploading file {0} to {1} of size {2}".format(local_path, remote_path, os.stat(local_path).st_size))
        with open(local_path, "rb") as file:
            upload_blob_from_stream(stream=file, artifact_uri=empty_artifact_content_info.content_uri)

    def upload_file(self, local_path, artifact_path):
        empty_artifact_res = self._create_empty_artifacts(
            paths=artifact_path, origin=self._origin, container=self._container)
        self.upload_artifact(
            local_path=local_path,
            remote_path=artifact_path,
            empty_artifact_content_info=empty_artifact_res.artifact_content_information[artifact_path]
        )

        return empty_artifact_res

    def upload_dir(self, local_dir, artifact_path):
        remote_paths = []
        local_paths = []

        local_dir = os.path.abspath(local_dir)

        for (root, _, filenames) in os.walk(local_dir):
            upload_path = artifact_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                upload_path = posixpath.join(artifact_path, rel_path)
            for f in filenames:
                remote_file_path = posixpath.join(upload_path, f)
                remote_paths.append(remote_file_path)
                local_file_path = os.path.join(root, f)
                local_paths.append(local_file_path)

        result = self._upload_files(
            local_paths=local_paths, remote_paths=remote_paths)
        return result

    def get_file_paths(self):
        """list artifact info"""
        artifacts = self._client.artifacts.list_in_container(
            subscription_id=self._service_context.subscription_id,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            origin=self._origin,
            container=self._container
        )

        return map(lambda artifact_dto: artifact_dto.path, artifacts)

    def _upload_artifact_from_stream(self, stream, name, origin, container):
        empty_artifact_res = self._create_empty_artifacts(paths=name, origin=origin, container=container)
        content_information = empty_artifact_res.artifact_content_information[name]
        upload_blob_from_stream(stream=stream, artifact_uri=content_information.content_uri)
        return empty_artifact_res

    def _create_empty_artifacts(self, paths, origin=None, container=None):
        if isinstance(paths, str):
            paths = [paths]

        artifacts = [ArtifactPath(path=path) for path in paths]

        return self._client.artifacts.batch_create_empty_artifacts(
            subscription_id=self._service_context.subscription_id,
            resource_group_name=self._service_context.resource_group_name,
            workspace_name=self._service_context.workspace_name,
            origin=origin if origin else self._origin,
            container=container if container else self._container,
            body=ArtifactPathList(paths=artifacts)
        )
