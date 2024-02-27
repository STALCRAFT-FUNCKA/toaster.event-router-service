import json
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM
)



class ClientSocket(object):
    client_soc = socket(
        AF_INET,
        SOCK_STREAM
    )

    ip_map = {
        "workstream_logging": "172.19.0.5",
    }

    def __init__(self, port: int = 8000):
        self.port = port


    def _get_addr(self, service: str):
        addr = (
            self.ip_map[service],
            self.port
        )

        return addr


    def log_workstream(self, logger_name: str, text:str , logging_lvl: str = "info") -> bool:
        data = {
            "name": logger_name,
            "mode": logging_lvl,
            "text": text
        }

        return self._send_workstream(data)


    def _send_workstream(self, data: dict) -> bool:
        self.client_soc.connect(self._get_addr("workstream_logging"))

        json_data = json.dumps(data)

        self.client_soc.sendall(json_data.encode("utf-8"))
        recived = self.client_soc.recv(1024)

        self.client_soc.close()

        # HTTP 202 - accepted
        if "202" in recived.decode('utf-8'):
            return True

        # HTTP 406 - rejected (not accepted)
        return False
