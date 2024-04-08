"""Module "fetcher"."""

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEvent
from producer import producer
import config
from logger import logger
from .fabric import Fabric


class Fetcher(object):
    """Fetcher main class.
    Provides receiving events from
    VK longpoll server with a
    community access token.
    """

    def __init__(self):
        self.__session = VkApi(token=config.TOKEN, api_version=config.API_VERSION)

        self.__longpoll = VkBotLongPoll(
            vk=self.__session, wait=config.LONGPOLL_REQUEST_TD, group_id=config.GROUP_ID
        )

        self.api = self.__session.get_api()

        self.fabricate_event = Fabric()

    async def _route(self, event):
        await producer.transfer_event(event)

    async def _fabric(self, event: VkBotEvent):
        return await self.fabricate_event(event, self.api)

    async def _handle(self, event: VkBotEvent):
        event = await self._fabric(event)

        if event is not None:
            log_text = f"New event recived:\n{event.attr_str}"
            await logger.info(log_text)

            await self._route(event)

    async def run(self):
        """Starts listening VK longpoll server.
        When a new event is received,
        it sends it for handling,
        fabricates custom events class
        instances from raw JSON data.
        """
        log_text = "Starting listening longpoll server..."
        await logger.info(log_text)

        for vk_event in self.__longpoll.listen():
            await self._handle(vk_event)


fetcher = Fetcher()
