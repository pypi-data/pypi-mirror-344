# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import urllib3
from azure.core.exceptions import ServiceResponseError, ServiceRequestError
from azure.core.pipeline.policies import HTTPPolicy
from requests.exceptions import ReadTimeout, ConnectTimeout
from azureml.mlflow._client.constants import ClientEnvVars

_LOGGER = logging.getLogger(__name__)


class HandleTimeoutPolicy(HTTPPolicy):
    """A redirect policy.

    An AML Policy to handle Service Timeout issue it covers Service Connection Timeout and
    Read Timeout

    """

    def send(self, request):
        """Checks for requests Timeout exception and provide more details on how to resolve it.
        """
        try:
            response = self.next.send(request)
        except (ServiceResponseError, ServiceRequestError) as ex:
            if isinstance(ex.inner_exception, (ReadTimeout, ConnectTimeout, urllib3.exceptions.ConnectTimeoutError)):
                message = ex.message + \
                    "Request failed with timeout exception. To increase timeout set the " \
                    "environment variable {} to larger value. ".format(ClientEnvVars.AZUREML_HTTP_REQUEST_TIMEOUT)
                raise ex.__class__(message, error=ex.inner_exception)
            raise ex

        return response
