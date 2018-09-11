"""
Thornleigh Farm Monitor
Disk IO Module
author: hugh@blinkybeach.com
"""
import json
import time
from typing import Tuple
from typing import List
from th_monitor.encodable import Encodable
from th_monitor.attribute import Attribute
from th_monitor.shell import Shell


class DiskIO(Encodable, Attribute):
    """
    A measure of disk input / output
    """
    NAME = 'disk_io'
    _COMMAND = 'sudo fdisk -l | /bin/grep "Sector size" | awk \'{print $4}\''
    _SAMPLE_TIME = 2
    _DISK_NAMES = ['xvda', 'sda', 'vda', 'nvme0n1']

    def __init__(self, shell: Shell) -> None:
        self._shell = shell
        result = shell.execute(self._COMMAND)
        try:
            self._sector_size = int(result)
        except ValueError:
            self._sector_size = int(result.split('\n')[0])

        root = 'cat /proc/diskstats | /bin/grep "{disk} "'
        sample = self._try_sample(root, self._DISK_NAMES)
        start_read = sample[0]
        start_write = sample[1]
        time.sleep(self._SAMPLE_TIME)
        sample = self._try_sample(root, self._DISK_NAMES)
        end_read = sample[0]
        end_write = sample[1]
        self._read_kb_s = self._compute_io_rate(end_read, start_read)
        self._write_kb_s = self._compute_io_rate(end_write, start_write)
        return

    def _compute_io_rate(self, end: int, start: int) -> int:
        """
        Return an integer rate of input / output over a period of time
        """
        change = end - start
        rate = change * self._sector_size / self._SAMPLE_TIME / 1000
        return int(rate)

    def _try_sample(self, root: str, disk_names: List[str]) -> Tuple[int, int]:
        """
        Attempt sampling with various potential disk names. This is hacky but,
        you know, it gets the job done.
        """
        for name in disk_names:
            result = self._shell.execute(root.format(disk=name))
            if result != '':
                data = result.split('{n} '.format(n=name))[1].split(' ')
                read = int(data[0])
                write = int(data[2])
                read_write = (read, write)
                return read_write
        raise RuntimeError('Unknown disk name!')

    def encode(self) -> dict:
        return {
            'read_kb_s': self._read_kb_s,
            'write_kb_s': self._write_kb_s
        }
