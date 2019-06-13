"""User Service"""

from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities
from app.models.user_model import User
from app.helpers.sql import Sql

class UserService:
    """User Service"""

    def __init__(self, logger=None, sql=None):
        self.logger = logger
        self.sql = Sql(sql, User)


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
            raise LookupError('the username cannot be None')

        if password is None:
            raise LookupError('the password cannot be None')

        return None


    def get_users(self, offset=None, limit=True):
        """Gets users on this services (useful when managing user accounts).

        Arguments:
            offset {int} -- offset to start fetching the record
            limit {int} -- limit of the data to return

        Returns:
            List -- the list of user objects or an empty list
        """
        return {}


    def add_user(self, data=None, user_id=None):
        """Adds a new User on the service.

        Arguments:
            data {dict} -- the data for the new user
            user_id {string} -- the id of user to add if available

        Returns:
            object -- the added user object or None
        """

        if data is None:
            raise LookupError('user data cannot be None or empty')

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
            raise LookupError('user id to update cannot be None')

        if data is None:
            raise LookupError('user data cannot be None or empty')

        return None

    def delete_user(self, user_id=None):
        """Deletes the user with the user_id from this service.

        Arguments:
            user_id {string} -- the id of user to delete

        Returns:
            boolean -- true / false
        """

        if user_id is None:
            raise LookupError('if of user to delete cannot be None')

        return False

