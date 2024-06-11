#/bin/bash
git submodule init
git submodule update
docker compose -f ../docker-compose-production.yml down
docker compose -f ../docker-compose-production.yml up --build