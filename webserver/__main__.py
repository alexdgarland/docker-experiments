#! /usr/bin/env python3.6

# TODO - this needs unit tests and proper logging

import sys
from getpass import getuser
from http.server import HTTPServer, BaseHTTPRequestHandler
from os import environ
from os.path import split, dirname

from jinja2 import Template

from .address import ServerAddressConfig

RESOURCE_ROOT = dirname(__file__)

# TODO load some of these from an app config file?
SERVER_IP = "0.0.0.0"
DEFAULT_WEBSERVER_PORT = 8000
INDEX_TEMPLATE_FILE = f"{RESOURCE_ROOT}/pages/index.j2"


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    @property
    def template_params(self):
        return {"username": getuser()}

    @property
    def index_page(self):
        with open(INDEX_TEMPLATE_FILE, "r") as f:
            template = Template(f.read())
        return template.render(self.template_params)

    def _content_get(self, content_type, body):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        print(f"Handling path {self.path}")

        # if self.path == "/":
        #     self._content_get("text/html", self.index_page.encode())

        directory = split(self.path)[0]
        # TODO full split here to dir, filename, filetype (MIME) (as a data object)

        # TODO - ultimately we are looking at behaviour like:
        #   If "/" serve index page (using text/html class with fixed param)
        #   Otherwise:
        #       Check if path exists - if not, 404
        #       Otherwise load from file and then:
        #       If exists and is pages/*.html, render, encode and serve as text/html
        #           (for the moment assume will always be a .j2 file with same dictionary)
        #       If exists and is images/*.filetype, serve as image/filetype with no further rendering or encoding

        resource_path = RESOURCE_ROOT + self.path

        if directory == '/images':
            with open(resource_path, "rb") as f:
                body_image = f.read()
            self._content_get("image/gif", body_image)
        else:
            self._content_get("text/html", self.index_page.encode())


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    # TODO break out this block for deciding how to config the server address
    webserver_port = int(environ.get("WEBSERVER_PORT", DEFAULT_WEBSERVER_PORT))

    server_address = (SERVER_IP, webserver_port)
    print(f"Starting webserver on: {server_address}")

    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
