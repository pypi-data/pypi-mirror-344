# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLTrackingStore** provides a base class for MLFlow RestStore related handling."""

import logging
from abc import ABCMeta

from mlflow.utils.rest_utils import MlflowHostCreds

logger = logging.getLogger(__name__)


class AzureMLAbstractRestStore(object):
    """
    Client for a remote rest server accessed via REST API calls.

    :param service_context: Service context for the AzureML workspace
    :type service_context: azureml._restclient.service_context.ServiceContext
    """

    __metaclass__ = ABCMeta

    def __init__(self, service_context, host_creds=None):
        """
        Construct an AzureMLRestStore object.

        :param service_context: Service context for the AzureML workspace
        :type service_context: azureml._restclient.service_context.ServiceContext
        """
        self.service_context = service_context
        self.get_host_creds = (
            host_creds if host_creds is not None else self.get_host_credentials
        )
        # self.workspace_client = WorkspaceClient(service_context)

    def get_host_credentials(self):
        """
        Construct a MlflowHostCreds to be used for obtaining fresh credentials and the host url.

        :return: The host and credential for rest calls.
        :rtype: mlflow.utils.rest_utils.MlflowHostCreds
        """
        import mlflow
        from packaging import version

        mlflow_version = version.parse(mlflow.__version__)
        api_version = None
        if mlflow_version >= version.parse(
            "2.0.0"
        ) and mlflow_version < version.parse("3.0.0"):
            api_version = "/mlflow/v2.0"
        elif mlflow_version >= version.parse(
            "1.0.0"
        ) and mlflow_version < version.parse("2.0.0"):
            api_version = "/mlflow/v1.0"
        # Set this to latest mlflow version for mlflow dev installs
        else:
            api_version = "/mlflow/v2.0"

        url_base = (
            self.service_context.host_url
            + api_version
            + self.service_context._get_scope()
        )

        auth_header = self.service_context.auth.get_token(
            self.service_context.cloud._get_default_scope()
        )
        # auth_header = self.service_context.auth.get_token()
        return MlflowHostCreds(url_base, token=auth_header.token)
