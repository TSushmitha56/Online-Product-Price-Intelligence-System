<a name="top"></a>

<div align="center">

# 🔍 PriceIntel
### Visual Product Search & Price Comparison Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Upload a product image → AI identifies it → Compare prices across Amazon, eBay & Walmart instantly.**

[Features](#features) · [Tech Stack](#tech-stack) · [Quick Start](#quick-start) · [API Docs](docs/API_DOCUMENTATION.md) · [Deployment](DEPLOYMENT.md)

</div>

---

## Overview

PriceIntel is a full-stack web application that combines **computer vision** with **real-time web scraping** to help users find the best prices for any product — just by taking a photo.

**Core workflow:**
1. User uploads a product image
2. CNN model identifies the product category and keywords
3. Web scrapers search Amazon, eBay, and Walmart simultaneously
4. Results are ranked and displayed with prices, ratings, and store links

---

## Features

| Feature | Description |
|---|---|
| 📸 **Visual Search** | Upload any product image — AI recognizes it instantly |
| 💰 **Price Comparison** | Real-time prices from Amazon, eBay & Walmart |
| 📊 **Dashboard** | Track search history and price trends with interactive charts |
| ❤️ **Wishlist** | Save products for later reference |
| 🔔 **Price Alerts** | Get notified when a product drops below your target price |
| 🔍 **Text Search** | Search by product name with async scraping |
| 🔐 **Secure Auth** | JWT + bcrypt, with password reset via email |
| 🛡️ **Rate Limiting** | Per-endpoint throttling to prevent abuse |
| 📦 **GDPR Compliant** | Data export and account deletion endpoints |
| 🐳 **Docker Ready** | Single `docker compose up` for full deployment |

---

## Tech Stack

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| React | 19 | UI framework |
| Vite | 7 | Build tool & dev server |
| TailwindCSS | 4 | Utility-first styling |
| React Router | 7 | Client-side routing (SPA) |
| Chart.js | 4 | Price history charts |
| Axios | 1 | HTTP client |
| Lucide React | — | Icon library |

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11 | Runtime |
| Django | 4.2 | Web framework |
| Django REST Framework | 3.14 | REST API layer |
| SimpleJWT | 5.3 | JWT authentication |
| Gunicorn | 21 | Production WSGI server |
| Pillow / OpenCV | — | Image processing |
| SQLAlchemy | — | Price history ORM |

### Infrastructure
| Technology | Purpose |
|---|---|
| PostgreSQL 15 | Primary database (production) |
| SQLite | Development database |
| Redis 7 | Caching & session store |
| nginx | Reverse proxy & SSL termination |
| Docker Compose | Container orchestration |
| GitHub Actions | CI/CD pipeline |

---

## Project Structure

```
priceintel/
├── frontend/                   # React/Vite application
│   ├── src/
│   │   ├── pages/              # 11 page components
│   │   ├── components/         # Reusable UI components
│   │   ├── context/            # AuthContext (JWT state)
│   │   ├── api/                # Axios configuration
│   │   ├── routes/             # PrivateRoute guard
│   │   └── utils/              # sanitize.js (security)
│   ├── Dockerfile
│   └── nginx-frontend.conf
│
├── backend/                    # Django application
│   ├── api/                    # Core API (upload, recognize, compare)
│   ├── users/                  # Auth & GDPR endpoints
│   ├── advanced/               # Alerts, wishlist, history
│   ├── scrapers/               # Amazon, eBay, Walmart scrapers
│   ├── recognition/            # CNN product identification
│   ├── comparison/             # Price aggregation engine
│   ├── security/               # Validators, rate limiters
│   ├── db/                     # SQLAlchemy price history models
│   ├── config/                 # Django settings
│   ├── Dockerfile
│   └── requirements.txt
│
├── nginx/                      # Reverse proxy configuration
│   └── nginx.conf
│
├── docs/                       # All documentation
├── docker-compose.yml          # Full stack orchestration
├── DEPLOYMENT.md               # Deployment guide
└── README.md                   # This file
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/your-org/priceintel.git
cd priceintel
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — at minimum set SECRET_KEY

# Apply database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
# → API available at http://localhost:8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Set VITE_API_BASE_URL=http://localhost:8000

# Start development server
npm run dev
# → App available at http://localhost:5173
```

---

## Docker Setup (Recommended for Production)

```bash
# From the project root:

# 1. Configure production environment
cp backend/.env.production.example backend/.env.production
# Edit backend/.env.production with your values

# 2. Add SSL certificates to nginx/ssl/

# 3. Start everything
docker compose up -d --build

# 4. Check status
docker compose ps
```

Services started:
- **nginx** → http://localhost (port 80/443)
- **backend** → Django/Gunicorn (internal port 8000)
- **frontend** → React/nginx (internal port 80)
- **db** → PostgreSQL (internal port 5432)
- **redis** → Redis (internal port 6379)

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | ✅ | — | Django secret key (50+ random chars) |
| `DEBUG` | ✅ | `False` | Enable debug mode (dev only) |
| `ALLOWED_HOSTS` | ✅ | `localhost` | Comma-separated list of allowed hosts |
| `DATABASE_URL` | — | SQLite | PostgreSQL DSN for production |
| `REDIS_URL` | — | `redis://127.0.0.1:6379/1` | Redis connection URL |
| `CORS_ALLOWED_ORIGINS` | ✅ | `http://localhost:5173` | Frontend origin(s) |
| `EMAIL_HOST_USER` | — | — | SMTP email address |
| `EMAIL_HOST_PASSWORD` | — | — | SMTP app password |

See `backend/.env.example` for the full list.

### Frontend (`frontend/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `VITE_API_BASE_URL` | ✅ | `http://localhost:8000` | Backend API base URL |
| `VITE_APP_NAME` | — | `PriceIntel` | App name displayed in UI |

---

## API Overview

Base URL: `http://localhost:8000/api/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/upload-image/` | Upload product image | ✅ |
| `POST` | `/api/recognize-product/` | Run AI recognition | ✅ |
| `GET` | `/api/price-comparison/{id}/` | Full image→price flow | ✅ |
| `GET` | `/api/compare-prices/` | Text-based search | ✅ |
| `GET` | `/api/search-async/` | Async search trigger | ✅ |
| `POST` | `/api/auth/login/` | Get JWT tokens | ❌ |
| `POST` | `/api/auth/register/` | Create account | ❌ |

Full API reference: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

---

## Security

- 🔐 JWT authentication with refresh token rotation + blacklisting
- 🛡️ Per-endpoint rate limiting (5/min login, 10/min upload)
- 🔎 Magic-byte file validation to reject disguised uploads
- 🧼 XSS sanitization with `bleach` on all text inputs
- 🏰 HSTS, X-Frame-Options, CSRF protection in production
- 🔑 All secrets via environment variables — never committed
- 📋 GDPR: data export & account deletion endpoints available

---

## Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=.

# Frontend tests
cd frontend
npm run test    # if configured

# Security-specific tests
pytest tests/test_security.py -v
```

---

## Documentation

| Document | Description |
|---|---|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment guide |
| [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md) | System architecture & data flows |
| [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) | All models and relationships |
| [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) | Complete API reference |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | End-user guide |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues & fixes |
| [docs/PROJECT_REPORT.md](docs/PROJECT_REPORT.md) | Full project report |
| [backend/docs/SECURITY_AUDIT.md](backend/docs/SECURITY_AUDIT.md) | Security audit report |
| [backend/docs/PRIVACY_POLICY.md](backend/docs/PRIVACY_POLICY.md) | Privacy policy |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push and open a pull request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ as a final-year internship project · 2026
</div>
