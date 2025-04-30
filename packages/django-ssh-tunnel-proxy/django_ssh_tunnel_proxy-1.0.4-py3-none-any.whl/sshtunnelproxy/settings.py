"""
Contains descriptions and default values for settings that are used by the sshtunnelproxy command.
The settings can be overridden in the django settings file by prefixing the names with `SSH_TUNNEL_`.
"""

from typing import Callable

from django.conf import settings

USER: str = getattr(settings, "SSH_TUNNEL_USER", "")
"""The SSH user to use for the tunnel. default: `''`"""

PASSWORD: str = getattr(settings, "SSH_TUNNEL_PASSWORD", "")
"""The SSH password to use for the tunnel. default: `''`"""

PORT_RANGE: tuple[int, int] = getattr(settings, "SSH_TUNNEL_PORT_RANGE", (24000, 24999))
"""The range of ports to use for the tunnel. default: `(24000, 24999)`"""

HOST: str = getattr(settings, "SSH_TUNNEL_HOST", "")
"""The host to tunnel to. default: `''`"""

URL_GENERATOR: Callable[[int], str] = getattr(
    settings, "SSH_TUNNEL_URL_GENERATOR", lambda port: f"http://{HOST}:{port + 1}"
)
"""
The function to generate the tunnel URL.
Takes the remote port as an argument and returns the URL at which the tunnel can be accessed.
default: `lambda port: f'http://{HOST}:{port + 1}'`
"""
