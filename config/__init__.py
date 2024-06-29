"""Module "config".
File:
    __init__.py

About:
    This module initializes the configuration variables
    used throughout the service. It imports and exposes
    key configuration constants such as API token,
    service name, and other settings required for proper
    operation.

Author:
    Oidaho (Ruslan Bashinsky)
    oidahomain@gmail.com
"""

from .config import (
    BROKER_ADDR,  # Address of the message broker
    TOKEN,  # API token
    API_VERSION,  # Version of the API
    LONGPOLL_REQUEST_TD,  # Timeout for long-polling requests
    SERVICE_NAME,  # Name of the service
    VK_GROUP_ID_DELAY,  # Delay for VK group ID
    COMMAND_PREFIXES,  # Prefixes for bot commands
    GROUP_ID,  # ID of the group
)

__all__ = (
    "BROKER_ADDR",
    "TOKEN",
    "API_VERSION",
    "LONGPOLL_REQUEST_TD",
    "SERVICE_NAME",
    "VK_GROUP_ID_DELAY",
    "COMMAND_PREFIXES",
    "GROUP_ID",
)
