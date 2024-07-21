"""Service "toaster.event-routing-service".

File:
    start.py

About:
    This service is responsible for receiving raw events
    from the VK LongPoll server, transforming them into
    custom event objects, and sending these serialized
    objects to Redis. The service listens for incoming
    events, processes them to fit the custom event schema,
    and ensures they are properly serialized before being
    dispatched to the Redis storage, enabling further handling
    and processing by other components of the system.
"""

import sys
from fetcher import Fetcher
from loguru import logger


def setup_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <red>{module}</red> | <level>{level}</level> | {message}",
        level="DEBUG",
    )


def main():
    """Entry point."""

    setup_logger()
    fetcher = Fetcher(DEBUG=False)
    fetcher.run()


if __name__ == "__main__":
    main()
