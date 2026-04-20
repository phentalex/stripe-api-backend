# Stripe API

![CI/CD](https://github.com/phentalex/stripe-api-backend/actions/workflows/main.yml/badge.svg)

Django + Stripe API бэкенд для приёма платежей.

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
- Docker / Docker Compose

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
```

## Запуск локально через Docker

```bash
git clone https://github.com/phentalex/stripe-api-backend.git
cd stripe-api
docker-compose up --build -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

Открой http://localhost:8000

## Запуск на сервере через Docker

```bash
git clone https://github.com/phentalex/stripe-api-backend.git
cd stripe-api
docker-compose -f docker-compose.production.yml up --build -d
docker-compose -f docker-compose.production.yml exec backend python manage.py migrate
docker-compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
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

## Админ панель

URL: `/admin/`

```
Логин: admin
Пароль: admin
```

> **Демо:** https://phentalex.ru

## Автор

**Александр Уваров** — [GitHub](https://github.com/phentalex)
