"""
Thornleigh Farm Monitor
Disk Space Used Module
author: hugh@blinkybeach.com
"""
from th_monitor.encodable import Encodable
from th_monitor.attribute import Attribute
from th_monitor.shell import Shell


class DiskAvailable(Encodable, Attribute):
    """
    A measure of the number of megabytes available on a system disk
    """
    NAME = 'disk_mb_available'
    _SINGLE_MOUNT = 'df -m | /bin/grep "^/" | awk \'{print $4}\''
    _MULTI_MOUNT = 'df -m | /bin/grep "^/" | awk \'{print $2}\''

    def __init__(self, shell: Shell) -> None:
        result = shell.execute(self._SINGLE_MOUNT)
        if result[-1] == '\n':
            result = result[:-1]
        try:
            free = int(result)
        except ValueError:
            block_result = shell.execute(self._MULTI_MOUNT)
            if block_result[-1] == '\n':
                block_result = block_result[:-1]
            sizes = block_result.split('\n')
            int_sizes = [int(b) for b in sizes]
            index = 0
            for blocksize in int_sizes:
                if int(blocksize) == max(int_sizes):
                    result_index = index
                    break
                else:
                    index += 1
            int_free = [int(f) for f in result.split('\n')]
            free = int_free[result_index]
        self._free_mb = free

    def encode(self) -> int:
        return self._free_mb
