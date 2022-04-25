#!/bin/bash

echo "Start Fluentbit building..."
docker build -f Dockerfile -t cloudfoundry/build_fluentbit .
docker run -d --name fluentbit_build_container cloudfoundry/build_fluentbit:latest

echo "Copy result..."
docker cp fluentbit_build_container:/fluent-bit-1.9.2/build/bin/fluent-bit ./

echo "Removing container..."

docker stop fluentbit_build_container
docker rm fluentbit_build_container

echo "Archiving bin file..."

tar -czf fluent-bit-1.9.2.tar.gz fluent-bit

echo "Done"