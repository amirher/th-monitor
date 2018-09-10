"""
Thornleigh Farm Monitor
Core Module
author: hugh@blinkybeach.com
"""
from client_config import EXAMINE_LOCAL, EXAMINE_REMOTE, LOCAL_MACHINE_ID
from client_config import REMOTE_MACHINES, REMOTE_URL, REMOTE_PORT, AGENT
from th_monitor.remote_shell import RemoteShell
from th_monitor.local_shell import LocalShell
from th_monitor.machine import Machine
from th_monitor.package import Package

machines = list()

if EXAMINE_LOCAL is True:
    machines.append(Machine(LOCAL_MACHINE_ID, LocalShell()))
if EXAMINE_REMOTE is True:
    for configuration in REMOTE_MACHINES:
        shell = RemoteShell(
            hostname=configuration['hostname'],
            key_filename=configuration['key_filename'],
            username=configuration['user']
        )
        machines.append(Machine(configuration['machine_id'], shell))

Package(machines).send(REMOTE_URL, AGENT, REMOTE_PORT)
