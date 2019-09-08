from ..abstract import AbstractResourceFetcher


class ImageResourceFetcher(AbstractResourceFetcher):

    @property
    def file_mode(self):
        return "rb"

    @property
    def content_type(self):
        return f"image/{self._request_path.file_ext}"
