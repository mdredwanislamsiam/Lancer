# Lancer — Freelancing Platform API

> A production-grade REST API for a full-featured freelancing marketplace, built with Django REST Framework, JWT authentication, and SSLCommerz payment integration.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.x-a30000?style=flat)](https://django-rest-framework.org)
[![JWT](https://img.shields.io/badge/Auth-JWT%20%2B%20Djoser-000000?style=flat&logo=jsonwebtokens)](https://jwt.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](./LICENSE)

---

## Overview

**Lancer** is a scalable backend API for a freelancing platform similar to Fiverr or Upwork. It handles the full lifecycle of a freelancing transaction — from service discovery and order placement to payment processing and notifications — with clean, modular architecture and interactive API documentation.

---

## Features

| Area | Details |
|---|---|
| **Authentication** | JWT via Djoser — register, login, token refresh |
| **Role-Based Access** | Buyer / Seller / Admin — enforced at view and serializer level |
| **Services** | Full CRUD, image uploads, filtering, search, and pagination |
| **Orders** | Place, cancel, update status, and track orders |
| **Payments** | SSLCommerz gateway integration (sandbox + live) |
| **Notifications** | Auto-generated system notifications on key order events |
| **Analytics** | Per-user income/cost tracking by month |
| **API Docs** | Swagger UI + ReDoc via `drf-yasg` |

---

## Architecture

```
Lancer_Freelancing_Platform/
│
├── api/                          # Shared routing and configuration
│
├── users/                        # Custom user model + analytics
│   ├── models.py                 # User, IncomeOrCostPerMonth
│   ├── serializers.py
│   └── views.py                  # Profile, public user, income data
│
├── services/                     # Service marketplace domain
│   ├── models.py                 # Service, Category, Review, ServiceImage
│   ├── serializers.py
│   ├── filters.py                # Price range, category filtering
│   ├── permissions.py            # IsSellerOrReadOnly, IsBuyerOrReadOnly
│   └── views.py
│
├── orders/                       # Transaction and notification domain
│   ├── models.py                 # Order, Notification
│   ├── serializers.py
│   ├── services.py               # Business logic layer
│   └── views.py                  # Orders, payments, notifications
│
├── Lancer_Freelancing_Platform/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
│
├── .env
├── requirements.txt
└── manage.py
```

---

## Quick Start

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/mdredwanislamsiam/Lancer.git
cd Lancer

python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

### 3. Run Migrations & Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start the Server

```bash
python manage.py runserver
```

API is now live at `http://localhost:8000`. Visit `/swagger/` for interactive documentation.

---

## API Reference

### Authentication

```
POST   /auth/users/           → Register
POST   /auth/jwt/create/      → Login (returns access + refresh tokens)
POST   /auth/jwt/refresh/     → Refresh access token
GET    /auth/users/me/        → Current user profile
```

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

---

### Services

```
GET     /services/                           → List all services (public)
POST    /services/                           → Create a service (seller only)
GET     /services/{id}/                      → Get service detail
PATCH   /services/{id}/                      → Update service (seller only)
DELETE  /services/{id}/                      → Delete service (seller only)

GET     /services/{id}/reviews/              → List reviews
POST    /services/{id}/reviews/              → Submit a review (buyer only)
PATCH   /services/{id}/reviews/{review_id}/  → Edit review
DELETE  /services/{id}/reviews/{review_id}/  → Delete review
```

**Supported filters:** `category`, `price` (ordering), `search` (title, seller username)

---

### Orders

```
GET     /orders/                   → List orders (filtered by role)
POST    /orders/                   → Place an order (buyer only)
GET     /orders/{id}/              → Order detail
POST    /orders/{id}/cancel/       → Cancel an order
PATCH   /orders/{id}/update_status/→ Update status (admin only)
DELETE  /orders/{id}/              → Delete order (admin only)
```

**Order statuses:** `NOT_PAID` → `ACTIVE` → `PAID` → `DELIVERED` / `CANCELED`

---

### Payments (SSLCommerz)

```
POST   /api/payment/initiate/     → Begin payment — returns gateway URL
POST   /api/payment/success/      → Handle successful payment
POST   /api/payment/fail/         → Handle failed payment
POST   /api/payment/cancel/       → Handle cancelled payment
```

On a successful payment, wallets are updated for both buyer and seller, and monthly income records are created automatically.

---

### Notifications

```
GET     /notifications/           → List your notifications
GET     /notifications/{id}/      → Notification detail
PATCH   /notifications/{id}/      → Mark as read
DELETE  /notifications/{id}/      → Delete notification
```

---

### Categories

```
GET     /categories/              → List all categories (public)
POST    /categories/              → Create category (admin only)
PATCH   /categories/{id}/         → Update category (admin only)
DELETE  /categories/{id}/         → Delete category (admin only)
```

---

## Permissions Matrix

| Endpoint | Anonymous | Buyer | Seller | Admin |
|---|:---:|:---:|:---:|:---:|
| List Services | ✅ | ✅ | ✅ | ✅ |
| Create Service | ❌ | ❌ | ✅ | ✅ |
| Place Order | ❌ | ✅ | ❌ | ✅ |
| Cancel Order | ❌ | ✅ | ✅ | ✅ |
| Update Order Status | ❌ | ❌ | ❌ | ✅ |
| Submit Review | ❌ | ✅ | ❌ | ✅ |
| Manage Categories | ❌ | ❌ | ❌ | ✅ |

---

## API Documentation

Lancer ships with full interactive API documentation:

| Interface | URL |
|---|---|
| Swagger UI | `/swagger/` |
| ReDoc | `/redoc/` |

---

## Testing

```bash
python manage.py test
```

---

## Roadmap

- [ ] WebSocket-based real-time messaging between buyers and sellers
- [ ] Elasticsearch integration for advanced service search
- [ ] Admin analytics dashboard
- [ ] Email verification and password reset flows
- [ ] Production deployment guide (Docker + Nginx + Gunicorn)

---

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Auth:** Djoser, SimpleJWT
- **Payments:** SSLCommerz
- **API Docs:** drf-yasg (Swagger / ReDoc)
- **Filtering:** django-filter
- **Database:** PostgreSQL (recommended) / SQLite (development)

---

## License

This project is licensed under the [MIT License](./LICENSE).

---

## Author

**Md. Redwan Islam Siam**
Backend Developer — Django & Django REST Framework

[![GitHub](https://img.shields.io/badge/GitHub-mdredwanislamsiam-181717?style=flat&logo=github)](https://github.com/mdredwanislamsiam)