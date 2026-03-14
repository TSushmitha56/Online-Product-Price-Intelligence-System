# PriceIntel — Troubleshooting Guide

**Date:** 13 March 2026

---

## Quick Diagnostic Checklist

Before diving into specific issues, check these first:

```bash
# 1. Is the backend running?
curl http://localhost:8000/api/health/

# 2. Is the frontend running?
curl http://localhost:5173

# 3. Is Redis running?
redis-cli ping   # should print PONG
# (Docker) docker compose exec redis redis-cli ping

# 4. Is the database reachable?
cd backend && python manage.py check --database default
```

---

## 1. Backend Server Issues

### Backend won't start — `ModuleNotFoundError`

**Symptom:**
```
ModuleNotFoundError: No module named 'decouple'
```

**Solution:** Dependencies not installed.
```bash
cd backend
pip install -r requirements.txt
```

---

### Backend won't start — `.env` missing

**Symptom:**
```
decouple.UndefinedValueError: SECRET_KEY not found
```

**Solution:** Create the `.env` file from the template.
```bash
cd backend
cp .env.example .env
# Edit .env and set SECRET_KEY to a random string
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

### Backend won't start — Port already in use

**Symptom:**
```
Error: That port is already in use.
```

**Solution:** Find and kill the process using port 8000.
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

### `python manage.py migrate` fails

**Symptom:**
```
django.db.utils.OperationalError: no such table: ...
```

**Solution:**
```bash
# Fresh migrations
python manage.py migrate

# If still failing, rebuild the database
del db.sqlite3   # Windows
python manage.py migrate
```

---

## 2. Database Connection Errors

### PostgreSQL connection refused

**Symptom:**
```
django.db.utils.OperationalError: could not connect to server
```

**Solutions:**

1. Verify `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgres://user:password@localhost:5432/priceintel
   ```

2. Ensure PostgreSQL is running:
   ```bash
   # Linux
   sudo systemctl status postgresql
   sudo systemctl start postgresql

   # Docker
   docker compose ps db
   docker compose start db
   ```

3. Verify credentials:
   ```bash
   psql -U priceintel_user -d priceintel -h localhost
   ```

---

### SQLite database locked

**Symptom:**
```
sqlite3.OperationalError: database is locked
```

**Solution:** SQLite only supports one writer at a time. In development, restart the server. In production, use PostgreSQL.

---

## 3. Redis Connection Issues

### Cache backend unavailable

**Symptom:**
```
redis.exceptions.ConnectionRefusedError: Error 111 connecting to 127.0.0.1:6379
```

**Solutions:**

1. Start Redis:
   ```bash
   # Local
   redis-server

   # Windows (via WSL)
   wsl redis-server

   # Docker
   docker compose start redis
   ```

2. Check `REDIS_URL` in `.env`:
   ```
   REDIS_URL=redis://127.0.0.1:6379/1
   ```

3. The app will fall back to local memory cache if Redis is unavailable during development.

---

## 4. Image Upload Failures

### "Invalid image format" error

**Symptom:** Upload rejected immediately.

**Solution:** Only JPEG, PNG, and WebP files are accepted. Check:
- File is not corrupted
- File extension matches actual format
- File size is under 10 MB

---

### "Could not process image" error

**Symptom:** Upload succeeds but recognition fails.

**Solutions:**
- Ensure `Pillow` and `opencv-python` are installed:
  ```bash
  pip install Pillow opencv-python
  ```
- Check `media/` directory is writable:
  ```bash
  mkdir -p backend/media
  ```
- Check logs: `python manage.py runserver --verbosity=2`

---

### Recognition returns low confidence

**Symptom:** Product category is wrong or "unknown".

**Solution:** Try a clearer image:
- More light
- Product fills frame
- Straight-on angle
- Remove packaging/background clutter

---

## 5. Scraping Failures

### Zero results returned

**Symptom:** Search completes but shows 0 results for all platforms.

**Possible causes and fixes:**

| Cause | Fix |
|---|---|
| IP blocked by retailer | Use a proxy or wait 30 minutes before retrying |
| Retailer changed HTML | The scraper selector may need updating |
| Search query too specific | Try a more general product name |
| Network timeout | Check internet connection; increase timeout in `scrapers/utils.py` |

---

### Amazon scraper returns prices as None

**Symptom:** Amazon results appear but all prices are `null`.

**Solution:** Amazon's layout changes frequently. Items without directly listed prices may show `null`. The aggregator will still include these results; they'll appear without a price. Check `amazon_scraper.py` selectors.

---

### Scraper blocked (CAPTCHA)

**Symptom:** Results are empty + requests return 503 or redirect to CAPTCHA.

**Solutions:**
- Rotate user agent strings in `scrapers/utils.py`
- Add proxy support to the scraper
- Implement delays between requests
- Consider using a scraping API as a fallback (e.g., SerpAPI, ScrapingBee) — configure via `SERPAPI_API_KEY` in `.env`

---

## 6. Authentication Errors

### `401 Unauthorized` on API calls

**Symptom:** API returns `{"detail": "Authentication credentials were not provided."}`

**Solutions:**
- Token may have expired — log out and log in again
- Frontend should automatically refresh the token — check if `axios.js` interceptor is configured

---

### `429 Too Many Requests` on login

**Symptom:** "Request was throttled" error on login page.

**Solution:** Rate limit is 5 attempts per minute per IP. Wait 1 minute and try again. If this happens in automated testing, reduce test parallelism.

---

### Token refresh loop

**Symptom:** App keeps showing login page even after logging in.

**Solution:**
1. Clear browser localStorage:
   ```javascript
   // In browser console:
   localStorage.clear()
   ```
2. Hard-refresh the page (Ctrl+Shift+R)
3. Log in again

---

## 7. Docker Container Issues

### `docker compose up` fails — port conflict

**Symptom:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
```

**Solution:**
```bash
# Find what's using port 80
# Windows
netstat -ano | findstr :80
taskkill /PID <PID> /F

# Or change the nginx port in docker-compose.yml:
ports:
  - "8080:80"
```

---

### Backend container exits immediately

**Solution:**
```bash
# View logs
docker compose logs backend

# Common fixes:
# 1. Missing .env.production file
cp backend/.env.production.example backend/.env.production

# 2. Database not ready yet
# The backend waits for db healthcheck — check db container
docker compose logs db
```

---

### Database migrations never run in Docker

**Solution:** Run manually:
```bash
docker compose exec backend python manage.py migrate
```

---

### Static files return 404 in Docker

**Solution:**
```bash
docker compose exec backend python manage.py collectstatic --noinput
docker compose restart nginx
```

---

## 8. Frontend Issues

### Blank white screen

**Symptom:** App loads but shows nothing.

**Solutions:**
1. Check browser console (F12 → Console) for errors
2. Verify backend is running:  
   ```bash
   curl http://localhost:8000/api/hello/
   ```
3. Clear browser cache (Ctrl+Shift+R)
4. Check `VITE_API_BASE_URL` in `frontend/.env`

---

### `CORS error` in browser console

**Symptom:**
```
Access to fetch blocked by CORS policy
```

**Solution:** Add your frontend origin to `CORS_ALLOWED_ORIGINS` in `backend/.env`:
```
CORS_ALLOWED_ORIGINS=http://localhost:5173
```
Then restart the backend.

---

### npm install fails

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rd /s /q node_modules    # Windows
npm install
```

---

## 9. SMTP / Email Issues

### Password reset emails not sending

**Solutions:**

1. Check email settings in `.env`:
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

2. Gmail requires **App Passwords** (not your account password):
   - Google Account → Security → 2-Step Verification → App passwords

3. For development, use the console backend — emails print to terminal:
   ```
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

---

## 10. Performance Issues

### Slow price comparison results

**Normal:** First search 8–15 seconds (live scraping). Cached results: <1 second.

If consistently slow:
- Check Redis is working: `redis-cli ping`
- Check `REDIS_URL` in `.env`
- Check network connectivity to Amazon/eBay/Walmart

---

### High memory usage

```bash
# Check container memory usage
docker stats

# Reduce gunicorn workers in backend/Dockerfile:
--workers 2   # instead of 4
```

---

## Getting More Help

- View backend logs: `python manage.py runserver` (shows all requests & errors)
- View Docker logs: `docker compose logs -f [service]`
- Enable verbose logging: Set `DJANGO_LOG_LEVEL=DEBUG` in `.env`
- Contact: **dev@priceintel.dev**
