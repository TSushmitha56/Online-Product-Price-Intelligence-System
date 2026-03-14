# PriceIntel — Project Presentation

**Visual Product Search & Price Comparison Platform**  
*Final Internship Project — March 2026*

---

## Slide 1: Title

# 🔍 PriceIntel
### Visual Product Search & Price Comparison

> *"Take a photo. Find the best price."*

**Team:** [Your Team]  
**Date:** March 2026  
**Supervisor:** [Supervisor Name]

---

## Slide 2: Problem Statement

### The Problem

🛒 Online shoppers waste significant time:

- Visiting **3–5 different websites** manually to compare prices
- Struggling to remember **exact product names** to search
- Missing better deals available on other platforms
- No easy way to **track price changes** over time

### The Cost

> The average consumer overpays by **15–25%** by not comparing prices across retailers

---

## Slide 3: Our Solution — PriceIntel

### One Upload. Three Stores. Best Price.

```
📸 Upload Photo
     ↓
🤖 AI Identifies Product
     ↓
🔍 Scrapes Amazon + eBay + Walmart
     ↓
💰 Shows Best Deal
```

**Also includes:**
- 🔔 Price Alerts — get notified when prices drop
- ❤️ Wishlist — save products for later
- 📊 Dashboard — track your search history and price trends
- 🔄 Side-by-side product comparison

---

## Slide 4: System Architecture

```
┌─────────────────────────────────────────────┐
│          React SPA (Browser)                │
│  Login │ Upload │ Compare │ Dashboard       │
└──────────────────┬──────────────────────────┘
                   │ HTTPS + JWT
                   ▼
┌─────────────────────────────────────────────┐
│     nginx Reverse Proxy (SSL + Gzip)        │
├──────────────────┬──────────────────────────┤
│   Django API     │   Static Frontend        │
│   (Gunicorn)     │   (nginx)                │
├──────────────────┤                          │
│  • Recognition   │                          │
│  • Scrapers      │                          │
│  • Aggregator    │                          │
│  • Auth + GDPR   │                          │
└────────┬─────────┘                          │
    ┌────┴────┐    ┌────────┐                 │
    │Postgres │    │ Redis  │                 │
    └─────────┘    └────────┘                 │
```

---

## Slide 5: Key Features

| Feature | Description |
|---|---|
| 📸 **Visual Search** | Upload any product photo — AI identifies it |
| 💰 **Price Comparison** | Real-time prices from 3 major retailers |
| 🤖 **AI Recognition** | CNN model (ResNet/EfficientNet) for product ID |
| 🔔 **Price Alerts** | Email notification when price drops to target |
| ❤️ **Wishlist** | Save products for tracking |
| 📊 **Dashboard** | Analytics, charts, search history |
| 🔄 **Side-by-Side** | Compare up to 3 products simultaneously |
| ⚡ **Async Search** | Non-blocking search with live polling |
| 🛡️ **Secure** | JWT auth, rate limiting, GDPR compliant |

---

## Slide 6: Technology Stack

### Frontend
| | |
|---|---|
| **React 19** | UI framework |
| **Vite 7** | Build tool (< 1s HMR) |
| **TailwindCSS 4** | Utility-first styling |
| **Chart.js** | Price history charts |

### Backend
| | |
|---|---|
| **Django 4.2** | Web framework |
| **Django REST Framework** | REST API |
| **SimpleJWT** | Authentication |
| **BeautifulSoup4** | Web scraping |
| **Redis** | Caching (30min TTL) |

### Infrastructure
| | |
|---|---|
| **Docker Compose** | Container orchestration |
| **nginx** | Reverse proxy + SSL |
| **GitHub Actions** | CI/CD pipeline |
| **PostgreSQL** | Production database |

---

## Slide 7: AI Product Recognition

### How It Works

```
User Photo
    │
    ▼ Preprocessing (resize 224×224, normalize)
    │
    ▼ CNN Inference (ResNet/EfficientNet)
    │
    ▼ Class Probabilities
    │
    ▼ label_mapper.py → "laptop computer" (89% confidence)
    │
    ▼ Search Query → Scrapers
```

### Performance
- Recognition: ~2–3 seconds per image
- Cached results: < 100ms (24h TTL)
- Accuracy: High confidence on common consumer products

---

## Slide 8: Web Scraping Architecture

### Parallel Scraping

```
search_all_platforms("laptop computer")
         │
┌────────┼────────┐
▼        ▼        ▼
Amazon  eBay   Walmart    ← ThreadPoolExecutor (parallel)
  │       │       │
  └───────┴───────┘
         │
   aggregator.py
   • Fuzzy match
   • Score & rank
   • Flag best deal
         │
    Final Results
```

**Speed:** Parallel scraping is 3× faster than sequential

**Caching:** Results cached 30 minutes — same query is instant on repeat

---

## Slide 9: Security Implementation

### Security Controls

| Control | Implementation |
|---|---|
| **Authentication** | JWT + refresh rotation + blacklisting |
| **Passwords** | PBKDF2-SHA256 (100k iterations) |
| **Rate Limiting** | 5/min login, 10/min upload, 3/min reset |
| **File Validation** | Magic-byte check rejects disguised files |
| **XSS Prevention** | `bleach` sanitization on all text input |
| **Transport** | HTTPS + HSTS (1 year) + nginx |
| **GDPR** | Data export & account deletion endpoints |

**Security Audit:** 6 vulnerabilities identified and fixed pre-launch

---

## Slide 10: Demonstration

### Workflow Demo

**Step 1:** User logs in
**Step 2:** Uploads photo of a product (e.g., wireless headphones)
**Step 3:** AI identifies: "Wireless headphones — 87% confidence"
**Step 4:** Results show:
- Sony WH-1000XM5 at Walmart: **$249.99** ← Best Deal
- Same product on Amazon: $279.99
- Similar on eBay: $265.00 (used)

**Step 5:** User adds Walmart deal to Wishlist
**Step 6:** Sets price alert at $230 target
**Step 7:** Dashboard shows price history chart

---

## Slide 11: Challenges & Solutions

| Challenge | Solution |
|---|---|
| Amazon blocks scrapers | Rotating user agents + retry backoff |
| Dual ORM conflict (Django + SQLAlchemy) | Scoped sessions, independent connection management |
| 10–15s blocking scrape time | Async search with task polling |
| Low-confidence recognition | Fallback to higher-level category labels |
| JWT tokens expiring mid-session | Auto-refresh via Axios interceptor |

---

## Slide 12: Performance Metrics

| Metric | Value |
|---|---|
| Cached query response time | < 100ms |
| Live scraping time (3 platforms) | 8–15 seconds |
| AI recognition time | ~2–3 seconds |
| Security test suite | 27/27 passing |
| Docker cold start | ~30 seconds |
| Supported concurrent users | 4× workers (scalable) |

---

## Slide 13: Future Enhancements

### Planned Improvements

| Priority | Feature |
|---|---|
| 🔴 High | Email verification on registration |
| 🔴 High | Automated price scheduler (daily scraping) |
| 🟡 Medium | Browser extension for one-click comparison |
| 🟡 Medium | Price prediction ML model |
| 🟡 Medium | Additional retailers (Best Buy, Target) |
| 🟡 Medium | Multi-factor authentication |
| 🟢 Low | Mobile app (React Native) |
| 🟢 Low | Multi-language support |

---

## Slide 14: Project Summary

### Deliverables Completed

✅ Task 1–5: Backend foundation, scraping engine, price comparison, database, authentication  
✅ Task 6–10: Frontend development, all 11 pages, Dashboard analytics  
✅ Task 11–15: Advanced features (wishlist, alerts, history, comparison)  
✅ Task 16–17: Price alert scheduler, performance optimization, Redis caching  
✅ Task 18: Security implementation (6 vulnerabilities fixed, GDPR compliance)  
✅ Task 19: Docker, CI/CD pipeline, nginx deployment  
✅ Task 20: Full documentation, user guide, project handover  

### Ready for Production

🐳 **`docker compose up -d --build`** → Entire stack running in one command

---

## Slide 15: Thank You

# 🔍 PriceIntel

**GitHub:** [your-org/priceintel]  
**Live Demo:** [https://your-domain.com]  
**Documentation:** [docs/ folder]

> *"Take a photo. Find the best price."*

**Questions?**
