# Stripe API

![CI/CD](https://github.com/phentalex/stripe-api-backend/actions/workflows/main.yml/badge.svg)

Веб-приложение для приёма онлайн-платежей на базе Django и Stripe Checkout. Позволяет просматривать товары, оформлять заказы и оплачивать их через Stripe. Поддерживает скидки, налоги и несколько валют. Развёртывание - Docker Compose + nginx.

## Возможности

- Просмотр товаров и оплата через Stripe Checkout
- Объединение нескольких товаров в один заказ
- Скидки и налоги через Stripe Coupons и Tax Rates
- Поддержка нескольких валют (USD, EUR)
- Панель Django Admin

## Стек

- Python 3.12
- Django 5.1
- Stripe API
- PostgreSQL
- Nginx
- Docker / Docker Compose
- pytest

## Переменные окружения

Создай файл `.env` в корне проекта:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=stripe_api_db
POSTGRES_USER=stripe_api_user
POSTGRES_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432

# Для SQLite необходимо указать любое значение. Для PostgreSQL - удалить эту строку или оставить пустой
USE_SQLITE=

STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY_USD=sk_test_...
STRIPE_SECRET_KEY_EUR=sk_test_...

# Для продакшена - необходимо указать домен с протоколом для CloudFlare
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
```

## Запуск локально через Docker

```bash
git clone https://github.com/phentalex/stripe-api-backend.git
cd stripe-api
docker compose up --build -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py collectstatic --no-input
docker compose exec backend cp -r /app/collected_static/. /backend_static/
```

Доступно здесь -> http://localhost:8000

## Запуск на сервере через Docker

```bash
git clone https://github.com/phentalex/stripe-api-backend.git
cd stripe-api
docker compose -f docker-compose.production.yml pull
docker compose -f docker-compose.production.yml up -d
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --no-input
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/
```

## Локальный запуск без Docker

**Linux/macOS:**
```bash
git clone https://github.com/phentalex/stripe-api-backend.git
cd stripe-api/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

**Windows:**
```bash
git clone https://github.com/phentalex/stripe-api-backend.git
cd stripe-api/backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Доступно здесь -> http://localhost:8000

## API эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/` | Список всех товаров |
| GET | `/item/<id>/` | Страница товара с кнопкой оплаты |
| GET | `/buy/<id>/` | Получить Stripe Session ID для товара |
| GET | `/order/<id>/` | Страница заказа с кнопкой оплаты |
| GET | `/buy/order/<id>/` | Получить Stripe Session ID для заказа |
| GET | `/success/` | Страница успешной оплаты |
| GET | `/cancel/` | Страница отменённой оплаты |

## Тесты

Тесты запускаются автоматически при каждом пуше через GitHub Actions.

Запуск локально:

```bash
pytest backend/payments/tests.py -v
```

## Админ панель

URL: `/admin/`

Логин и пароль задаются при выполнении `createsuperuser`.

> **Демо:** https://stripe-api.phentalex.ru

Логин: **admin**

Пароль: **admin**

## Автор

**Александр Уваров** — [GitHub](https://github.com/phentalex)
