"""Module "fetcher".
About:
    A file containing a description of
    the fetcher main class. Fetcher receives
    data from VK longpoll server by сщььгтшен 
    access token.
"""
from vk_api import VkApi
from vk_api.bot_longpoll import (
    VkBotLongPoll,
    VkBotEvent
)
from client import clsoc
import config
from .fabric import Fabric
from .router import Router


class Fetcher(object):
    """Fetcher main class.
    Provides receiving events from
    VK longpoll server with a
    community access token.
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
        self.route_event = Router()

    async def _route(self, event: "BaseEvent"):
        if not await self.route_event(event):
            reason = "missing route"
            log_text = f"Unable to route event <{event.event_id}|{reason}>"
            await clsoc.log_workstream(config.SERVICE_NAME, log_text)


    async def _fabric(self, event: VkBotEvent) -> "BaseEvent":
        return await self.fabricate_event(event, self.api)


    async def _handle(self, event: VkBotEvent):
        event = await self._fabric(event)

        log_text = f"New event recived:\n{event.attr_str}"
        await clsoc.log_workstream(config.SERVICE_NAME, log_text)

        await self._route(event)


    async def run(self):
        """Starts listening VK longpoll server.
        When a new event is received,
        it sends it for handling,
        fabricates custom events class
        instances from raw JSON data.
        """
        log_text = "Starting listening longpoll server..."
        await clsoc.log_workstream(config.SERVICE_NAME, log_text)

        for vk_event in self.__longpoll.listen():
            await self._handle(vk_event)
