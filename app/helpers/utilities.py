"""Utilities
"""
from re import match
from urllib import parse
import datetime
import calendar
import time
import json
import requests
import uuid

class Utilities:
    """Utilities
    """

    @staticmethod
    def generate_id():
        """Generates a uuid - suitable for DB primary column
        """
        return uuid.uuid4().hex

    @staticmethod
    def decode_string(text):
        """Decode a URL encoded strinf

        Arguments:
            text {str} -- URL encoded string to decode
        """
        return parse.unquote(text)

    @staticmethod
    def url_generator(url, params):
        """A method to generate a url from the params input to this method

        Arguments:
            url {string} -- URL of request
            params {object} -- the dict containg the query parameters

        Returns:
            str -- the generated url string
        """

        params = parse.urlencode(params)
        if parse.urlparse(url)[4]:
            return url + '&' + params
        return url + '?' + params

    @staticmethod
    def get_request(url, headers=None, query=None, timeout=5, is_json=True):
        """API GET request
        Arguments:
            url {string} -- URL of request

        Keyword Arguments:
            headers {dict} -- Headers for the HTTP request (default: {None})
            query {dict} -- HTTP query parameters (default: {None})
            timeout {int} -- Request timeout in seconds (default: {5})
            is_json {bool} -- If request is JSON (default: {True})

        Returns:
            object -- the response from the request
        """

        request_headers = {'content-type':'text/plain'} if not headers else headers
        req = requests.get(url, headers=request_headers, params=query, timeout=timeout)
        if is_json:
            return req.json()
        return req

    @staticmethod
    def post_request(url, payload, headers=None, timeout=5, is_json=True):
        """API POST request

        Arguments:
            url {string} -- URL of request
            payload {dict} -- POST body

        Keyword Arguments:
            headers {dict} -- Headers for the HTTP request (default: {None})
            timeout {int} -- Request timeout in seconds (default: {5})
            is_json {bool} -- If request is JSON (default: {True})

        Returns:
            object -- the response from the request
        """

        request_headers = {'content-type':'application/json'} if not headers else headers
        # JSON.stringify() the payload
        if not isinstance(payload, str):
            payload_str = json.dumps(payload)
        else:
            payload_str = payload

        req = requests.post(url, data=payload_str, headers=request_headers, timeout=timeout)
        if is_json:
            return req.json()
        return req

    @staticmethod
    def get_day_time(month='', day='', year=''):
        """Get the day time stamp for the day, month and year

        Keyword Arguments:
            month {str} -- the month int (default: {''})
            day {str} -- the day int (default: {''})
            year {str} -- the year int (default: {''})

        Returns:
            {int} -- the int of the day timestamp
        """

        day = time.strftime("%d") if day == '' else day
        month = time.strftime("%m") if month == '' else month
        year = time.strftime("%Y") if year == '' else year
        year = int(year)
        month = int(month)
        day = int(day)
        date_time = datetime.datetime(year=year, month=month, day=day)
        return int(time.mktime(date_time.timetuple()))

    @staticmethod
    def get_month_time(month='', year=''):
        """Get the month time stamp from the month and year

        Keyword Arguments:
            month {str} -- the month int (default: {''})
            year {str} -- the year int (default: {''})

        Returns:
            {int} -- the int of the month timestamp
        """

        month = time.strftime("%m") if month == '' else month
        year = time.strftime("%Y") if year == '' else year
        month = int(month)
        month -= 1
        year = int(year)

        if month == 0:
            month = 12
            year -= 1
        month = max(1, month)
        month_range = calendar.monthrange(year, month)
        day = month_range[1]

        date_time = datetime.datetime(year=year, month=month, day=day)
        return int(time.mktime(date_time.timetuple()))

