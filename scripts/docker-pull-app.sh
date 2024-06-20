#!/usr/bin/env bash
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/


IMAGE="registry.certi.org.br/cdm/mobeq2/steve-certi-app:latest" 

DOCKERFILE="docker/Dockerfile.app"


docker login registry.certi.org.br

docker pull ${IMAGE} 
