# django-ssh-tunnel-proxy

Opens an ssh tunnel so your local development server can be accessed remotely

## Quick start
1. Install with `pip install django-ssh-tunnel-proxy`
2. Add `sshtunnelproxy` to `INSTALLED_APPS`
3. Set the settings described below
4. Start a dev-server using `python manage.py runserver`
5. Open a tunnel using `python manage.py opensshtunnelproxy`
6. Visit the URL displayed in your terminal

## Context manager
Create a temporary tunnel using the context manager
```python
from sshtunnelproxy import tunnel

with tunnel() as remote_url:
    pass  # do something
```

## Available settings
```python
SSH_TUNNEL_USER: str = ''
"""The SSH user to use for the tunnel. default: `''`"""

SSH_TUNNEL_PASSWORD: str = ''
"""The SSH password to use for the tunnel. default: `''`"""

SSH_TUNNEL_PORT_RANGE: tuple[int, int] = (24000, 24999)
"""The range of ports to use for the tunnel. default: `(24000, 24999)`"""

SSH_TUNNEL_HOST: str = ''
"""The host to tunnel to. default: `''`"""

SSH_TUNNEL_URL_GENERATOR: Callable[[int], str] = lambda port: f"http://{SSH_TUNNEL_HOST}:{port + 1}"
"""
The function to generate the tunnel URL.
Takes the remote port as an argument and returns the URL at which the tunnel can be accessed.
default: `lambda port: f'http://{HOST}:{port + 1}'`
"""
```

## Remote server
For this to work, you need a remote web server to reverse-proxy the tunneled port.

## What else
Make sure to add `SSH_TUNNEL_HOST` to your `ALLOWED_HOSTS`.  
Also, `SESSION_COOKIE_SECURE = False` must be set, or else you won't be able to log in.
