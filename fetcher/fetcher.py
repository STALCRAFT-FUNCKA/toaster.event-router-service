"""Module "fetcher".

File:
    fetcher.py

About:
    This file defines the Fetcher class responsible
    for fetching VK API events using long polling,
    processing them into Event objects using the
    Fabric class, and publishing them to a message
    broker.
"""

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
from loguru import logger
from toaster.broker import Publisher, build_connection
from fabric import Fabric
import config


class Fetcher:
    """Initializes Fetcher with optional debug mode.

    Description:
        Class responsible for fetching VK API events using long polling,
        processing them into Event objects using the Fabric class,
        and publishing them to a message broker.

    Args:
        DEBUG (bool, optional): Debug mode flag. Defaults to False.

    Attributes:
        DEBUG (bool): Debug mode flag.
        api (object): VK API object.
    """

    __broker = Publisher(client=build_connection(config.REDIS_CREDS))
    __fabric = Fabric()

    def __init__(self, DEBUG: bool = False) -> None:
        self.DEBUG = DEBUG
        self._session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        self._longpoll = VkBotLongPoll(
            vk=self._session,
            wait=config.LONGPOLL_REQUEST_TD,
            group_id=config.GROUP_ID,
        )
        self.api = self._session.get_api()

    def run(self) -> None:
        """Listen long-poll server

        Description:
            Starts listening to the VK longpoll server and processes incoming events.
            Logs received events and publishes them to the message broker.
        """

        logger.info("Starting listening longpoll server...")

        for vk_event in self._longpoll.listen():
            event = self.__fabric(vk_event, self.api)
            if event is not None:
                logger.info(f"New event received: \n{event}")
                if self.DEBUG:
                    logger.debug(f"Dict repr: \n{event.as_dict()}")

                self.__broker.publish(
                    obj=event,
                    channel_name=event.event_type,
                )
