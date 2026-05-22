# Foodgram

Сервис публикации рецептов.

## Локальный запуск

```bash
cd infra
cp .env.example .env
docker compose up --build
```

Приложение: http://localhost  
API: http://localhost/api/docs/  
Админка: http://localhost/admin/

## Данные для ревью

Файл `tests.yml` в корне проекта. Перед сдачей укажите реальное имя ВМ в `vm_name`.

Учётные данные администратора по умолчанию:

- login: `admin@foodgram.ru`
- password: `admin123`

## Стек

- Django, DRF
- PostgreSQL
- Docker, nginx, gunicorn
- React (frontend)
