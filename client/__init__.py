"""Module "cliient".
About:
    Provides a client socket class for communication
    with server sockets of other microservices. Allows
    send data in JSON format.
"""
from .socket import client


__all__ = (
    "client",
)
