"""Module "broker"."""

from redis import Redis
import config
import pickle
from typing import NoReturn


class Subscriber(object):
    """DOCSTRING"""

    def __init__(self, channel_name: str) -> NoReturn:
        r: Redis = Redis(host=config.BROKER_ADDR, port=6379, db=0)
        self.client = r.pubsub()
        self.client.subscribe(channel_name)

    # TODO: Make logs
    # TODO: handle possible exeptions
    def listen(self) -> object:
        """DCOSTRING"""

        for event in self.client.listen():
            if event.get("type") == "message":
                yield self.__deserialize(event.get("data"))

    @staticmethod
    def __deserialize(data: bytes) -> object:
        return pickle.loads(data=data)
