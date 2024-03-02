"""Module "fetcher".
About:
    A file that describes the fabric
    class required to create custom
    event objects.
"""
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent
import config
from producer import producer
from events import (
    BaseEvent,
    MessageEvent,
    ButtonEvent
)


class Fabric(object):
    """A router class that creates custom events
    according to the type of raw event.

    Args:
        raw_event (Event): vk longpoll event.
        api (VkApi): vk api object.

    Returns:
        CustomEvent: Custom event
    """
    _fabric_lines = {
        "message_new": MessageEvent,
        "message_event": ButtonEvent
    }

    async def _handle(self, raw_event: dict, api: VkApi) -> BaseEvent:
        """The function determines the type of raw event,
        and then routes it to the desired custom event for subsequent redefinition.

        Args:
            raw_event (Event): vk longpoll event object.
            api (VkApi): vk api object.

        Returns:
            CustomEvent: Custom event object.
        """
        reason = None
        if raw_event.get("type") not in self._fabric_lines:
            reason = "missing fabric line."

        if reason is not None:
            log_text = f"Event <{raw_event.get('event_id')}|{raw_event.get('type')}> skipped. " \
            f"Reason: {reason}\n"
            await producer.log_workstream(config.SERVICE_NAME, log_text)

            return None

        return self._fabric_lines[raw_event.get("type")](raw_event, api)


    async def __call__(self, vk_event: VkBotEvent, api: VkApi) -> BaseEvent:
        return await self._handle(vk_event.raw, api)
