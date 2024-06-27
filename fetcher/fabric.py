"""Module "fetcher"."""

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent
from events import BaseEvent, MessageEvent, ButtonEvent


class Fabric(object):
    """DOCSTRING"""

    _routes = {
        "message_new": MessageEvent,
        "message_event": ButtonEvent,
    }

    def __handle(self, raw_event: dict, api: VkApi) -> BaseEvent | None:
        """The function determines the type of raw event,
        and then routes it to the desired custom event for subsequent redefinition.

        Args:
            raw_event (Event): vk longpoll event object.
            api (VkApi): vk api object.

        Returns:
            CustomEvent: Custom event object.
        """
        if raw_event.get("type") not in self._routes:
            return None

        return self._routes[raw_event.get("type")](raw_event)

    def __call__(self, vk_event: VkBotEvent, api: VkApi) -> BaseEvent:
        self.api
        return self.__handle(vk_event.raw, api)
