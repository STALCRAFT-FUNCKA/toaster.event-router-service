"""Module "fetcher".

File:
    fetcher.py

About:
    This file describes the Fetcher class, which accepts
    events from the VK LongPoll server and sends them to
    the Fabric class.
"""

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
from loguru import logger
from funcka_bots.broker import Publisher
from fabric import Fabric
import config


class Fetcher:
    """VK event fetcher.

    Init args:
        DEBUG (bool, optional): Debug mode flag. Defaults to False.
    """

    __broker = Publisher(creds=config.BROKER_CREDS)
    __fabric = Fabric()

    def __init__(self, DEBUG: bool = False) -> None:
        session = VkApi(
            token=config.VK_GROUP_TOKEN,
            api_version=config.VK_API_VERSION,
        )

        self.DEBUG = DEBUG
        self._longpoll = VkBotLongPoll(
            vk=session,
            wait=config.LONGPOLL_REQUEST_TD,
            group_id=config.VK_GROUP_ID,
        )
        self.api = session.get_api()

    def run(self) -> None:
        """Start listening to LongPoll server."""

        logger.info("Starting listening to LPS...")

        for vk_event in self._longpoll.listen():
            event = self.__fabric(vk_event, self.api)
            if event is not None:
                logger.info(f"New event received: \n{event}")
                if self.DEBUG:
                    logger.debug(f"Dict repr: \n{event.as_dict()}")

                self.__broker.publish(
                    obj=event,
                    queue_name=event.event_type,
                )
