"""Annotation Model"""

import datetime
import peewee as pw
from app.models.base_model import BaseModel
from app.models.document_model import Document
from app.models.user_model import User
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS


class Annotation(BaseModel):
    """Annotation Model for the SQL db"""

    annotation_id = pw.UUIDField(primary_key=True, unique=True)

    document_id = pw.ForeignKeyField(Document, backref='documents')

    user_id = pw.ForeignKeyField(User, backref='users')

    data = pw.TextField()

    version_number = pw.IntegerField()

    is_deleted = pw.BooleanField(default=False)

    created_at = pw.DateTimeField(default=datetime.datetime.now)

    last_modified_at = pw.DateTimeField()


    class Meta:
        table_name = SETTINGS['sql']['tables']['annotations']
