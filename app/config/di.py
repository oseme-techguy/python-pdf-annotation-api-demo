"""
Application DI class
"""
import logging
from sys import stdout
from sanic import Sanic
from dependency_injector import containers, providers
from app import webhandlers
from app.services import UserService, DocumentService, AnnotationService, NamedEntityService, NominatimService
import app.controllers
from . import settings


class Core(containers.DeclarativeContainer):
    """IoC container of core component providers."""
    config = providers.Configuration('config')

    logger = providers.Singleton(logging.Logger, name='api_logger')
    # configure logger
    logger().setLevel(logging.DEBUG)
    logFormatter = logging.Formatter\
    ("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    consoleHandler = logging.StreamHandler(stdout)
    consoleHandler.setFormatter(logFormatter)
    logger().addHandler(consoleHandler)

# pylint: disable=no-member
class Databases(containers.DeclarativeContainer):
    """IoC container for databases"""

    # Connect to a MySQL database on network.
    # sql_db = MySQLDatabase('my_app', user='app', password='db_password',
    #                      host='10.1.0.8', port=3316)
    # sql_db = providers.Singleton(MySQLDatabase,
    #                              host=Core.config.sql.connection.host,
    #                              port=Core.config.sql.connection.port,
    #                              user=Core.config.sql.connection.user,
    #                              password=Core.config.sql.connection.password,
    #                              database=Core.config.sql.connection.database)
    # Core.logger().info('Sql Database connected')


class Services(containers.DeclarativeContainer):
    """IoC container for services"""

    user = providers.Factory(UserService, logger=Core.logger)

    document = providers.Factory(DocumentService, logger=Core.logger)

    annotation = providers.Factory(AnnotationService, logger=Core.logger)

    named_entity = providers.Factory(NamedEntityService, logger=Core.logger)

    nominatim = providers.Factory(NominatimService, logger=Core.logger)


class Controllers(containers.DeclarativeContainer):
    """IoC container for controllers"""

    user = providers.Factory(app.controllers.User,
                             logger=Core.logger,
                             service=Services.user)

    document = providers.Factory(app.controllers.Document,
                             logger=Core.logger,
                             service=Services.document,
                             nominatim_service=Services.nominatim)

    annotation = providers.Factory(app.controllers.Annotation,
                             logger=Core.logger,
                             service=Services.annotation)

    named_entity = providers.Factory(app.controllers.NamedEntity,
                             logger=Core.logger,
                             service=Services.named_entity)

class Application(containers.DeclarativeContainer):
    """
    Application components container
    """

    Core.config.override(settings.SETTINGS)

    webapi = providers.Factory(Sanic, __name__)
    config = Core.config


    index_webhandler = providers.Callable(
        webhandlers.index
    )

    """
        Users Endpoint
    """
    login_webhandler = providers.Callable(Controllers.user().login) # Login
    get_user_webhandler = providers.Callable(Controllers.user().get_users) # get one
    get_users_webhandler = providers.Callable(Controllers.user().get_users) # get all
    create_user_webhandler = providers.Callable(Controllers.user().add_users) # add user
    patch_user_webhandler = providers.Callable(Controllers.user().update_users) # patch user
    delete_user_webhandler = providers.Callable(Controllers.user().delete_users) # delete user

    """
        Documents Endpoint
    """
    get_document_webhandler = providers.Callable(Controllers.document().get_documents) # get one
    get_documents_webhandler = providers.Callable(Controllers.document().get_documents) # get all
    create_document_webhandler = providers.Callable(Controllers.document().upload_documents) # upload document
    patch_document_webhandler = providers.Callable(Controllers.document().update_documents) # patch
    delete_document_webhandler = providers.Callable(Controllers.document().delete_documents) # delete

    """
        Annotations Endpoint
    """
    get_annotation_webhandler = providers.Callable(Controllers.annotation().get_annotations) # get one
    get_annotations_webhandler = providers.Callable(Controllers.annotation().get_annotations) # get all
    create_annotation_webhandler = providers.Callable(Controllers.annotation().add_annotions) # post
    patch_annotation_webhandler = providers.Callable(Controllers.annotation().update_annotations) # patch
    delete_annotation_webhandler = providers.Callable(Controllers.annotation().delete_annotations) # delete

    """
        Named Entities Endpoint
    """
    get_named_entity_webhandler = providers.Callable(Controllers.named_entity().get_entities) # get one
    get_named_entities_webhandler = providers.Callable(Controllers.named_entity().get_entities) # get all
    create_named_entity_webhandler = providers.Callable(Controllers.named_entity().add_entities) # post
    patch_named_entity_webhandler = providers.Callable(Controllers.named_entity().update_entities) # patch
    delete_named_entity_webhandler = providers.Callable(Controllers.named_entity().delete_entities) # delete
