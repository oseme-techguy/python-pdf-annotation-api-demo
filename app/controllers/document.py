"""Document Controller
"""
from sanic import response
from sanic_ipware import get_client_ip
from app.helpers import ApiResponse
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS
import time # used to control pausing of the consumer
import datetime
import json

class Document:
    """Document Controller"""

    def __init__(self, logger=None, service=None, nominatim_service=None):
        self.logger = logger
        self.service = service
        self.nominatim_service = nominatim_service

    def get_documents(self, request, document_id=None):
        """Fetches document(s) on the service
        - Receive and parse get request
        - Go into AWS RDS and fetch document(s)
        - Return success or not found
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        # query_params = request.raw_args
        # document_id = query_params['document_id'] if 'document_id' in query_params else None

        self.logger.info('Received get document request for id: {document_id}'.format(
            document_id=(document_id if document_id is not None else '')
        ))

        document = None
        documents = {}
        try:
            if document_id is None:
                documents = self.service.get_documents()
            else:
                document = self.service.get_document(document_id)
        except LookupError as error:
            self.logger.error('Error Occurred: {error}'.format(error=error))
            return ApiResponse.failure({
                'message': 'Error while fetching document(s)',
                'response': {}
            }, 500)

        if not documents and document is None:
            return ApiResponse.failure({
                'message': 'No document(s) found',
                'response': {}
            }, 404)

        return_data = document if document is not None else documents
        print(return_data)

        # Return document object on successful login
        return ApiResponse.success({
            'code': 200,
            'message': 'successfully fetched document(s) on service',
            'response': return_data
        })


    def upload_documents(self, request):
        """Verifies that the required fields are set in request
        - open db connection and parse get request
        - commit model to db
        - colse db connection
        - Return created document object
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

        self.logger.info('Received create document request: {params}'.format(
            params=body_params
        ))

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'document data cannot be null',
                'response':{}
            }, 400)

        pdf_content = body_params['pdf_content'] if 'pdf_content' in body_params else None
        user_id = body_params['user_id'] if 'user_id' in body_params else None

        document_data = {
            'pdf_content': pdf_content,
            'user_id': user_id,
        }

        try:
            document = self.service.upload_document(document_data)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while adding the new document. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if document is None:
            return ApiResponse.failure({
                'message': 'An error occured while adding the new document',
                'response': {}
            }, 500)

        # Return document object on successful login
        return ApiResponse.success({
            'code': 201,
            'message': 'document was successfully uploaded',
            'response': document
        }, 201)


    def update_documents(self, request):
        """Verifies that the required fields are set in request
        - open db connection and parse get/post request
        - update model within db
        - close db connection
        - Return updated document object
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        request_body = request.body
        query_params = request.raw_args
        body_params = {}
        if request_body != b'':
            body_params = json.loads(request_body)

        document_id = query_params['document_id'] if 'document_id' in query_params else None
        if document_id is None or document_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the document_id of the document to patch',
                'response': {}
            }, 400)

        self.logger.info('Received update document request for id: {document_id} // : {params}'.format(
            document_id=document_id,
            params=body_params
        ))

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'document data cannot be null',
                'response':{}
            }, 400)

        pdf_content = body_params['pdf_content'] if 'pdf_content' in body_params else None
        user_id = body_params['user_id'] if 'user_id' in body_params else None

        document_data = {
            'pdf_content': pdf_content,
            'user_id': user_id
        }

        try:
            document = self.service.update_document(document_id, document_data)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while updating the document. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if document is None:
            return ApiResponse.failure({
                'message': 'An error occured while updating the document',
                'response': {}
            }, 500)

        # Document has been successfully updated
        return ApiResponse.success({
            'code': 200,
            'message': 'document was successfully updated',
            'response': document
        }, 200)


    def delete_documents(self, request):
        """Verifies that the required fields are set in request
        - open db connection and parse get/post request
        - delete document where document_id in db
        - close db connection
        - Return successful or failed
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        query_params = request.raw_args
        document_id = query_params['document_id'] if 'document_id' in query_params else None

        if document_id is None or document_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the document_id of the document to patch',
                'response': {}
            }, 400)

        self.logger.info('Received delete document request for id: {document_id}'.format(
            document_id=document_id
        ))

        try:
            is_deleted = self.service.delete_document(document_id)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while deleting the document. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if is_deleted is False:
            return ApiResponse.failure({
                'message': 'An error occured while deleting the document',
                'response': {}
            }, 500)

        # Document has been successfully updated
        return ApiResponse.success({
            'code': 204,
            'message': 'document was successfully deleted',
            'response': {}
        }, 204)
