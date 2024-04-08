"""Module "producer"."""

from .body import Producer


class CustomProducer(Producer):
    """Custom producer class.
    Preferences for implimentation of custom
    functions for working with data that needs
    to be pushed into a queue inside RabbitMQ.
    """

    event_queues = {
        "command_call": "commands",
        "message_new": "messages",
        "button_pressed": "buttons",
    }

    async def transfer_event(self, event):
        """A function that provides the ability to send an event
        to event handler services via a queue in RabbitMQ.

        Args:
            event (MessageEvent): Custom vk message event.
        """
        queue = self.event_queues.get(event.event_type, "Unknown")
        data = event.as_dict

        if queue != "Unknown":
            await self._send_data(data, queue)


producer = CustomProducer()
