"""Module "config".

File:
    __init__.py

About:
    Initializing the "config" module.
"""

from .config import (
    REDIS_CREDS,  # Данные авторизации Redis
    TOKEN,  # API токен
    API_VERSION,  # Версия используемого API
    LONGPOLL_REQUEST_TD,  # Тайм-аут для запросов на LPS
    VK_GROUP_ID_DELAY,  # Разница между id чата и узла
    COMMAND_PREFIXES,  # Префиксы команд
    GROUP_ID,  # ID группы, под которой развернут бот
)

__all__ = (
    "REDIS_CREDS",
    "TOKEN",
    "API_VERSION",
    "LONGPOLL_REQUEST_TD",
    "VK_GROUP_ID_DELAY",
    "COMMAND_PREFIXES",
    "GROUP_ID",
)
