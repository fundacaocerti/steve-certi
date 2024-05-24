#!/usr/bin/env bash
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/
set -e
/code/scripts/steve-certi-build.sh --prod
/code/scripts/steve-certi-run.sh
