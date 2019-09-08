from unittest2 import TestCase
from mock import Mock, patch

from webserver.response import get_resource_fetcher, PAGE_TEMPLATE_PARAMS


class GetResourceFetcherTest(TestCase):

    @patch("webserver.response.ImageResourceFetcher")
    def test_gets_image_fetcher_if_image_path(self, image_fetcher_constructor_mock):
        request_path = Mock(request_dir="images")

        returned_fetcher = get_resource_fetcher(request_path)

        image_fetcher_constructor_mock.assert_called_once_with(request_path)
        self.assertEqual(returned_fetcher, image_fetcher_constructor_mock.return_value)

    @patch("webserver.response.PageResourceFetcher")
    def test_gets_page_fetcher_if_no_path(self, page_fetcher_constructor_mock):
        request_path = Mock(request_dir="")

        returned_fetcher = get_resource_fetcher(request_path)

        page_fetcher_constructor_mock.assert_called_once_with(request_path, PAGE_TEMPLATE_PARAMS)
        self.assertEqual(returned_fetcher, page_fetcher_constructor_mock.return_value)
