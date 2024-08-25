"""Module "fabric".

File:
    fabric.py

About:
    This file defines the Fabric class, which produces
    custom event objects from raw VK events.
"""

from typing import Dict, Optional, Union, List, Tuple
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent
from funcka_bots.events import BaseEvent, event_builder
import config


RawData = Dict[str, Union[str, int]]
Payload = RawData


class Fabric:
    """Custom event factory class."""

    def __call__(self, vk_event: VkBotEvent, api: VkApi) -> BaseEvent:
        """Converts a raw VK event into a custom event object.

        :param VkBotEvent vk_event: Raw VK event.
        :param VkApi api: VK API object.
        :return: Custom VK event object.
        :rtype: Event
        """

        self._api = api
        return self.__handle(vk_event.raw)

    def __handle(self, raw_event: RawData) -> Optional[BaseEvent]:
        event_type = self.__get_event_type(raw_event)
        event_id = raw_event.get("event_id")
        message_obj = (
            raw_event.get("object")
            if event_type in ("button", "reaction")
            else raw_event.get("object").get("message")
        )

        if not message_obj:
            # TODO: Rise error inside try-except block and log it
            return None

        peer = self._get_peer_data(message_obj)
        user = self._get_user_data(message_obj)
        message, message_reply, message_forward = self._get_message_data(message_obj)
        button = self._get_button_data(message_obj) if event_type == "button" else None
        reaction = (
            self._get_reaction_data(message_obj) if event_type == "reaction" else None
        )

        event = event_builder.build_vkevent(
            event_type=event_type,
            event_id=event_id,
            peer=peer,
            user=user,
            message=message,
            message_reply=message_reply,
            message_forward=message_forward,
            button=button,
            reaction=reaction,
        )
        return event

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

    def _get_user_data(self, msg_obj: RawData) -> Payload:
        uuid = (
            msg_obj.get("user_id")
            or msg_obj.get("from_id")
            or msg_obj.get("reacted_id")
        )

        user_info = self._api.users.get(user_ids=uuid, fields=["domain"])
        user_info = user_info[0] if user_info else {}

        payload = {
            "uuid": uuid,
            "name": " ".join(
                [
                    user_info.get("first_name"),
                    user_info.get("last_name"),
                ]
            ),
            "firstname": user_info.get("first_name"),
            "lastname": user_info.get("last_name"),
            "nick": user_info.get("domain"),
        }

        return payload

    def _get_peer_data(self, msg_obj: RawData) -> Payload:
        bpid = msg_obj.get("peer_id")

        peer_info = self._api.messages.getConversationsById(peer_ids=bpid)
        peer_info = (
            peer_info["items"][0]["chat_settings"]
            if peer_info.get("count") != 0
            else {}
        )

        payload = {
            "bpid": bpid,
            "cid": bpid - config.VK_PEER_ID_DELAY,
            "name": peer_info.get("title"),
        }

        return payload

    def _get_message_data(self, msg_obj: RawData) -> Tuple[Payload, List[Payload]]:
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
            reply_payload = self._get_message_reply_data(reply)
            attachments.append("reply")

        else:
            reply_payload = None

        if forward := msg_obj.get("fwd_messages"):
            forward_payload = self._get_message_forward_data(forward)
            attachments.append("forward")

        else:
            forward_payload = []

        payload = {
            "cmid": cmid,
            "text": msg_obj.get("text"),
            "attachments": attachments,
        }
        return (payload, reply_payload, forward_payload)

    def _get_message_reply_data(self, reply: RawData) -> Payload:
        paylaod = {
            "uuid": reply.get("from_id"),
            "cmid": reply.get("conversation_message_id"),
            "text": reply.get("text"),
        }
        return paylaod

    def _get_message_forward_data(self, forward: List[RawData]) -> List[Payload]:
        # TODO: Научить метод отличать пересланные сообщения из той же беседы, и из сторонней
        replies = [self._get_message_reply_data(fwd) for fwd in forward]
        return replies

    @staticmethod
    def _get_button_data(msg_obj: RawData) -> Payload:
        payload = {
            "cmid": msg_obj.get("conversation_message_id"),
            "beid": msg_obj.get("event_id"),
            "payload": msg_obj.get("payload"),
        }
        return payload

    @staticmethod
    def _get_reaction_data(msg_obj: RawData) -> Payload:
        payload = {
            "cmid": msg_obj.get("cmid"),
            "rid": msg_obj.get("reaction_id"),
        }
        return payload
