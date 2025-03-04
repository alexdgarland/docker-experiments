from setuptools import setup, find_packages

REQUIREMENTS = ["jinja2", "ruamel.yaml"]

setup(
    name="WebServer",
    version="0.0.1",
    author="Alex Garland",
    author_email="alex.d.garland@gmail.com",
    url="https://github.com/alexdgarland/docker-experiments",
    packages=find_packages(),
    package_data={
        "webserver": [
            "resources/images/*",
            "resources/css/*",
            "pages/*",
            "config/*"
        ]
    },
    install_requires=REQUIREMENTS,
    entry_points={
          'console_scripts': [
              'webserver = webserver.__main__:main'
          ]
      }
)
