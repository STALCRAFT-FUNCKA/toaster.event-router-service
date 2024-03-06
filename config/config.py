"""Module "config".
"""
import os

SERVICE_NAME = "toaster.event-routing-service"

QUEUE_BROKER_IP = "172.18.0.40"

TOKEN: str = os.getenv("TOASTER_DEV_TOKEN")
GROUP_ID: int = int(os.getenv("TOASTER_DEV_GROUPID"))

API_VERSION: str = "5.199"
LONGPOLL_REQUEST_TD: int = 10

VK_GROUP_ID_DELAY = 2000000000

COMMAND_PREFIXES = ("/", "!")
