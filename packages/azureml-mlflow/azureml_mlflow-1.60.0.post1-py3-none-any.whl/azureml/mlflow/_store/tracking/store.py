# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowStore** provides a class to read and record run metrics and artifacts on Azure via MLflow."""

import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from mlflow import MlflowException

from mlflow.utils.proto_json_utils import message_to_json
from azureml.mlflow._common.constants import RunEnvVars
from azureml.mlflow._store.azureml_reststore import AzureMLAbstractRestStore
from azureml.mlflow._protos.aml_service_pb2 import (
    LogBatchAsync,
    GetRunDataStatus,
    AMLMlflowService,
)

from mlflow.utils.async_logging.run_operations import RunOperations
from mlflow.utils.rest_utils import (
    _REST_API_PATH_PREFIX,
    call_endpoint,
    extract_api_info_for_service,
)

_METHOD_TO_INFO_AML = extract_api_info_for_service(
    AMLMlflowService, _REST_API_PATH_PREFIX
)

VERSION_WARNING = "Could not import {}. Please upgrade to Mlflow 1.4.0 or higher."

logger = logging.getLogger(__name__)

try:
    from mlflow.store.tracking.rest_store import RestStore
except ImportError:
    logger.warning(VERSION_WARNING.format("from mlflow"))
    from mlflow.store.rest_store import RestStore

_MLFLOW_RUN_ID_ENV_VAR = "MLFLOW_RUN_ID"
_thread_pool = ThreadPoolExecutor(max_workers=10)
DEFAULT_TIMEOUT_SEC = 60  # seconds
_MLFLOW_RUN_DATA_WAIT_TIMEOUT_SEC_ENV_VAR = "MLFLOW_RUN_DATA_WAIT_TIMEOUT_SEC"
_run_data_wait_timeout_sec = int(
    os.environ.get(_MLFLOW_RUN_DATA_WAIT_TIMEOUT_SEC_ENV_VAR, DEFAULT_TIMEOUT_SEC)
)


class AzureMLRestStore(AzureMLAbstractRestStore, RestStore):
    """
    Client for a remote tracking server accessed via REST API calls.

    :param service_context: Service context for the AzureML workspace
    :type service_context: azureml._restclient.service_context.ServiceContext
    """

    def __init__(self, service_context, host_creds=None, **kwargs):
        """
        Construct an AzureMLRestStore object.

        :param service_context: Service context for the AzureML workspace
        :type service_context: azureml._restclient.service_context.ServiceContext
        """
        logger.debug("Initializing the AzureMLRestStore")
        AzureMLAbstractRestStore.__init__(self, service_context, host_creds)
        RestStore.__init__(self, self.get_host_creds, **kwargs)

    @wraps(RestStore.update_run_info)
    def update_run_info(self, run_id, *args, **kwargs):
        remote_run_id = os.environ.get(RunEnvVars.ID)
        if remote_run_id is not None and run_id == remote_run_id:
            logger.debug("Status update was skipped for remote run {}".format(run_id))
            return self.get_run(run_id).info
        return super(AzureMLRestStore, self).update_run_info(run_id, *args, **kwargs)

    def log_batch_async(self, run_id, metrics, params, tags) -> RunOperations:
        metric_protos = [metric.to_proto() for metric in metrics]
        param_protos = [param.to_proto() for param in params]
        tag_protos = [tag.to_proto() for tag in tags]
        req_body = message_to_json(
            LogBatchAsync(
                metrics=metric_protos,
                params=param_protos,
                tags=tag_protos,
                run_id=run_id,
            )
        )
        response_proto = self._call_to_endpoint(LogBatchAsync, req_body)
        response = LogBatchAsync.Response()
        response.batch_tracking_id = response_proto.batch_tracking_id
        run_data_wait_timeout_sec = int(
            os.environ.get(
                _MLFLOW_RUN_DATA_WAIT_TIMEOUT_SEC_ENV_VAR, DEFAULT_TIMEOUT_SEC
            )
        )
        # This is so that when we dont have any metrics, we dont poll backend
        # for run data, as params and tags are persisted in sync fashion always.
        return (
            self._await_run_data(
                run_id, response_proto.batch_tracking_id, run_data_wait_timeout_sec
            )
            if response_proto.batch_tracking_id != ""
            else RunOperations(operation_futures=[])
        )

    def _call_to_endpoint(self, api, json_body):
        endpoint, method = _METHOD_TO_INFO_AML[api]
        response_proto = api.Response()
        return call_endpoint(
            self.get_host_creds(), endpoint, method, json_body, response_proto
        )

    def _await_run_data(self, run_id, batch_tracking_id, timeout_sec) -> RunOperations:
        run_data_await_future = _thread_pool.submit(
            self._await_run_data_impl,
            run_id,
            batch_tracking_id,
            timeout_sec=timeout_sec,
        )
        return RunOperations(operation_futures=[run_data_await_future])

    def _await_run_data_impl(self, run_id, batch_tracking_id, timeout_sec):
        stop_at = time.time() + timeout_sec
        while True:
            req_body = message_to_json(
                GetRunDataStatus(run_id=run_id, batch_tracking_id=batch_tracking_id)
            )
            response_proto = self._call_to_endpoint(GetRunDataStatus, req_body)
            is_complete = response_proto.is_complete
            if time.time() > stop_at:
                raise MlflowException(
                    message="Timed out waiting for run data to be available",
                    error_code="TIMEOUT",
                )
            if is_complete:
                break
            time.sleep(5)
