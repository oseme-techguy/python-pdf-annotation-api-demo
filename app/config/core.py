"""
Application Core class
"""
import logging
from sys import stdout
from dependency_injector import containers, providers


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
