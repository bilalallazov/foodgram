#!/bin/bash
set -e

sudo apt update
sudo apt install -y docker.io docker-compose-plugin git
sudo systemctl stop nginx 2>/dev/null || true
sudo systemctl disable nginx 2>/dev/null || true

sudo usermod -aG docker "$USER"

if [ ! -d "$HOME/foodgram" ]; then
    git clone https://github.com/bilalallazov/foodgram.git "$HOME/foodgram"
fi

cd "$HOME/foodgram/infra"

if [ ! -f .env ]; then
    cp .env.production.example .env
    echo "Отредактируйте ~/foodgram/infra/.env перед запуском"
fi

echo "Выйдите из SSH и зайдите снова, затем: cd ~/foodgram/infra && bash deploy.sh"
