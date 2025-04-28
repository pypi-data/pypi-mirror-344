# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
from azureml.mlflow._restclient.mfe_v2022_02_01_preview.models import \
    OnlineEndpointDetails, OnlineEndpointData as RestOnlineEndpoint, ManagedServiceIdentity, PartialOnlineEndpoint, \
    PartialOnlineEndpointPartialTrackedResource

logger = logging.getLogger(__name__)


class OnlineEndpointConfiguration(object):

    def __init__(
            self,
            identity=None,
            location=None,
            tags=None,
            auth_mode=None,
            description=None,
            traffic=None,
            mirror_traffic=None,
            properties=None,
    ):

        self.identity = identity
        self.location = location
        self.tags = tags
        self.traffic = traffic
        self.auth_mode = auth_mode
        self.description = description
        self.mirror_traffic = mirror_traffic
        self.properties = properties

    @staticmethod
    def _from_dict_config(config):
        online_endpoint_config = OnlineEndpointConfiguration()

        if 'identity' in config:
            online_endpoint_config.identity = config['identity']

        if 'location' in config:
            online_endpoint_config.location = config['location']

        if 'tags' in config:
            online_endpoint_config.tags = config['tags']

        if 'auth_mode' in config:
            online_endpoint_config.auth_mode = config['auth_mode']
        if 'description' in config:
            online_endpoint_config.description = config['description']
        if 'traffic' in config:
            online_endpoint_config.traffic = config['traffic']
        if 'mirror_traffic' in config:
            online_endpoint_config.mirror_traffic = config['mirror_traffic']
        if 'properties' in config:
            online_endpoint_config.properties = config['properties']

        return online_endpoint_config

    def _to_rest(self):
        auth_mode_switch = {
            'aml_token': "AMLToken",
            'aad_token': "AADToken",
            'key': 'Key'
        }

        auth_mode = auth_mode_switch.get(self.auth_mode, self.auth_mode)

        properties = OnlineEndpointDetails(
            auth_mode=auth_mode,
            properties=self.properties,
            description=self.description,
            traffic=self.traffic,
            mirror_traffic=self.mirror_traffic
        )

        identity = self.identity
        if self.identity:
            identity_type = self.identity.get("type", None)
            if identity_type == "system_assigned":
                identity = {"type": "SystemAssigned"}

        online_endpoint = RestOnlineEndpoint(
            location=self.location,
            properties=properties,
            identity=ManagedServiceIdentity(**identity) if identity else None,
            tags=self.tags
        )

        return online_endpoint

    def _to_rest_update_config(self):
        partial_online_endpoint = PartialOnlineEndpoint(
            traffic=self.traffic,
            mirror_traffic=self.mirror_traffic
        )

        partial_online_endpoint_resource = PartialOnlineEndpointPartialTrackedResource(
            properties=partial_online_endpoint,
            location=self.location,
            tags=self.tags
        )

        return partial_online_endpoint_resource
