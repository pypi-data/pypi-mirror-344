# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains loaders for integrating Azure Machine Learning with MLflow."""

import logging


logger = logging.getLogger(__name__)


def azureml_artifacts_builder(artifact_uri=None):
    """Create an artifact repository for AzureMLflow.

    :param artifact_uri: A URI where artifacts are stored.
    :type artifact_uri: str
    """
    from azureml.mlflow._store.artifact.artifact_repo import AzureMLflowArtifactRepository
    return AzureMLflowArtifactRepository(artifact_uri)


def azureml_store_builder(store_uri, artifact_uri=None):
    """Create or return a store to read and record metrics and artifacts in Azure via MLflow.

    :param store_uri: A URI to the store.
    :type store_uri: str
    :param artifact_uri: A URI where artifacts are stored.
    :type artifact_uri: str
    """
    from mlflow.exceptions import MlflowException
    from ._internal.service_context_loader import _AzureMLServiceContextLoader
    from azureml.mlflow._store.tracking.store import AzureMLRestStore
    if not store_uri:
        raise MlflowException('Store URI provided to azureml_tracking_store_build cannot be None or empty.')

    service_context = _AzureMLServiceContextLoader.load_service_context(store_uri)
    return AzureMLRestStore(service_context)


def azureml_model_registry_builder(store_uri):
    """Create or return a registry for models in Azure via MLflow.

    :param store_uri: A URI to the registry.
    :type store_uri: str
    """
    from mlflow.exceptions import MlflowException
    from ._internal.service_context_loader import _AzureMLServiceContextLoader
    from azureml.mlflow._store.model_registry.model_registry import AzureMLflowModelRegistry

    if not store_uri:
        raise MlflowException('Store URI provided to azureml_model_registry_builder cannot be None or empty.')
    service_context = _AzureMLServiceContextLoader.load_service_context(store_uri)
    return AzureMLflowModelRegistry(service_context)


def azureml_project_run_builder():
    """Create an empty AzureMLProjectBackend object for MLflow Projects to access run function."""
    from ._internal.projects import AzureMLProjectBackend
    return AzureMLProjectBackend()


def azureml_request_header_provider():
    """Create or return a request header provider in Azure via MLflow."""
    from azureml.mlflow._tracking.request_header import AzureMLRequestHeaderProvider
    return AzureMLRequestHeaderProvider()
