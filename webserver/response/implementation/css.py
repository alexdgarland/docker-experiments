from ..abstract import AbstractResourceFetcher


class CssResourceFetcher(AbstractResourceFetcher):

    @property
    def file_mode(self):
        return "r"

    @property
    def content_type(self):
        return "text/css"

    def convert_resource_content_to_body(self, content):
        return content.encode()
