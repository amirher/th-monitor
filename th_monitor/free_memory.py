"""
Thornleigh Farm Monitor
Free Memory Module
author: hugh@blinkybeach.com
"""
import json
from th_monitor.shell import Shell
from th_monitor.encodable import Encodable
from th_monitor.attribute import Attribute


class FreeMemory(Encodable, Attribute):
    """
    A measure of free RAM, in megabytes
    """
    NAME = 'free_memory_mb'
    _COMMAND = "free -m | /bin/grep 'Mem:' | awk '{printf $7}'"

    def __init__(self, shell: Shell) -> None:
        self._available_memory = int(shell.execute(self._COMMAND))
        return

    def encode(self) -> int:
        return self._available_memory
