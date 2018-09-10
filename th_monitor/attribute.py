"""
Thornleigh Farm Monitor
Attribute Module
author: hugh@blinkybeach.com
"""
from th_monitor.shell import Shell


class Attribute:
    """
    Abstract class defining an interface for classes examining an attribute
    of a machine
    """
    NAME = NotImplemented

    def __init__(self, shell: Shell) -> None:
        raise NotImplementedError
