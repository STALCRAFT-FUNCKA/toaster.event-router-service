"""Module "fabric".

File:
    fabric.py

About:
    This file defines the Fabric class, which produces
    custom event objects from raw VK events.
"""

from typing import Dict, Optional, Union
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent
from toaster.broker.events import (
    Event,
    Message,
    Reply,
    Reaction,
    Button,
    User,
    Peer,
)
import config


RawData = Dict[str, Union[str, int]]


class Fabric:
    """Custom event factory class."""

    def __call__(self, vk_event: VkBotEvent, api: VkApi) -> Event:
        """Converts a raw VK event into a custom event object.

        Args:
            vk_event (VkBotEvent): Raw VK event.
            api (VkApi): VK API object.

        Returns:
            Event: Custom VK event object.
        """

        self._api = api
        return self.__handle(vk_event.raw, api)

    def __handle(self, raw_event: RawData, api: VkApi) -> Optional[Event]:
        event = Event(
            raw_event=raw_event,
            event_type=self.__get_event_type(raw_event),
        )

        message_obj = (
            raw_event.get("object")
            if event.event_type in ("button", "reaction")
            else raw_event.get("object").get("message")
        )

        if not message_obj:
            # TODO: Rise error inside try-except block and log it
            return None

        self.__set_event_attributes(
            event=event,
            msg_obj=message_obj,
        )

        return event

    def __set_event_attributes(self, event: Event, msg_obj: RawData) -> None:
        attribute_methods = {
            "user": self.__get_user_data,
            "peer": self.__get_peer_data,
        }

        if event.event_type == "button":
            attribute_methods["button"] = self.__get_button_data
        elif event.event_type == "reaction":
            attribute_methods["reaction"] = self.__get_reaction_data
        else:
            attribute_methods["message"] = self.__get_message_data

        for name, method in attribute_methods.items():
            event.add_object(name=name, value=method(msg_obj=msg_obj))

    @staticmethod
    def __get_event_type(raw_event: RawData) -> str:
        if raw_event.get("type") == "message_new":
            text: str = raw_event["object"]["message"].get("text")
            if text.startswith(config.COMMAND_PREFIXES):
                return "command"

            return "message"

        if raw_event.get("type") == "message_event":
            return "button"

        if raw_event.get("type") == "message_reaction_event":
            return "reaction"

    def __get_user_data(self, msg_obj: RawData) -> User:
        uuid = (
            msg_obj.get("user_id")
            or msg_obj.get("from_id")
            or msg_obj.get("reacted_id")
        )

        user_info = self._api.users.get(user_ids=uuid, fields=["domain"])
        user_info = user_info[0] if user_info else {}

        result = User(
            uuid=uuid,
            name=" ".join(
                [
                    user_info.get("first_name"),
                    user_info.get("last_name"),
                ]
            ),
            firstname=user_info.get("first_name"),
            lastname=user_info.get("last_name"),
            nick=user_info.get("domain"),
        )

        return result

    def __get_peer_data(self, msg_obj: RawData) -> Peer:
        bpid = msg_obj.get("peer_id")

        peer_info = self._api.messages.getConversationsById(peer_ids=bpid)
        peer_info = (
            peer_info["items"][0]["chat_settings"]
            if peer_info.get("count") != 0
            else {}
        )

        result = Peer(
            bpid=bpid,
            cid=bpid - config.VK_GROUP_ID_DELAY,
            name=peer_info.get("title"),
        )

        return result

    def __get_message_data(self, msg_obj: RawData) -> Reply:
        def _parse_reply(reply: Dict):
            return Reply(
                uuid=reply.get("from_id"),
                cmid=reply.get("conversation_message_id"),
                text=reply.get("text"),
            )

        cmid = msg_obj.get("conversation_message_id")
        bpid = msg_obj.get("peer_id")

        msg_obj = self._api.messages.getByConversationMessageId(
            peer_id=bpid,
            conversation_message_ids=cmid,
        )
        msg_obj = msg_obj["items"][0] if msg_obj["count"] else {}

        attachments = []
        msg_attachments = msg_obj.get("attachments")
        if msg_attachments:
            for attachment in msg_attachments:
                attachments.append(attachment.get("type"))

        if msg_obj.get("geo"):
            attachments.append("geo")

        if reply := msg_obj.get("reply_message"):
            reply = _parse_reply(reply)
            attachments.append("reply")

        if forward := msg_obj.get("fwd_messages"):
            forward = [_parse_reply(fwd) for fwd in forward if fwd.get("peer_id")]

            # The attachments "forward" tag may also be present
            # If forward = []
            # This is because forwarded messages
            # Transform into objects only if they
            # Are in the same conversation where they were forwarded
            attachments.append("forward")

        return Message(
            cmid=cmid,
            text=msg_obj.get("text"),
            reply=reply,
            forward=forward,
            attachments=attachments,
        )

    def __get_button_data(self, msg_obj: RawData) -> Button:
        return Button(
            cmid=msg_obj.get("conversation_message_id"),
            beid=msg_obj.get("event_id"),
            payload=msg_obj.get("payload"),
        )

    def __get_reaction_data(self, msg_obj: RawData) -> Reaction:
        return Reaction(
            cmid=msg_obj.get("cmid"),
            rid=msg_obj.get("reaction_id"),
        )
