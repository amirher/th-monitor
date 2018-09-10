"""
Thornleigh Farm Monitor
Delivery Module
author: hugh@blinkybeach.com
"""
import json
from syslog import syslog
import traceback
from th_monitor.record import Record
from th_monitor.database import Database


class Delivery:
    """
    Data received from a client
    """
    def __init__(self, data: str, database: Database) -> None:

        self._status_code = None
        try:
            decoded_data = json.loads(data)
        except json.JSONDecodeError:
            self._status_code = 400
            return

        if not isinstance(decoded_data, list):
            self._status_code = 400
            return

        try:
            Record(database, decoded_data)
        except Exception as error:
            message = 'Error in delivery of monitoring data.\n'
            message += 'Error: ' + str(error) + '\n'
            message += 'Trace: ' + str(traceback.format_exc())
            message += '\n\n Data supplied: ' + str(data)
            syslog(message)
            self._status_code = 400
            return
        self._status_code = 200
        return

    status_code = property(lambda s: s._status_code)
