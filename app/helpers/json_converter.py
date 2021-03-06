"""JSONConverter
"""
import json
from uuid import UUID
from datetime import datetime

class JSONConverter(json.JSONEncoder):
    """JSONConverter
    """

    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the hex value of uuid
            return obj.hex
        if isinstance(obj, datetime):
            # if the obj is datetime, we simply return its string value
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return json.JSONEncoder.default(self, obj)
