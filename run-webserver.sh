#/bin/bash
git submodule init
git submodule update
docker compose -f docker-compose-webserver.yml down
docker compose -f docker-compose-webserver.yml up --build