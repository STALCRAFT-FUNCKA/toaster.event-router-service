"""Module "config".

File:
    __init__.py

About:
    Initializing the "config" module.
"""

from .config import (
    REDIS_CREDS,
    TOKEN,
    API_VERSION,
    LONGPOLL_REQUEST_TD,
    VK_GROUP_ID_DELAY,
    COMMAND_PREFIXES,
    GROUP_ID,
)

__all__ = (
    "REDIS_CREDS",  # Redis authorization data
    "TOKEN",  # API token
    "API_VERSION",  # Version of the API used
    "LONGPOLL_REQUEST_TD",  # Timeout for LPS requests
    "VK_GROUP_ID_DELAY",  # Difference between chat and node id
    "COMMAND_PREFIXES",  # Command prefixes
    "GROUP_ID",  # ID of the group under which the bot is deployed
)
