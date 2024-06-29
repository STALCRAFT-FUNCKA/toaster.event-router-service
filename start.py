"""Service "toaster.event-routing-service".
About:
    A service that listening to VKontakte long-polling server,
    receives events from it, and then forms them
    custom events, sending json data through the RabbitMQ
    to other handling services.
"""

from fetcher import Fetcher


def main():
    """Entry point."""
    fetcher = Fetcher(DEBUG=True)
    fetcher.run()


if __name__ == "__main__":
    main()
