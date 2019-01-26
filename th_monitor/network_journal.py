"""
Thornleigh Farm Monitor
Network Journal Module
author: hugh@blinkybeach.com
"""
from th_monitor.network_io import NetworkIO
from th_monitor.encodable import Encodable
from th_monitor.attribute import Attribute
from th_monitor.shell import Shell
from typing import List
from typing import Dict
from typing import Any


EXCLUDE = ('l', 'n')


class NetworkJournal(Encodable, Attribute):
    """Record of the absolute network traffic quantity across an interface"""
    NAME = 'network_journal'

    def __init__(self, shell: Shell) -> None:
        self.shell = shell
        interfaces = NetworkIO.list_interfaces(shell)
        self._samples = [NetworkJournal.Sample(i, shell) for i in interfaces]
        return

    def encode(self) -> List[Dict]:
        return [s.encode() for s in self._samples]

    class Sample(Encodable):
        """Journal sample"""
        def __init__(
            self,
            interface: str,
            shell: Shell
        ) -> None:

            self._interface = interface
            root = 'cat /sys/class/net/' + self._interface + '/statistics/'
            rx_bytes_cmd = root + 'rx_bytes'
            tx_bytes_cmd = root + 'tx_bytes'
            rx_packets_cmd = root + 'rx_packets'
            tx_packets_cmd = root + 'tx_packets'
            self._rx_bytes = int(shell.execute(rx_bytes_cmd))
            self._tx_bytes = int(shell.execute(tx_bytes_cmd))
            self._rx_packets_cmd = int(shell.execute(rx_packets_cmd))
            self._tx_packets_cmd = int(shell.execute(tx_packets_cmd))
            return

        def encode(self) -> Dict[str, Any]:

            return {
                'iface_name': self._interface,
                'rx_bytes': self._rx_bytes,
                'tx_bytes': self._tx_bytes,
                'rx_packets': self._rx_packets,
                'tx_packets': self._tx_packets
            }
