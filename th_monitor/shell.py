"""
Thornleigh Farm
Shell Module
author: hugh@blinkybeach.com
"""


class Shell:
    """
    Abstract class defining an interface for the execution of commands on a
    machine.
    """
    def execute(self, command: str) -> str:
        """
        Return the output of executing the specified command
        """
        raise NotImplementedError
