# PriceIntel — Deployment Documentation

> **Version:** 2.0.0 | **Updated:** 13 March 2026

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Prerequisites](#2-prerequisites)
3. [Local Development Setup](#3-local-development-setup)
4. [Environment Variable Configuration](#4-environment-variable-configuration)
5. [Docker Compose Deployment](#5-docker-compose-deployment)
6. [Database Setup & Migrations](#6-database-setup--migrations)
7. [SSL Certificate Setup](#7-ssl-certificate-setup)
8. [Domain Configuration](#8-domain-configuration)
9. [CI/CD Pipeline](#9-cicd-pipeline)
10. [Rollback Procedures](#10-rollback-procedures)
11. [Monitoring & Health Checks](#11-monitoring--health-checks)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Architecture Overview

```
                        Internet
                           │
                     ┌─────▼──────┐
                     │   nginx    │  :443 (HTTPS)
                     │ (reverse   │  :80  (→ HTTPS redirect)
                     │  proxy)    │
                     └──┬─────┬───┘
                        │     │
              /api/*     │     │  /*
              ┌──────────▼─┐ ┌▼──────────────┐
              │  backend   │ │   frontend     │
              │  (Django/  │ │  (nginx SPA)   │
              │  gunicorn) │ │                │
              └──┬──────┬──┘ └───────────────┘
                 │      │
         ┌───────▼─┐ ┌──▼─────┐
         │ PostgreSQL│ │ Redis  │
         │   db    │ │ cache  │
         └─────────┘ └────────┘
```

---

## 2. Prerequisites

### Server Requirements
- Ubuntu 22.04 LTS (or similar Linux distro)  
- Minimum: **2 vCPU, 4 GB RAM, 20 GB SSD**

### Software
| Tool | Minimum Version |
|---|---|
| Docker | 24.x |
| Docker Compose | 2.x (`docker compose` — note: no hyphen) |
| Git | 2.x |

### Networking
- Domain name pointing to your server's IP
- Ports 80 and 443 open in firewall

---

## 3. Local Development Setup

```bash
# 1. Clone the project
git clone https://github.com/your-org/priceintel.git
cd priceintel

# 2. Set up backend
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
cp .env.example .env           # Edit .env with your local values

python manage.py migrate
python manage.py runserver

# 3. Set up frontend (new terminal)
cd frontend
npm install
cp .env.example .env           # Edit VITE_API_BASE_URL=http://localhost:8000
npm run dev
```

Access:
- Frontend: http://localhost:5173  
- Backend API: http://localhost:8000/api/  
- API Docs: http://localhost:8000/api/docs/

---

## 4. Environment Variable Configuration

### Backend (`.env`)

Copy from `backend/.env.example` → `backend/.env`:

```bash
cp backend/.env.example backend/.env
```

**Critical variables to change for production:**

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key (50+ random chars) | `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DEBUG` | Must be `False` in production | `False` |
| `ALLOWED_HOSTS` | Your domain(s) | `your-domain.com,www.your-domain.com` |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@db:5432/priceintel` |
| `POSTGRES_PASSWORD` | DB password | Strong random string |
| `CORS_ALLOWED_ORIGINS` | Frontend origin | `https://your-domain.com` |
| `EMAIL_HOST_PASSWORD` | Gmail App Password | See Google account settings |

Use `backend/.env.production.example` as the production template.

### CI/CD GitHub Secrets Required

Configure these in **GitHub → Repository → Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `PRODUCTION_SSH_HOST` | Production server IP or hostname |
| `PRODUCTION_SSH_USER` | SSH username (e.g., `ubuntu`) |
| `PRODUCTION_SSH_KEY` | Private SSH key (PEM format) |
| `PRODUCTION_SSH_PORT` | SSH port (default `22`) |
| `VITE_API_BASE_URL` | API URL for frontend build (e.g., `https://api.your-domain.com`) |

---

## 5. Docker Compose Deployment

### First-Time Setup

```bash
# On your production server:

# 1. Clone repository
git clone https://github.com/your-org/priceintel.git
cd priceintel

# 2. Create production environment file
cp backend/.env.production.example backend/.env.production
nano backend/.env.production   # Fill in all values

# 3. Create the SSL directory
mkdir -p nginx/ssl

# 4. Add SSL certificates (see Section 7)
# Then:

# 5. Start all services
docker compose up -d --build

# 6. Check all services are healthy
docker compose ps
```

### Starting / Stopping

```bash
# Start
docker compose up -d

# Stop (preserves data volumes)
docker compose down

# Stop and remove all data (DESTRUCTIVE)
docker compose down --volumes

# View logs
docker compose logs -f [service_name]  # e.g., backend, nginx, db

# Restart a single service
docker compose restart backend
```

---

## 6. Database Setup & Migrations

```bash
# Run migrations (automatically runs on backend container start, but can be run manually)
docker compose exec backend python manage.py migrate

# Create a superuser
docker compose exec backend python manage.py createsuperuser

# Backup the database
docker compose exec db pg_dump -U priceintel_user priceintel > backup_$(date +%Y%m%d).sql

# Restore from backup
cat backup_20260313.sql | docker compose exec -T db psql -U priceintel_user priceintel
```

### Automated Backups

Add to crontab on the production server:

```bash
# Daily backup at 2 AM, keep last 30 days
0 2 * * * cd /opt/priceintel && docker compose exec -T db pg_dump -U priceintel_user priceintel | gzip > /backups/priceintel_$(date +\%Y\%m\%d).sql.gz && find /backups -name "*.sql.gz" -mtime +30 -delete
```

---

## 7. SSL Certificate Setup

### Option A: Let's Encrypt (Free, Recommended)

```bash
# Install certbot
sudo apt install certbot

# Obtain certificate (stop nginx first if it's using port 80)
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Copy certs to nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/

# Auto-renew: Let's Encrypt certs expire every 90 days
# Add to crontab:
0 3 * * 0 certbot renew --quiet && docker compose restart nginx
```

### Update nginx.conf

In `nginx/nginx.conf`, replace `your-domain.com` with your actual domain:

```nginx
server_name your-domain.com www.your-domain.com;
```

---

## 8. Domain Configuration

1. Log in to your domain registrar (e.g., Namecheap, GoDaddy, Cloudflare)
2. Add an **A record**: `your-domain.com` → `YOUR_SERVER_IP`
3. Add a **CNAME record**: `www` → `your-domain.com`
4. DNS propagation can take up to 24–48 hours

Verify DNS:  
```bash
nslookup your-domain.com
dig your-domain.com A
```

---

## 9. CI/CD Pipeline

The GitHub Actions pipeline (`.github/workflows/ci-cd.yml`) runs automatically:

| Trigger | Jobs Run |
|---|---|
| Pull Request to `main` | `test` only |
| Push to `main` | `test` → `docker` → `deploy` |

### Pipeline Steps

```
Push to main
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ test                                                │
│  1. Setup Python 3.11                               │
│  2. Install pip deps (cached)                       │
│  3. Create test .env                                │
│  4. Run: pytest tests/ -v --cov                     │
│  5. Setup Node 20                                   │
│  6. Install npm deps (cached)                       │
│  7. Run: npm run build                              │
│  8. Run: npm run lint                               │
└──────────────────────┬──────────────────────────────┘
                       │ (if tests pass)
                       ▼
┌─────────────────────────────────────────────────────┐
│ docker                                              │
│  1. Login to GitHub Container Registry (ghcr.io)   │
│  2. Build backend image (with layer caching)        │
│  3. Push backend image                              │
│  4. Build frontend image                            │
│  5. Push frontend image                             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│ deploy  [Requires "production" environment approval]│
│  1. SSH into production server                      │
│  2. docker compose pull                             │
│  3. docker compose up -d --remove-orphans           │
│  4. python manage.py migrate --noinput              │
│  5. docker image prune -f                           │
└─────────────────────────────────────────────────────┘
```

### Enabling Production Environment Gate

In GitHub → Repository → Settings → Environments → Create `production`:
- Enable "Required reviewers" to require manual approval before deploy
- Add secrets listed in Section 4

---

## 10. Rollback Procedures

### Quick Rollback (Previous Docker Image)

```bash
# On production server — find the previous image SHA
docker images ghcr.io/your-org/priceintel-backend --format "{{.Tag}} {{.CreatedAt}}"

# Modify docker-compose.yml to pin to previous SHA tag
# e.g., image: ghcr.io/your-org/priceintel-backend:abc1234

docker compose up -d backend
```

### Git-Based Rollback

```bash
# On production server
cd /opt/priceintel

# Identify last known good commit
git log --oneline -10

# Checkout that commit
git checkout <commit_sha>

# Rebuild and restart
docker compose up -d --build backend
docker compose exec backend python manage.py migrate --noinput
```

### Database Rollback

```bash
# Stop backend to prevent writes
docker compose stop backend

# Restore from backup
cat backup_YYYYMMDD.sql | docker compose exec -T db psql -U priceintel_user priceintel

# Restart
docker compose start backend
```

---

## 11. Monitoring & Health Checks

### Built-in Health Endpoint

```bash
curl https://your-domain.com/api/health/
# Expected: {"status": "healthy", "service": "backend-api", "version": "2.0.0"}
```

### Docker Health Checks

```bash
# View health status of all containers
docker compose ps

# View health check logs for a container
docker inspect priceintel_backend | python -m json.tool | grep -A 20 '"Health"'
```

### Suggested Production Monitoring
- **Uptime monitoring:** UptimeRobot (free), Better Uptime
- **Error tracking:** Sentry (`pip install sentry-sdk[django]`)
- **Resource monitoring:** Netdata, Prometheus + Grafana

---

## 12. Troubleshooting

| Problem | Solution |
|---|---|
| `502 Bad Gateway` from nginx | Check backend is running: `docker compose ps backend` |
| Database connection error | Verify `DATABASE_URL` in `.env.production` |
| Migrations fail on startup | Run manually: `docker compose exec backend python manage.py migrate` |
| Static files 404 | Run: `docker compose exec backend python manage.py collectstatic --noinput` |
| SSL certificate error | Verify cert files exist in `nginx/ssl/`; check cert expiry |
| Redis connection refused | Verify Redis container is healthy: `docker compose exec redis redis-cli ping` |
| CORS errors from frontend | Add your domain to `CORS_ALLOWED_ORIGINS` in `.env.production` |
| `403 Forbidden` on API | Check `ALLOWED_HOSTS` includes your domain |
| Rate limit `429` on login | Wait 1 minute or use a different IP; limit is 5/min |
| Image upload fails | Check `MAX_UPLOAD_SIZE` and nginx `client_max_body_size` |

---

*For questions, contact the development team at dev@priceintel.dev*
