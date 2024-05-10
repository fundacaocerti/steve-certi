#!/usr/bin/env bash
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/
set -e
/code/scripts/steve-certi-build.sh 
/code/scripts/steve-certi-run.sh &
/code/scripts/wait-for.sh --host=localhost --port=8180 --timeout=20 
/code/scripts/shortcuts/integration-test-runner