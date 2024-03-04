"""Module "events".
"""
from vk_api import VkApi
from tools import (
    timestamp,
    msk_now
)
from logger import logger


class BaseEvent(object):
    """Custom description of an event
    coming from a longpoll server.
    """
    # VK api object
    # It is necessary for receipt
    # an additional data of the events
    # and making actions with it
    _api: VkApi = None

    # Event data
    ts: int = None
    datetime: str = None
    event_id: str = None
    event_type: str = None

    def __init__(self, raw_event: dict, api: VkApi):
        self.ts = timestamp()
        self.datetime = msk_now()
        self.event_type = raw_event.get("type")
        self.event_id = raw_event.get("event_id")

        self.__api = api


    def _get_userinfo(self, user_id: int):
        user_info = self.api.users.get(
            user_ids=user_id,
            fields=["domain"]
        )

        if not user_info:
            user_info = {}
            log_text = "Unable to obtain user information." \
                       "Bot don't have administrator rights or" \
                       "user doesn't exist."
            logger.info(log_text)

        else:
            user_info = user_info[0]

        return user_info


    def _get_peerinfo(self, peer_id: int):
        peer_info = self.api.messages.getConversationsById(
            peer_ids=peer_id
        )

        if peer_info.get("count") == 0:
            peer_info = {}
            log_text = "Unable to obtain conversation information." \
                       "Bot don't have administrator rights or" \
                       "conversation doesn't exist."
            logger.info(log_text)

        else:
            peer_info = peer_info["items"][0]["chat_settings"]

        return peer_info


    @property
    def api(self):
        """Returns the VKontakte API object from the parent class.

        Returns:
            VkApi: vk api object.
        """
        return self.__api


    @property
    def attr_str(self) -> str:
        """Returns a string representation of the class's. 
        Attributes as text in a convenient form.
        
        Returns:
            str: Data represintation.
        """
        blacklisted_keys = (
            "_BaseEvent__api",
        )

        summary = ""

        for key, value in vars(self).items():
            if key not in blacklisted_keys:
                summary += f"{key}: {value} \n"
        summary += "-------------------------------------------------"

        return summary


    @property
    def as_dict(self) -> dict:
        """Returns a dict representation
        of the class's.
        Returns:
            dict: Dict object.
        """
        data = {
            key: value for key, value in vars(self).items()
        }
        data.pop("_BaseEvent__api")

        return data
