from posixpath import basename, dirname
from os.path import splitext


INDEX_PAGE = "index.html"


class ParsedRequestPath(object):

    def __init__(self, request_path):
        self.request_base_path = request_path

        # TODO Stripping off the leading "/" here is really important when we later try and join paths -
        # TODO  need to ensure that gets captured in tests as and when we write some!
        self.request_dir = dirname(self.request_base_path)[1:]

        name = basename(self.request_base_path)
        self.request_filename = INDEX_PAGE if name == "" else name  # Poor man's redirect ;-)
        self.filename_root, self.file_ext = splitext(self.request_filename)


    # TODO potential test cases:
    #   - "/" -> index page
    #   - regular page, with or without subfolder
    #   - image, with or without subfolder
