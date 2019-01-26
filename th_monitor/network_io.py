"""
Thornleigh Farm Monitor
Network IO Module
author: hugh@blinkybeach.com
"""
import time
from th_monitor.encodable import Encodable
from th_monitor.attribute import Attribute
from th_monitor.shell import Shell
from multiprocessing.dummy import Pool
from typing import Type
from typing import TypeVar
from typing import List

T = TypeVar('T', bound='NetworkIO')


class NetworkIO(Encodable, Attribute):
    """
    A measure of network IO activity over a period
    """
    NAME = 'network_io'
    _SAMPLE_TIME = 2
    _EXCLUDE = ('l', 'n')

    def __init__(self, shell: Shell) -> None:
        self._shell = shell
        interfaces = NetworkIO.list_interfaces(shell)
        sample_time = self._SAMPLE_TIME
        pool = Pool(len(interfaces))
        samples = list()

        def sample(interface):
            samples.append(NetworkIO.Sample(interface, shell, sample_time))
        pool.map(sample, interfaces)
        pool.close()
        pool.join()
        self._samples = samples
        return

    def encode(self) -> list:
        return [s.encode() for s in self._samples]

    class Sample(Encodable):
        """Input / output sample"""
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

    @classmethod
    def list_interfaces(cls: Type[T], shell: Shell) -> List[str]:
        """Return a list of network interface names"""
        interfaces = shell.execute('ls /sys/class/net').split()
        # exclude loopback and unused interfaces
        return [i for i in interfaces if i[0] not in cls._EXCLUDE]
