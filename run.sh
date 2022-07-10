#!/bin/bash

image="local-weblog:22.1"

if [[ "$(docker images -q $image 2> /dev/null)" == "" ]]; then
  echo "build docker image $image"
  docker build -t $image -f ./Dockerfile .
fi

cmd="cd /var/weblog-src && poetry run $@"
here=$(dirname "$BASH_SOURCE")
here=$(readlink -m $here)
docker run -i --rm -e TZ=Asia/Shanghai  -v "$here":/var/weblog-src $image /bin/bash -c "$cmd"