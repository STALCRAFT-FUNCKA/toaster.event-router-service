"""A file containing a description of the bot's main class with all its functions.
"""
from vk_api import VkApi
from vk_api.bot_longpoll import (
    VkBotLongPoll
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


    def run(self):
        """Starts listening VK longpoll server.
        """
        log_text = "Starting listening longpoll server..."
        clsoc.log_workstream(config.SERVICE_NAME, log_text)

        for vk_event in self.__longpoll.listen():
            event = self.fabricate_event(vk_event, self.api)

            # TODO: Сделать переброску ивентов в формате JSON на другие сервисы

            log_text = f"New event recived:\n{event.attr_str}"
            clsoc.log_workstream(config.SERVICE_NAME, log_text)
