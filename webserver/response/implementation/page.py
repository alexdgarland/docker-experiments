from os.path import join

from jinja2 import Template

from ..abstract import AbstractResourceFetcher


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
