"""Nominatim Service"""

from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities
from app.helpers.sql import Sql

class NominatimService:
    """Nominatim Service"""

    def __init__(self, logger=None):
        self.logger = logger


    def fetch_location(self, annotation=None):
        """Fetches the Logitude and Latitude for an annotation via the Nominatim API.

        Arguments:
            annotation {string} -- the annotation to check

        Returns:
            object -- the object containing log. and lat. info or None
        """

        if annotation is None:
            raise ValueError('the annotation cannot be None')


        return None
