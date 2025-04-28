# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import re

from dateutil.parser import parse

try:
    from abc import ABCMeta, abstractmethod

    ABC = ABCMeta('ABC', (), {})
except ImportError:
    from abc import ABC


class Webservice(ABC):
    """
    Defines base functionality for deploying models as web service endpoints in Azure Machine Learning.

    Webservice constructor is used to retrieve a cloud representation of a Webservice object associated with the
    provided Workspace. Returns an instance of a child class corresponding to the specific type of the retrieved
    Webservice object. The Webservice class allows for deploying machine learning models from either a
    :class:`azureml.core.Model` or :class:`azureml.core.Image` object.

    For more information about working with Webservice, see `Deploy models
    with Azure Machine Learning <https://docs.microsoft.com/azure/machine-learning/how-to-deploy-and-where>`_.

    .. remarks::

        The following sample shows the recommended deployment pattern where you first create a configuration object
        with the ``deploy_configuration`` method of the child class of Webservice (in this case
        :class:`azureml.core.webservice.AksWebservice`) and then use the configuration with the ``deploy`` method of
        the :class:`azureml.core.model.Model` class.

        .. code-block:: inject notebooks/how-to-use-azureml/deployment/production-deploy-to-aks
            /production-deploy-to-aks.ipynb#sample-deploy-to-aks

        The following sample shows how to find an existing :class:`azureml.core.webservice.AciWebservice` in a
        workspace and delete it if it exists so the name can be reused.

        .. code-block:: inject notebooks/how-to-use-azureml/deployment/deploy-to-cloud
            /model-register-and-deploy.ipynb#azuremlexception-remarks-sample

        There are a number of ways to deploy a model as a webservice, including with the:

        * ``deploy`` method of the :class:`azureml.core.model.Model` for models already registered in the workspace.

        * ``deploy_from_image`` method of :class:`azureml.core.webservice.Webservice` for images already created from
          a model.

        * ``deploy_from_model`` method of :class:`azureml.core.webservice.Webservice` for models already registered
          in the workspace. This method will create an image.

        * ``deploy`` method of the :class:`azureml.core.webservice.Webservice`, which will register a model and
          create an image.

        For information on working with webservices, see

        * `Consume an Azure Machine Learning model deployed
          as a web service <https://docs.microsoft.com/azure/machine-learning/how-to-consume-web-service>`_

        * `Monitor and collect data from ML web service
          endpoints <https://docs.microsoft.com/azure/machine-learning/how-to-enable-app-insights>`_

        The *Variables* section lists attributes of a local representation of the cloud Webservice object. These
        variables should be considered read-only. Changing their values will not be reflected in the corresponding
        cloud object.

    :var auth_enabled: Whether or not the Webservice has auth enabled.
    :vartype auth_enabled: bool
    :var compute_type: What type of compute the Webservice is deployed to.
    :vartype compute_type: str
    :var created_time: When the Webservice was created.
    :vartype created_time: datetime.datetime
    :var azureml.core.Webservice.description: A description of the Webservice object.
    :vartype description: str
    :var azureml.core.Webservice.tags: A dictionary of tags for the Webservice object.
    :vartype tags: dict[str, str]
    :var azureml.core.Webservice.name: The name of the Webservice.
    :vartype name: str
    :var azureml.core.Webservice.properties: Dictionary of key value properties for the Webservice. These properties
        cannot be changed after deployment, however new key value pairs can be added.
    :vartype properties: dict[str, str]
    :var created_by: The user that created the Webservice.
    :vartype created_by: str
    :var error: If the Webservice failed to deploy, this will contain the error message for why it failed.
    :vartype error: str
    :var azureml.core.Webservice.state: The current state of the Webservice.
    :vartype state: str
    :var updated_time: The last time the Webservice was updated.
    :vartype updated_time: datetime.datetime
    :var azureml.core.Webservice.workspace: The Azure Machine Learning Workspace which contains this Webservice.
    :vartype workspace: azureml.core.Workspace
    :var token_auth_enabled: Whether or not the Webservice has token auth enabled.
    :vartype token_auth_enabled: bool

    :param workspace: The workspace object containing the Webservice object to retrieve.
    :type workspace: azureml.core.Workspace
    :param name: The name of the of the Webservice object to retrieve.
    :type name: str
    """

    # TODO: Add "createdBy" back to expected payload keys upon rollout of
    # https://msdata.visualstudio.com/Vienna/_git/model-management/pullrequest/290466?_a=overview
    _expected_payload_keys = ['computeType', 'createdTime', 'description', 'kvTags', 'name', 'properties']
    _webservice_type = None

    @staticmethod
    def _all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in Webservice._all_subclasses(c)])

    def __init__(self, obj_dict):
        # Expected payload keys
        self.auth_enabled = obj_dict.get('authEnabled')
        self.compute_type = obj_dict.get('computeType')
        self.created_time = parse(obj_dict.get('createdTime')) if 'createdTime' in obj_dict else None
        self.description = obj_dict.get('description')
        self.image_id = obj_dict.get('imageId')
        self.image_digest = obj_dict.get('imageDigest')
        self.tags = obj_dict.get('kvTags')
        self.name = obj_dict.get('name')
        self.properties = obj_dict.get('properties')
        self.created_by = obj_dict.get('createdBy')

        # Common amongst Webservice classes but optional payload keys
        self.error = obj_dict.get('error')
        self.state = obj_dict.get('state')
        self.updated_time = parse(obj_dict['updatedTime']) if 'updatedTime' in obj_dict else None

    def __repr__(self):
        """Return the string representation of the Webservice object.

        :return: String representation of the Webservice object
        :rtype: str
        """
        return "{}(workspace={}, name={}, image_id={}, compute_type={}, state={}, scoring_uri={}, " \
               "tags={}, properties={}, created_by={})" \
            .format(
                self.__class__.__name__,
                self.workspace.__repr__() if hasattr(self, 'workspace') else None,
                self.name if hasattr(self, 'name') else None,
                self.image_id if hasattr(self, 'image_id') else None,
                self.image_digest if hasattr(self, 'image_digest') else None,
                self.compute_type if hasattr(self, 'compute_type') else None,
                self.state if hasattr(self, 'state') else None,
                self.scoring_uri if hasattr(self, 'scoring_uri') else None,
                self.tags if hasattr(self, 'tags') else None,
                self.properties if hasattr(self, 'properties') else None,
                self.created_by if hasattr(self, 'created_by') else None
            )

    @staticmethod
    def _check_validate_error(content):
        payload = json.loads(content)

        if payload and "error" in payload and "message" in payload["error"]:
            return payload["error"]["message"]
        else:
            return None

    @staticmethod
    def _get_deploy_compute_type(deploy_payload):
        if deploy_payload \
                and 'computeType' in deploy_payload:
            return deploy_payload['computeType']

        return None

    @staticmethod
    def _check_for_local_deployment(deployment_config):  # pragma: no cover
        from azureml.core.webservice.local import LocalWebserviceDeploymentConfiguration
        if deployment_config and (type(deployment_config) is LocalWebserviceDeploymentConfiguration):
            raise Exception('This method does not support local deployment configuration. Please use '
                            'deploy_local_from_model for local deployment.')

    @staticmethod
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

    def update_deployment_state(self):
        """
        Refresh the current state of the in-memory object.

        Perform an in-place update of the properties of the object based on the current state of the corresponding
        cloud object. Primarily useful for manual polling of creation state.
        """
        service = Webservice(self.workspace, name=self.name)
        for key in self.__dict__.keys():
            if key != "_operation_endpoint":
                self.__dict__[key] = service.__dict__[key]

    @staticmethod
    def _attribute_transformer(key, attr_desc, value):
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
        return (key, value)

    def serialize(self):
        """
        Convert this Webservice object into a JSON serialized dictionary.

        Use :func:`deserialize` to convert back into a Webservice object.

        :return: The JSON representation of this Webservice.
        :rtype: dict
        """
        created_time = self.created_time.isoformat() if self.created_time else None
        updated_time = self.updated_time.isoformat() if self.updated_time else None
        scoring_uri = getattr(self, 'scoring_uri', None)
        workspace_name = self.service_context.workspace_name if getattr(self, 'service_context', None) else None
        image_details = None
        # TODO : Check serialization for createdBy
        return {'name': self.name, 'description': self.description, 'tags': self.tags,
                'properties': self.properties, 'state': self.state, 'createdTime': created_time,
                'updatedTime': updated_time, 'error': self.error, 'computeType': self.compute_type,
                'workspaceName': workspace_name, 'imageId': self.image_id, 'imageDigest': self.image_digest,
                'imageDetails': image_details, 'scoringUri': scoring_uri,
                'createdBy': self.created_by.as_dict(key_transformer=self._attribute_transformer)}

    @classmethod
    def deserialize(cls, workspace, webservice_payload):
        """
        Convert a Model Management Service response JSON object into a Webservice object.

        Will fail if the provided workspace is not the workspace the Webservice is registered under.

        :param cls: Indicates that this is a class method.
        :type cls:
        :param workspace: The workspace object the Webservice is registered under.
        :type workspace: azureml.core.Workspace
        :param webservice_payload: A JSON object to convert to a Webservice object.
        :type webservice_payload: dict
        :return: The Webservice representation of the provided JSON object.
        :rtype: azureml.core.Webservice
        """
        cls._validate_get_payload(webservice_payload)
        webservice = cls(None, None)
        webservice._initialize(workspace, webservice_payload)
        return webservice

    @classmethod
    def _validate_get_payload(cls, payload):
        """Validate the payload for this Webservice.

        :param payload:
        :type payload: dict
        :return:
        :rtype:
        """
        if 'computeType' not in payload:
            raise Exception('Invalid payload for {} webservice, missing computeType:\n'
                            '{}'.format(cls._webservice_type, payload))
        if payload['computeType'] != cls._webservice_type and cls._webservice_type != "Unknown":
            raise Exception('Invalid payload for {} webservice, computeType is not {}":\n'
                            '{}'.format(cls._webservice_type, cls._webservice_type, payload))
        for service_key in cls._expected_payload_keys:
            if service_key not in payload:
                raise Exception('Invalid {} Webservice payload, missing "{}":\n'
                                '{}'.format(cls._webservice_type, service_key, payload))


class WebserviceDeploymentConfiguration(ABC):
    """Defines the base-class functionality for all Webservice deployment configuration objects.

    This class represents the configuration parameters for deploying a Webservice on a specific target.
    For example, to create deployment for Azure Kubernetes Service, use the ``deploy_configuration`` method
    of the :class:`azureml.core.webservice.aks.AksWebservice` class.

    :var azureml.core.webservice.Webservice.description: A description to give this Webservice.
    :vartype description: str
    :var azureml.core.webservice.Webservice.tags: A dictionary of key value tags to give this Webservice.
    :vartype tags: dict[str, str]
    :var azureml.core.webservice.Webservice.properties: A dictionary of key value properties to give this Webservice.
        These properties cannot be changed after deployment, however new key value pairs can be added.
    :vartype properties: dict[str, str]
    :var azureml.core.webservice.Webservice.primary_key: A primary auth key to use for this Webservice.
    :vartype primary_key: str
    :var azureml.core.webservice.Webservice.secondary_key: A secondary auth key to use for this Webservice.
    :vartype secondary_key: str
    :var azureml.core.webservice.Webservice.location: The Azure region to deploy this Webservice to.
    :vartype location: str

    :param type: The type of Webservice associated with this object.
    :type type: azureml.core.webservice.webservice.Webservice
    :param description: A description to give this Webservice.
    :type description: str
    :param tags: A dictionary of key value tags to give this Webservice.
    :type tags: dict[str, str]
    :param properties: A dictionary of key value properties to give this Webservice. These properties cannot
        be changed after deployment, however new key value pairs can be added.
    :type properties: dict[str, str]
    :param primary_key: A primary auth key to use for this Webservice.
    :type primary_key: str
    :param secondary_key: A secondary auth key to use for this Webservice.
    :type secondary_key: str
    :param location: The Azure region to deploy this Webservice to.
    :type location: str
    """

    def __init__(self, type, description=None, tags=None, properties=None, primary_key=None, secondary_key=None,
                 location=None):
        """Initialize the configuration object.

        :param type: The type of Webservice associated with this object.
        :type type: azureml.core.webservice.webservice.Webservice
        :param description: A description to give this Webservice.
        :type description: str
        :param tags: A dictionary of key value tags to give this Webservice.
        :type tags: dict[str, str]
        :param properties: A dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added.
        :type properties: dict[str, str]
        :param primary_key: A primary auth key to use for this Webservice.
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Webservice.
        :type secondary_key: str
        :param location: The Azure region to deploy this Webservice to.
        :type location: str
        """
        self._webservice_type = type
        self.description = description
        self.tags = tags
        self.properties = properties
        self.primary_key = primary_key
        self.secondary_key = secondary_key
        self.location = location

    @abstractmethod
    def validate_configuration(self):
        """Check that the specified configuration values are valid.

        Raises a :class:`azureml.exceptions.WebserviceException` if validation fails.

        :raises: :class:`azureml.exceptions.WebserviceException`
        """
        pass

    @abstractmethod
    def print_deploy_configuration(self):
        """Print the deployment configuration."""
        pass

    # @classmethod
    # def validate_image(cls, image):
    #     """Check that the image that is being deployed to the Webservice is valid.
    #
    #     Raises a :class:`azureml.exceptions.WebserviceException` if validation fails.
    #
    #     :param cls: Indicates that this is a class method.
    #     :type cls:
    #     :param image: The image that will be deployed to the webservice.
    #     :type image: azureml.core.Image
    #     :raises: :class:`azureml.exceptions.WebserviceException`
    #     """
    #     if image is None:
    #         raise WebserviceException("Image is None", logger=module_logger)
    #     if image.creation_state != 'Succeeded':
    #         raise WebserviceException('Unable to create service with image {} in non "Succeeded" '
    #                                   'creation state.'.format(image.id), logger=module_logger)
    #     if image.image_flavor not in CLOUD_DEPLOYABLE_IMAGE_FLAVORS:
    #         raise WebserviceException('Deployment of {} images is not supported'.format(image.image_flavor),
    #                                   logger=module_logger)

    def _build_base_create_payload(self, name, environment_image_request):
        """Construct the base webservice creation payload.

        :param name:
        :type name: str
        :param environment_image_request:
        :type environment_image_request: dict
        :return:
        :rtype: dict
        """
        import copy
        from azureml._model_management._util import base_service_create_payload_template
        json_payload = copy.deepcopy(base_service_create_payload_template)
        json_payload['name'] = name
        json_payload['description'] = self.description
        json_payload['kvTags'] = self.tags

        properties = self.properties or {}
        # TODO: check if this needs to be ported
        # properties.update(global_tracking_info_registry.gather_all())
        json_payload['properties'] = properties

        if self.primary_key:
            json_payload['keys']['primaryKey'] = self.primary_key
            json_payload['keys']['secondaryKey'] = self.secondary_key

        json_payload['computeType'] = self._webservice_type._webservice_type
        json_payload['environmentImageRequest'] = environment_image_request
        json_payload['location'] = self.location

        return json_payload
