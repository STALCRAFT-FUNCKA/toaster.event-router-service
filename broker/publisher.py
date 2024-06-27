"""Module "producer"."""

from redis import Redis
import config
import pickle
from typing import NoReturn


class Publisher(object):
    """DOCSTRING"""

    def __init__(self) -> NoReturn:
        self.client: Redis = Redis(host=config.BROKER_ADDR, port=6379, db=0)

    # TODO: make logs
    # TODO: handle possible exeptions
    def publish(self, obj: object, channel_name: str) -> int:
        """DOCSTRING"""

        data = self.__serialize(obj)
        status = self.client.publish(channel_name, data)

        return status

    @staticmethod
    def __serialize(obj: object) -> str:
        return pickle.dumps(obj=obj, protocol=pickle.HIGHEST_PROTOCOL)
