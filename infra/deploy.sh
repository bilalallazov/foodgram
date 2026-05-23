#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "Создайте .env из .env.production.example"
    exit 1
fi

docker compose -f docker-compose.yml down --remove-orphans || true
docker compose -f docker-compose.yml up -d --build
sleep 20
if [ -f ../frontend/build/build/index.html ]; then
    cp -r ../frontend/build/build/. ../frontend/build/
fi
docker compose -f docker-compose.yml restart nginx
docker compose -f docker-compose.yml ps
