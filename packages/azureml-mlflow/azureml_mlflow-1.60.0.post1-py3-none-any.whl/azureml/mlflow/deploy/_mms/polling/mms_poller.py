# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import sys
from datetime import datetime

from azure.core.exceptions import HttpResponseError
from azure.core.polling import PollingMethod
from azure.core.polling.base_polling import OperationResourcePolling, BadResponse, OperationFailed, BadStatus
from azureml.mlflow.deploy._mms.polling.base_polling import _raise_if_bad_http_status_and_method, _is_empty,\
    _finished, get_retry_after, _as_json, _failed, _format_error_response, _succeeded
from dateutil import tz


class MMSPolling(PollingMethod):

    def __init__(
            self,
            timeout=30,
            lro_algorithms=None,
            lro_options=None,
            path_format_arguments=None,
            show_output=False,
            **operation_config
    ):
        self._lro_algorithms = lro_algorithms or [
            OperationResourcePolling()
        ]

        self._timeout = timeout
        self._client = None  # Will hold the Pipelineclient
        self._operation = None  # Will hold an instance of LongRunningOperation
        self._initial_response = None  # Will hold the initial response
        self._pipeline_response = None  # Will hold latest received response
        self._deserialization_callback = None  # Will hold the deserialization callback
        self._operation_config = operation_config
        self._lro_options = lro_options
        self._path_format_arguments = path_format_arguments
        self._status = None
        self._last_status = None
        self._show_output = show_output
        self._streaming_log_offset = 0

    def initialize(self, client, initial_response, deserialization_callback):
        """Set the initial status of this LRO.

                :param initial_response: The initial response of the poller
                :raises: HttpResponseError if initial status is incorrect LRO state
                """
        self._client = client
        self._pipeline_response = self._initial_response = initial_response
        self._deserialization_callback = deserialization_callback

        for operation in self._lro_algorithms:
            if operation.can_poll(initial_response):
                self._operation = operation
                break
        else:
            raise BadResponse("Unable to find status link for polling.")

        try:
            _raise_if_bad_http_status_and_method(self._initial_response.http_response)
            self._status = self._operation.set_initial_status(initial_response)

        except BadStatus as err:
            self._status = "Failed"
            raise HttpResponseError(response=initial_response.http_response, error=err)
        except BadResponse as err:
            self._status = "Failed"
            raise HttpResponseError(
                response=initial_response.http_response, message=str(err), error=err
            )
        except OperationFailed as err:
            raise HttpResponseError(response=initial_response.http_response, error=err)

    def run(self):
        try:
            self._poll()

        except BadStatus as err:
            self._status = "Failed"
            raise HttpResponseError(
                response=self._pipeline_response.http_response,
                error=err
            )

        except BadResponse as err:
            self._status = "Failed"
            raise HttpResponseError(
                response=self._pipeline_response.http_response,
                message=str(err),
                error=err
            )

        except OperationFailed as err:
            raise HttpResponseError(
                response=self._pipeline_response.http_response,
                error=err
            )

    def status(self):
        if not self._operation:
            raise ValueError(
                "set_initial_status was never called. Did you give this instance to a poller?"
            )
        return self._status

    def request_status(self, status_link):
        """Do a simple GET to this status link.

        This method re-inject 'x-ms-client-request-id'.

        :rtype: azure.core.pipeline.PipelineResponse
        """
        if self._path_format_arguments:
            status_link = self._client.format_url(status_link, **self._path_format_arguments)
        request = self._client.get(status_link)
        # Re-inject 'x-ms-client-request-id' while polling
        if "request_id" not in self._operation_config:
            self._operation_config["request_id"] = self._get_request_id()
        return self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=False, **self._operation_config
        )

    def finished(self):
        return _finished(self.status())

    def resource(self):
        return self._parse_resource(self._pipeline_response)

    def update_status(self):
        """Update the current status of the LRO."""
        self._pipeline_response = self.request_status(self._operation.get_polling_url())
        _raise_if_bad_http_status_and_method(self._pipeline_response.http_response)
        self._last_status = self._status
        self._status = self._operation.get_status(self._pipeline_response)

        if self._show_output:
            self._display_output(self._pipeline_response)

    def _parse_resource(self, pipeline_response):
        # type: (PipelineResponseType) -> Optional[Any]
        """Assuming this response is a resource, use the deserialization callback to parse it.
        If body is empty, assuming no resource to return.
        """
        response = pipeline_response.http_response
        if not _is_empty(response):
            return self._deserialization_callback(pipeline_response)
        return None

    @property
    def _transport(self):
        return self._client._pipeline._transport  # pylint: disable=protected-access

    def _sleep(self, delay):
        self._transport.sleep(delay)

    def _extract_delay(self):
        if self._pipeline_response is None:
            return None
        delay = get_retry_after(self._pipeline_response)
        if delay:
            return delay
        return self._timeout

    def _delay(self):
        """Check for a 'retry-after' header to set timeout,
        otherwise use configured timeout.
        """
        delay = self._extract_delay()
        self._sleep(delay)

    def _poll(self):
        while not self.finished():
            self._delay()
            self.update_status()

        if _failed(self.status()):
            self._handle_failure()

        if _succeeded(self.status()):
            self._handle_success()

    def _get_request_id(self):
        return self._pipeline_response.http_response.request.headers[

            "x-ms-client-request-id"
        ]

    def _handle_success(self):
        if self._show_output:
            json_response = _as_json(self._pipeline_response.http_response)
            operation_type = json_response.get("operationType", None)
            state = json_response.get("state", None)
            print('{} creation operation finished, operation "{}"'.format(operation_type,
                                                                          state))

    def _handle_failure(self):
        print("test")
        json_response = _as_json(self._pipeline_response.http_response)
        error = json_response.get("error")
        operation = json_response

        if error:  # Operation response error
            error_response = json.dumps(error, indent=2)
        elif self.error:  # Service response error
            error_response = json.dumps(self.error, indent=2)
        else:
            error_response = 'No error message received from server.'

        format_error_response = _format_error_response(error_response)
        logs_response = None
        operation_details = operation.get('operationDetails')
        if operation_details:
            sub_op_type = operation_details.get('subOperationType')
            if sub_op_type:
                if sub_op_type == 'BuildEnvironment' or sub_op_type == 'BuildImage':
                    operation_log_uri = operation.get('operationLog')
                    logs_response = 'More information can be found here: {}'.format(operation_log_uri)
                elif sub_op_type == 'DeployService':
                    logs_response = 'More information can be found using \'.get_logs()\''
        if not logs_response:
            logs_response = 'Current sub-operation type not known, more logs unavailable.'

        raise OperationFailed('Service deployment polling reached non-successful terminal state, current '
                              'service state: {}\n'
                              'Operation ID: {}\n'
                              '{}\n'
                              'Error:\n'
                              '{}'.format(self._status, self._operation.get_polling_url().split('/')[-1],
                                          logs_response, format_error_response))

    def _display_output(self, pipeline_response):
        json_response = _as_json(pipeline_response.http_response)
        # print(json_response)
        if self._streaming_log_offset == 0:
            sys.stdout.write('{}'.format(self._status))
            self._last_status = self._status
            sys.stdout.flush()

        streaming_log = json_response.get("streamingOperationLog", None)

        if streaming_log:
            streaming_log = streaming_log[self._streaming_log_offset:]
            self._streaming_log_offset += len(streaming_log)
            streaming_logs = streaming_log.split('#')
            for log in streaming_logs:
                time_and_log = log.split('|')
                if len(time_and_log) != 2:
                    sys.stdout.write('.')
                else:
                    utc_time = time_and_log[0]
                    utc_time = datetime.strptime(utc_time, '%Y%m%d%H%M%S').replace(tzinfo=tz.tzutc())
                    local_time = utc_time.astimezone(tz.tzlocal())
                    sys.stdout.write('\n' + str(local_time) + ' ' + time_and_log[1])
        else:
            sys.stdout.write('.')

        if self._status != self._last_status:
            # print("Old status : " + self._last_status)
            # print("New status : " + self._status)
            sys.stdout.write('\n{}\n'.format(self._status))
        sys.stdout.flush()


class MMSOperationResourcePolling(OperationResourcePolling):

    def __init__(self, service_context, **kwargs):
        self._service_context = service_context
        self._streaming_log_offset = 0
        super(MMSOperationResourcePolling, self).__init__(**kwargs)

    def get_status(self, pipeline_response):
        # type: (PipelineResponseType) -> str
        """Process the latest status update retrieved from an "Operation-Location" header.

        :param azure.core.pipeline.PipelineResponse response: The response to extract the status.
        :raises: BadResponse if response has no body, or body does not contain status.
        """
        response = pipeline_response.http_response
        if _is_empty(response):
            raise BadResponse(
                "The response from long running operation does not contain a body."
            )

        body = _as_json(response)
        status = body.get("state")
        if not status:
            raise BadResponse("No status found in body")

        return status
