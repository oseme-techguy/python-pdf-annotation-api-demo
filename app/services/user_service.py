"""User Service"""

import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities
from app.models.user_model import User
from app.helpers.sql import Sql

class UserService:
    """User Service"""

    def __init__(self, logger=None):
        self.logger = logger
        try:
            User.create_table() # create the table for the user
        except Exception:
            self.logger.error('Error occurred while creating User table')


    def login(self, username=None, password=True):
        """Checks whether the user with the username and password can log
            into the application.

        Arguments:
            username {string} -- Username of user
            password {string} -- Password of user

        Returns:
            object -- the user object or None
        """

        if username is None:
            raise ValueError('the username cannot be None')

        if password is None:
            raise ValueError('the password cannot be None')

        # Todo: finish up the login
        try:
            user = User.select().where(User.username == str(username)).get()
            return Utilities.convert_unserializable_fields(model_to_dict(user))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('User does not exists on this service')

        return None


    def get_user(self, user_id=None):
        """Gets users on this services (useful when managing user accounts).

        Arguments:
            user_id {str} -- id of the user to find

        Returns:
            dict -- the user object or an None
        """
        if user_id is None:
            raise ValueError('id of user to fetch cannot be None')

        try:
            user = User.select().where(User.user_id == str(user_id)).get()
            return Utilities.convert_unserializable_fields(model_to_dict(user))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('User does not exists on this service')

        return None


    def get_users(self, offset=None, limit=True):
        """Gets users on this services (useful when managing user accounts).

        Arguments:
            offset {int} -- offset to start fetching the record
            limit {int} -- limit of the data to return

        Returns:
            List -- the list of user objects or an empty list
        """
        all_users = []
        try:
            users = User.select()
            for user in users:
                all_users \
                    .append(Utilities.convert_unserializable_fields(model_to_dict(user)))
            return all_users
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Error while fetching all users on this service')

        return []


    def add_user(self, data=None, user_id=None):
        """Adds a new User on the service.

        Arguments:
            data {dict} -- the data for the new user
            user_id {string} -- the id of user to add if available

        Returns:
            object -- the added user object or None
        """

        if data is None:
            raise ValueError('user data cannot be None or empty')

        if user_id is None:
            user_id = Utilities.generate_id() # generate an uuid for this record

        data['user_id'] = user_id # set the user_id for this record

        try:
            saved_user = User.create(**data)
            return model_to_dict(saved_user)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise ValueError('Unable to save the user object')

        return None


    def update_user(self, user_id=None, data=None):
        """Updates the User on the service.

        Arguments:
            user_id {string} -- the id of user to update (required)
            data {dict} -- the new update data for the user

        Returns:
            object -- the added user object or None
        """

        if user_id is None:
            raise ValueError('user id to update cannot be None')

        if data is None:
            raise ValueError('user data cannot be None or empty')

        data['last_modified_at'] = datetime.datetime.now()

        try:
            updated_rows = User.update(**data).where(User.user_id == user_id).execute()
            return updated_rows > 0
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Update Error: User does not exists on this service')

        return False

    def delete_user(self, user_id=None):
        """Deletes the user with the user_id from this service.

        Arguments:
            user_id {string} -- the id of user to delete

        Returns:
            boolean -- true / false
        """

        if user_id is None:
            raise ValueError('id of user to delete cannot be None')

        try:
            deleted_rows = User.delete().where(User.user_id == user_id).execute()
            return deleted_rows > 0
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('User does not exists on this service')

        return False
