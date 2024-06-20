#!/usr/bin/env bash
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/

NC="\033[0m"
RED="\033[1;31m"

IMAGE="registry.certi.org.br/cdm/mobeq2/steve-certi-app" 

IMAGE_TAG="latest"

CONTAINER_NAME="steve-certi-app"

NETWORK="steve-certi-network"

WORKSPACE="/code"

ROOT_DIR="$(dirname $(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"

CHECK_IMAGE=$(docker images | grep -o -m 1 ${IMAGE})

if [ "${CHECK_IMAGE}" != "${IMAGE}" ]; then
  echo -e "${RED}Docker image for ${IMAGE} not found!${NC}"

  exit 1
fi

source $ROOT_DIR/scripts/docker-network-check.sh

docker run --rm -it  \
  --volume "$ROOT_DIR":"$WORKSPACE" \
  --volume /home/$USER/.bash_history:/home/$USER/.bash_history \
  --publish 8180:8180 \
  --publish 8443:8443 \
  --user root \
  --name $CONTAINER_NAME \
  --net $NETWORK \
  --detach \
  "$IMAGE:$IMAGE_TAG" \
