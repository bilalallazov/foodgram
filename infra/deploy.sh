#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "Создайте .env из .env.production.example"
    exit 1
fi

set -a
source .env
set +a

if [ -z "$YC_SA_JSON_CREDENTIALS" ]; then
    echo "Выполните: export YC_SA_JSON_CREDENTIALS=\"\$(cat путь/к/authorized_key.json)\""
    exit 1
fi

echo "$YC_SA_JSON_CREDENTIALS" | docker login -u json_key --password-stdin cr.yandex

docker compose -f docker-compose.production.yml pull backend
docker compose -f docker-compose.production.yml up -d --build
docker compose -f docker-compose.production.yml ps
