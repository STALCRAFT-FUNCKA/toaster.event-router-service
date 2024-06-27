"""Module "fetcher"."""

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
import config
from logger import Logger
from broker import Publisher
from .fabric import Fabric


class Fetcher(object):
    """DOCSTRING"""

    __logger = Logger()
    __broker = Publisher()
    __fabric = Fabric()

    def __init__(self):
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

    def run(self):
        """Starts listening VK longpoll server."""

        self.__logger.info("Starting listening longpoll server...")

        for vk_event in self._longpoll.listen():
            # event = self.__fabric(vk_event, self.api)
            event = vk_event
            if event is not None:
                self.__logger.info(f"New event recived:\n{event.attr_str}")
                self.__broker.publish(
                    obj=event,
                    channel_name="test",
                )


fetcher = Fetcher()
