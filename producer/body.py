"""Module "producer".
"""
import json
import pika
import config


class Producer(object):
    """Producer's main class.
    Describes basic connection methods
    and sending data to RabbitMQ.
    """
    event_queues = {
        "command_call": "commands",
        "message_new": "messages",
        "button_pressed": "buttons" 
    }

    async def log_workstream(self, logger_name: str, text:str , logging_lvl: str = "info"):
        """A function that provides the ability to send a log
        to the general logging service via a queue in RabbitMQ.

        Args:
            logger_name (str): Name of the logger instance.
            text (str): Log text.
            logging_lvl (str, optional): Logging lvl. Defaults to "info".
        """
        data = {
            "name": logger_name,
            "mode": logging_lvl,
            "text": text
        }

        queue = "logs"

        await self._send_data(data, queue)


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
            await self._send_data(encoded, queue)


    async def _send_data(self, data: dict, queue: str):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config.QUEUE_BROKER_IP
            )
        )
        channel = connection.channel()

        json_string = json.dumps(data)

        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=self._serialize(json_string),
        )

        connection.close()


    @staticmethod
    def _serialize(string: str) -> bytes:
        return string.encode("utf-8")


    @staticmethod
    def _deserialize(byte_string: bytes) -> str:
        return byte_string.decode("utf-8")



producer = Producer()
