"""
Thornleigh Farm Monitor
Monitor Server Module
author: hugh@blinkybeach.com
"""
from http.server import HTTPServer
from typing import Tuple
from th_monitor.database import Database
from th_monitor.receiver import Receiver


class MonitorServer(HTTPServer):
    """
    An HTTP server for receiving monitoring data
    """
    def __init__(self, address: Tuple[str, int], database: Database) -> None:
        self.database = database
        super().__init__(address, Receiver)
        return
