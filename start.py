"""Service "toaster.event-routing-service".
About:
    A service that listening to VKontakte longpolling server,
    receives events from it, and then forms them
    custom events, sending json data through the RabbitMQ
    to other handling services.

Author:
    Oidaho (Ruslan Bashinsky)
    oidahomain@gmail.com
"""

from fetcher import Fetcher


def main():
    """Entry point."""
    fetcher = Fetcher()
    fetcher.run()


if __name__ == "__main__":
    main()
