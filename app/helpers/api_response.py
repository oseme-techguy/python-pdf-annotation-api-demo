"""API Responses
"""
from sanic import response

class ApiResponse:
    """API Response Helper class
    """

    @staticmethod
    def respond(data, http_code):
        data = {
            'error': data['error'],
            'code': http_code,
            'message': data['message'],
            'response': data['response'],
        }
        return response.json(data, status=http_code)

    @staticmethod
    def success(data, status=200):
        response_data = data
        response_data['error'] = False
        return ApiResponse.respond(response_data, status)

    @staticmethod
    def failure(data, status=503):
        response_data = data
        response_data['error'] = True
        return ApiResponse.respond(response_data, status)
