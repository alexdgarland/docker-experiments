#! /usr/bin/env python3.6

# TODO - this needs proper logging

from http.server import HTTPServer
from os.path import join

from .config import ServerConfig
from .resource import RESOURCE_ROOT
from .handler import SimpleHTTPRequestHandler


def main():
    server_config = ServerConfig.create(join(RESOURCE_ROOT, "server_defaults.yaml"))
    print(server_config)
    httpd = HTTPServer(server_config.address, SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
