# PriceIntel — Technical Architecture Documentation

**Version:** 2.0.0 | **Date:** 13 March 2026

---

## Table of Contents

1. [High-Level System Architecture](#1-high-level-system-architecture)
2. [Frontend Architecture](#2-frontend-architecture)
3. [Backend Architecture](#3-backend-architecture)
4. [Database Architecture](#4-database-architecture)
5. [Data Flow Diagrams](#5-data-flow-diagrams)
6. [Caching Strategy](#6-caching-strategy)
7. [Authentication Flow](#7-authentication-flow)
8. [Security Architecture](#8-security-architecture)
9. [Deployment Architecture](#9-deployment-architecture)
10. [Scraper Service Design](#10-scraper-service-design)

---

## 1. High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                            │
│                    React SPA (Vite)                            │
│   Login │ Upload │ Compare │ Dashboard │ Wishlist │ Alerts     │
└──────────────────────────┬─────────────────────────────────────┘
                           │ HTTPS (JSON REST API)
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                    nginx Reverse Proxy                         │
│  • SSL/TLS Termination   • HTTP→HTTPS Redirect                │
│  • Gzip Compression      • Security Headers (HSTS, CSP)       │
│  • Rate Limiting (nginx) • Route: /api/* → Django             │
│                          • Route: /*    → React SPA           │
└──────────┬───────────────────────────────────────┬────────────┘
           │ /api/*                                │ /*
           ▼                                       ▼
┌────────────────────────┐             ┌────────────────────────┐
│   Django Backend       │             │   Frontend (nginx)     │
│   (Gunicorn: 4 workers)│             │   Static React dist/   │
│                        │             └────────────────────────┘
│  ┌──────────────────┐ │
│  │  api/            │ │◄──── Image Upload, Recognition, Compare
│  │  users/          │ │◄──── Auth, GDPR
│  │  advanced/       │ │◄──── Alerts, Wishlist, History
│  │  security/       │ │◄──── Validators, Throttles
│  │  scrapers/       │ │◄──── Amazon, eBay, Walmart
│  │  recognition/    │ │◄──── CNN Model (TensorFlow/Keras)
│  │  comparison/     │ │◄──── Price Aggregation Engine
│  └──────────────────┘ │
└──────────┬─────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
┌────────┐   ┌────────────────────────────────┐
│ Redis  │   │  Database Layer                │
│ Cache  │   │  ┌──────────────┐              │
│        │   │  │ PostgreSQL   │ (production) │
│ • API  │   │  │  Django ORM  │              │
│   resp │   │  │  (User, Image│              │
│ • ML   │   │  │  Alert,      │              │
│   pred │   │  │  Wishlist)   │              │
│ • Task │   │  └──────────────┘              │
│   queue│   │  ┌──────────────┐              │
└────────┘   │  │ SQLAlchemy   │              │
             │  │  (Product,   │              │
             │  │  Price,      │              │
             │  │  SearchHist) │              │
             │  └──────────────┘              │
             └────────────────────────────────┘
```

---

## 2. Frontend Architecture

### Technology Stack
- **Framework**: React 19 with Vite 7
- **Styling**: TailwindCSS 4 (PostCSS plugin)
- **Routing**: React Router DOM 7 (client-side SPA)
- **State Management**: React Context API (`AuthContext`)
- **HTTP Client**: Axios with interceptors
- **Charts**: Chart.js 4 + react-chartjs-2
- **Icons**: Lucide React

### Application Routes

| Path | Component | Access | Description |
|---|---|---|---|
| `/` | `Login.jsx` | Public | Email/password login |
| `/register` | `Register.jsx` | Public | Account creation |
| `/forgot-password` | `ForgotPassword.jsx` | Public | Password reset request |
| `/reset-password` | `ResetPassword.jsx` | Public | Password reset form |
| `/home` | `Home.jsx` | 🔐 Private | Landing page after login |
| `/upload` | `Upload.jsx` | 🔐 Private | Image upload trigger |
| `/compare` | `Compare.jsx` | 🔐 Private | Price comparison results |
| `/dashboard` | `Dashboard.jsx` | 🔐 Private | Analytics & history |
| `/wishlist` | `Wishlist.jsx` | 🔐 Private | Saved products |
| `/alerts` | `PriceAlerts.jsx` | 🔐 Private | Price alert management |
| `/profile` | `Profile.jsx` | 🔐 Private | Account settings |

### Component Architecture

```
App.jsx
├── AuthProvider (Context)      — JWT token state, login/logout
├── Router
│   ├── Public Routes
│   │   ├── Login, Register, ForgotPassword, ResetPassword
│   ├── PrivateRoute (guard)    — Redirects to / if no token
│   │   ├── Home, Upload, Compare, Dashboard
│   │   ├── Wishlist, PriceAlerts, Profile
│   ├── ComparisonBasket        — Floating basket, always visible
│   └── CompareOverlay          — Side-by-side product comparison
```

### Auth Context Flow

```
Login → POST /api/auth/login/ → { access, refresh }
      → Store in localStorage + AuthContext
      → Axios interceptor injects Bearer token
      → Refresh token auto-renewed via /api/auth/refresh/
      → Logout clears tokens + redirects to /
```

### Code Splitting
All pages are lazy-loaded via `React.lazy()` with a spinner fallback, reducing initial bundle size.

---

## 3. Backend Architecture

### Django Application Structure

```
backend/
├── config/          # Project settings, WSGI, URL root
│   ├── settings.py  # Env-var driven, security hardened
│   ├── urls.py      # Root URL router
│   └── wsgi.py
│
├── api/             # Core functionality app
│   ├── models.py    # Image model (Django ORM)
│   ├── views.py     # Upload, Recognize, Compare endpoints
│   ├── urls.py      # /api/* routes
│   ├── utils.py     # ImageValidator, ImageStorage
│   └── pagination.py
│
├── users/           # Auth & GDPR app
│   ├── models.py    # Custom User model
│   ├── serializers.py
│   ├── views.py     # Register, login, profile, GDPR
│   └── urls.py      # /api/auth/* routes
│
├── advanced/        # User features app
│   ├── models.py    # PriceAlert, SearchHistory, Wishlist, PriceHistory
│   ├── views.py     # CRUD for each model
│   └── urls.py      # /api/advanced/* routes
│
├── scrapers/        # Web scraping engine
│   ├── amazon_scraper.py
│   ├── ebay_scraper.py
│   ├── walmart_scraper.py
│   ├── base_scraper.py
│   └── utils.py    # Headers, proxy, retry logic
│
├── recognition/     # AI product identification
│   ├── predictor.py # CNN inference entrypoint
│   ├── label_mapper.py # Class ID → human label mapping
│   └── (model weights)
│
├── comparison/      # Price matching & scoring
│   └── aggregator.py # Fuzzy match, score offers, rank
│
├── security/        # Security utilities
│   ├── validators.py  # XSS, SQL injection, magic bytes
│   └── rate_limiters.py # Custom DRF throttle classes
│
└── db/              # SQLAlchemy models (price history)
    ├── models.py    # Product, Price, SearchHistory
    └── connection.py # DB session management
```

### Request Lifecycle

```
Client Request
    │
    ▼
nginx (port 443)
    │ Proxy: Host, X-Real-IP, X-Forwarded-Proto headers
    ▼
Django Middleware Stack
    1. SecurityMiddleware (HTTPS redirect)
    2. WhitenoiseMiddleware (static files)
    3. CorsMiddleware (CORS headers)
    4. CompressionMiddleware (gzip)
    5. SessionMiddleware
    6. CsrfViewMiddleware
    7. AuthenticationMiddleware (JWT decode)
    8. XFrameOptionsMiddleware
    │
    ▼
URL Router → View Function
    │
    ├── Throttle check (per-endpoint rate limiter)
    ├── Input validation (security/validators.py)
    ├── Permission check (IsAuthenticated etc.)
    └── Business Logic → Response
```

---

## 4. Database Architecture

### ORM Layers

The system uses **two ORM layers** for different data:

| ORM | Tables | Use Case |
|---|---|---|
| Django ORM | User, Image, PriceAlert, Wishlist, SearchHistory (Django), PriceHistory | Transactional user data via PostgreSQL |
| SQLAlchemy | Product, Price, SearchHistory (SQLAlchemy) | Price tracking across sessions |

### Entity Relationship Diagram

```
User (Django)
 │
 ├──< PriceAlert (FK: user)
 │      ├── product_name
 │      ├── target_price
 │      ├── current_price
 │      └── status: active|triggered|paused
 │
 ├──< Wishlist (FK: user)
 │      ├── product_name
 │      ├── store, price
 │      └── product_url (unique with user)
 │
 ├──< SearchHistory/Django (FK: user)
 │      └── query, timestamp
 │
 └──< Image (no FK to user in current schema)
        ├── image_id (unique)
        ├── file, original_filename
        ├── processed_path
        └── mime_type, file_size

Product (SQLAlchemy)
 └──< Price (FK: product_id)
        ├── store_name
        ├── price (Numeric)
        └── timestamp, product_url
```

---

## 5. Data Flow Diagrams

### Visual Search Flow (Main)

```
User selects image file
        │
        ▼
Frontend validateFileUpload()   ← type/size check
        │
        ▼
POST /api/upload-image/         ← multipart form
        │
        ├── MIME type check
        ├── Magic-byte validation
        ├── Filename sanitization
        ├── Image saved to media/images/
        └── Preprocess (resize, normalize) → media/preprocessed/
                │
                ▼
        { image_id, processed_path }
                │
                ▼
POST /api/recognize-product/    ← { image_id }
        │
        ├── Load preprocessed image
        ├── CNN inference (ResNet/EfficientNet)
        └── Map class IDs → { category, keywords, confidence }
                │
                ▼
GET /api/price-comparison/{image_id}
        │
        ├── Build search query from recognition keywords
        ├── search_all_platforms(query) — parallel scrapers
        │     ├── AmazonScraper.search()
        │     ├── EbayScraper.search()
        │     └── WalmartScraper.search()
        │
        ├── aggregate_prices(query, results)
        │     ├── Fuzzy match results to query
        │     ├── Score by price + rating + availability
        │     └── Rank offers, flag best_deal
        │
        └── Return { product, summary, offers[] }
```

### Async Text Search Flow

```
User types product name
        │
        ▼
validate_search_query()        ← XSS + SQL injection check
        │
        ▼
GET /api/search-async/?product=...
        │
        ├── Generate task_id (UUID)
        ├── cache.set("search_task:{id}", {status: "processing"})
        └── ThreadPoolExecutor.submit(run_search, task_id, query)
                │ (returns immediately with task_id)
                ▼
Frontend polls GET /api/search-status/?task_id=...
every 2 seconds
        │
        ▼ (when status = "completed")
Display results from cache
```

---

## 6. Caching Strategy

Redis is used as the primary cache backend. Falls back to in-memory if Redis is unavailable (dev mode).

| Cache Key Pattern | TTL | Content |
|---|---|---|
| `recognition:{image_id}` | 24 hours | ML inference result |
| `price_compare_v2:{query}` | 30 minutes | Scraping results |
| `search_task:{task_id}` | 10 minutes | Async task status |
| `pwd_reset_{token}` | 1 hour | Password reset token |

**Cache invalidation**: TTL-based expiry only. No manual invalidation.

**Cache hit flow**: If cache hit, skip scraping (expensive) and return immediately. This cuts response time from ~10s to <100ms on cached queries.

---

## 7. Authentication Flow

```
Registration:
  POST /api/auth/register/ { name, email, password, password2 }
    → validate_password() (Django validators, min 8 chars)
    → User.objects.create_user() — PBKDF2-SHA256 hash
    → Return { access_token, refresh_token, user }

Login:
  POST /api/auth/login/ { email, password }  ← rate limited: 5/min
    → SimpleJWT TokenObtainPairView
    → Return { access (60min), refresh (7d) }

Authenticated Request:
  Header: Authorization: Bearer <access_token>
    → JWTAuthentication.authenticate()
    → Decode JWT, verify signature with SECRET_KEY
    → Set request.user

Token Refresh:
  POST /api/auth/refresh/ { refresh }
    → Issue new access token
    → Old refresh token blacklisted (BLACKLIST_AFTER_ROTATION=True)
    → Return new { access, refresh }

Password Reset:
  POST /api/auth/forgot-password/  ← rate limited: 3/min
    → Generate secrets.token_urlsafe(32)
    → cache.set("pwd_reset_{token}", user_pk, timeout=3600)
    → Send email with reset link
  POST /api/auth/reset-password/ { token, new_password }
    → Validate token from cache
    → user.set_password() — new hash stored
    → Delete token from cache
```

---

## 8. Security Architecture

See [SECURITY_AUDIT.md](../backend/docs/SECURITY_AUDIT.md) for the full audit report.

| Layer | Control | Implementation |
|---|---|---|
| Transport | HTTPS/TLS | nginx + Let's Encrypt |
| Transport | HSTS | `max-age=31536000; includeSubDomains` |
| Application | CSRF | Django `CsrfViewMiddleware` |
| Application | XSS Prevention | `bleach.clean()` on all text inputs |
| Application | SQL Injection | Django ORM parameterised queries |
| Application | Rate Limiting | Custom DRF throttle classes |
| File Upload | Type Validation | MIME header + magic bytes |
| File Upload | Filename Safety | Path traversal prevention |
| Auth | Password Storage | PBKDF2-SHA256 (bcrypt-strength) |
| Auth | Token Security | JWT rotation + blacklisting |
| Secrets | Key Management | `python-decouple` env vars |
| GDPR | Data Export | `GET /api/auth/data-export/` |
| GDPR | Account Deletion | `DELETE /api/auth/delete-account/` |

---

## 9. Deployment Architecture

```
                       ┌──────────────────────┐
                       │   GitHub Actions      │
                       │   CI/CD Pipeline      │
                       │  Test→Docker→Deploy   │
                       └──────────┬───────────┘
                                  │ SSH deploy
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Production Server (VPS)                   │
│                                                             │
│  ┌─────────┐  ┌───────────┐  ┌──────────┐  ┌──────────┐   │
│  │  nginx  │  │  backend  │  │ frontend │  │   db     │   │
│  │ :80/:443│  │  :8000    │  │  :80     │  │  :5432   │   │
│  └────┬────┘  └─────┬─────┘  └────┬─────┘  └──────────┘   │
│       │             │             │                         │
│       └──backend_net┘    frontend_net                       │
│                                             ┌──────────┐   │
│                                             │  redis   │   │
│                                             │  :6379   │   │
│                                             └──────────┘   │
│                                                             │
│  Named Volumes: postgres_data, redis_data,                  │
│                 backend_media, backend_static               │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Scraper Service Design

### Scraper Architecture

```
search_all_platforms(query)          ← scrapers/__init__.py
    │
    ├── AmazonScraper(query).search()  → List[Dict]
    ├── EbayScraper(query).search()    → List[Dict]
    └── WalmartScraper(query).search() → List[Dict]
    │
    └── merged results list → aggregator
```

### Base Scraper Pattern

Each scraper inherits from `BaseScraper` which provides:
- Rotating user-agent headers
- Request retry logic with exponential backoff
- Timeout configuration (10–30s)
- Response parsing utilities

### Normalized Result Schema

Every scraper returns items conforming to:

```json
{
  "platform": "Amazon",
  "title": "Product Name",
  "price": 29.99,
  "currency": "USD",
  "product_url": "https://amazon.com/dp/...",
  "image_url": "https://...",
  "availability": "In Stock",
  "rating": 4.5,
  "shipping_cost": 0.0
}
```

### Price Aggregation Engine (`comparison/aggregator.py`)

1. **Normalization**: Strips brand names, units, variants from titles
2. **Fuzzy Matching**: Compares search query against result titles using similarity score
3. **Scoring**: Ranks by: price weight (50%) + rating weight (30%) + availability (20%)
4. **Best Deal**: Lowest total cost (price + shipping) flagged as `is_best_deal`
