# Секреты GitHub Actions (без Yandex Container Registry)

Settings → Secrets and variables → Actions → New repository secret

Для деплоя достаточно **трёх** секретов:

| Name | Значение |
|------|----------|
| `HOST` | `81.26.183.233` |
| `USER` | `ubuntu` |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ ВМ (блок OPENSSH) |

Секреты `YC_REGISTRY_ID` и `YC_SA_JSON_CREDENTIALS` **не нужны**.

Образ backend собирается на ВМ: `docker compose up -d --build`.

После push в `main`:

1. **Foodgram CI** — проверка сборки Dockerfile
2. **Foodgram Deploy** — деплой по SSH
