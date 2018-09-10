"""
Thornleigh Farm Monitor
Encoder module
author: hugh@blinkybeach.com
"""
from json import JSONEncoder
from th_monitor.encodable import Encodable


class Encoder(JSONEncoder):
    """
    A custom JSONEncoder capable of encoding objects conforming to the Encodable
    protocol
    """
    def default(self, object_to_encode):
        if isinstance(object_to_encode, Encodable):
            return super().default(object_to_encode.encode())

        return super().default(object_to_encode)
