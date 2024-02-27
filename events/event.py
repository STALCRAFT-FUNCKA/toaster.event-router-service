from vk_api import VkApi
from .base import BaseEvent


VK_GROUP_ID_DELAY = 2000000000


class MessageEvent(BaseEvent):
    """Custom message event.
    """
    # message data
    from_id: int = None
    peer_id: int = None
    chat_id: int = None
    cmid: int = None

    # message content
    text: str = None
    reply: dict = None # dcit form
    forward: list = None # list of dicts
    attachments: list = None # list of dicts

    # additional
    from_name = None
    from_nickname: str = None
    peer_name = None

    def __init__(self, raw_event: dict, api: VkApi):
        super().__init__(raw_event, api)

        # building event fields
        self.__get_data(raw_event)
        self.__get_content(raw_event)
        self.__get_additionals()


    def __get_data(self, raw_event: dict):
        message = raw_event.get("object")
        if message is None:
            return

        message = message["message"]

        self.from_id = message.get("from_id")
        self.peer_id = message.get("peer_id")
        self.chat_id = self.peer_id - VK_GROUP_ID_DELAY
        self.cmid = message.get("conversation_message_id")
        self.timestamp = message.get("date")


    def __get_content(self, raw_event: dict):
        message = raw_event.get("object")

        message = message["message"]

        self.text = message.get("text")
        self.reply = message.get("reply_message")
        self.forward = message.get("fwd_messages")
        self.attachments = message.get("attachments")


    def __get_additionals(self):
        user_info = self.__get_userinfo()
        peer_info = self.__get_peerinfo()

        self.from_name = " ".join([
            user_info.get("first_name"),
            user_info.get("last_name")
        ])
        self.from_nickname = user_info.get("domain")
        self.peer_name = peer_info.get("title")


    def __get_userinfo(self):
        necessary_feilds = [
            "domain",
        ]
        user_info = super().api.users.get(
            user_ids=self.from_id,
            fields=necessary_feilds
        )
        if not user_info:
            user_info = {}

        else:
            user_info = user_info[0]

        return user_info


    def __get_peerinfo(self):
        peer_info = super().api.messages.getConversationsById(
            peer_ids=self.peer_id
        )

        if peer_info.get("count") == 0:
            peer_info = {}

        else:
            peer_info = peer_info["items"][0]["chat_settings"]

        return peer_info



class ButtonEvent(BaseEvent):
    """Custom button event.
    """
    # message data
    user_id: int = None
    peer_id: int = None
    chat_id: int = None
    cmid: int = None

    # button content
    button_event_id: str = None
    payload: dict = None

    # additional
    from_name = None
    from_nickname: str = None
    peer_name = None


    def __init__(self, raw_event: dict, api: VkApi):
        super().__init__(raw_event, api)

        # custom event_type
        self.event_type = "button_pressed"

        # building event fields
        self.__get_data(raw_event)
        self.__get_content(raw_event)
        self.__get_additionals()


    def __get_data(self, raw_event: dict):
        event_object = raw_event.get("object")

        self.from_id = event_object.get("user_id")
        self.peer_id = event_object.get("peer_id")
        self.chat_id = self.peer_id - VK_GROUP_ID_DELAY
        self.cmid = event_object.get("conversation_message_id")


    def __get_content(self, raw_event: dict):
        event_object = raw_event.get("object")

        self.payload = event_object.get("payload")
        self.button_event_id = event_object.get("event_id")


    def __get_additionals(self):
        user_info = self.__get_userinfo()
        peer_info = self.__get_peerinfo()

        self.from_name = " ".join([
            user_info.get("first_name"),
            user_info.get("last_name")
        ])
        self.from_nickname = user_info.get("domain")
        self.peer_name = peer_info.get("title")


    def __get_userinfo(self):
        necessary_feilds = [
            "domain",
        ]
        user_info = super().api.users.get(
            user_ids=self.from_id,
            fields=necessary_feilds
        )
        if not user_info:
            user_info = {}
        else:
            user_info = user_info[0]

        return user_info


    def __get_peerinfo(self):
        peer_info = super().api.messages.getConversationsById(
            peer_ids=self.peer_id
        )

        if peer_info.get("count") == 0:
            peer_info = {}

        else:
            peer_info = peer_info["items"][0]["chat_settings"]

        return peer_info
