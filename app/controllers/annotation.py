"""Annotation Controller
"""
from sanic import response
from sanic_ipware import get_client_ip
from app.helpers import ApiResponse
from app.helpers.utilities import Utilities
from app.config.settings import SETTINGS
import time # used to control pausing of the consumer
import datetime
import json

class Annotation:
    """Annotation Controller"""

    def __init__(self, logger=None, service=None):
        self.logger = logger
        self.service = service

    def get_annotations(self, request, annotation_id=None):
        """Fetches annotation(s) on the service
        - Receive and parse get request
        - Go into AWS RDS and fetch annotation(s)
        - Return success or not found
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        # query_params = request.raw_args
        # annotation_id = query_params['annotation_id'] if 'annotation_id' in query_params else None

        self.logger.info('Received get annotation request for id: {annotation_id}'.format(
            annotation_id=(annotation_id if annotation_id is not None else '')
        ))

        annotation = None
        annotations = {}
        try:
            if annotation_id is None:
                annotations = self.service.get_annotations()
            else:
                annotation = self.service.get_annotation(annotation_id)
        except LookupError as error:
            self.logger.error('Error Occurred: {error}'.format(error=error))
            return ApiResponse.failure({
                'message': 'Error while fetching annotation(s)',
                'response': {}
            }, 500)

        if not annotations and annotation is None:
            return ApiResponse.failure({
                'message': 'No annotation(s) found',
                'response': {}
            }, 404)

        return_data = annotation if annotation is not None else annotations
        print(return_data)

        # Return annotation object on successful login
        return ApiResponse.success({
            'code': 200,
            'message': 'successfully fetched annotation(s) on service',
            'response': return_data
        })


    def get_document_annotations(self, request, document_id=None):
        """Fetches annotation(s) on the document on the service
        - Receive and parse get request
        - Go into AWS RDS and fetch annotation(s)
        - Return success or not found
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        self.logger.info('Received get annotations request for document_id: {document_id}'.format(
            document_id=(document_id if document_id is not None else '')
        ))

        try:
            annotations = self.service.get_annotations_in_document(document_id)
        except LookupError as error:
            self.logger.error('Error Occurred: {error}'.format(error=error))
            return ApiResponse.failure({
                'message': 'Error while fetching annotation(s)',
                'response': {}
            }, 500)

        if not annotations:
            return ApiResponse.failure({
                'message': 'No annotation(s) found on document',
                'response': {}
            }, 404)

        # Return annotation object on successful login
        return ApiResponse.success({
            'code': 200,
            'message': 'successfully fetched annotation(s) on document on service',
            'response': annotations
        })


    def add_annotations(self, request):
        """Verifies that the required fields are set in request
        - open db connection and parse get request
        - commit model to db
        - colse db connection
        - Return created annotation object
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

        self.logger.info('Received create annotation request: {params}'.format(
            params=body_params
        ))

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'annotation data cannot be null',
                'response':{}
            }, 400)

        document_id = body_params['document_id'] if 'document_id' in body_params else None
        user_id = body_params['user_id'] if 'user_id' in body_params else None
        data = body_params['data'] if 'data' in body_params else None

        annotation_data = {
            'document_id': document_id,
            'user_id': user_id,
            'data': json.dumps(data), # serialize the annotation data
        }

        try:
            annotation = self.service.add_annotation(annotation_data)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while adding the new annotation. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if annotation is None:
            return ApiResponse.failure({
                'message': 'An error occured while adding the new annotation',
                'response': {}
            }, 500)

        # Return annotation object on successful login
        return ApiResponse.success({
            'code': 201,
            'message': 'annotation was successfully created',
            'response': annotation
        }, 201)


    def update_annotations(self, request, annotation_id=None):
        """Verifies that the required fields are set in request
        - open db connection and parse get/post request
        - update model within db
        - close db connection
        - Return updated annotation object
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

        if annotation_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the annotation_id of the annotation to patch',
                'response': {}
            }, 400)

        self.logger.info(
            'Received update annotation request for id: {annotation_id} // : {params}' \
                .format(
                    annotation_id=annotation_id,
                    params=body_params
                ))

        if not body_params.keys():
            return ApiResponse.failure({
                'message':'annotation data cannot be null',
                'response':{}
            }, 400)

        document_id = body_params['document_id'] if 'document_id' in body_params else None
        user_id = body_params['user_id'] if 'user_id' in body_params else None
        data = body_params['data'] if 'data' in body_params else None

        annotation_data = {}

        if document_id is not None:
            annotation_data['document_id'] = document_id
        if user_id is not None:
            annotation_data['user_id'] = user_id
        if data is not None:
            annotation_data['data'] = json.dumps(data) # serialize the annotation data

        try:
            annotation = self.service.update_annotation(annotation_id, annotation_data)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while updating the annotation. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if annotation is None:
            return ApiResponse.failure({
                'message': 'An error occured while updating the annotation',
                'response': {}
            }, 500)

        # Annotation has been successfully updated
        return ApiResponse.success({
            'code': 200,
            'message': 'annotation was successfully updated',
            'response': annotation
        }, 200)


    def delete_annotations(self, request, annotation_id=None):
        """Verifies that the required fields are set in request
        - open db connection and parse get/post request
        - delete annotation where annotation_id in db
        - close db connection
        - Return successful or failed
        - end

        Arguments:
            request {object} -- the query parameters passed into this function

        Returns:
            object -- response from this endpoint
        """

        # query_params = request.raw_args
        # annotation_id = query_params['annotation_id'] if 'annotation_id' in query_params else None

        if annotation_id is None:
            return ApiResponse.failure({
                'message': 'Kindly pass the annotation_id of the annotation to patch',
                'response': {}
            }, 400)

        self.logger.info('Received delete annotation request for id: {annotation_id}'.format(
            annotation_id=annotation_id
        ))

        try:
            is_deleted = self.service.delete_annotation(annotation_id)
        except Exception as err:
            self.logger.error('Error Occurred: {error}'.format(error=err))
            return ApiResponse.failure({
                'message': 'Error occured while deleting the annotation. ' +
                           'Error: {error}'.format(error=err),
                'response': {}
            }, 500)

        if is_deleted is False:
            return ApiResponse.failure({
                'message': 'An error occured while deleting the annotation',
                'response': {}
            }, 500)

        # Annotation has been successfully updated
        return ApiResponse.success({
            'code': 204,
            'message': 'annotation was successfully deleted',
            'response': {}
        }, 204)
