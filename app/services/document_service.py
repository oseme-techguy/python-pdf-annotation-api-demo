"""Document Service"""

from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities
from app.models.document_model import Document
from app.helpers.sql import Sql

class DocumentService:
    """Document Service"""

    def __init__(self, logger=None):
        self.logger = logger
        try:
            Document.create_table() # create the table for the document
        except Exception:
            self.logger.error('Error occurred while creating Document table')

    def get_document(self, document_id=None):
        """Gets documents on this services (useful when managing document accounts).

        Arguments:
            document_id {str} -- id of the document to find

        Returns:
            dict -- the document object or an None
        """
        if document_id is None:
            raise ValueError('id of document to fetch cannot be None')

        try:
            document = Document.select().where(Document.ref_id == str(document_id)).get()
            return Utilities.convert_uuid_fields(model_to_dict(document))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Document does not exists on this service')

        return None


    def get_documents(self, offset=None, limit=True):
        """Gets documents on this services (useful when managing document accounts).

        Arguments:
            offset {int} -- offset to start fetching the record
            limit {int} -- limit of the data to return

        Returns:
            List -- the list of document objects or an empty list
        """

        try:
            documents = Document.select()
            return Utilities.convert_uuid_fields(model_to_dict(documents))
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Error while fetching all documents on this service')

        return {}


    def upload_document(self, data=None, document_id=None):
        """Adds a new Document on the service.

        Arguments:
            data {dict} -- the data for the new document
            document_id {string} -- the id of document to add if available

        Returns:
            object -- the added document object or None
        """

        if data is None:
            raise ValueError('document data cannot be None or empty')

        if document_id is None:
            document_id = Utilities.generate_id() # generate an uuid for this record

        data['ref_id'] = document_id # set the document_id for this record

        try:
            saved_document = Document.create(**data)
            return model_to_dict(saved_document)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise ValueError('Unable to save the document object')

        return None


    def update_document(self, document_id=None, data=None):
        """Updates the Document on the service.

        Arguments:
            document_id {string} -- the id of document to update (required)
            data {dict} -- the new update data for the document

        Returns:
            object -- the added document object or None
        """

        if document_id is None:
            raise ValueError('document id to update cannot be None')

        if data is None:
            raise ValueError('document data cannot be None or empty')

        try:
            updated_rows = Document.update(**data).where(Document.document_id == document_id).execute()
            return updated_rows > 0
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Update Error: Document does not exists on this service')

        return False

    def delete_document(self, document_id=None):
        """Deletes the document with the document_id from this service.

        Arguments:
            document_id {string} -- the id of document to delete

        Returns:
            boolean -- true / false
        """

        if document_id is None:
            raise ValueError('id of document to delete cannot be None')

        try:
            deleted_rows = Document.delete().where(Document.document_id == document_id).execute()
            return deleted_rows > 0
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            raise LookupError('Document does not exists on this service')

        return False
