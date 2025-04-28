# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowModelRegistry** provides a class to manage MLFlow models in Azure."""

import logging
import os
import uuid
from datetime import datetime

from functools import wraps

from mlflow.store.model_registry.rest_store import RestStore
from azureml.mlflow._store.azureml_reststore import AzureMLAbstractRestStore

logger = logging.getLogger(__name__)


class AzureMLflowModelRegistry(AzureMLAbstractRestStore, RestStore):
    """
    Client for a remote model registry accessed via REST API calls.

    :param service_context: Service context for the AzureML workspace
    :type service_context: azureml._restclient.service_context.ServiceContext
    """

    def __init__(self, service_context, host_creds=None, **kwargs):
        """
        Construct an AzureMLflowModelRegistry object.

        :param service_context: Service context for the AzureML workspace
        :type service_context: azureml._restclient.service_context.ServiceContext
        """
        logger.debug("Initializing the AzureMLflowModelRegistry")
        self.set_is_registry = hasattr(service_context, "registry_name")
        AzureMLAbstractRestStore.__init__(self, service_context, host_creds)
        RestStore.__init__(self, self.get_host_creds, **kwargs)

    @wraps(RestStore.create_model_version)
    def create_model_version(self, name, source, *args, **kwargs):
        if source.startswith("file://"):
            if len(args) > 0 and args[0] is not None:
                run_id = args[0]
                raise ValueError(
                    '"run_id={}" provided when registering local file.'.format(
                        run_id
                    )
                )
            source = source.split("file://")[1]
            if not os.path.isdir(source) or not os.path.exists(
                os.path.join(source, "MLmodel")
            ):
                raise ValueError(
                    "Model source must be a directory containing an mlflow MLmodel, as is produced "
                    "by an mlflow save_model function."
                )
            # Source is always a directory for MLModel as validated in above check
            if self.set_is_registry:
                source = self._create_registry_artifacts(source, name)
            else:
                artifacts_path = self._create_artifacts(source, name)
                source = "azureml://artifacts/{}".format(artifacts_path)

        return super(AzureMLflowModelRegistry, self).create_model_version(
            name, source, *args, **kwargs
        )

    def _create_artifacts(self, source, name):
        from azureml.mlflow._client.artifact.local_artifact_client import (
            LocalArtifactClient,
        )

        # Artifact ID components.
        origin = "LocalUpload"
        container = "{}-{}".format(
            datetime.now().strftime("%y%m%dT%H%M%S"), str(uuid.uuid4())[:8]
        )
        model_base_name = os.path.basename(os.path.abspath(source))

        artifacts_client = LocalArtifactClient(
            self.service_context, origin, container, None
        )

        artifacts_client.upload_dir(source, model_base_name)

        artifacts_path = "{}/{}/{}".format(origin, container, model_base_name)
        return artifacts_path

    def _create_registry_artifacts(self, source, name):
        from azureml.mlflow._client.artifact.registry_artifact_client import (
            RegistryArtifactClient,
        )

        artifacts_client = RegistryArtifactClient(self.service_context, None)
        container_uri = artifacts_client.upload_dir(source, name)
        return container_uri
