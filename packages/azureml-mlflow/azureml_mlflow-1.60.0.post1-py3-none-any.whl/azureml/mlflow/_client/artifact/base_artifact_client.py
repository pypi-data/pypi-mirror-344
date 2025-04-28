# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Access base run artifacts client"""
import logging
import os

from azureml.mlflow._common.async_utils.task_queue import TaskQueue

module_logger = logging.getLogger(__name__)

ARTIFACTS_BATCH_SIZE_ENV_VAR = "AZUREML_ARTIFACT_BATCH_SIZE"
ARTIFACTS_BATCH_SIZE_DEFAULT = 50
AZUREML_ARTIFACTS_TIMEOUT_ENV_VAR = "AZUREML_ARTIFACTS_DEFAULT_TIMEOUT"
AZUREML_ARTIFACTS_MIN_TIMEOUT = 300


class BaseArtifactsClient(object):

    def _upload_files(self, local_paths, remote_paths):

        batch_size = int(os.environ.get(ARTIFACTS_BATCH_SIZE_ENV_VAR, ARTIFACTS_BATCH_SIZE_DEFAULT))
        results = []
        timeout_seconds = float(
            os.environ.get(AZUREML_ARTIFACTS_TIMEOUT_ENV_VAR, AZUREML_ARTIFACTS_MIN_TIMEOUT))

        for i in range(0, len(local_paths), batch_size):
            with TaskQueue(_ident="upload_files", flush_timeout_seconds=timeout_seconds) as task_queue:
                batch_local_paths = local_paths[i:i + batch_size]
                batch_remote_paths = remote_paths[i:i + batch_size]

                # Make batch request to create empty artifacts
                empty_artifact_content = self._create_empty_artifacts(paths=batch_remote_paths)

                for local_path, remote_path in zip(batch_local_paths, batch_remote_paths):
                    task = task_queue.add(
                        self.upload_artifact, local_path, remote_path,
                        empty_artifact_content.artifact_content_information[remote_path])
                    results.append(task)

        return map(lambda result: result.wait(), results)
