"""Module "cliient".
About:

"""
import pickle
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
        data = self._serialize({
            "name": logger_name,
            "mode": logging_lvl,
            "text": text
        })

        queue = "logs"

        return await self._send_data(data, queue)


    async def transfer_event(self, event: "MessageEvent"):
        """
        """
        queue = self.event_queues.get(event.event_type, "Unknown")
        data = self._serialize(event)

        if queue != "Unknown":
            data = self._serialize(event)
            await self._send_data(data, queue)


    async def _send_data(self, data: bytes, queue: str):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config.QUEUE_BROKER_IP
            )
        )
        channel = connection.channel()

        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=self._serialize(data),
        )

        connection.close()


    @staticmethod
    def _serialize(obj: object) -> bytes:
        return pickle.dumps(obj)


    @staticmethod
    def _deserialize(bts: bytes) -> object:
        return pickle.loads(bts)



client = Client()
