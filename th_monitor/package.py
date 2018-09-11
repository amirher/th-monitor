"""
Thornleigh Farm Monitor
Package Module
author: hugh@blinkybeach.com
"""
import json
from urllib.request import Request
from urllib.request import urlopen
from typing import List
from th_monitor.machine import Machine
from th_monitor.encoder import Encoder


class Package:
    """
    A collection of data describing a machine
    """

    def __init__(self, machines: List[Machine]) -> None:

        assert False not in [isinstance(m, Machine) for m in machines]
        self._machines = machines

        return

    def _to_json(self) -> str:
        """
        Return string serialised data
        """
        data = [m.encode() for m in self._machines]
        return json.dumps(data, cls=Encoder)

    def send(self, url: str, agent: str) -> None:

        assert isinstance(agent, str)
        assert isinstance(url, str)

        headers = {
            'content-type': 'application/json',
            'User-Agent': agent
        }

        request = Request(
            url,
            method='POST',
            headers=headers,
            data=self._to_json().encode('utf-8')
        )

        urlopen(request)

        return
