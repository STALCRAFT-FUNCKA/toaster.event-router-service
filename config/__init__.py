"""Module "config".

File:
    __init__.py

About:
    Initializing the "config" module.
"""

from .config import (
    BROKER_CREDS,
    VK_GROUP_TOKEN,
    VK_GROUP_ID,
    VK_API_VERSION,
    LONGPOLL_REQUEST_TD,
    VK_PEER_ID_DELAY,
    COMMAND_PREFIXES,
)

__all__ = (
    "BROKER_CREDS",
    "VK_GROUP_TOKEN",
    "VK_GROUP_ID",
    "VK_API_VERSION",
    "LONGPOLL_REQUEST_TD",
    "VK_PEER_ID_DELAY",
    "COMMAND_PREFIXES",
)
