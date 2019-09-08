from unittest2 import TestCase

from webserver.request_path import ParsedRequestPath


class ParsedRequestPathTest(TestCase):

    def test_handles_page(self):
        """NB this test does NOT include an additional dir level of path, as per standard for pages at the moment."""
        parsed = ParsedRequestPath("/mypage.html")
        self.assertEqual(parsed.request_base_path, "/mypage.html")
        self.assertEqual(parsed.request_dir, "")
        self.assertEqual(parsed.request_filename, "mypage.html")
        self.assertEqual(parsed.filename_root, "mypage")
        self.assertEqual(parsed.file_ext, "html")

    def test_handles_image(self):
        """NB this test DOES include an additional dir level of path, as per standard for pages at the moment."""
        parsed = ParsedRequestPath("/images/hellobear.gif")
        self.assertEqual(parsed.request_base_path, "/images/hellobear.gif")
        self.assertEqual(parsed.request_dir, "images")
        self.assertEqual(parsed.request_filename, "hellobear.gif")
        self.assertEqual(parsed.filename_root, "hellobear")
        self.assertEqual(parsed.file_ext, "gif")

    def test_redirects_index_page_as_default(self):
        """Tests simple direct of '/' to index.html"""
        parsed = ParsedRequestPath("/")
        self.assertEqual(parsed.request_base_path, "/")
        self.assertEqual(parsed.request_dir, "")
        self.assertEqual(parsed.request_filename, "index.html")
        self.assertEqual(parsed.filename_root, "index")
        self.assertEqual(parsed.file_ext, "html")
