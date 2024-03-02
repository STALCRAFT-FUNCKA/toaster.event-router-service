"""Module "cliient".
About:

"""
import json
import pika
import config



class Client(object):
    """
    """
    event_queues = {
        "command_call": "commands",
        "message_new": "messages",
        "button_pressed": "buttons" 
    }

    async def log_workstream(self, logger_name: str, text:str , logging_lvl: str = "info") -> bool:
        """
        """
        data = {
            "name": logger_name,
            "mode": logging_lvl,
            "text": text
        }

        queue = "logs"

        return await self._send_data(data, queue)


    async def transfer_event(self, event: "MessageEvent"):
        """
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



client = Client()
