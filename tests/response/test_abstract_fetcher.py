from pyfakefs.fake_filesystem_unittest import TestCase
from mock import Mock

from webserver.response.abstract import AbstractResourceFetcher

TEST_FILE_MODE = "rb"
TEST_CONTENT_TYPE = "image/myext"
TEST_CONVERTED_BODY = object()
TEST_RESOURCE_ROOT = "some/path"


class AbstractResourceFetcherTest(TestCase):

    class TestableImplementation(AbstractResourceFetcher):

        def __init__(self, parsed_request_path):
            super(AbstractResourceFetcherTest.TestableImplementation, self).__init__(parsed_request_path)
            self.captured_content_input = None

        @property
        def resource_root(self):
            return TEST_RESOURCE_ROOT

        @property
        def file_mode(self):
            return TEST_FILE_MODE

        @property
        def content_type(self):
            return TEST_CONTENT_TYPE

        def convert_resource_content_to_body(self, content):
            self.captured_content_input = content
            return TEST_CONVERTED_BODY

    def setUp(self):
        self.existing_file = "good-route.myext"
        self.directory = "some_dir"
        self.good_request_path = Mock(request_dir=self.directory, request_filename=self.existing_file)
        self.expected_good_resource_path = f"{TEST_RESOURCE_ROOT}/{self.directory}/{self.existing_file}"
        self.resource_content = b"Some file content"
        self.setUpPyfakefs()
        self.fs.create_file(file_path=self.expected_good_resource_path, contents=self.resource_content)

    def test_creates_expected_resource_path(self):
        fetcher = self.TestableImplementation(self.good_request_path)
        self.assertEqual(fetcher.resource_path, self.expected_good_resource_path)

    def test_content_converter_called_as_expected(self):
        fetcher = self.TestableImplementation(self.good_request_path)
        fetcher.get_response()
        self.assertEqual(fetcher.captured_content_input, self.resource_content)

    def test_gets_expected_response_where_file_exists_at_resource_path(self):
        fetcher = self.TestableImplementation(self.good_request_path)
        response = fetcher.get_response()

        self.assertEqual(response.response_code, 200)
        self.assertEqual(response.content_type, TEST_CONTENT_TYPE)
        self.assertEqual(response.body, TEST_CONVERTED_BODY)

    def test_gets_not_found_response_where_resource_path_empty(self):
        bad_request_path = Mock(
            request_dir=self.directory, request_filename="bad-route.myext", request_base_path="some-request-path"
        )

        fetcher = self.TestableImplementation(bad_request_path)
        response = fetcher.get_response()

        self.assertEqual(response.response_code, 404)
        self.assertEqual(response.content_type, "text/html")
        self.assertEqual(response.body, b"ERROR - resource \"some-request-path\" was not found")
