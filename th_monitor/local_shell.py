"""
Thornleigh Farm
Local Shell Module
author: hugh@blinkybeach.com
"""
from th_monitor.shell import Shell
import subprocess


class LocalShell(Shell):
    """
    A shell on the local machine
    """
    def execute(self, command: str) -> str:
        return subprocess.getoutput(command)
