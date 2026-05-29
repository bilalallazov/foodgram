#!/bin/bash
set -e
cd "$(dirname "$0")"
COMPOSE="docker compose"
command -v docker-compose >/dev/null 2>&1 && COMPOSE="docker-compose"
$COMPOSE up -d
sleep 5
if docker image inspect infra-frontend >/dev/null 2>&1; then
  IMG=infra-frontend
elif docker image inspect infra_frontend >/dev/null 2>&1; then
  IMG=infra_frontend
else
  exit 0
fi
docker run --rm -v "$HOME/foodgram/frontend/build:/out" alpine \
  sh -c 'rm -rf /out/* /out/.[!.]* 2>/dev/null || true'
docker run --rm -v "$HOME/foodgram/frontend/build:/out" "$IMG" \
  sh -c 'cp -r /app/build/. /out/'
$COMPOSE restart nginx
