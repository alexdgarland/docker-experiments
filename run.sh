#!/usr/bin/env bash

container_name=web-test-$(date +%Y%m%d%H%M%s)

docker run -d --rm --name $container_name -p 80:8000 mywebserver:latest
