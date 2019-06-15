"""PDF Annotation API application - annotation routes."""

from sanic_jwt import protected


def set_annotation_routes(web_api, controller):
    """
        Annotations Endpoint
    """

    @web_api.route('/annotations/<annotation_id>', methods=['GET']) # get one
    @protected()
    def get_annotation(request, *args, **kwargs):
        return controller.get_annotations(request, *args, **kwargs)

    @web_api.route('/annotations', methods=['GET']) # get all
    @protected()
    def get_annotations(request, *args, **kwargs):
        return controller.get_annotations(request, *args, **kwargs)

    @web_api.route('/documents/<document_id>/annotations', methods=['GET']) # get all
    @protected()
    def get_document_annotations(request, *args, **kwargs):
        return controller.get_document_annotations(request, *args, **kwargs)

    @web_api.route('/documents/<document_id>/annotations', methods=['POST']) # post
    @protected()
    def add_annotations(request, *args, **kwargs):
        return controller.add_annotations(request, *args, **kwargs)

    @web_api.route('/annotations/<annotation_id>', methods=['PATCH']) # patch
    @protected()
    def update_annotations(request, *args, **kwargs):
        return controller.update_annotations(request, *args, **kwargs)

    @web_api.route('/annotations', methods=['DELETE']) # delete
    @protected()
    def delete_annotations(request, *args, **kwargs):
        return controller.delete_annotations(request, *args, **kwargs)
