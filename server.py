"""
Thornleigh Farm Monitor
Server Module
author: hugh@blinkybeach.com
"""
from th_monitor.monitor_server import MonitorServer
from server_config import PORT
from server_config import DB_DSN
from th_monitor.database import Database

with open('insertion.sql') as sql_file:
    INSERTION_QUERY = sql_file.read()


def run() -> None:
    database = Database(DB_DSN, INSERTION_QUERY)
    server = MonitorServer(('', PORT), database=database)
    server.serve_forever()
    return


if __name__ == '__main__':
    run()
