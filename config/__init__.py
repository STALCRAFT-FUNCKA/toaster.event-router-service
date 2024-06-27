"""Module "config".
About:
    Service configurations and settings.
"""

from .config import (
    QUEUE_BROKER_IP,
    TOKEN,
    API_VERSION,
    LONGPOLL_REQUEST_TD,
    SERVICE_NAME,
    VK_GROUP_ID_DELAY,
    COMMAND_PREFIXES,
)


__all__ = (
    "QUEUE_BROKER_IP",
    "TOKEN",
    "API_VERSION",
    "LONGPOLL_REQUEST_TD",
    "SERVICE_NAME",
    "VK_GROUP_ID_DELAY",
    "COMMAND_PREFIXES",
)
