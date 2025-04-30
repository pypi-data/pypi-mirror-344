import random
from contextlib import contextmanager

import pexpect

from sshtunnelproxy import settings


@contextmanager
def tunnel(remote_port: int = 0, local_port: int = 8000):
    """
    Create an SSH tunnel to a remote server
    """
    remote_port = remote_port or random.randint(*settings.PORT_RANGE)  # noqa: S311
    ssh_tunnel = pexpect.spawn(
        f"ssh -NtR {remote_port}:localhost:{local_port} {settings.USER}@{settings.HOST}",
    )
    index = ssh_tunnel.expect(
        ["Are you sure you want to continue connecting", "password:"]
    )
    if index == 0:
        ssh_tunnel.sendline("yes")
        ssh_tunnel.expect("password:")

    ssh_tunnel.sendline(settings.PASSWORD)

    # We need to expect something to keep the tunnel open
    # But expect("") doesn't work for some reason
    ssh_tunnel.expect(pexpect.TIMEOUT, timeout=1)

    try:
        yield settings.URL_GENERATOR(remote_port)
    finally:
        ssh_tunnel.close()
