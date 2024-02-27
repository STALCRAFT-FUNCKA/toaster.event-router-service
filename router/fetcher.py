"""A file containing a description of the bot's main class with all its functions.
"""
from vk_api import VkApi
from vk_api.bot_longpoll import (
    VkBotLongPoll
)
from client import clsoc
import config
from .router import Router


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

        self.router = Router()


    def run(self):
        """Starts listening VK longpoll server.
        """
        log_text = "Starting listening longpoll server..."
        clsoc.log_workstream(config.SERVICE_NAME, log_text)

        for vk_event in self.__longpoll.listen():
            event = self.router(vk_event, self.api)

            log_text = f"New event recived:\n{event.attr_str}"
            clsoc.log_workstream(config.SERVICE_NAME, log_text)
