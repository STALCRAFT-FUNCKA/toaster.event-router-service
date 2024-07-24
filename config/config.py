"""Module "config".

File:
    config.py

About:
    This file defines the used variables
    and configuration objects.
"""

import os
from toaster.credentials import RedisCredentials

# Redis (broker) credentials
REDIS_CREDS = RedisCredentials(
    host="172.18.0.40",
    port=6379,
    db=0,
)

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
