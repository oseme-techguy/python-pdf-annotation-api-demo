"""User Model"""

import datetime
import peewee as pw
from app.models.base_model import BaseModel
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS


class User(BaseModel):
    """User Model for the SQL db"""

    user_id = pw.UUIDField(primary_key=True, unique=True)

    username = pw.CharField(unique=True, null=False, max_length=50)

    password = pw.CharField(null=False, max_length=130)

    first_name = pw.CharField(null=True, max_length=100)

    last_name = pw.CharField(null=True, max_length=100)

    role = pw.SmallIntegerField(null=False, default=0) # 0 - Analysts, 1 - Managers

    ip_address = pw.CharField(null=True, default=None, max_length=50)

    last_login_time = pw.DateTimeField(null=True, default=None)

    created_at = pw.DateTimeField(default=datetime.datetime.now)

    last_modified_at = pw.DateTimeField(null=True, default=None)

    """
        Meta definition for the table
    """
    class Meta:
        table_name = SETTINGS['sql']['tables']['users']
