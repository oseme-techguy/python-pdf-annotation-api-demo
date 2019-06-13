"""NamedEntity Controller
"""
from sanic import response
from sanic_ipware import get_client_ip
from app.helpers import ApiResponse
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS
import time # used to control pausing of the consumer
import datetime
import json

class NamedEntity:
    """NamedEntity Controller"""

    def __init__(self, logger=None, service=None):
        self.logger = logger
        self.service = service


    def get_entities(self, request, entity_id=None):
        """Fetches named_entity(s) on the service
        - Receive and parse get request
        - Go into AWS RDS and fetch named_entity(s)
        - Return success or not found
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        # query_params = request.raw_args
        # entity_id = query_params['entity_id'] if 'entity_id' in query_params else None

        self.logger.info('Received get named_entity request for id: {entity_id}'.format(
            entity_id=(entity_id if entity_id is not None else '')
        ))

        named_entity = None
        named_entities = {}
        try:
            if entity_id is None:
                named_entities = self.service.get_named_entities()
            else:
                named_entity = self.service.get_named_entity(entity_id)
        except LookupError as error:
            self.logger.error('Error Occurred: {error}'.format(error=error))
            return ApiResponse.failure({
                'message': 'Error while fetching named_entity(s)',
                'response': {}
            }, 500)

        if not named_entities and named_entity is None:
            return ApiResponse.failure({
                'message': 'No named_entity(s) found',
                'response': {}
            }, 404)

        return_data = named_entity if named_entity is not None else named_entities
        print(return_data)

        # Return named_entity object on successful login
        return ApiResponse.success({
            'code': 200,
            'message': 'successfully fetched named_entity(s) on service',
            'response': return_data
        })


    def add_entities(self, request):
        """Verifies that the required fields are set in request
        - open db connection and parse get request
        - commit model to db
        - colse db connection
        - Return created named_entity object
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        request_body = request.body
        body_params = {}
        if request_body != b'':
            body_params = json.loads(request_body)

        self.logger.info('Received create named_entity request: {params}'.format(
            params=body_params
        ))

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'named_entity data cannot be null',
                'response':{}
            }, 400)

        value = body_params['value'] if 'value' in body_params else None
        description = body_params['description'] if 'description' in body_params else None
        user_id = body_params['user_id'] if 'user_id' in body_params else None
        should_use = body_params['should_use'] if 'should_use' in body_params else None

        entity_data = {
            'value': value,
            'description': description,
            'user_id': user_id,
            'should_use': bool(should_use) if should_use is bool else False,
        }

        try:
            named_entity = self.service.add_named_entity(entity_data)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while adding the new named_entity. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if named_entity is None:
            return ApiResponse.failure({
                'message': 'An error occured while adding the new named_entity',
                'response': {}
            }, 500)

        # Return named_entity object on successful login
        return ApiResponse.success({
            'code': 201,
            'message': 'named_entity was successfully created',
            'response': named_entity
        }, 201)


    def update_entities(self, request, entity_id=None):
        """Verifies that the required fields are set in request
        - open db connection and parse get/post request
        - update model within db
        - close db connection
        - Return updated named_entity object
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        request_body = request.body
        body_params = {}
        if request_body != b'':
            body_params = json.loads(request_body)

        if entity_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the entity_id of the named_entity to patch',
                'response': {}
            }, 400)

        self.logger.info('Received update named_entity request for id: {entity_id} // : {params}'.format(
            entity_id=entity_id,
            params=body_params
        ))

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'named_entity data cannot be null',
                'response':{}
            }, 400)

        value = body_params['value'] if 'value' in body_params else None
        description = body_params['description'] if 'description' in body_params else None
        user_id = body_params['user_id'] if 'user_id' in body_params else None
        should_use = body_params['should_use'] if 'should_use' in body_params else None

        entity_data = {}

        if value is not None:
            entity_data['value'] = value
        if description is not None:
            entity_data['description'] = description
        if user_id is not None:
            entity_data['user_id'] = user_id
        if should_use is not None:
            entity_data['should_use'] = bool(should_use) if should_use is bool else False

        try:
            named_entity = self.service.update_named_entity(entity_id, entity_data)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while updating the named_entity. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if named_entity is None:
            return ApiResponse.failure({
                'message': 'An error occured while updating the named_entity',
                'response': {}
            }, 500)

        # NamedEntity has been successfully updated
        return ApiResponse.success({
            'code': 200,
            'message': 'named_entity was successfully updated',
            'response': named_entity
        }, 200)


    def delete_entities(self, request, entity_id=None):
        """Verifies that the required fields are set in request
        - open db connection and parse get/post request
        - delete named_entity where entity_id in db
        - close db connection
        - Return successful or failed
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        # query_params = request.raw_args
        # entity_id = query_params['entity_id'] if 'entity_id' in query_params else None

        if entity_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the entity_id of the named_entity to patch',
                'response': {}
            }, 400)

        self.logger.info('Received delete named_entity request for id: {entity_id}'.format(
            entity_id=entity_id
        ))

        try:
            is_deleted = self.service.delete_named_entity(entity_id)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while deleting the named_entity. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if is_deleted is False:
            return ApiResponse.failure({
                'message': 'An error occured while deleting the named_entity',
                'response': {}
            }, 500)

        # NamedEntity has been successfully updated
        return ApiResponse.success({
            'code': 204,
            'message': 'named_entity was successfully deleted',
            'response': {}
        }, 204)
