#!/bin/bash
set -e # Stop on errors

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
$PROJECT_ROOT/scripts/docker-pull-app.sh
# $PROJECT_ROOT/scripts/docker-build-app.sh // uncomment this if you do not have access to the registry
$PROJECT_ROOT/scripts/docker-build-db.sh
$PROJECT_ROOT/scripts/docker-run-app.sh
$PROJECT_ROOT/scripts/docker-run-db.sh
$PROJECT_ROOT/scripts/docker-exec-app.sh