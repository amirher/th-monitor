"""
Thornleigh Farm
Remote Shell Module
author: hugh@blinkybeach.com
"""
from th_monitor.shell import Shell
from paramiko import SSHClient
from paramiko import AutoAddPolicy


class RemoteShell(Shell):
    """
    A shell executed on a remote machine
    """
    def __init__(
        self,
        hostname: str,
        key_filename: str,
        username: str
    ) -> None:

        assert isinstance(hostname, str)
        assert isinstance(key_filename, str)
        assert isinstance(username, str)

        self._ssh = SSHClient()
        self._ssh.set_missing_host_key_policy(AutoAddPolicy())
        self._ssh.connect(
            hostname,
            key_filename=key_filename,
            username=username,
            timeout=4,
            banner_timeout=4,
            auth_timeout=4
        )

        return

    def execute(self, command: str) -> str:
        _, stdout, _ = self._ssh.exec_command(command)
        return stdout.read().decode('utf-8')
