"""Module "cliient".
About:
    Provides a client socket class for communication
    with server sockets of other microservices. Allows
    send data in JSON format.
"""
import json
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM
)


class ClientSocket(object):
    """Client socket class.
    Provides functions for sending logs, as well as sending
    events after previous routing to the necessary
    microservices for their subsequent handling.
    """
    ip_map = {
        "localhost": "127.0.0.1",
        "workstream-logging-service": "172.19.0.5",
        "toaster.command-handling-service": "",
        "toaster.button-handling-service": "",
        "toaster.message-handling-service": "",
    }

    def __init__(self, port: int = 8000):
        self.port = port


    def _get_addr(self, service_name: str):
        addr = (
            self.ip_map[service_name],
            self.port
        )

        return addr


    async def log_workstream(self, logger_name: str, text:str , logging_lvl: str = "info") -> bool:
        """Sends JSON data to the
        general logging microservice.

        Args:
            logger_name (str): Logger name. (Service name)
            text (str): Log text.
            logging_lvl (str, optional): Logging level. Defaults to "info".

        Returns:
            bool: Transfering status.
        """
        data = {
            "name": logger_name,
            "mode": logging_lvl,
            "text": text
        }

        service_name = "workstream-logging-service"
        #service_name = "localhost"

        return await self._send_data(data, service_name)


    async def transfer_command(self, event: "MessageEvent"):
        pass # TODO: Заполнить после поднятия микросервиса


    async def transfer_message(self, event: "MessageEvent"):
        pass # TODO: Заполнить после поднятия микросервиса


    async def transfer_button(self, event: "ButtonEvent"):
        pass # TODO: Заполнить после поднятия микросервиса


    async def _send_data(self, data: dict, service_name: str) -> bool:
        client_soc = socket(AF_INET, SOCK_STREAM)
        client_soc.connect(self._get_addr(service_name))

        json_data = json.dumps(data)

        client_soc.sendall(json_data.encode("utf-8"))
        recived = client_soc.recv(1024)

        client_soc.close()

        # HTTP 202 - accepted
        if "202" in recived.decode('utf-8'):
            return True

        # HTTP 406 - rejected (not accepted)
        return False
