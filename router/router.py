"""Module "router".
About:
    A file that describes the router
    class required to create custom
    event objects.
"""
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent
import config
from client import clsoc
from events import (
    BaseEvent,
    MessageEvent,
    ButtonEvent
)


class Router(object):
    """A router class that creates custom events
    according to the type of raw event.

    Args:
        raw_event (Event): vk longpoll event.
        api (VkApi): vk api object.

    Returns:
        CustomEvent: Custom event
    """
    _routes = {
        "message_new": MessageEvent,
        "message_event": ButtonEvent
    }

    def _route(self, raw_event: dict, api: VkApi) -> BaseEvent:
        """The function determines the type of raw event,
        and then routes it to the desired custom event for subsequent redefinition.

        Args:
            raw_event (Event): vk longpoll event object.
            api (VkApi): vk api object.

        Returns:
            CustomEvent: Custom event object.
        """
        reason = None
        if raw_event.get("type") not in self._routes:
            reason = "missing route"

        if reason is not None:
            log_text = f"Event <{raw_event.get('event_id')}|{raw_event.get('type')}> skipped." \
            f"Reason: {reason}\n"
            clsoc.log_workstream(config.SERVICE_NAME, log_text)

            return None

        return self._routes[raw_event.get("type")](raw_event, api)


    def __call__(self, vk_event: VkBotEvent, api: VkApi) -> BaseEvent:
        return self._route(vk_event.raw, api)
