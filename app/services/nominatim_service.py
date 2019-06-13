"""Nominatim Service"""

from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities

class NominatimService:
    """Nominatim Service"""

    def __init__(self, logger=None):
        self.logger = logger


    def fetch_location(self, annotation=None):
        """Fetches the Logitude and Latitude for an annotation via the Nominatim API.
            Actions:
                - Makes API call to their search endpoint
                - Gets list of all results (first 10)
                - Since they are sorted by "importance", 
                    I just start from the top and iterate through until I find a match

        Arguments:
            annotation {string} -- the annotation to check

        Returns:
            object -- the object containing log. and lat. info or None
        """

        if annotation is None:
            raise ValueError('the annotation cannot be None')

        annotation = annotation.lower() # convert to lower case

        # call the location search service api to get the Lag. and Lat.
        url = SETTINGS['location_lookup']['url']
        search_size = SETTINGS['location_lookup']['search_size']
        search_size = search_size if search_size is not None else '20'

        headers = {
            'content-type': 'application/json'
        }
        # define search criteria object
        search_criteria = {
            'q': str(annotation),
            'format': 'json',
            'limit': search_size
        }

        try:
            response = Utilities.get_request(url, headers, search_criteria)
        except Exception as connection_error: # pylint: disable=W0703
            self.logger.error('Error connecting to the Location Search Query API service: {error}'.format(
                error=connection_error
            ))
            return None

        if len(response) == 0:
            return None

        for record in response:
            if record['display_name'] is not None \
                and annotation.lower() in record['display_name'].lower():
                return {
                    'latitude': record['lat'],
                    'longitude': record['lon']
                }

        return None
