"""Document Model"""

import datetime
import peewee as pw
from app.models.base_model import BaseModel
from app.models.user_model import User
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS


class Document(BaseModel):
    """Document Model for the SQL db"""

    ref_id = pw.UUIDField(primary_key=True, unique=True)

    name = pw.CharField(unique=True)

    pdf_content = pw.TextField(null=False)

    user_id = pw.ForeignKeyField(User, backref='users')

    created_at = pw.DateTimeField(default=datetime.datetime.now)

    last_modified_at = pw.DateTimeField(null=True, default=None)


    class Meta:
        table_name = SETTINGS['sql']['tables']['documents']
