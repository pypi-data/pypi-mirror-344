# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging

import jwt
from azure.core.credentials import AccessToken
from azure.identity import CredentialUnavailableError

_LOGGER = logging.getLogger(__name__)


class _DatabricksClusterAuthentication(object):

    def __init__(self, **kwargs):
        self._credential_available = True
        try:
            self.get_token()
        except Exception as e:
            _LOGGER.debug("Token fetch failed for _DatabricksClusterAuthentication: {}".format(str(e)))
            self._credential_available = False

    def get_token(self, *scopes, **kwargs):
        """Contract for Track 2 SDKs to get token.

        Currently supports Auth classes with self.get_authentication_header function implemented.

        :param scopes: Args.
        :param kwargs: Kwargs.
        :return: Returns a named tuple.
        :rtype: collections.namedtuple
        """
        if self._credential_available:
            import IPython
            dbutils = IPython.get_ipython().user_ns["dbutils"]
            token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().adlsAadToken().get()  # noqa
            expiry = \
                jwt.decode(token, options={'verify_signature': False, 'verify_aud': False})['exp']
            return AccessToken(token, int(expiry))
        else:
            raise CredentialUnavailableError(
                message="_DatabricksClusterAuthentication could not fetch token. Either we are "
                        "not in Databricks cluster or credentials not available")
