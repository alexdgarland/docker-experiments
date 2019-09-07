#! /usr/bin/env python3.6

# TODO - this needs proper logging

from http.server import HTTPServer, BaseHTTPRequestHandler
from os.path import join

from .config import ServerConfig
from .request_path import ParsedRequestPath
from .resource_fetching import get_resource_fetcher, RESOURCE_ROOT


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = ParsedRequestPath(self.path)
        response_details = get_resource_fetcher(parsed_path).get_response()
        self.send_response(response_details.response_code)
        self.send_header("Content-type", response_details.content_type)
        self.end_headers()
        self.wfile.write(response_details.body)


def main():
    server_config = ServerConfig.create(join(RESOURCE_ROOT, "server_defaults.yaml"))
    print(server_config)
    httpd = HTTPServer(server_config.address, SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
