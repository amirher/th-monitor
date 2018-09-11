"""
Thornleigh Monitor
CPU Module
© 2018 Blinky Beach Pty Ltd
author: hugh@blinkybeach.com
"""
from th_monitor.shell import Shell
from th_monitor.attribute import Attribute
from th_monitor.encodable import Encodable


class CPUStats(Encodable, Attribute):
    """
    A measure of CPU time allocations
    """
    NAME = 'cpu_usage'
    # %Cpu(s):  1.1 us,  0.7 sy,  0.0 ni, 98.2 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st

    _COMMAND = 'top -d 3 -b -n 2 | /bin/grep "%Cpu"'

    def __init__(self, shell: Shell) -> None:
        cpu_data = shell.execute(self._COMMAND).split('\n')[1]
        if 'us' not in cpu_data:
            raise RuntimeError('Unexpected cpu_data: ' + cpu_data)
        self._user = round(float(cpu_data.split('us')[0].split()[1]), None)
        self._system = round(float(cpu_data.split('sy')[0].split()[-1]), None)
        self._io_wait = round(float(cpu_data.split('wa')[0].split()[-1]), None)
        self._idle = round(float(cpu_data.split('id')[0].split()[-1]), None)
        return

    def encode(self) -> dict:
        return {
            'user': self._user,
            'system': self._system,
            'io_wait': self._io_wait,
            'idle': self._io_wait
        }
