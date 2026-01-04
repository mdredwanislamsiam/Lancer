# Lancer – Freelancing Platform API

Lancer is a **Django Rest Framework (DRF)**–based freelancing platform backend. It provides a complete REST API for managing users, services, categories, reviews, orders, and notifications, with **JWT authentication**, **role-based access**, and **Swagger API documentation**.

This project is designed as a clean, scalable backend suitable for real-world freelancing platforms like Fiverr or Upwork.

---

## Features

* **JWT Authentication** using **Djoser**
* Custom User model
* Services, Categories, and Reviews
* Order management with status updates & cancellation
* Notification system
* Interactive API documentation (Swagger / ReDoc)
* Modular Django apps structure

---

## Project Structure

```
Lancer_Freelancing_Platform/
│
├── api/                    # API routing & shared config
│
├── orders/                 # Orders & Notifications
│   ├── models.py           # Order, Notification models
│   ├── serializers.py
│   ├── services.py         # Business logic
│   └── views.py
│
├── services/               # Services domain
│   ├── models.py           # Service, Category, Review models
│   ├── serializers.py
│   ├── filters.py
│   └── views.py
│
├── users/                  # Custom user management
│   ├── models.py
│   ├── serializers.py
│   └── views.py
│
├── Lancer_Freelancing_Platform/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
│
├── .env
└── manage.py
```

---

## Domain Models

### Users App

* Custom user model
* JWT-based authentication
* Role-based permissions (buyer / seller / admin)

### Services App

* **Category** – Organizes services
* **Service** – Freelance services posted by sellers
* **Review** – Buyer feedback on services

### Orders App

* **Order** – Purchase of a service
* **Notification** – System-generated user notifications

---

## Authentication

Authentication is implemented using **Djoser + JWT**.

### Auth Endpoints (Djoser)

```
POST   /auth/jwt/create/
POST   /auth/jwt/refresh/
POST   /auth/users/
GET    /auth/users/me/
```

Include the token in request headers:

```
Authorization: Bearer <access_token>
```

---

## API Endpoints Overview

### Categories

```
GET     /categories/
POST    /categories/
GET     /categories/{id}/
PUT     /categories/{id}/
PATCH   /categories/{id}/
DELETE  /categories/{id}/
```

### Services

```
GET     /services/
POST    /services/
GET     /services/{id}/
PUT     /services/{id}/
PATCH   /services/{id}/
DELETE  /services/{id}/
```

### Service Reviews (Nested)

```
GET     /services/{service_pk}/reviews/
POST    /services/{service_pk}/reviews/
GET     /services/{service_pk}/reviews/{id}/
PUT     /services/{service_pk}/reviews/{id}/
PATCH   /services/{service_pk}/reviews/{id}/
DELETE  /services/{service_pk}/reviews/{id}/
```

### Orders

```
GET     /orders/
POST    /orders/
GET     /orders/{id}/
PATCH   /orders/{id}/
DELETE  /orders/{id}/
POST    /orders/{id}/cancel/
PATCH   /orders/{id}/update_status/
```

### Notifications

```
GET     /notifications/
GET     /notifications/{id}/
PATCH   /notifications/{id}/
DELETE  /notifications/{id}/
```

---

## API Documentation

Swagger UI is available via **drf-yasg**:

```
/swagger/
/redoc/
```

This provides interactive testing and full schema visibility.

---

## Installation & Setup

### Clone the Repository

```
git clone https://github.com/mdredwanislamsiam/Lancer.git
cd Lancer

```

### Create Virtual Environment

```
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```
SECRET_KEY= 'django-insecure-i@3%y0cxeokd#owniiwna5w*dgm5nxytv$2$-*qrtu4@-rhy^g'
```

### Run Migrations

```
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```
python manage.py createsuperuser
```

### Run Server

```
python manage.py runserver
```

---

## Testing

```
python manage.py test
```

---

## Security Notes

* JWT authentication required for protected routes
* Role-based access enforced at view/serializer level
* Sensitive settings loaded from `.env`

---

## Future Improvements

* Payment gateway integration
* Messaging between buyers and sellers
* Service search with Elasticsearch
* Admin analytics dashboard

---

## License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Md. Redwan Islam Siam**\
Backend Developer (Django & DRF)

---