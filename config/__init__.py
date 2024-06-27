"""Module "config".
About:
    Service configurations and settings.
"""

from .config import (
    BROKER_ADDR,
    TOKEN,
    API_VERSION,
    LONGPOLL_REQUEST_TD,
    SERVICE_NAME,
    VK_GROUP_ID_DELAY,
    COMMAND_PREFIXES,
)


__all__ = (
    "BROKER_ADDR",
    "TOKEN",
    "API_VERSION",
    "LONGPOLL_REQUEST_TD",
    "SERVICE_NAME",
    "VK_GROUP_ID_DELAY",
    "COMMAND_PREFIXES",
)
