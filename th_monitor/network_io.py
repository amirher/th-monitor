"""
Thornleigh Farm Monitor
Network IO Module
author: hugh@blinkybeach.com
"""
import time
from th_monitor.encodable import Encodable
from th_monitor.attribute import Attribute
from th_monitor.shell import Shell


class NetworkIO(Encodable, Attribute):
    """
    A measure of network IO activity over a period
    """
    NAME = 'network_io'
    _SAMPLE_TIME = 2

    def __init__(self, shell: Shell) -> None:
        self._shell = shell
        interfaces = shell.execute('ls /sys/class/net').split('\n')
        sample_time = self._SAMPLE_TIME
        samples = [NetworkIO.Sample(i, shell, sample_time) for i in interfaces]
        self._samples = samples
        return

    def encode(self) -> list:
        return [s.encode() for s in self._samples]

    class Sample(Encodable):
        """
        Input / output sample
        """
        def __init__(
            self,
            interface: str,
            shell: Shell,
            sample_time: int
        ) -> None:
            self._interface = interface
            root = 'cat /sys/class/net/' + self._interface + '/statistics/'
            rx_command = root + 'rx_bytes'
            tx_command = root + 'tx_bytes'
            start_rx = int(shell.execute(rx_command))
            start_tx = int(shell.execute(tx_command))
            time.sleep(sample_time)
            end_rx = int(shell.execute(rx_command))
            end_tx = int(shell.execute(tx_command))
            rx_delta = end_rx - start_rx
            tx_delta = end_tx - start_tx
            if rx_delta < 0:
                rx_delta = 0
            if tx_delta < 0:
                tx_delta = 0
            self._rx_kbs = int(rx_delta / sample_time / 1000)
            self._tx_kbs = int(tx_delta / sample_time / 1000)
            return

        def encode(self) -> dict:
            return {
                'iface_name': self._interface,
                'tx_kb_s': self._tx_kbs,
                'rx_kb_s': self._rx_kbs
            }
