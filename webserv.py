#! /usr/bin/env python3.6

from http.server import HTTPServer, BaseHTTPRequestHandler
from getpass import getuser

USERNAME = getuser()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Hello, world from {USERNAME}!\n".encode())

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('0.0.0.0', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
