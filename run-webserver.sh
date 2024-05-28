#/bin/bash
docker compose -f docker-compose-webserver.yml down
docker compose -f docker-compose-webserver.yml up --build