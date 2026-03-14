# PriceIntel — Database Schema Documentation

**Version:** 2.0.0 | **Date:** 13 March 2026

---

## Overview

PriceIntel uses two database backends:

| Backend | ORM | Tables |
|---|---|---|
| **PostgreSQL** (production) / **SQLite** (dev) | **Django ORM** | `users_user`, `api_image`, `advanced_pricealert`, `advanced_searchhistory`, `advanced_wishlist`, `advanced_pricehistory` |
| **PostgreSQL** / **SQLite** (secondary) | **SQLAlchemy** | `products`, `prices`, `search_history` |

---

## Django ORM Tables

### 1. `users_user` — Custom User

Extends Django's built-in `AbstractUser`. Uses email as the login identifier.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, Auto | Auto-increment primary key |
| `email` | VARCHAR(254) | UNIQUE, NOT NULL | Login identifier |
| `username` | VARCHAR(150) | UNIQUE, NOT NULL | Display name |
| `first_name` | VARCHAR(150) | | First name |
| `last_name` | VARCHAR(150) | | Last name |
| `password` | VARCHAR(128) | NOT NULL | PBKDF2-SHA256 hashed password |
| `is_active` | BOOLEAN | Default: True | Account enabled flag |
| `is_staff` | BOOLEAN | Default: False | Django admin access |
| `date_joined` | DATETIME | Auto | Registration timestamp |
| `last_login` | DATETIME | Nullable | Last successful login |

**Key relationships:**
- One `User` → Many `PriceAlert` (cascade delete)
- One `User` → Many `Wishlist` (cascade delete)
- One `User` → Many `SearchHistory` (cascade delete)

---

### 2. `api_image` — Uploaded Images

Stores metadata about product images uploaded by users.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK | Auto-generated UUID4 |
| `image_id` | VARCHAR(255) | UNIQUE, INDEXED | String ID for API responses (e.g. `20260313_abc123`) |
| `original_filename` | VARCHAR(255) | NOT NULL | Sanitized original filename |
| `stored_filename` | VARCHAR(255) | NOT NULL | Filename saved on disk |
| `processed_path` | VARCHAR(255) | Nullable | Relative path to preprocessed image |
| `file` | VARCHAR | NOT NULL | Storage path: `images/YYYY/MM/DD/` |
| `file_size` | BIGINT | NOT NULL | File size in bytes |
| `mime_type` | VARCHAR(50) | NOT NULL | `image/jpeg`, `image/png`, `image/webp` |
| `uploaded_at` | DATETIME | Auto, INDEXED | Upload timestamp |

**Ordering:** `-uploaded_at` (newest first)

---

### 3. `advanced_pricealert` — Price Alerts

Tracks user-defined price thresholds for products. A background scheduler checks current prices nightly.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, Auto | Primary key |
| `user_id` | INTEGER | FK → `users_user`, CASCADE | Alert owner |
| `product_name` | VARCHAR(255) | INDEXED | Product to monitor |
| `target_price` | DECIMAL(10,2) | NOT NULL | Alert triggers when price ≤ this |
| `current_price` | DECIMAL(10,2) | Nullable | Last known price |
| `product_url` | URLField(2048) | Blank OK | Direct product link |
| `created_at` | DATETIME | Auto, INDEXED | Alert creation time |
| `updated_at` | DATETIME | Auto | Last modification |
| `status` | VARCHAR(20) | Default: `active` | `active` / `triggered` / `paused` |

**Statuses:**
- `active` — Monitoring enabled, price not yet hit
- `triggered` — Target price was reached (alert fired)
- `paused` — User temporarily disabled the alert

---

### 4. `advanced_searchhistory` — User Search History (Django)

Logs every product search a user performs for the Dashboard history view.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, Auto | Primary key |
| `user_id` | INTEGER | FK → `users_user`, CASCADE | Searching user |
| `query` | VARCHAR(512) | INDEXED | Sanitized search term |
| `timestamp` | DATETIME | Auto, INDEXED | When search occurred |

**Ordering:** `-timestamp` (most recent first)

---

### 5. `advanced_wishlist` — User Wishlist

Saved product listings. Prevents duplicate saves of the same product URL per user.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, Auto | Primary key |
| `user_id` | INTEGER | FK → `users_user`, CASCADE | List owner |
| `product_name` | VARCHAR(255) | INDEXED | Product display name |
| `store` | VARCHAR(100) | Blank OK | Retailer name |
| `price` | DECIMAL(10,2) | Nullable | Price at time of save |
| `product_url` | URLField(2048) | Blank OK | Link to product page |
| `image_url` | URLField(2048) | Blank OK | Product thumbnail URL |
| `added_at` | DATETIME | Auto, INDEXED | When user saved it |

**Unique constraint:** `(user_id, product_url)` — prevents duplicate wishlist entries

---

### 6. `advanced_pricehistory` — Price History Log

Time-series price data used for the price trend charts on the Dashboard.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, Auto | Primary key |
| `product_name` | VARCHAR(255) | INDEXED | Product identifier |
| `store` | VARCHAR(100) | Blank OK | Retailer name |
| `price` | DECIMAL(10,2) | NOT NULL | Recorded price |
| `timestamp` | DATETIME | Auto, INDEXED | When price was recorded |

**Ordering:** `timestamp` (chronological)

---

## SQLAlchemy Tables (Price Tracking)

### 7. `products` — Product Catalog

| Column | Type | Constraints | Description |
|---|---|---|---|
| `product_id` | VARCHAR(36) | PK | UUID string primary key |
| `name` | VARCHAR | NOT NULL, validated | Product name (cannot be empty) |
| `category` | VARCHAR | INDEXED | Product category |
| `image_url` | VARCHAR | Nullable | Product image URL |

**Relationship:** One `Product` → Many `Price` (cascade delete-orphan)

---

### 8. `prices` — Price Records

Time-series price entries linked to a product.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `price_id` | VARCHAR(36) | PK | UUID string primary key |
| `product_id` | VARCHAR(36) | FK → `products`, INDEXED | Parent product |
| `store_name` | VARCHAR | NOT NULL, INDEXED | Retailer (Amazon / eBay / Walmart) |
| `price` | NUMERIC(10,2) | NOT NULL, > 0 | Price in USD |
| `timestamp` | DATETIME | INDEXED | When price was scraped |
| `product_url` | VARCHAR | Nullable, URL validated | Direct link to listing |

**Validation:** `price` must be > 0; `product_url` must be a valid URL format

---

### 9. `search_history` (SQLAlchemy) — Search Log

| Column | Type | Constraints | Description |
|---|---|---|---|
| `search_id` | VARCHAR(36) | PK | UUID string |
| `user_id` | VARCHAR | NOT NULL, INDEXED | User identifier (string) |
| `query` | VARCHAR | NOT NULL, INDEXED | Search term (validated non-empty) |
| `timestamp` | DATETIME | INDEXED | Search time |

---

## Redis Cache Keys

Redis stores ephemeral data and is not persisted to any relational table.

| Key Pattern | TTL | Content |
|---|---|---|
| `recognition:{image_id}` | 86400s (24h) | CNN model output: `{ category, keywords, confidence }` |
| `price_compare_v2:{query}` | 1800s (30min) | Scraped price list for query |
| `search_task:{task_id}` | 600s (10min) | Async task state: `{ status, results }` |
| `pwd_reset_{token}` | 3600s (1h) | User PK for password reset |

---

## Database Migrations

```bash
# Apply all pending migrations
python manage.py migrate

# Create a new migration after model changes
python manage.py makemigrations <app_name>

# View migration history
python manage.py showmigrations

# Rollback to a specific migration
python manage.py migrate <app_name> <migration_name>
```

Django apps with migrations: `api`, `users`, `advanced`  
SQLAlchemy tables: created via `Base.metadata.create_all(engine)` in `db/connection.py`

---

## Backup & Restore

```bash
# Backup (PostgreSQL via Docker)
docker compose exec db pg_dump -U priceintel_user priceintel > backup.sql

# Restore
cat backup.sql | docker compose exec -T db psql -U priceintel_user priceintel
```
