"""Module "logger"."""

import logging
from colorama import Fore


def get_formatter(colored: bool):
    """DOCSTRING"""

    return __colored() if colored else __mono()


def __colored():
    formatter = logging.Formatter(
        Fore.RED
        + "[ %(name)s | %(levelname)s | %(asctime)s ] "
        + Fore.WHITE
        + "Message: %(message)s"
    )

    return formatter


def __mono():
    formatter = logging.Formatter(
        "[ %(name)s | %(levelname)s | %(asctime)s ] " + "Message: %(message)s"
    )

    return formatter
