"""
Application DI class
"""
import logging
from sys import stdout
from sanic import Sanic
from dependency_injector import containers, providers
from app.services import UserService, DocumentService, AnnotationService, NamedEntityService, NominatimService
import app.controllers
from app.config import Core
from . import settings


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
