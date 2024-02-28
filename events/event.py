"""Module "events".
About:
    Provides custom VK events. Convenient form,
    additional data, nothing superfluous.
    Message and Button event.
"""
from vk_api import VkApi
import config
from .base import BaseEvent


class MessageEvent(BaseEvent):
    """Custom message event.
    """
    # user data
    user_id: int
    user_name: str
    user_nick: str

    # peer data
    peer_id: int
    peer_name: str
    chat_id: int

    # message data
    cmid: int
    text: str # TODO: addtext validating (Optional)
    reply: dict
    forward: list
    attachments: list

    def __init__(self, raw_event: dict, api: VkApi):
        super().__init__(raw_event, api)
        message = raw_event.get("object").get("message")

        self._get_userdata(message)
        self._get_peerdata(message)
        self._get_messagedata(message)


    def _get_userdata(self, message: dict):
        self.user_id = message.get("from_id")
        info = self._get_userinfo(self.user_id)
        self.user_name = " ".join([
                info.get("first_name"),
                info.get("last_name")
            ])
        self.user_nick = info.get("domain")


    def _get_peerdata(self, message: dict):
        self.peer_id = message.get("peer_id")
        info = self._get_peerinfo(self.peer_id)
        self.peer_name = info.get("title")
        self.chat_id = self.peer_id - config.VK_GROUP_ID_DELAY


    def _get_messagedata(self, message: dict):
        self.cmid = message.get("conversation_message_id")
        self.text = message.get("text")
        self.reply = message.get("reply_message")
        self.forward = message.get("fwd_messages")
        self.attachments = [
            attachment.get("type") for attachment in message.get("attachments")
        ]
        if message.get("geo"):
            self.attachments.append("geo")



class ButtonEvent(BaseEvent):
    """Custom button event.
    """
    # user data
    user_id: int
    user_name: str
    user_nick: str

    # peer data
    peer_id: int
    peer_name: str
    chat_id: int

    # button data
    cmid : int
    button_event_id: str
    payload: dict

    def __init__(self, raw_event: dict, api: VkApi):
        super().__init__(raw_event, api)
        self.event_type = "button_pressed"
        message = raw_event.get("object")

        self._get_userdata(message)
        self._get_peerdata(message)
        self._get_buttondata(message)


    def _get_userdata(self, message: dict):
        self.user_id = message.get("user_id")
        info = self._get_userinfo(self.user_id)
        self.user_name = " ".join([
                info.get("first_name"),
                info.get("last_name")
            ])
        self.user_nick = info.get("domain")


    def _get_peerdata(self, message: dict):
        self.peer_id = message.get("peer_id")
        info = self._get_peerinfo(self.peer_id)
        self.peer_name = info.get("title")
        self.chat_id = self.peer_id - config.VK_GROUP_ID_DELAY


    def _get_buttondata(self, message: dict):
        self.cmid = message.get("conversation_message_id")
        self.button_event_id = message.get("event_id")
        self.payload = message.get("payload")
