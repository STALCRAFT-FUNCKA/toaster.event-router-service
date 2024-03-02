"""Module "cliient".
About:
    Provides a client socket class for communication
    with server sockets of other microservices. Allows
    send data in JSON format.
"""
from .body import producer


__all__ = (
    "producer",
)
