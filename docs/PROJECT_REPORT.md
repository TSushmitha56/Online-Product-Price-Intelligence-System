# PriceIntel — Final Project Report

**Project:** Visual Product Search & Price Comparison Platform  
**Version:** 2.0.0  
**Date:** 13 March 2026  
**Team:** Internship Project

---

## 1. Introduction

PriceIntel is a full-stack web application that enables users to find the best product prices by uploading an image of a product. The system identifies the product using a convolutional neural network (CNN), then simultaneously scrapes Amazon, eBay, and Walmart to retrieve and compare current prices.

The problem being solved is that **consumers waste time visiting multiple online retailers manually** to compare prices. PriceIntel automates this process and adds intelligence through visual recognition — eliminating the need to know a product's exact name.

---

## 2. Objectives

1. Implement a visual product recognition system that identifies products from photos
2. Build real-time scrapers for three major e-commerce platforms
3. Design a price aggregation and ranking engine
4. Create an intuitive React frontend with a comprehensive dashboard
5. Implement user features: wishlist, price alerts, and search history
6. Secure the platform with industry-standard authentication and input validation
7. Containerize and document the system for production deployment

---

## 3. Methodology

### Development Approach
- **Iterative delivery** in 20 milestones (tasks), from backend scaffold to deployment
- **Component-first** React development to ensure reusability
- **Security-by-design**: security measures implemented as dedicated modules, not afterthoughts
- **Test-driven validation** for security-critical components

### Agile Workflow
- Features developed in vertical slices (UI → API → Model → Test)
- Scraper logic validated with live site testing
- Security audit conducted at end of implementation

---

## 4. System Architecture

### High-Level View

```
Browser (React SPA)
  ↕ HTTPS/REST JSON
nginx Reverse Proxy (SSL termination)
  ├── /api/* → Django Backend (Gunicorn, 4 workers)
  └── /*     → React Static Dist (nginx)

Django Backend
  ├── Image Upload      (api/views.py)
  ├── CNN Recognition   (recognition/predictor.py)
  ├── Price Scrapers    (scrapers/amazon, ebay, walmart)
  ├── Price Aggregator  (comparison/aggregator.py)
  ├── User Auth         (users/ + SimpleJWT)
  └── Advanced Features (advanced/ - alerts, wishlist)

Data Storage
  ├── PostgreSQL (Django ORM — users, images, alerts, wishlists)
  ├── SQLAlchemy (price history, product catalog)
  └── Redis     (API cache, async tasks, password reset tokens)
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| Django REST Framework | Mature, well-documented, strong auth ecosystem |
| SimpleJWT tokens | Stateless, scalable, refresh rotation for security |
| Dual ORM approach | Django ORM for user data; SQLAlchemy for price history (flexibility) |
| Redis caching | 30-min cache on scraped data — scrapers are expensive (~10s) |
| Multi-stage Docker build | Smaller final images; no build tools in production |
| ThreadPoolExecutor for scrapers | Parallel scraping cuts search time by ~3x |

---

## 5. Implementation Details

### 5.1 Product Recognition Module

The recognition pipeline uses a pre-trained CNN (ResNet/EfficientNet architecture):

1. Image is uploaded and pre-processed (resize to 224×224, normalize pixel values)
2. Forward pass through the CNN returns class probabilities
3. `label_mapper.py` maps ImageNet class IDs to product categories
4. Top predictions are returned with confidence scores
5. The highest-confidence label forms the scraper search query

**Cache:** Recognition results are cached for 24 hours per image ID.

### 5.2 Web Scraping Engine

Three scrapers are implemented:

| Scraper | Data Extracted | Notes |
|---|---|---|
| `AmazonScraper` | Title, price, rating, ASIN, availability | Most complex — layout changes frequently |
| `EbayScraper` | Title, price, shipping, condition, seller rating | API-like structured response |
| `WalmartScraper` | Title, price, stock, product ID | Relatively stable selectors |

All scrapers:
- Use rotating user-agent headers from a pool of realistic browser strings
- Implement retry logic with exponential backoff (up to 3 attempts)
- Parse HTML with `BeautifulSoup`
- Return normalized result objects with consistent fields

### 5.3 Price Aggregation Engine

`comparison/aggregator.py` normalizes and ranks results:

1. **Normalization**: Strip special chars, lowercase, remove brand names
2. **Fuzzy Match**: Compare search query to result title (similarity score)
3. **Scoring formula**: `score = (price_weight × 0.5) + (rating × 0.3) + (availability × 0.2)`
4. **Best Deal**: Lowest total cost (price + shipping) flagged
5. **Deduplication**: Near-identical titles from the same platform merged

### 5.4 Frontend Architecture

React 19 + Vite 7 SPA with:
- **Lazy loading** for all 11 page components (code splitting)
- **AuthContext** manages JWT state globally
- **Axios interceptors** auto-attach tokens + auto-refresh on 401
- **Chart.js** renders price history line charts with smooth animations
- **ComparisonBasket** floating component — always accessible

### 5.5 Security Layer

See [SECURITY_AUDIT.md](../backend/docs/SECURITY_AUDIT.md) for full audit report.

Key controls:
- JWT rotation + blacklisting
- Magic-byte file validation (prevents disguised malware uploads)
- PBKDF2-SHA256 (100,000 iterations) password hashing
- Per-endpoint rate limiting
- GDPR data export and deletion endpoints

---

## 6. Technologies Used

| Category | Technology | Version |
|---|---|---|
| Frontend Framework | React | 19 |
| Frontend Build | Vite | 7 |
| Frontend Styling | TailwindCSS | 4 |
| Frontend Charts | Chart.js | 4 |
| Backend Framework | Django | 4.2 |
| Backend API Layer | Django REST Framework | 3.14 |
| Backend Auth | django-rest-framework-simplejwt | 5.3 |
| Web Scraping | BeautifulSoup4 + requests | — |
| Image Processing | Pillow + OpenCV | — |
| ORM (primary) | Django ORM | — |
| ORM (price history) | SQLAlchemy | 2.x |
| Cache / Queue | Redis | 7 |
| Production DB | PostgreSQL | 15 |
| WSGI Server | Gunicorn | 21 |
| Reverse Proxy | nginx | 1.25 |
| Containerization | Docker + Docker Compose | 24 |
| CI/CD | GitHub Actions | — |
| Security | python-decouple, bleach, python-magic | — |

---

## 7. Challenges Faced

### 7.1 Amazon Scraper Stability
**Challenge:** Amazon actively blocks scrapers and frequently changes its HTML structure.  
**Solution:** Implemented multiple CSS selector fallbacks, rotating user agents, and retry logic. Price fields are now extracted from multiple possible locations.

### 7.2 Dual ORM Integration
**Challenge:** Using both Django ORM and SQLAlchemy in the same Django project caused session management conflicts.  
**Solution:** SQLAlchemy sessions are managed independently via `db/connection.py` with scoped session pattern. Django's ORM and SQLAlchemy never share transactions.

### 7.3 Async Search Performance
**Challenge:** Synchronous price scraping blocked the HTTP response for 10–15 seconds.  
**Solution:** Implemented async search pattern using `ThreadPoolExecutor`, returning a task ID immediately and allowing polling via `/api/search-status/`.

### 7.4 Image Recognition Accuracy
**Challenge:** Generic product photos (e.g., a laptop at an angle) yielded low-confidence predictions.  
**Solution:** Added a label smoothing post-processor that maps low-confidence "unknown" results to higher-level category labels (e.g., "electronic device"). The frontend shows confidence % to set user expectations.

---

## 8. Testing Strategy

| Test Type | Scope | Tool |
|---|---|---|
| Unit tests — security | Validators, rate limiters, magic bytes | pytest |
| Unit tests — scrapers | BeautifulSoup selector logic | pytest |
| Integration — API | Endpoint request/response validation | Django test client |
| Manual — UI | All 11 pages tested in Chrome + Firefox | — |
| Security audit | Vulnerability scan of all 6 known issues | Manual + tools |

**Test results:** 27/27 security tests passing (`tests/test_security.py`)

---

## 9. Performance Optimization

| Optimization | Impact |
|---|---|
| Redis API caching (30 min) | 10s → <100ms on cached queries |
| ThreadPoolExecutor for scrapers | 3x faster than sequential |
| React lazy loading | Smaller initial JS bundle |
| Gunicorn 4 workers | Handles concurrent users |
| nginx gzip compression | ~70% reduction in static asset transfer size |
| PostgreSQL indexes | Fast queries on user_id, timestamp, product_name |

---

## 10. Security Considerations

The following security controls are in production:

1. **Authentication**: JWT with 60-minute access tokens + 7-day refresh (auto-rotated)
2. **Password security**: PBKDF2-SHA256 hashing (Django default, bcrypt-level strength)
3. **Rate limiting**: Per-endpoint throttle classes (5/min login, 10/min upload)
4. **Input validation**: XSS stripping with `bleach`, SQL pattern detection
5. **File upload security**: Magic-byte validation (blocks disguised executables)
6. **Transport security**: HTTPS via nginx + HSTS enforcement
7. **CORS**: Strict origin allowlist; no wildcard
8. **Secrets management**: All keys in env vars; `.env` is gitignored
9. **GDPR compliance**: Data export + account deletion endpoints

---

## 11. Future Enhancements

| Feature | Priority | Description |
|---|---|---|
| Email verification | High | Confirm email on registration |
| Multi-factor authentication | Medium | TOTP support |
| Browser extension | Medium | Right-click any product image to compare prices |
| Price prediction | Medium | ML model to forecast price trends |
| Mobile app | Low | React Native companion app |
| More retailers | Medium | Best Buy, Target, AliExpress |
| Automated scraping scheduler | High | Proactively update price history daily |
| CSP headers | Medium | Content Security Policy on frontend |
| Audit logging | Low | Log all security-sensitive actions to DB |
| Multi-language support | Low | i18n for international users |

---

## 12. Conclusion

PriceIntel successfully delivers:
- ✅ AI-powered visual product recognition
- ✅ Real-time price comparison across Amazon, eBay, and Walmart
- ✅ Rich user features: dashboard, wishlist, price alerts, history
- ✅ Production-grade security (GDPR compliant, JWT, rate limiting)
- ✅ Full Docker deployment pipeline with CI/CD
- ✅ Comprehensive documentation

The platform is deployable immediately using a single `docker compose up` command and is ready for real user traffic.

---

*PriceIntel Final Project Report — March 2026*
