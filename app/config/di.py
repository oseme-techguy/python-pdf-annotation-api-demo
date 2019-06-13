"""
Application DI class
"""
import logging
from sys import stdout
from sanic import Sanic
from dependency_injector import containers, providers
from app import webhandlers
from app.services import UserService #, DocumentService, AnnotationService, NominatimService
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


class Controllers(containers.DeclarativeContainer):
    """IoC container for controllers"""

    user = providers.Factory(app.controllers.User,
                             logger=Core.logger,
                             service=Services.user)

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
    # Login
    login_webhandler = providers.Callable(
        Controllers.user().login
    )

    # get one or all
    get_users_webhandler = providers.Callable(
        Controllers.user().get_users
    )

    # add user
    create_user_webhandler = providers.Callable(
        Controllers.user().add_users
    )
