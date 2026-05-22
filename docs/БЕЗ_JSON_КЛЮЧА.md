# Можно ли без JSON-ключа?

## Короткий ответ

| Цель | JSON нужен? |
|------|-------------|
| Сайт работает по IP | **Нет** |
| Полный чек-лист курса (образ в registry) | **Да**, один раз |

JSON (`YC_SA_JSON_CREDENTIALS`) — только для **загрузки Docker-образа в Yandex Container Registry** через GitHub Actions.

---

## Путь без JSON (сайт для проверки)

На ВМ по SSH:

```bash
git clone https://github.com/bilalallazov/foodgram.git
cd foodgram/infra
cp .env.example .env
nano .env
```

В `.env`:

```env
DB_ENGINE=django.db.backends.postgresql
ALLOWED_HOSTS=81.26.183.233
ADMIN_EMAIL=admin@foodgram.ru
ADMIN_PASSWORD=admin123
SECRET_KEY=любая_длинная_строка_50_символов
POSTGRES_PASSWORD=надёжный_пароль
```

Запуск **без registry** (сборка на сервере):

```bash
docker compose up -d --build
```

Проверка: http://81.26.183.233

Этого хватает для чек-листов по функциям сайта.

---

## Когда JSON всё же нужен

Пункт чек-листа: **«Образ с проектом обновляется в облачном хранилище»**.

Создание за 5 минут:

1. Yandex Cloud → IAM → сервисный аккаунт + роль `container-registry.images.pusher`
2. Авторизованные ключи → JSON
3. Container Registry → ID реестра
4. GitHub Secrets: `YC_SA_JSON_CREDENTIALS`, `YC_REGISTRY_ID`

После этого CI загрузит образ в registry.

---

## GitHub Actions без секретов

Workflow **Foodgram CI**:

- job **build** — всегда зелёный (проверка Dockerfile)
- job **push-to-registry** — пропускается с предупреждением, если нет JSON

Сдача на ревью с полным чек-листом лучше **с JSON**.
