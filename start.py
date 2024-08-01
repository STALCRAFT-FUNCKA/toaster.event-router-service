"""Service "service.event-fetching".

File:
    start.py

About:
    This service is responsible for receiving raw events from
    LongPoll VKontakte servers, converting them into custom ones
    event objects. Custom event objects are sent in serialized
    form to the Redis bus for further routing.
"""

import sys
from db import TOASTER_DB
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


def setup_db() -> None:
    TOASTER_DB.create_tables()


def main():
    """Program entry point."""

    setup_logger()
    setup_db()
    fetcher = Fetcher(DEBUG=False)
    fetcher.run()


if __name__ == "__main__":
    main()
