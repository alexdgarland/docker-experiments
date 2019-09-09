from unittest2 import TestCase
from mock import Mock, patch

from webserver.response.implementation.image import ImageResourceFetcher
from webserver.response.implementation.page import PageResourceFetcher
from webserver.response.implementation.css import CssResourceFetcher


class ImageResourceFetcherTest(TestCase):

    def setUp(self):
        self.request_path = Mock(file_ext="myext")
        self.fetcher = ImageResourceFetcher(self.request_path)

    def test_file_mode_as_expected(self):
        self.assertEqual(self.fetcher.file_mode, "rb")

    def test_content_type_as_expected(self):
        self.assertEqual(self.fetcher.content_type, "image/myext")


class PageResourceFetcherTest(TestCase):

    def setUp(self):
        self.request_path = Mock(request_dir="some-dir", filename_root="mypage")
        self.template_params = object()
        self.fetcher = PageResourceFetcher(self.request_path, self.template_params)

    def test_full_resource_dir_as_expected(self):
        self.assertEqual(self.fetcher.full_resource_dir, "pages/some-dir")

    def test_resource_filename_as_expected(self):
        self.assertEqual(self.fetcher.resource_filename, "mypage.j2")

    def test_file_mode_as_expected(self):
        self.assertEqual(self.fetcher.file_mode, "r")

    def test_content_type_as_expected(self):
        self.assertEqual(self.fetcher.content_type, "text/html")

    @patch("webserver.response.implementation.page.Template")
    def test_resource_conversion_works_as_expected(self, template_constructor_mock):
        dummy_content = Mock()

        response_body = self.fetcher.convert_resource_content_to_body(dummy_content)

        template_constructor_mock.assert_called_once_with(dummy_content)

        render_method = template_constructor_mock.return_value.render
        render_method.assert_called_once_with(self.template_params)

        encode_method = render_method.return_value.encode
        encode_method.assert_called_once_with()

        self.assertEqual(response_body, encode_method.return_value)


class CssResourceFetcherTest(TestCase):

    def setUp(self):
        self.request_path = Mock()
        self.fetcher = CssResourceFetcher(self.request_path)

    def test_file_mode_as_expected(self):
        self.assertEqual(self.fetcher.file_mode, "r")

    def test_content_type_as_expected(self):
        self.assertEqual(self.fetcher.content_type, "text/css")

    def test_resource_conversion_works_as_expected(self):
        dummy_content = Mock()

        response_body = self.fetcher.convert_resource_content_to_body(dummy_content)

        dummy_content.encode.assert_called_once_with()
        self.assertEqual(response_body, dummy_content.encode.return_value)
