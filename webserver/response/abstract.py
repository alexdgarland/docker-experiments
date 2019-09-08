from abc import ABC, abstractproperty
from os.path import join

from ..resource import RESOURCE_ROOT


class HttpResponseDetails(object):

    def __init__(self, response_code, content_type, body):
        self.response_code = response_code
        self.content_type = content_type
        self.body = body


class AbstractResourceFetcher(ABC):

    def __init__(self, parsed_request_path):
        self._request_path = parsed_request_path

    @property
    def resource_root(self):
        return RESOURCE_ROOT

    @abstractproperty
    def file_mode(self):
        pass

    @abstractproperty
    def content_type(self):
        pass

    @property
    def full_resource_dir(self):
        # Default pass-through implementation
        return self._request_path.request_dir

    @property
    def resource_filename(self):
        # Default pass-through implementation
        return self._request_path.request_filename

    @property
    def resource_path(self):
        return join(self.resource_root, self.full_resource_dir, self.resource_filename)

    def convert_resource_content_to_body(self, content):
        # Default pass-through implementation
        return content

    @property
    def not_found_response(self):
        error_message = f"ERROR - resource \"{self._request_path.request_base_path}\" was not found"
        return HttpResponseDetails(404, "text/html", error_message.encode())

    def get_response(self):
        try:
            with open(self.resource_path, self.file_mode) as f:
                content = f.read()
        except FileNotFoundError as fe:
            return self.not_found_response
        body = self.convert_resource_content_to_body(content)
        return HttpResponseDetails(200, self.content_type, body)
