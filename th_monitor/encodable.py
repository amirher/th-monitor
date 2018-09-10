"""
Thornleigh Farm Monitor
Encodable Module
author: hugh@blinkybeach.com
"""
from typing import Any


class Encodable:
    """
    Abstract class defining an interface for serialising data for transmission
    """
    def encode(self) -> Any:
        """
        Return a string encoded representation of this type's data
        """
        raise NotImplementedError
