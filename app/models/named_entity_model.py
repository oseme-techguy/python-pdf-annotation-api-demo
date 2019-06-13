"""NamedEntity Model"""

import datetime
import peewee as pw
from app.models.base_model import BaseModel
from app.models.user_model import User
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS


class NamedEntity(BaseModel):
    """NamedEntity Model for the SQL db"""

    entity_id = pw.UUIDField(primary_key=True, unique=True)

    value = pw.CharField(unique=True)

    description = pw.TextField()

    user_id = pw.ForeignKeyField(User, backref='users')

    should_use = pw.BooleanField()

    created_at = pw.DateTimeField(default=datetime.datetime.now)

    last_modified_at = pw.DateTimeField()


    class Meta:
        table_name = SETTINGS['sql']['tables']['named_entities']
