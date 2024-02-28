import json
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM
)


class ClientSocket(object):
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
        data = {
            "name": logger_name,
            "mode": logging_lvl,
            "text": text
        }

        service_name = "workstream-logging-service"

        return await self._send_data(data, service_name)


    async def transfer_command(self):
        pass


    async def transfer_button(self):
        pass


    async def transfer_message(self):
        pass


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
