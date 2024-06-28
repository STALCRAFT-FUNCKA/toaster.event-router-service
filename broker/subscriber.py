"""Module "broker"."""

from redis import Redis
import dill as pickle
from typing import NoReturn, Any


class Subscriber(object):
    """DOCSTRING"""

    def __init__(
        self, host: str = "localhost", port: int = 6379, db: int = 0
    ) -> NoReturn:
        r = Redis(host=host, port=port, db=db)
        self.client = r.pubsub()

    # TODO: Make logs
    # TODO: handle possible exeptions
    def listen(self, channel_name: str) -> object:
        """DCOSTRING"""

        self.client.subscribe(channel_name)
        for event in self.client.listen():
            if event.get("type") == "message":
                yield self.__deserialize(event.get("data"))

    @staticmethod
    def __deserialize(data: bytes) -> Any:
        return pickle.loads(data=data)
