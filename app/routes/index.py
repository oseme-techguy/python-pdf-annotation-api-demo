"""PDF Annotation API - web request handlers."""

from sanic import response

# pylint: disable=W0613
async def index(request):
    """Index request handler."""
    return response.text("Welcome to the PDF Annotation API")
