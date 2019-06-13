"""NamedEntity Service"""

from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities
from app.models.named_entity_model import NamedEntity
from app.helpers.sql import Sql

class NamedEntityService:
    """NamedEntity Service"""

    def __init__(self, logger=None):
        self.logger = logger
        try:
            NamedEntity.create_table() # create the table for the named_entity
        except Exception:
            self.logger.error('Error occurred while creating NamedEntity table')

    def get_named_entity(self, entity_id=None):
        """Gets named_entities on this services (useful when managing named_entity accounts).

        Arguments:
            entity_id {str} -- id of the named_entity to find

        Returns:
            dict -- the named_entity object or an None
        """
        if entity_id is None:
            raise ValueError('id of named_entity to fetch cannot be None')

        try:
            named_entity = NamedEntity.select().where(NamedEntity.entity_id == str(entity_id)).get()
            return Utilities.convert_uuid_fields(model_to_dict(named_entity))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('NamedEntity does not exists on this service')

        return None


    def get_named_entities(self, offset=None, limit=True):
        """Gets named_entities on this services (useful when managing named_entities).

        Arguments:
            offset {int} -- offset to start fetching the record
            limit {int} -- limit of the data to return

        Returns:
            List -- the list of named_entity objects or an empty list
        """

        try:
            named_entities = NamedEntity.select()
            return Utilities.convert_uuid_fields(model_to_dict(named_entities))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Error while fetching all named_entities on this service')

        return {}


    def add_named_entity(self, data=None, entity_id=None):
        """Adds a new NamedEntity on the service.

        Arguments:
            data {dict} -- the data for the new named_entity
            entity_id {string} -- the id of named_entity to add if available

        Returns:
            object -- the added named_entity object or None
        """

        if data is None:
            raise ValueError('named_entity data cannot be None or empty')

        if entity_id is None:
            entity_id = Utilities.generate_id() # generate an uuid for this record

        data['entity_id'] = entity_id # set the entity_id for this record

        try:
            saved_entity = NamedEntity.create(**data)
            return model_to_dict(saved_entity)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise ValueError('Unable to save the named_entity object')

        return None


    def update_named_entity(self, entity_id=None, data=None):
        """Updates the NamedEntity on the service.

        Arguments:
            entity_id {string} -- the id of named_entity to update (required)
            data {dict} -- the new update data for the named_entity

        Returns:
            object -- the added named_entity object or None
        """

        if entity_id is None:
            raise ValueError('named_entity id to update cannot be None')

        if data is None:
            raise ValueError('named_entity data cannot be None or empty')

        try:
            updated_rows = NamedEntity.update(**data).where(NamedEntity.entity_id == entity_id).execute()
            return updated_rows > 0
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Update Error: NamedEntity does not exists on this service')

        return False

    def delete_named_entity(self, entity_id=None):
        """Deletes the named_entity with the entity_id from this service.

        Arguments:
            entity_id {string} -- the id of named_entity to delete

        Returns:
            boolean -- true / false
        """

        if entity_id is None:
            raise ValueError('id of named_entity to delete cannot be None')

        try:
            deleted_rows = NamedEntity.delete().where(NamedEntity.entity_id == entity_id).execute()
            return deleted_rows > 0
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('NamedEntity does not exists on this service')

        return False
