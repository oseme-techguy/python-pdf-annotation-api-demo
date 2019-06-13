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
                named_entities = self.service.get_users()
            else:
                named_entity = self.service.get_user(entity_id)
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

        username = body_params['username'] if 'username' in body_params else None
        password = body_params['password'] if 'password' in body_params else None
        first_name = body_params['first_name'] if 'first_name' in body_params else None
        last_name = body_params['last_name'] if 'last_name' in body_params else None
        role = body_params['role'] if 'role' in body_params else None

        user_data = {
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'role': int(role) if role is not None else 0,
            'ip_address': None,
            'last_login_time': None,
        }

        if user_data['role'] < 0 or user_data['role'] > 1:
            user_data['role'] = 0

        try:
            named_entity = self.service.add_user(user_data)
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


    def update_entities(self, request):
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
        query_params = request.raw_args
        body_params = {}
        if request_body != b'':
            body_params = json.loads(request_body)

        entity_id = query_params['entity_id'] if 'entity_id' in query_params else None
        if entity_id is None or entity_id is None:
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

        username = body_params['username'] if 'username' in body_params else None
        first_name = body_params['first_name'] if 'first_name' in body_params else None
        last_name = body_params['last_name'] if 'last_name' in body_params else None
        role = body_params['role'] if 'role' in body_params else None

        user_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'role': int(role) if role is not None else 0
        }

        if user_data['role'] < 0 or user_data['role'] > 1:
            user_data['role'] = 0

        try:
            named_entity = self.service.update_user(entity_id, user_data)
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


    def delete_entities(self, request):
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

        query_params = request.raw_args
        entity_id = query_params['entity_id'] if 'entity_id' in query_params else None

        if entity_id is None or entity_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the entity_id of the named_entity to patch',
                'response': {}
            }, 400)

        self.logger.info('Received delete named_entity request for id: {entity_id}'.format(
            entity_id=entity_id
        ))

        try:
            is_deleted = self.service.delete_user(entity_id)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while updating the named_entity. ' +
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
