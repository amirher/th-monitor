"""
Thornleigh Monitor
CPU Module
© 2018 Blinky Beach Pty Ltd
author: hugh@blinkybeach.com
"""
import json
from th_monitor.shell import Shell
from th_monitor.attribute import Attribute
from th_monitor.encodable import Encodable


class CPUStats(Encodable, Attribute):
    """
    A measure of CPU time allocations
    """
    NAME = 'cpu_usage'
    _COMMAND = 'top -d 3 -b -n 2 | grep "%Cpu"'

    def __init__(self, shell: Shell) -> None:
        cpu_data = shell.execute(self._COMMAND).split('\n')[1]
        self._user = round(float(cpu_data[8:13]), None)
        self._system = round(float(cpu_data[17:22]), None)
        self._io_wait = round(float(cpu_data[44:49]), None)
        self._idle = round(float(cpu_data[35:40]), None)
        return

    def encode(self) -> dict:
        return {
            'user': self._user,
            'system': self._system,
            'io_wait': self._io_wait,
            'idle': self._io_wait
        }
