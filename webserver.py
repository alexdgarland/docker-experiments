#! /usr/bin/env python3.6

from os import environ
from getpass import getuser
from http.server import HTTPServer, BaseHTTPRequestHandler

from jinja2 import Template

SERVER_IP = "0.0.0.0"
DEFAULT_WEBSERVER_PORT = 80
INDEX_TEMPLATE_FILE = "pages/index.j2"


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    @property
    def index_page(self):
        with open(INDEX_TEMPLATE_FILE) as f:
            template = Template(f.read())
        return template.render(username=getuser())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.index_page.encode())


def run(port, server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = (SERVER_IP, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    webserver_port = int(environ.get("WEBSERVER_PORT", DEFAULT_WEBSERVER_PORT))
    run(port=webserver_port)
