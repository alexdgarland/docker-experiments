from ruamel.yaml import safe_load
from os import environ


class ServerConfig(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)

    @property
    def address(self):
        return self.ip, self.port

    def __repr__(self):
        return f"Server configuration - IP: {self.ip}, Port: {self.port}"

    @classmethod
    def create(cls, defaults_file_path):
        with open(defaults_file_path) as f:
            defaults = safe_load(f.read())

        return ServerConfig(
            ip=defaults["ip"],
            port=environ.get("WEBSERVER_PORT") or defaults["port"]
        )
