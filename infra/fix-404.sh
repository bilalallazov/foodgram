#!/bin/bash
set -e

echo "Останавливаем системный nginx (он даёт 404 Ubuntu)..."
sudo systemctl stop nginx 2>/dev/null || true
sudo systemctl disable nginx 2>/dev/null || true

cd "$(dirname "$0")"

if [ ! -f .env ]; then
    cp .env.example .env
    sed -i 's/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=81.26.183.233/' .env 2>/dev/null || \
    sed -i '' 's/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=81.26.183.233/' .env 2>/dev/null || true
fi

echo "Запуск Foodgram в Docker..."
docker compose down 2>/dev/null || true
docker compose up -d --build

echo "Ожидание сборки frontend (до 3 минут)..."
sleep 30
docker compose ps

if [ ! -f ../frontend/build/index.html ]; then
    echo "Сборка frontend..."
    docker compose run --rm frontend
    docker compose up -d nginx
fi

echo ""
echo "Проверка:"
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1/ || true
echo "Откройте: http://81.26.183.233"
