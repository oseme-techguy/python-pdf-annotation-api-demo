"""PDF Annotation API application - named entities routes."""

from sanic_jwt import protected


def set_named_entities_routes(web_api, controller):
    """
        Named Entities Endpoint
    """

    @web_api.route('/named-entities/<entity_id>', methods=['GET']) # get one
    @protected()
    def get_entity(request, *args, **kwargs):
        return controller.get_entities(request, *args, **kwargs)

    @web_api.route('/named-entities', methods=['GET']) # get all
    @protected()
    def get_entities(request, *args, **kwargs):
        return controller.get_entities(request, *args, **kwargs)

    @web_api.route('/named-entities', methods=['POST']) # post
    @protected()
    def add_entities(request, *args, **kwargs):
        return controller.add_entities(request, *args, **kwargs)

    @web_api.route('/named-entities/<entity_id>', methods=['PATCH']) # patch
    @protected()
    def update_entities(request, *args, **kwargs):
        return controller.update_entities(request, *args, **kwargs)

    @web_api.route('/named-entities', methods=['DELETE']) # delete
    @protected()
    def delete_entities(request, *args, **kwargs):
        return controller.delete_entities(request, *args, **kwargs)
