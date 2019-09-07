
from webserver.config import ServerConfig
from pyfakefs.fake_filesystem_unittest import TestCase
from mock import patch


class ServerConfigTest(TestCase):

    def setUp(self):
        self.default_ip = "0.0.0.0"
        self.default_port = "8000"
        self.defaults = {
            "ip": self.default_ip,
            "port": self.default_port
        }
        self.config_file_path = "/some/file/path"
        config_file_contents = f"ip: \"{self.default_ip}\"\nport: {self.default_port}"
        self.setUpPyfakefs()
        self.fs.create_file(self.config_file_path, contents=config_file_contents)

    def _test_create_method(self, environ_get_mock, expected_port):
        config = ServerConfig.create(defaults_file_path=self.config_file_path)

        environ_get_mock.assert_called_once_with("WEBSERVER_PORT")
        self.assertEqual(config.ip, self.default_ip)
        self.assertTrue(type(config.port) is int)
        self.assertEqual(config.port, expected_port)

    @patch("webserver.config.environ.get", return_value=None)
    def test_create_method_passes_defaults_from_file(self, environ_get_mock):
        self._test_create_method(environ_get_mock, 8000)

    @patch("webserver.config.environ.get", return_value="8001")
    def test_create_method_sets_port_from_environment_if_available(self, environ_get_mock):
        self._test_create_method(environ_get_mock, 8001)

    def test_get_address(self):
        config = ServerConfig(self.default_ip, self.default_port)

        self.assertEqual(config.address, (self.default_ip, 8000))

    def test_string_representation(self):
        config = ServerConfig(self.default_ip, self.default_port)

        self.assertEqual(f"{config}", "Server configuration - IP: 0.0.0.0, Port: 8000")
