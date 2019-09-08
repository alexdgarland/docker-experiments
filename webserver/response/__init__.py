from getpass import getuser
from .implementation.image import ImageResourceFetcher
from .implementation.page import PageResourceFetcher

PAGE_TEMPLATE_PARAMS = {
    "username": getuser()
}


def get_resource_fetcher(parsed_request_path):
    if parsed_request_path.request_dir == "images":
        return ImageResourceFetcher(parsed_request_path)
    else:
        return PageResourceFetcher(parsed_request_path, PAGE_TEMPLATE_PARAMS)
