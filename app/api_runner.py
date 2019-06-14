"""PDF Annotation API - runner."""

from sanic_jwt import initialize

def run_api(application, user_controller):
    """Run the web application API
    Arguments:
        application -- The injected application
    """
    web_api = application.webapi
    initialize(web_api, authenticate=user_controller().login)

    web_api.add_route(application.index_webhandler, '/')
    # web_api.add_route(application.login_webhandler, '/login', methods=['POST'])

    # User Endpoints
    web_api.add_route(application.get_user_webhandler, '/users/<user_id>', methods=['GET'])
    # web_api.add_route(application.get_users_webhandler, '/users', methods=['GET'])
    # web_api.add_route(application.create_user_webhandler, '/users', methods=['POST'])
    web_api.add_route(application.patch_user_webhandler, '/users/<user_id>', methods=['PATCH'])
    web_api.add_route(application.delete_user_webhandler, '/users', methods=['DELETE'])

    # Document Endpoints
    web_api.add_route(application.get_document_webhandler, '/documents/<document_id>', methods=['GET'])
    web_api.add_route(application.get_documents_webhandler, '/documents', methods=['GET'])
    web_api.add_route(application.create_document_webhandler, '/documents', methods=['POST'])
    web_api.add_route(application.patch_document_webhandler, '/documents/<document_id>', methods=['PATCH'])
    web_api.add_route(application.delete_document_webhandler, '/documents', methods=['DELETE'])

    # Annotation Endpoints
    web_api.add_route(application.get_annotation_webhandler, '/annotations/<annotation_id>', methods=['GET'])
    web_api.add_route(application.get_annotations_webhandler, '/annotations', methods=['GET'])
    web_api.add_route(application.get_document_annotations_webhandler, '/documents/<document_id>/annotations', methods=['GET'])
    web_api.add_route(application.create_annotation_webhandler, '/documents/<document_id>/annotations', methods=['POST'])
    web_api.add_route(application.patch_annotation_webhandler, '/annotations/<annotation_id>', methods=['PATCH'])
    web_api.add_route(application.delete_annotation_webhandler, '/annotations', methods=['DELETE'])

    # NamedEntity Endpoints
    web_api.add_route(application.get_named_entity_webhandler, '/named-entities/<entity_id>', methods=['GET'])
    web_api.add_route(application.get_named_entities_webhandler, '/named-entities', methods=['GET'])
    web_api.add_route(application.create_named_entity_webhandler, '/named-entities', methods=['POST'])
    web_api.add_route(application.patch_named_entity_webhandler, '/named-entities/<entity_id>', methods=['PATCH'])
    web_api.add_route(application.delete_named_entity_webhandler, '/named-entities', methods=['DELETE'])

    web_api.run(
        host=application.config.api.host(),
        port=application.config.api.port(),
        debug=application.config.api.debug(),
    )
