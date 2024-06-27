"""Module "logger"."""

import logging
from colorama import Fore


def get_formatter(self, colored: bool):
    """Provides a formatter with color\mono output.

    Args:
        colored (boold): Colored/Mono switch.

    Returns:
        Formatter: Formatter object for the logger.
    """
    return self.__colored() if colored else self.__mono()


@staticmethod
def __colored():
    formatter = logging.Formatter(
        Fore.RED
        + "[ %(name)s | %(levelname)s | %(asctime)s ] "
        + Fore.WHITE
        + "Message: %(message)s"
    )

    return formatter


@staticmethod
def __mono():
    formatter = logging.Formatter(
        "[ %(name)s | %(levelname)s | %(asctime)s ] " + "Message: %(message)s"
    )

    return formatter
