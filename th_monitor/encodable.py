"""
Thornleigh Farm Monitor
Encodable Module
author: hugh@blinkybeach.com
"""


class Encodable:
    """
    Abstract class defining an interface for serialising data for transmission
    """
    def encode(self) -> str:
        """
        Return a string encoded representation of this type's data
        """
        raise NotImplementedError
