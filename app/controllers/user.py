"""User Controller
"""

from sanic import Sanic
from sanic import response
from sanic_jwt import exceptions
from sanic_ipware import get_client_ip
from app.helpers import ApiResponse
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS
import time
import datetime
import json


class User:
    """User Controller"""

    def __init__(self, logger=None, service=None):
        self.logger = logger
        self.service = service

    async def login(self, request, *args, **kwargs):
        """Logs in the user into this application
        - Receive and parse get request
        - Verify that the user is valid on the service
        - Go into AWS RDS and fetch user details and verify
        - Return success or unauthorized
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

        self.logger.info('Received user login request: {params}'.format(
            params=body_params
        ))

        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username or not password:
            raise exceptions.AuthenticationFailed("Missing username or password.")

        try:
            user = self.service.login(username, password)
        except LookupError as error:
            self.logger.error('Error Occurred: {error}'.format(error=error))
            raise exceptions.AuthenticationFailed("You are not authorized to login.")

        if user is None:
            raise exceptions.AuthenticationFailed("You are not authorized to login.")

        last_login_time = datetime.datetime.now() #.strftime("%Y-%m-%d %H:%M:%S")
        # pylint: disable=unused-variable,invalid-name
        ip, routable = get_client_ip(request)
        if ip is not None:
            # update the ip_address here for user
            pass

        return user

    async def add_user_roles_to_payload(self, user):
        """Enriches the payload with the user's scopes/role

        Arguments:
            user {object} -- the user object

        Returns:
            object {list} -- the scopes for the user
        """
        role = 'analyst' if user['role'] == 0  else 'manager' # 0 - Analysts, 1 - Managers
        return [role]

    async def get_logged_in_user(self, request, payload, *args, **kwargs):
        """Retrieves the profile for the logged in user

        Arguments:
            request {object} -- the request object
            payload {object} -- the payload
            args {object} -- the args
            kwargs {object} -- the kwargs

        Returns:
            object -- response from this endpoint
        """
        if payload:
            user_id = payload.get('user_id', None)
            try:
                return self.service.get_user(user_id)
            except LookupError as error:
                self.logger \
                    .error('Error Occurred while fetching profile: {error}'.format(error=error))
                return None
        return None

    def get_users(self, request, user_id=None):
        """Fetches user(s) on the service
        - Receive and parse get request
        - Go into AWS RDS and fetch user(s)
        - Return success or not found
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        # query_params = request.raw_args
        # user_id = query_params['user_id'] if 'user_id' in query_params else None

        self.logger.info('Received get user request for id: {user_id}'.format(
            user_id=(user_id if user_id is not None else '')
        ))

        user = None
        users = {}
        try:
            if user_id is None:
                users = self.service.get_users()
            else:
                user = self.service.get_user(user_id)
        except LookupError as error:
            self.logger.error('Error Occurred: {error}'.format(error=error))
            return ApiResponse.failure({
                'message': 'Error while fetching user(s)',
                'response': {}
            }, 500)

        if not users and user is None:
            return ApiResponse.failure({
                'message': 'No user(s) found',
                'response': {}
            }, 404)

        return_data = user if user is not None else users

        # Return users
        return ApiResponse.success({
            'code': 200,
            'message': 'successfully fetched user(s) on service',
            'response': return_data
        })

    def add_users(self, request):
        """Verifies that the required fields are set in request
        - open db connection and parse get request
        - commit model to db
        - colse db connection
        - Return created user object
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

        self.logger.info('Received create user request: {params}'.format(
            params=body_params
        ))

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'user data cannot be null',
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
            user = self.service.add_user(user_data)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while adding the new user. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if user is None:
            return ApiResponse.failure({
                'message': 'An error occured while adding the new user',
                'response': {}
            }, 500)

        # Return user object on successful login
        return ApiResponse.success({
            'code': 201,
            'message': 'user was successfully created',
            'response': user
        }, 201)

    def update_users(self, request, user_id=None):
        """Verifies that the required fields are set in request
        - open db connection and parse get/post request
        - update model within db
        - close db connection
        - Return updated user object
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

        if user_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the user_id of the user to patch',
                'response': {}
            }, 400)

        self.logger.info('Received update user request for id: {user_id} // : {params}'.format(
            user_id=user_id,
            params=body_params
        ))

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'user data cannot be null',
                'response':{}
            }, 400)

        username = body_params['username'] if 'username' in body_params else None
        first_name = body_params['first_name'] if 'first_name' in body_params else None
        last_name = body_params['last_name'] if 'last_name' in body_params else None
        role = body_params['role'] if 'role' in body_params else None

        user_data = {}

        if first_name is not None:
            user_data['first_name'] = first_name
        if last_name is not None:
            user_data['last_name'] = last_name
        if username is not None:
            user_data['username'] = username
        if role is not None:
            role = int(role, base=10)
            user_data['role'] = 0 if (role < 0 or role > 1) else role

        try:
            user = self.service.update_user(user_id, user_data)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while updating the user. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if user is None:
            return ApiResponse.failure({
                'message': 'An error occured while updating the user',
                'response': {}
            }, 500)

        # User has been successfully updated
        return ApiResponse.success({
            'code': 200,
            'message': 'user was successfully updated',
            'response': user
        }, 200)

    def delete_users(self, request):
        """Verifies that the required fields are set in request
        - open db connection and parse get/post request
        - delete user where user_id in db
        - close db connection
        - Return successful or failed
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        query_params = request.raw_args
        user_id = query_params['user_id'] if 'user_id' in query_params else None

        if user_id is None or user_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the user_id of the user to patch',
                'response': {}
            }, 400)

        self.logger.info('Received delete user request for id: {user_id}'.format(
            user_id=user_id
        ))

        try:
            is_deleted = self.service.delete_user(user_id)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while updating the user. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if is_deleted is False:
            return ApiResponse.failure({
                'message': 'An error occured while deleting the user',
                'response': {}
            }, 500)

        # User has been successfully updated
        return ApiResponse.success({
            'code': 204,
            'message': 'user was successfully deleted',
            'response': {}
        }, 204)
