#!/usr/bin/env bash

container_name=web-test-$(date +%Y%m%d%H%M%s)

echo "Running container as $container_name"

docker run -it --name "$container_name" -p 80:8000 mywebserver:latest > .server_logs/$container_name.log
