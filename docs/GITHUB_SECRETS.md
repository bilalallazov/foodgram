# Секреты GitHub Actions (без Yandex Container Registry)

Settings → Secrets and variables → Actions → New repository secret

Для деплоя достаточно **трёх** секретов:

| Name | Значение |
|------|----------|
| `HOST` | `81.26.183.233` |
| `USER` | `ubuntu` (только это слово, без пробелов и переносов строк) |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ ВМ (блок OPENSSH) |

Секреты `YC_REGISTRY_ID` и `YC_SA_JSON_CREDENTIALS` **не нужны**.

Образы собираются на ВМ: `docker-compose up -d --build` (или `docker compose`).

После push в `main`:

1. **Foodgram CI** — проверка сборки Dockerfile
2. **Foodgram Deploy** — деплой по SSH
