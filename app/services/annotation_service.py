"""Annotation Service"""

from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities
from app.models.annotation_model import Annotation
from app.helpers.sql import Sql

class AnnotationService:
    """Annotation Service"""

    def __init__(self, logger=None):
        self.logger = logger
        try:
            Annotation.create_table() # create the table for the annotation
        except Exception:
            self.logger.error('Error occurred while creating Annotation table')


    def get_annotation(self, annotation_id=None):
        """Gets annotations on this services (useful when managing annotation accounts).

        Arguments:
            annotation_id {str} -- id of the annotation to find

        Returns:
            dict -- the annotation object or an None
        """
        if annotation_id is None:
            raise ValueError('id of annotation to fetch cannot be None')

        try:
            annotation = Annotation.select().where(Annotation.annotation_id == str(annotation_id)).get()
            return Utilities.convert_uuid_fields(model_to_dict(annotation))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Annotation does not exists on this service')

        return None

    
    def get_annotations(self, offset=None, limit=True):
        """Gets annotations on this services (useful when managing annotation accounts).

        Arguments:
            offset {int} -- offset to start fetching the record
            limit {int} -- limit of the data to return

        Returns:
            List -- the list of annotation objects or an empty list
        """

        try:
            annotations = Annotation.select()
            return Utilities.convert_uuid_fields(model_to_dict(annotations))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Error while fetching all annotations on this service')

        return {}


    def get_annotations_in_document(self, document_id=None):
        """Gets annotations on document on this services (useful when managing annotation accounts).

        Arguments:
            document_id {str} -- id of the document

        Returns:
            dict -- the list of annotation objects or an None
        """
        if document_id is None:
            raise ValueError('id of document cannot be None')

        try:
            annotations = Annotation.select().where(Annotation.document_id == str(document_id)).get()
            return Utilities.convert_uuid_fields(model_to_dict(annotations))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Annotations does not exists on this document')

        return None


    def add_annotation(self, data=None, document_id=None):
        """Adds a new Annotation to a document on the service.

        Arguments:
            data {dict} -- the data for the new annotation
            document_id {string} -- the id of document to add the annotation to

        Returns:
            object -- the added annotation object or None
        """

        if data is None:
            raise ValueError('annotation data cannot be None or empty')

        if document_id is None:
            raise ValueError('document_id cannot be None or empty')

        if data['annotation_id'] is None:
            annotation_id = Utilities.generate_id() # generate an uuid for this record

        data['annotation_id'] = annotation_id # set the annotation_id for this record
        data['annotation_id'] = 0; # default version is 0

        try:
            saved_annotation = Annotation.create(**data)
            return model_to_dict(saved_annotation)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise ValueError('Unable to save the annotation object')

        return None


    def update_annotation(self, annotation_id=None, data=None):
        """Updates the Annotation on the service.

        Arguments:
            annotation_id {string} -- the id of annotation to update (required)
            data {dict} -- the new update data for the annotation

        Returns:
            object -- the added annotation object or None
        """

        if annotation_id is None:
            raise ValueError('annotation id to update cannot be None')

        if data is None:
            raise ValueError('annotation data cannot be None or empty')

        try:
            updated_rows = Annotation.update(**data).where(Annotation.annotation_id == annotation_id).execute()
            return updated_rows > 0
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Update Error: Annotation does not exists on this service')

        return False

    def delete_annotation(self, annotation_id=None):
        """Deletes the annotation with the annotation_id from this service.

        Arguments:
            annotation_id {string} -- the id of annotation to delete

        Returns:
            boolean -- true / false
        """

        if annotation_id is None:
            raise ValueError('id of annotation to delete cannot be None')

        try:
            deleted_rows = Annotation.delete().where(Annotation.annotation_id == annotation_id).execute()
            return deleted_rows > 0
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Annotation does not exists on this service')

        return False
