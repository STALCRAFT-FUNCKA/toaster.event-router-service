"""Module "fetcher".
About:
    Provides Fetcher class that receives data
    from VK longpoll server by community access
    token and roting events to queues in RabbitMQ.
"""
from .fetcher import Fetcher


__all__ = (
    "Fetcher",
)
