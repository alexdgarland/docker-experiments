from http.server import BaseHTTPRequestHandler

from .request_path import ParsedRequestPath
from .response import get_resource_fetcher


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        SimpleHTTPRequestHandler.handle_get(path=self.path, handler=self)

    @staticmethod
    def build_response(path):
        parsed_path = ParsedRequestPath(path)
        return get_resource_fetcher(parsed_path).get_response()

    @staticmethod
    def handle_get(path, handler):

        response_details = SimpleHTTPRequestHandler.build_response(path)

        handler.send_response(response_details.response_code)
        handler.send_header("Content-type", response_details.content_type)
        handler.end_headers()
        handler.wfile.write(response_details.body)
