"""Module "config".
About:
    Service configurations and settings.
"""
import os

SERVICE_NAME = "toaster.event-routing-service"

TOKEN: str = os.getenv("TOKEN")
GROUP_ID: int = int(os.getenv("GROUPID"))

API_VERSION: str = "5.199"
LONGPOLL_REQUEST_TD: int = 10

VK_GROUP_ID_DELAY = 2000000000

COMMAND_PREFIXES = ("/", "!")
