# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
import time

import jwt
from azure.identity import CredentialUnavailableError
from azure.core.credentials import AccessToken

_TOKEN_REFRESH_THRESHOLD_SEC = 5 * 60

_LOGGER = logging.getLogger(__name__)


class _ArcadiaAuthentication(object):
    """Authentication class for Arcadia cluster."""

    _cached_arm_token = None

    _cached_graph_token = None

    _ARCADIA_ENVIRONMENT_VARIABLE_NAME = "AZURE_SERVICE"
    _ARCADIA_ENVIRONMENT_VARIABLE_VALUE = "Microsoft.ProjectArcadia"

    def __init__(self, **kwargs):
        self._credential_available = True
        self._is_arcadia_environment = \
            os.environ.get(_ArcadiaAuthentication._ARCADIA_ENVIRONMENT_VARIABLE_NAME, None) == \
            _ArcadiaAuthentication._ARCADIA_ENVIRONMENT_VARIABLE_VALUE
        _LOGGER.debug("Arcadia environment is {}".format(str(self._is_arcadia_environment)))

        if self._is_arcadia_environment:
            try:
                self.get_token()
            except Exception:
                _LOGGER.debug("Token fetch failed for arcadia auth")
                self._credential_available = False
        else:
            self._credential_available = False

    def get_token(self, *scopes, **kwargs):
        """Return arm token.

        :return: Returns the arm token.
        :rtype: str
        """
        if self._credential_available:
            from azureml.mlflow._common._authentication._arcadia_token_wrapper import PyTokenLibrary
            expiry = _get_exp_time(_ArcadiaAuthentication._cached_arm_token)\
                if _ArcadiaAuthentication._cached_arm_token else None
            if _ArcadiaAuthentication._cached_arm_token and \
                    not ((expiry - time.time())
                         < _TOKEN_REFRESH_THRESHOLD_SEC):
                return AccessToken(_ArcadiaAuthentication._cached_arm_token, int(expiry))
            else:
                _ArcadiaAuthentication._cached_arm_token = PyTokenLibrary.get_AAD_token(PyTokenLibrary._ARM_RESOURCE)
                expiry = _get_exp_time(_ArcadiaAuthentication._cached_arm_token)
                return AccessToken(_ArcadiaAuthentication._cached_arm_token, int(expiry))
        else:
            raise CredentialUnavailableError(
                message="_ArcadiaAuthentication could not fetch token. Either we are "
                        "not in arcadia cluster or credentials not available"
            )

    @staticmethod
    def _is_arcadia_environment():
        return os.environ.get(_ArcadiaAuthentication._ARCADIA_ENVIRONMENT_VARIABLE_NAME, None) \
            == _ArcadiaAuthentication._ARCADIA_ENVIRONMENT_VARIABLE_VALUE


def _get_exp_time(access_token):
    """Return the expiry time of the supplied arm access token.

    :param access_token:
    :type access_token: str
    :return:
    :rtype: float
    """
    # We set verify=False, as we don't have keys to verify signature, and we also don't need to
    # verify signature, we just need the expiry time.
    decode_json = jwt.decode(access_token, options={'verify_signature': False, 'verify_aud': False})
    return decode_json['exp']
