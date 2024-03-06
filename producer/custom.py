"""Module "producer".
"""
import json
from .body import Producer


class CustomProducer(Producer):
    """Custom producer class.
    Preferences for implimentation of custom
    functions for working with data that needs
    to be pushed into a queue inside RabbitMQ.
    """
    event_queues = {
        "command_call": "commands",
        #"message_new": "messages",
        #"button_pressed": "buttons" #TODO: enable later
    }

    async def transfer_event(self, event: "MessageEvent"):
        """A function that provides the ability to send an event
        to event handler services via a queue in RabbitMQ.

        Args:
            event (MessageEvent): Custom vk message event.
        """
        queue = self.event_queues.get(event.event_type, "Unknown")
        data = json.dumps(event.as_dict)

        if queue != "Unknown":
            encoded = self._serialize(data)
            await self._send_data(encoded, queue)\



producer = CustomProducer()
