#/bin/bash
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
git submodule init
git submodule update
docker compose -f $PROJECT_ROOT/docker-compose-production.yml down
docker compose -f $PROJECT_ROOT/docker-compose-production.yml up --build