# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


from mlflow.tracking.request_header.abstract_request_header_provider import RequestHeaderProvider
from azureml.mlflow import __version__

_USER_AGENT = "User-Agent"
_DEFAULT_HEADERS = {_USER_AGENT: "azureml-mlflow/%s" % __version__}


class AzureMLRequestHeaderProvider(RequestHeaderProvider):
    """
    Provides request headers for Azure Machine Learning
    """

    def in_context(self):
        return True

    def request_headers(self):
        return dict(**_DEFAULT_HEADERS)
