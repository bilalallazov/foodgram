# Все секреты GitHub Actions

Settings → Secrets and variables → Actions → New repository secret

## Для сборки образа (workflow Foodgram CI)

| Name | Значение |
|------|----------|
| `YC_REGISTRY_ID` | ID Container Registry (`crp...`) |
| `YC_SA_JSON_CREDENTIALS` | JSON ключ сервисного аккаунта |

## Для деплоя на ВМ (workflow Foodgram Deploy)

| Name | Значение |
|------|----------|
| `HOST` | `81.26.183.233` |
| `USER` | `yc-user` (или `ubuntu` — как в консоли Yandex) |
| `SSH_PRIVATE_KEY` | Приватный SSH-ключ (весь блок OPENSSH) |

Те же `YC_REGISTRY_ID` и `YC_SA_JSON_CREDENTIALS` используются при деплое.

## Итого: 5 секретов

1. YC_REGISTRY_ID
2. YC_SA_JSON_CREDENTIALS
3. HOST
4. USER
5. SSH_PRIVATE_KEY

## tests.yml (не секрет, файл в репозитории)

```yaml
login: admin@foodgram.ru
password: admin123
vm_name: r-backend-vm-1670829377
```

Пароль совпадает с `ADMIN_PASSWORD` в `.env` на сервере.
