"""Module "config".

File:
    config.py

About:
    This file defines configuration variables used
    throughout the application, including service names,
    API tokens, broker addresses, and other settings.
"""

import os

# Service name used for identification
SERVICE_NAME = "toaster-dev.event-routing-service"

# Address of the message broker
BROKER_ADDR = "172.18.0.40"

# API token obtained from environment variable
TOKEN: str = os.getenv("TOKEN")

# Group ID for identifying specific groups
GROUP_ID: int = int(os.getenv("GROUPID"))

# API version used for API requests
API_VERSION: str = "5.199"

# Timeout duration for long-polling requests (sec)
LONGPOLL_REQUEST_TD: int = 10

# Delay for VK group ID (difference between chat and peer)
VK_GROUP_ID_DELAY = 2000000000

# Command prefixes recognized by the bot
COMMAND_PREFIXES = ("/", "!")
