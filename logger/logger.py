"""Module "logger"."""

import logging
import config
from .formatters import get_formatter


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=Singleton):
    """Logger class, creator of a new instance,
    Let's start registering. Provides basic
    logging functionality.
    """

    def __init__(self):
        self.logger = logging.getLogger(config.SERVICE_NAME)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(get_formatter(colored=True))

        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.DEBUG)

    def info(self, text: str):
        """Logs a message as info.

        Args:
            text (str): Text of log message.
        """
        self.logger.info(text)

    def debug(self, text: str):
        """Logs a message as debug.

        Args:
            text (str): Text of log message.
        """
        self.logger.debug(text)

    def warning(self, text: str):
        """Logs a message as warning.

        Args:
            text (str): Text of log message.
        """
        self.logger.warning(text)

    def error(self, text: str):
        """Logs a message as error.

        Args:
            text (str): Text of log message.
        """
        self.logger.error(text)

    def critical(self, text: str):
        """Logs a message as critical.

        Args:
            text (str): Text of log message.
        """
        self.logger.critical(text)
