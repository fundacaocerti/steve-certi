#!/usr/bin/env bash
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/

IMAGE="steve-certi-app-img"

DOCKERFILE="docker/Dockerfile-prod.app"

docker build -t ${IMAGE} -f ${DOCKERFILE} .
