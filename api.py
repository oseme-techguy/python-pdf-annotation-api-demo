"""PDF Annotation API application - entrypoint."""

from app import webhandlers
from app import Application, Controllers#, run_api
from sanic_jwt import initialize


def run_api(application, app_controllers=None):
    """Run the web application API
    Arguments:
        application -- The injected application
    """
    web_api = application.webapi()
    initialize(
        web_api,
        authenticate=app_controllers.user().login,
        path_to_authenticate='/login'
    )

    web_api.add_route(webhandlers.index, '/')

    """
        Users Endpoint
    """
    # web_api.add_route(app_controllers.user().login, '/login', methods=['POST']) # Login
    web_api.add_route(app_controllers.user().get_users, '/users/<user_id>', methods=['GET']) # get one
    web_api.add_route(app_controllers.user().get_users, '/users', methods=['GET']) # get all
    web_api.add_route(app_controllers.user().add_users, '/users', methods=['POST']) # add user
    web_api.add_route(app_controllers.user().update_users, '/users/<user_id>', methods=['PATCH']) # patch user
    web_api.add_route(app_controllers.user().delete_users, '/users', methods=['DELETE']) # delete user


    """
        Documents Endpoint
    """
    web_api.add_route(app_controllers.document().get_documents, '/documents/<document_id>', methods=['GET']) # get one
    web_api.add_route(app_controllers.document().get_documents, '/documents', methods=['GET']) # get all
    web_api.add_route(app_controllers.document().upload_documents, '/documents', methods=['POST']) # upload document
    web_api.add_route(app_controllers.document().update_documents, '/documents/<document_id>', methods=['PATCH']) # patch
    web_api.add_route(app_controllers.document().delete_documents, '/documents', methods=['DELETE']) # delete

    """
        Annotations Endpoint
    """
    web_api.add_route(app_controllers.annotation().get_annotations, '/annotations/<annotation_id>', methods=['GET'])
    web_api.add_route(app_controllers.annotation().get_annotations, '/annotations', methods=['GET'])
    web_api.add_route(app_controllers.annotation().get_document_annotations, '/documents/<document_id>/annotations', methods=['GET'])
    web_api.add_route(app_controllers.annotation().add_annotions, '/documents/<document_id>/annotations', methods=['POST'])
    web_api.add_route(app_controllers.annotation().update_annotations, '/annotations/<annotation_id>', methods=['PATCH'])
    web_api.add_route(app_controllers.annotation().delete_annotations, '/annotations', methods=['DELETE'])

    """
        Named Entities Endpoint
    """
    web_api.add_route(app_controllers.named_entity().get_entities, '/named-entities/<entity_id>', methods=['GET'])
    web_api.add_route(app_controllers.named_entity().get_entities, '/named-entities', methods=['GET'])
    web_api.add_route(app_controllers.named_entity().add_entities, '/named-entities', methods=['POST'])
    web_api.add_route(app_controllers.named_entity().update_entities, '/named-entities/<entity_id>', methods=['PATCH'])
    web_api.add_route(app_controllers.named_entity().delete_entities, '/named-entities', methods=['DELETE'])

    web_api.run(
        host=application.config.api.host(),
        port=application.config.api.port(),
        debug=application.config.api.debug(),
    )

if __name__ == '__main__':
    APP = Application()
    CONTROLLERS = Controllers()
    run_api(APP, CONTROLLERS)
