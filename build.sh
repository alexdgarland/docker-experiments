#!/usr/bin/env bash

docker build --rm --tag mywebserver --build-arg USER .
