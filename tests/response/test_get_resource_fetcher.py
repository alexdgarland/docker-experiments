from unittest2 import TestCase
from mock import Mock, patch

from webserver.response.get import get_resource_fetcher, PAGE_TEMPLATE_PARAMS


class GetResourceFetcherTest(TestCase):

    def _check_get_as_expected(self, request_dir, expected_fetcher_mock, additional_expected_args=[]):
        request_path = Mock(request_dir=request_dir)

        returned_fetcher = get_resource_fetcher(request_path)

        expected_args = [request_path] + additional_expected_args
        expected_fetcher_mock.assert_called_once_with(*expected_args)
        self.assertEqual(returned_fetcher, expected_fetcher_mock.return_value)

    @patch("webserver.response.get.ImageResourceFetcher")
    def test_gets_image_fetcher_if_image_path(self, image_fetcher_constructor_mock):
        self._check_get_as_expected("resources/images", image_fetcher_constructor_mock)

    @patch("webserver.response.get.CssResourceFetcher")
    def test_gets_css_fetcher_if_css_path(self, css_fetcher_constructor_mock):
        self._check_get_as_expected("resources/css", css_fetcher_constructor_mock)

    @patch("webserver.response.get.PageResourceFetcher")
    def test_gets_page_fetcher_if_no_path(self, page_fetcher_constructor_mock):
        self._check_get_as_expected("", page_fetcher_constructor_mock, additional_expected_args=[PAGE_TEMPLATE_PARAMS])
