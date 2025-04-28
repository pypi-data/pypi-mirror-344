# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import re

from azureml.mlflow.deploy._mir.mir import OnlineEndpointConfiguration


def convert_v2_deploy_config_to_rest_config(v2_deploy_config, existing_deployment=None):
    rest_config = {}

    if 'app_insights_enabled' in v2_deploy_config or existing_deployment:
        rest_config['app_insights_enabled'] = \
            v2_deploy_config.get('app_insights_enabled') or existing_deployment.properties.app_insights_enabled
    if 'description' in v2_deploy_config or existing_deployment:
        rest_config['description'] = \
            v2_deploy_config.get('description') or existing_deployment.properties.description
    if 'environment_variables' in v2_deploy_config or existing_deployment:
        rest_config['environment_variables'] = \
            v2_deploy_config.get('environment_variables') or existing_deployment.properties.environment_variables
    if 'instance_type' in v2_deploy_config or existing_deployment:
        rest_config['instance_type'] = \
            v2_deploy_config.get('instance_type') or existing_deployment.properties.instance_type
    if 'properties' in v2_deploy_config or existing_deployment:
        rest_config['properties'] = \
            v2_deploy_config.get('properties') or existing_deployment.properties.properties

    if 'liveness_probe' in v2_deploy_config or existing_deployment:
        rest_config['liveness_probe'] = _convert_probe_settings_for_rest_config(
            v2_deploy_config.get('liveness_probe')) or existing_deployment.properties.liveness_probe
    if 'readiness_probe' in v2_deploy_config or existing_deployment:
        rest_config['readiness_probe'] = _convert_probe_settings_for_rest_config(
            v2_deploy_config.get('readiness_probe')) or existing_deployment.properties.readiness_probe
    if 'request_settings' in v2_deploy_config or existing_deployment:
        rest_config['request_settings'] = _convert_request_settings_for_rest_config(
            v2_deploy_config.get('request_settings')) or existing_deployment.properties.request_settings
    if 'scale_settings' in v2_deploy_config or existing_deployment:
        rest_config['scale_settings'] = _convert_scale_settings_for_rest_config(
            v2_deploy_config.get('scale_settings')) or existing_deployment.properties.scale_settings
    if 'model' in v2_deploy_config:
        rest_config['model'] = v2_deploy_config.get('model')

    return rest_config


def _convert_probe_settings_for_rest_config(clientside_probe_settings):
    if not clientside_probe_settings:
        return None
    rest_config_request_settings = {}
    if 'failure_threshold' in clientside_probe_settings:
        rest_config_request_settings['failure_threshold'] = clientside_probe_settings['failure_threshold']
    if 'initial_delay' in clientside_probe_settings:
        rest_config_request_settings['initial_delay'] = 'PT{}S'.format(clientside_probe_settings['initial_delay'])
    if 'period' in clientside_probe_settings:
        rest_config_request_settings['period'] = 'PT{}S'.format(clientside_probe_settings['period'])
    if 'success_threshold' in clientside_probe_settings:
        rest_config_request_settings['success_threshold'] = clientside_probe_settings['success_threshold']
    if 'timeout' in clientside_probe_settings:
        rest_config_request_settings['timeout'] = 'PT{}S'.format(clientside_probe_settings['timeout'])

    return rest_config_request_settings


def _convert_request_settings_for_rest_config(clientside_request_settings):
    if not clientside_request_settings:
        return None
    rest_config_request_settings = {}
    if 'max_concurrent_requests_per_instance' in clientside_request_settings:
        rest_config_request_settings['max_concurrent_requests_per_instance'] = \
            clientside_request_settings['max_concurrent_requests_per_instance']
    if 'max_queue_wait_ms' in clientside_request_settings:
        rest_config_request_settings['max_queue_wait'] = clientside_request_settings['max_queue_wait_ms']
    if 'request_timeout_ms' in clientside_request_settings:
        rest_config_request_settings['request_timeout'] = clientside_request_settings['request_timeout_ms']

    return rest_config_request_settings


def _convert_scale_settings_for_rest_config(clientside_scale_settings):
    if not clientside_scale_settings:
        return None
    rest_config_scale_settings = {}
    if 'type' in clientside_scale_settings:
        rest_config_scale_settings['type'] = clientside_scale_settings['type']
    if rest_config_scale_settings['type'].lower() != 'default':
        if 'max_instances' in clientside_scale_settings:
            rest_config_scale_settings['max_instances'] = clientside_scale_settings['max_instances']
        if 'min_instances' in clientside_scale_settings:
            rest_config_scale_settings['min_instances'] = clientside_scale_settings['min_instances']
        if 'polling_interval' in clientside_scale_settings:
            rest_config_scale_settings['polling_interval'] = clientside_scale_settings['polling_interval']
        if 'target_utilization_percentage' in clientside_scale_settings:
            rest_config_scale_settings['target_utilization_percentage'] = \
                clientside_scale_settings['target_utilization_percentage']
    return rest_config_scale_settings


def _get_default_online_endpoint_config():
    online_endpoint_configuration = OnlineEndpointConfiguration(
        auth_mode="aml_token",
        properties={
            "azureml.mlflow_client_endpoint": "True"
        },
        identity={"type": "system_assigned"}
    )

    return online_endpoint_configuration


def _attribute_transformer_snake_to_camel_case(key, attr_desc, value):
    """A key transformer that returns the Python attribute.

    :param str key: The attribute name
    :param dict attr_desc: The attribute metadata
    :param object value: The value
    :returns: A key using attribute name
    """
    # v1 contract has the properties exposed in camel case so converting snake case to camel case
    if key:
        # Special case for just one key since they mismatch on client and service side
        if key == "kv_tags":
            key = "tags"
        key = re.sub("_([a-zA-Z0-9])", lambda m: m.group(1).upper(), key)
    return key, value
