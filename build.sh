#!/usr/bin/env bash

python setup.py sdist

docker build \
  --rm \
  --tag mywebserver \
  --build-arg USER \
  --build-arg PACKAGE_FULLNAME="$(python setup.py --fullname)" \
  .
