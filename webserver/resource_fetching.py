
from abc import ABC, abstractmethod, abstractproperty
from getpass import getuser
from os.path import dirname, join

from jinja2 import Template

RESOURCE_ROOT = dirname(__file__)


# TODO - this needs unit tests and proper logging


TEMPLATE_PARAMS = {
    "username": getuser()
}


def get_resource_fetcher(parsed_request_path):
    if parsed_request_path.request_dir == "images":
        return ImageResourceFetcher(parsed_request_path)
    else:
        return PageResourceFetcher(parsed_request_path, TEMPLATE_PARAMS)


class HttpResponseDetails(object):

    def __init__(self, response_code, content_type, body):
        self.response_code = response_code
        self.content_type = content_type
        self.body = body


class AbstractResourceFetcher(ABC):

    def __init__(self, parsed_request_path):
        self._request_path = parsed_request_path

    @property
    def full_resource_dir(self):
        # Default pass-through implementation
        return self._request_path.request_dir

    @property
    def resource_filename(self):
        # Default pass-through implementation
        return self._request_path.request_filename

    @abstractproperty
    def file_mode(self):
        pass

    @abstractproperty
    def content_type(self):
        pass

    @abstractmethod
    def convert_resource_content_to_body(self, content):
        pass

    def get_response(self):
        resource_path = join(RESOURCE_ROOT, self.full_resource_dir, self.resource_filename)
        try:
            with open(resource_path, self.file_mode) as f:
                content = f.read()
        except FileNotFoundError as fe:
            error_body = f"ERROR - resource \"{self._request_path.request_path}\" was not found".encode()
            return HttpResponseDetails(404, "text/html", error_body)
        body = self.convert_resource_content_to_body(content)
        return HttpResponseDetails(200, self.content_type, body)


class PageResourceFetcher(AbstractResourceFetcher):

    def __init__(self, parsed_request_path, template_parameters):
        super(PageResourceFetcher, self).__init__(parsed_request_path)
        self.template_parameters = template_parameters

    @property
    def full_resource_dir(self):
        return join("pages", self._request_path.request_dir)

    @property
    def resource_filename(self):
        return self._request_path.filename_root + ".j2"

    @property
    def file_mode(self):
        return "r"

    @property
    def content_type(self):
        return "text/html"

    def convert_resource_content_to_body(self, content):
        return Template(content).render(self.template_parameters).encode()


class ImageResourceFetcher(AbstractResourceFetcher):

    @property
    def file_mode(self):
        return "rb"

    @property
    def content_type(self):
        return f"image/{self._request_path.file_ext}"

    def convert_resource_content_to_body(self, content):
        return content
