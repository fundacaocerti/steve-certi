#!/usr/bin/env bash
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/

NETWORK="steve-certi-network"

CHECK_NETWORK=$(docker network ls | grep -o -m 1 ${NETWORK})

if [ "${CHECK_NETWORK}" != "${NETWORK}" ]; then
    docker network create -d bridge ${NETWORK}
fi
