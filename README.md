# Test Python Backend

Асинхронный REST API на Sanic + SQLAlchemy async + PostgreSQL.

## Требования

```text
Python 3.12
PostgreSQL 16+
Docker Compose
```

## Запуск через Docker Compose

```bash
docker compose up --build
```

Приложение будет доступно на `http://localhost:3993`. Миграции выполняются автоматически при старте контейнера приложения.

## Запуск без Docker

1. Создайте PostgreSQL базу `test_pythonmid`.
2. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Укажите переменные окружения и примените миграции:

```bash
export PYTHONPATH=src
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/test_pythonmid
export JWT_SECRET=dev-jwt-secret
export PAYMENT_SECRET_KEY=gfdmhghif38yrf9ew0jkf32
export PORT=3993
alembic upgrade head
```

4. Запустите приложение:

```bash
python -m app.main
```

## Тесты

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## Пользователи по умолчанию

Тестовый пользователь:

```text
email: user@example.com
password: user12345
```

Тестовый администратор:

```text
email: admin@example.com
password: admin12345
```

## Основные endpoints

```text
POST /api/users/login
GET  /api/users/me
GET  /api/users/me/accounts
GET  /api/users/me/payments

POST   /api/admin/login
GET    /api/admin/me
GET    /api/admin/users
POST   /api/admin/users
PATCH  /api/admin/users/{user_id}
DELETE /api/admin/users/{user_id}

POST /api/payments/webhook
GET  /health
```

Для защищённых endpoints передавайте токен:

```text
Authorization: Bearer <access_token>
```

## Пример webhook платежа

```bash
curl -X POST http://localhost:3993/api/payments/webhook \
  -H 'Content-Type: application/json' \
  -d '{
    "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
    "user_id": 1,
    "account_id": 1,
    "amount": 100,
    "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
  }'
```

Подпись считается как SHA256 от строки `{account_id}{amount}{transaction_id}{user_id}{PAYMENT_SECRET_KEY}`.
