#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -f .env ]; then
    cp .env.example .env
    sed -i 's/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=81.26.183.233/' .env 2>/dev/null || \
    sed -i '' 's/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=81.26.183.233/' .env 2>/dev/null || true
    echo "Проверьте .env: ALLOWED_HOSTS, SECRET_KEY, POSTGRES_PASSWORD"
fi

docker compose up -d --build
docker compose ps

echo "Готово: http://81.26.183.233"
echo "Админка: http://81.26.183.233/admin/"
