from contextlib import suppress

from django.core.management.base import BaseCommand, CommandError

from sshtunnelproxy import settings, tunnel


class Command(BaseCommand):
    """
    Management command to create an SSH tunnel to a remote server
    """

    help = "Makes your dev server accessible from the internet"

    def add_arguments(self, parser):
        """
        Add arguments to the command
        """
        parser.add_argument(
            "-l",
            "--local_port",
            default=8000,
            type=int,
            help="The port of your local server",
        )
        parser.add_argument(
            "-r",
            "--remote_port",
            default=0,
            type=int,
            help="The port of the remote server ({} <= remote_port <= {}, default: random)".format(
                *settings.PORT_RANGE
            ),
        )

    def handle(self, *args, **options):
        """
        Handle the command
        """
        if not settings.PASSWORD:
            raise CommandError("settings.SSH_TUNNEL_PASSWORD is not set")

        local_port = options.get("local_port")
        remote_port = options.get("remote_port")

        min_port, max_port = settings.PORT_RANGE
        if remote_port and (remote_port < min_port or remote_port > max_port):
            raise CommandError(f"Remote port must be between {min_port} and {max_port}")

        with tunnel(remote_port, local_port) as tunnelUrl:
            self.stdout.write("you can access your server at:")
            self.stdout.write(self.style.SUCCESS(tunnelUrl))

            with suppress(KeyboardInterrupt):
                input("Press Enter to close the tunnel")

        self.stdout.write("")
        self.stdout.write("Tunnel closed")
