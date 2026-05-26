# Foodgram

Сервис публикации рецептов. Финальный проект Яндекс Практикума.

Репозиторий: https://github.com/bilalallazov/foodgram

## Структура

- `backend/` — Django, DRF, API
- `frontend/` — React
- `infra/` — Docker, nginx, PostgreSQL
- `tests.yml` — данные для ревьюера
- `docs/` — инструкции по сдаче

## GitHub Actions

| Workflow | Назначение |
|----------|------------|
| Foodgram CI | Проверка сборки Docker-образов |
| Foodgram Deploy | Деплой на ВМ по SSH (`docker compose up --build`) |

Секреты (3 шт., без Yandex Registry): `docs/GITHUB_SECRETS.md`.

## Локальный запуск

```bash
cd infra
cp .env.example .env
docker compose up --build
```

http://localhost

## Продакшен (ВМ)

IP: `81.26.183.233`  
ВМ: `r-backend-vm-1670829377`

```bash
cd infra
cp .env.production.example .env
nano .env
docker compose up -d --build
```

## Админка

- URL: `/admin/`
- login: `admin@foodgram.ru`
- password: `admin123` (или из `ADMIN_PASSWORD` в `.env`)

## Сдача на ревью

1. Все секреты в GitHub
2. CI и Deploy зелёные
3. Сайт открывается по IP
4. `tests.yml` в репозитории
5. Практикум → Отправить на ревьюПодробно: `docs/ПОЛНАЯ_СДАЧА.md`
