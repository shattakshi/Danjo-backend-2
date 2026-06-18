# Danjo Backend 

## Overview

This project is a Django REST Framework backend application developed at.

The system manages products, stores, inventory, and orders while demonstrating:

* Django REST APIs
* PostgreSQL integration
* Redis rate limiting
* Celery asynchronous task processing
* Docker containerization
* Search and autocomplete functionality
* Database transactions and consistency
* Automated testing

---

## Tech Stack

* Python 3.12
* Django 6
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker & Docker Compose
* Faker

---

## Features

### Product Management

* Categories
* Products
* Product search
* Product autocomplete

### Store & Inventory Management

* Store inventory tracking
* Inventory listing per store

### Order Processing

* Order creation
* Inventory validation
* Automatic stock deduction
* Atomic database transactions
* Order status management

### Search

Supports:

* Keyword search
* Category filtering
* Price filtering
* Store filtering
* In-stock filtering
* Pagination
* Sorting

### Redis Integration

Implemented request rate limiting for:

GET /api/search/suggest/

Limit:

* 20 requests per minute per IP

### Celery Integration

Asynchronous task:

* Order confirmation processing

Redis is used as the Celery broker and result backend.

---

## Project Structure

```text
aforro_backend/

├── products/
├── stores/
├── orders/
├── search/
├── project/

├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd aforro_backend
```

### Run with Docker

```bash
docker compose up --build
```

### Apply Migrations

```bash
docker compose exec web python manage.py migrate
```

### Generate Dummy Data

```bash
docker compose exec web python manage.py seed_data
```

---

## Docker Services

The application starts the following containers:

### Web

Django REST API

### PostgreSQL

Primary database

### Redis

Used for:

* Rate limiting
* Celery broker

### Celery Worker

Processes asynchronous tasks

---

## API Endpoints

### Product Search

```http
GET /api/search/products/
```

Example:

```http
GET /api/search/products/?q=laptop
```

Filters:

* category
* min_price
* max_price
* store_id
* in_stock

Sorting:

* price
* newest
* relevance

---

### Product Autocomplete

```http
GET /api/search/suggest/?q=nat
```

Features:

* Minimum 3 characters
* Prefix matches prioritized
* Maximum 10 results
* Redis rate limiting

---

### Inventory Listing

```http
GET /api/stores/<store_id>/inventory/
```

Returns:

* Product title
* Price
* Category
* Quantity

---

### Store Orders

```http
GET /api/stores/<store_id>/orders/
```

Returns:

* Order ID
* Status
* Created timestamp
* Total items

---

### Create Order

```http
POST /api/orders/
```

Example Request:

```json
{
  "store": 1,
  "items": [
    {
      "product": 1,
      "quantity_requested": 2
    }
  ]
}
```

Business Rules:

* Validate inventory
* Reject insufficient stock
* Deduct stock when available
* Execute inside transaction.atomic()

---

## Seed Data

Management Command:

```bash
python manage.py seed_data
```

Creates:

* 10+ Categories
* 1000+ Products
* 20+ Stores
* Store Inventory Records

---

## Running Tests

Execute:

```bash
docker compose exec web python manage.py test orders.tests
```

Current Result:

```text
Ran 3 tests

OK
```

---

## Scalability Considerations

### Search

* Uses optimized queryset filtering
* Supports pagination
* Uses select_related where appropriate

### Database

* PostgreSQL for production readiness
* Indexed foreign-key relationships

### Redis

* Handles rate limiting efficiently
* Can be extended for caching

### Celery

* Offloads background tasks
* Scales horizontally with additional workers

### Docker

* Consistent development and deployment environment
* Easy service orchestration using Docker Compose

---

## Author

Shatakshi Tiwari

B.Tech Computer Science & Engineering

AI/ML & Backend Development Enthusiast
