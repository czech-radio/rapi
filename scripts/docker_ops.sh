#!/bin/bash
# Build docker image with non root user. User will have name, ID, GID as user running the docker commands.

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="${SCRIPT_PATH%/*}"
DOCKERFILE_PATH="${SCRIPT_DIR}/../Dockerfile"
IMAGENAME="localhost/rapi_tester"
# TAG="v0.1.0"

build_local_image(){
  if [ ! -f "$DOCKERFILE_PATH" ] ; then
    echo "File ${DOCKERFILE_PATH} does not exist"
    exit 1
  fi

  DOCKER_BUILDKIT=1 docker build  -f "$DOCKERFILE_PATH" -t "$IMAGENAME" \
    --progress=plain \
    --build-arg MY_UID="$(id -u)" \
    --build-arg MY_GID="$(id -g)" \
    --build-arg MY_GROUP="$(id -g -n)" \
    --build-arg MY_USER="$USER" .
}

run_image(){
  docker run -ti  $IMAGENAME
}

"$@"
