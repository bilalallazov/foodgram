# Важно для Windows

## Нельзя вводить в PowerShell

Строки из `.env` — это **текст внутри файла**, не команды:

```
ALLOWED_HOSTS=81.26.183.233
ADMIN_EMAIL=admin@foodgram.ru
```

PowerShell выдаст ошибку — это нормально.

## Как открыть .env

В Cursor слева: `foodgram` → `infra` → `.env` (двойной клик).

Или:

```powershell
notepad "C:\Users\user\Desktop\Новая папка (2)\foodgram\infra\.env"
```

## Docker на Windows

Если `docker` не найден — Docker Desktop **не установлен**.

На ПК проект **не запустится**. Запускайте только **на ВМ** по SSH.

## Что делать дальше

1. Файл `.env` уже настроен в `infra/.env`
2. Подключиться к ВМ: `ssh -i C:\Users\user\.ssh\foodgram_vm yc-user@81.26.183.233`
3. На сервере выполнить команды из `docs/ПОЛНАЯ_СДАЧА.md`
