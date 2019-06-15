"""
Application DI class
"""
import logging
from sys import stdout
from sanic import Sanic
from dependency_injector import containers, providers
from app.config import Core
from . import settings

class Application(containers.DeclarativeContainer):
    """
    Application components container
    """

    Core.config.override(settings.SETTINGS)

    webapi = providers.Factory(Sanic, __name__)
    config = Core.config
