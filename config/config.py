"""Module "config".

File:
    config.py

About:
    This file defines the used variables
    and configuration objects.
"""

import os
from funcka_bots.credentials import RabbitMQCredentials

# Redis (broker) credentials
BROKER_CREDS = RabbitMQCredentials(
    host=os.getenv("rabbitmq_host"),
    port=os.getenv("rabbitmq_port"),
    vhost=os.getenv("rabbitmq_vhost"),
    user=os.getenv("rabbitmq_user"),
    pswd=os.getenv("rabbitmq_pswd"),
)

# API token obtained from environment variable
VK_GROUP_TOKEN: str = os.getenv("vk_group_token")

# Group ID for identifying specific groups
VK_GROUP_ID: int = int(os.getenv("vk_group_id"))

# API version used for API requests
VK_API_VERSION: str = "5.199"

# Timeout duration for long-polling requests (sec)
LONGPOLL_REQUEST_TD: int = 10

# Delay for VK group ID (difference between chat and peer)
VK_PEER_ID_DELAY = 2000000000

# Command prefixes recognized by the bot
COMMAND_PREFIXES = ("/", "!")
