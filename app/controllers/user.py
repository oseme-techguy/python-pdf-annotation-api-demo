"""User Controller
"""
from sanic import response
from sanic_ipware import get_client_ip
from app.helpers import ApiResponse
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS
import time # used to control pausing of the consumer
import datetime
import json

class User:
    """User Controller"""

    def __init__(self, logger=None, service=None, survey_service=None):
        self.logger = logger
        self.service = service
        self.survey_service = survey_service

    def login(self, request):
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

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'username and password is required to log into application',
                'response':{}
            }, 400)

        username = body_params['username'] if 'username' in body_params else None
        password = body_params['password'] if 'password' in body_params else None

        if username is None or password is None:
            return ApiResponse.failure({
                'message':'username and password is required to log into application',
                'response': {}
            }, 400)

        try:
            user = self.service.login(username, password)
        except LookupError as error:
            self.logger.error('Error Occurred: {error}'.format(error=error))
            return ApiResponse.failure({
                'message': 'You are not authorized to login',
                'response': {}
            }, 401)

        if user is None:
            return ApiResponse.failure({
                'message': 'You are not authorized to login',
                'response': {}
            }, 401)

        last_login_time = datetime.datetime.now() #.strftime("%Y-%m-%d %H:%M:%S")
        # pylint: disable=unused-variable,invalid-name
        ip, routable = get_client_ip(request)
        if ip is not None:
            # update the ip_address here for user
            pass

        # Return user object on successful login
        return ApiResponse.success({
            'code': 200,
            'message': 'successfully logged in',
            'response': user
        })

    def get_users(self, request):
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

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'username and password is required to log into application',
                'response':{}
            }, 400)

        username = body_params['username'] if 'username' in body_params else None
        password = body_params['password'] if 'password' in body_params else None

        if username is None or password is None:
            return ApiResponse.failure({
                'message':'username and password is required to log into application',
                'response': {}
            }, 400)

        try:
            user = self.service.login(username, password)
        except LookupError as error:
            self.logger.error('Error Occurred: {error}'.format(error=error))
            return ApiResponse.failure({
                'message': 'You are not authorized to login',
                'response': {}
            }, 401)

        if user is None:
            return ApiResponse.failure({
                'message': 'You are not authorized to login',
                'response': {}
            }, 401)

        # Return user object on successful login
        return ApiResponse.success({
            'code': 200,
            'message': 'successfully logged in',
            'response': user
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

