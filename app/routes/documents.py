"""PDF Annotation API application - document routes."""

from sanic_jwt import protected


def set_document_routes(web_api, controller):
    """
        Documents Endpoint
    """

    @web_api.route('/documents/<document_id>', methods=['GET']) # get one
    @protected()
    def get_document(request, *args, **kwargs):
        return controller.get_documents(request, *args, **kwargs)

    @web_api.route('/documents', methods=['GET']) # get all
    @protected()
    def get_documents(request, *args, **kwargs):
        return controller.get_documents(request, *args, **kwargs)

    @web_api.route('/documents', methods=['POST']) # upload document
    @protected()
    def upload_documents(request, *args, **kwargs):
        return controller.upload_documents(request, *args, **kwargs)

    @web_api.route('/documents/<document_id>', methods=['PATCH']) # patch
    @protected()
    def update_documents(request, *args, **kwargs):
        return controller.update_documents(request, *args, **kwargs)

    @web_api.route('/documents', methods=['DELETE']) # delete
    @protected()
    def delete_documents(request, *args, **kwargs):
        return controller.delete_documents(request, *args, **kwargs)
