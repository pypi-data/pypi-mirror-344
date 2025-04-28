# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json

from azure.core.exceptions import DecodeError
from azure.core.pipeline.policies._utils import parse_retry_after
from azure.core.polling.base_polling import BadStatus

_FINISHED = frozenset(["succeeded", "canceled", "failed"])
_FAILED = frozenset(["canceled", "failed"])
_SUCCEEDED = frozenset(["succeeded"])


def _finished(status):
    if hasattr(status, "value"):
        status = status.value
    return str(status).lower() in _FINISHED


def _failed(status):
    if hasattr(status, "value"):
        status = status.value
    return str(status).lower() in _FAILED


def _succeeded(status):
    if hasattr(status, "value"):
        status = status.value
    return str(status).lower() in _SUCCEEDED


def _as_json(response):
    # type: (ResponseType) -> dict
    """Assuming this is not empty, return the content as JSON.

    Result/exceptions is not determined if you call this method without testing _is_empty.

    :raises: DecodeError if response body contains invalid json data.
    """
    try:
        return json.loads(response.text())
    except ValueError:
        raise DecodeError("Error occurred in deserializing the response body.")


def _is_empty(response):
    # type: (ResponseType) -> bool
    """Check if response body contains meaningful content.

    :rtype: bool
    """
    return not bool(response.body())


def _raise_if_bad_http_status_and_method(response):
    # type: (ResponseType) -> None
    """Check response status code is valid.

    Must be 200, 201, 202, or 204.

    :raises: BadStatus if invalid status.
    """
    code = response.status_code
    if code in {200, 201, 202, 204}:
        return
    raise BadStatus(
        "Invalid return status {!r} for {!r} operation".format(
            code, response.request.method
        )
    )


def _format_error_response(error_response):
    """Format mms returned error message to make it more readable.

    :param error_response: the mms returned error message str.
    :type error_response: str
    :return:
    :rtype: str
    """
    try:
        # error_response returned may have some 2-times escapes, so here need decode twice to un-escape all.
        format_error_response = error_response.encode('utf-8').decode('unicode_escape')
        format_error_response = format_error_response.encode('utf-8').decode('unicode_escape')
        return format_error_response
    except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
        return error_response


def get_retry_after(response):
    """Get the value of Retry-After in seconds.

    :param response: The PipelineResponse object
    :type response: ~azure.core.pipeline.PipelineResponse
    :return: Value of Retry-After in seconds.
    :rtype: float or None
    """
    headers = _case_insensitive_dict(response.http_response.headers)
    retry_after = headers.get("retry-after")
    if retry_after:
        return parse_retry_after(retry_after)
    for ms_header in ["retry-after-ms", "x-ms-retry-after-ms"]:
        retry_after = headers.get(ms_header)
        if retry_after:
            parsed_retry_after = parse_retry_after(retry_after)
            return parsed_retry_after / 1000.0
    return None


def _case_insensitive_dict(*args, **kwargs):
    """Return a case-insensitive dict from a structure that a dict would have accepted.

    Rational is I don't want to re-implement this, but I don't want
    to assume "requests" or "aiohttp" are installed either.
    So I use the one from "requests" or the one from "aiohttp" ("multidict")
    If one day this library is used in an HTTP context without "requests" nor "aiohttp" installed,
    we can add "multidict" as a dependency or re-implement our own.
    """
    try:
        from requests.structures import CaseInsensitiveDict

        return CaseInsensitiveDict(*args, **kwargs)
    except ImportError:
        pass
    try:
        # multidict is installed by aiohttp
        from multidict import CIMultiDict

        if len(kwargs) == 0 and len(args) == 1 and (not args[0]):
            return CIMultiDict()    # in case of case_insensitive_dict(None), we don't want to raise exception
        return CIMultiDict(*args, **kwargs)
    except ImportError:
        raise ValueError(
            "Neither 'requests' or 'multidict' are installed and no case-insensitive dict impl have been found"
        )
