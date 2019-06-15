"""PDF Annotation API application - entrypoint."""

from sanic_jwt import protected
from sanic_jwt import initialize
from app import Application, Controllers
from app.routes import index
from app.routes import users
from app.routes import documents
from app.routes import annotations
from app.routes import named_entities


def run_api(application, app_controllers=None):
    """Run the web application API
    Arguments:
        application -- The injected application
    """
    web_api = application.webapi()
    initialize(
        web_api,
        authenticate=app_controllers.user().login
    )

    web_api.add_route(index, '/')
    users.set_user_routes(web_api, app_controllers.user())
    documents.set_document_routes(web_api, app_controllers.document())
    annotations.set_annotation_routes(web_api, app_controllers.annotation())
    named_entities.set_named_entities_routes(web_api, app_controllers.named_entity())

    web_api.run(
        host=application.config.api.host(),
        port=application.config.api.port(),
        debug=application.config.api.debug(),
    )

if __name__ == '__main__':
    APP = Application()
    CONTROLLERS = Controllers()
    run_api(APP, CONTROLLERS)
