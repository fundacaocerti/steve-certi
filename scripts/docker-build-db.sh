#!/usr/bin/env bash
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/

IMAGE="steve-certi-db-img"

DOCKERFILE="docker/Dockerfile.db"

docker build -t ${IMAGE} -f ${DOCKERFILE} .
