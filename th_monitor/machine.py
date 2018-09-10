"""
Thornleigh Farm Monitor
Machine Module
author: hugh@blinkybeach.com
"""
import json
from datetime import datetime
from th_monitor.encodable import Encodable
from th_monitor.shell import Shell
from th_monitor.cpu import CPUStats
from th_monitor.disk_io import DiskIO
from th_monitor.disk_available import DiskAvailable
from th_monitor.free_memory import FreeMemory
from th_monitor.network_io import NetworkIO
from th_monitor.attribute import Attribute
from multiprocessing.dummy import Pool
from th_monitor.encoder import Encoder


class Machine(Encodable):
    """
    A collection of data describing a logical machine whose attributes we wish
    to sample. For example, a physical machine or a virtual machine.
    """
    _ATTRIBUTES = [CPUStats, DiskIO, DiskAvailable, FreeMemory, NetworkIO]
    DATETIME_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'

    def __init__(self, machine_id: str, shell: Shell) -> None:

        assert isinstance(machine_id, str)
        assert isinstance(shell, Shell)

        self._machine_id = machine_id
        self._sample_time = datetime.utcnow()
        self._attributes = list()

        def examine(attribute: type) -> None:
            assert issubclass(attribute, Attribute)
            self._attributes.append(attribute(shell))

        pool = Pool(len(self._ATTRIBUTES))
        pool.map(examine, self._ATTRIBUTES)
        pool.close()
        pool.join()

        return

    def encode(self) -> str:
        data = {
            'machine_id': self._machine_id,
            'sample_time': self._sample_time.strftime(self.DATETIME_FORMAT)
        }
        for attribute in self._attributes:
            data[attribute.NAME] = attribute
        return json.dumps(data, cls=Encoder)
