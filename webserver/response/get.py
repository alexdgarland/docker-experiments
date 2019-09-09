from getpass import getuser
from .implementation.image import ImageResourceFetcher
from .implementation.page import PageResourceFetcher
from .implementation.css import CssResourceFetcher

PAGE_TEMPLATE_PARAMS = {
    "username": getuser()
}


def get_resource_fetcher(parsed_request_path):

    def get_page_resource(rpath):
        return PageResourceFetcher(rpath, PAGE_TEMPLATE_PARAMS)

    return {
        "resources/images": ImageResourceFetcher,
        "resources/css": CssResourceFetcher
    }.get(parsed_request_path.request_dir, get_page_resource)(parsed_request_path)
