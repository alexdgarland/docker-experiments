#!/usr/bin/env bash

container_name=web-test-$(date +%Y%m%d%H%M%s)

echo "Running container as $container_name"

docker run -it --rm --name "$container_name" -it -p 80:8000 mywebserver:latest
