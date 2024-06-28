"""Module "broker"."""

from redis import Redis
import dill as pickle
from typing import NoReturn


class Publisher(object):
    """DOCSTRING"""

    def __init__(
        self, host: str = "localhost", port: int = 6379, db: int = 0
    ) -> NoReturn:
        self.client = Redis(host=host, port=port, db=db)

    # TODO: make logs
    # TODO: handle possible exeptions
    def publish(self, obj: object, channel_name: str) -> int:
        """DOCSTRING"""

        data = self.__serialize(obj)
        status = self.client.publish(channel_name, data)

        return status

    @staticmethod
    def __serialize(obj: object) -> bytes:
        return pickle.dumps(obj=obj, protocol=pickle.HIGHEST_PROTOCOL)
