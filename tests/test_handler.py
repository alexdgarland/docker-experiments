from unittest2 import TestCase
from mock import patch, Mock

from webserver.handler import SimpleHTTPRequestHandler
from webserver.response.abstract import HttpResponseDetails

TEST_RESPONSE_DETAILS = HttpResponseDetails(object(), object(), object())


class MyTestCase(TestCase):

    def setUp(self):
        self.test_path = "some/path"

    @patch("webserver.handler.ParsedRequestPath")
    @patch("webserver.handler.get_resource_fetcher")
    def test_build_response_method(self, get_resource_fetcher_mock, parsedpath_constructor_mock):

        response = SimpleHTTPRequestHandler.build_response(self.test_path)

        parsedpath_constructor_mock.assert_called_once_with(self.test_path)

        get_resource_fetcher_mock.assert_called_once_with(parsedpath_constructor_mock.return_value)

        final_response_method = get_resource_fetcher_mock.return_value.get_response
        self.assertEqual(response, final_response_method.return_value)

    @patch("webserver.handler.SimpleHTTPRequestHandler.build_response", return_value=TEST_RESPONSE_DETAILS)
    def test_handler_method(self, response_builder_mock):

        mock_handler = Mock()
        SimpleHTTPRequestHandler.handle_get(self.test_path, mock_handler)

        mock_handler.send_response.assert_called_once_with(TEST_RESPONSE_DETAILS.response_code)
        mock_handler.send_header.assert_called_once_with("Content-type", TEST_RESPONSE_DETAILS.content_type)
        mock_handler.end_headers.assert_called_once_with()
        mock_handler.wfile.write.assert_called_once_with(TEST_RESPONSE_DETAILS.body)
