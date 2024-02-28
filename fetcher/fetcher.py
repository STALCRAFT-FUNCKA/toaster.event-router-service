"""A file containing a description of the bot's main class with all its functions.
"""
import asyncio
from vk_api import VkApi
from vk_api.bot_longpoll import (
    VkBotLongPoll,
    VkBotEvent
)
from client import clsoc
import config
from .fabric import Fabric


class Fetcher(object):
    """Fetcher main class.
    """
    def __init__(self):
        self.__session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION
        )

        self.__longpoll = VkBotLongPoll(
            vk=self.__session,
            wait=config.LONGPOLL_REQUEST_TD,
            group_id=config.GROUP_ID
        )

        self.api = self.__session.get_api()

        self.fabricate_event = Fabric()


    async def _fabric(self, event: VkBotEvent) -> "BaseEvent":
        return await self.fabricate_event(event, self.api)


    async def _handle(self, event: VkBotEvent):
        event = await self._fabric(event)

        # TODO: Сделать переброску ивентов в формате JSON на другие сервисы

        log_text = f"New event recived:\n{event.attr_str}"
        await clsoc.log_workstream(config.SERVICE_NAME, log_text)


    async def run(self):
        """Starts listening VK longpoll server.
        """
        log_text = "Starting listening longpoll server..."
        await clsoc.log_workstream(config.SERVICE_NAME, log_text)

        for vk_event in self.__longpoll.listen():
            await self._handle(vk_event)
