"""
Thornleigh Farm Monitor
Record Module
author: hugh@blinkybeach.com
"""
import json
from th_monitor.database import Database
from typing import List


class Record:
    """
    An instance of monitoring data recorded in the database
    """
    def __init__(self, database: Database, data: List[dict]) -> None:

        database.insert(json.dumps(data))

        return
