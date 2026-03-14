# Privacy Policy — PriceIntel

**Effective Date:** 13 March 2026  
**Last Updated:** 13 March 2026

---

## 1. Introduction

PriceIntel ("we", "us", "our") operates a visual product search and price comparison platform. This Privacy Policy explains how we collect, use, store, and protect your personal data in accordance with the **General Data Protection Regulation (GDPR)**, the UK Data Protection Act 2018, and other applicable privacy laws.

By using PriceIntel, you agree to this Privacy Policy.

---

## 2. Data We Collect

| Category | Data | Purpose |
|---|---|---|
| **Account data** | Email address, name | Registration & authentication |
| **Authentication tokens** | JWT access/refresh tokens | Session management |
| **Uploaded images** | Image files you upload | Visual product search |
| **Search queries** | Product name strings | Price comparison |
| **Usage data** | Request timestamps, IP address | Security, rate limiting, fraud prevention |

We do **not** collect:
- Payment or financial information
- Geolocation data
- Device fingerprints beyond standard server logs

---

## 3. How We Use Your Data

- **Service delivery**: Processing your image uploads and returning price comparisons.
- **Authentication**: Verifying your identity via JWT tokens.
- **Security**: Detecting abuse, enforcing rate limits, preventing attacks.
- **Communication**: Sending password-reset emails you explicitly request.

We do **not** sell or share your personal data with third parties for marketing purposes.

---

## 4. Legal Basis for Processing (GDPR)

| Processing activity | Legal basis |
|---|---|
| Account creation & login | Contract (Art. 6(1)(b)) |
| Image processing & search | Contract (Art. 6(1)(b)) |
| Security monitoring | Legitimate interests (Art. 6(1)(f)) |
| Password-reset email | Consent (Art. 6(1)(a)) |

---

## 5. Data Retention

| Data type | Retention period |
|---|---|
| Account data | Until account deletion |
| Uploaded images | 30 days from upload date |
| Server logs | 90 days |
| Password-reset tokens | 1 hour (cached, auto-expires) |

---

## 6. Cookies

We use the following cookies:

| Cookie | Purpose | Duration |
|---|---|---|
| `sessionid` | Django session management | Session |
| `csrftoken` | CSRF protection (Django) | 1 year |

No third-party tracking or advertising cookies are used.

---

## 7. Your Rights (GDPR)

As a data subject you have the following rights:

- **Right of access** (Art. 15): Request a copy of all data we hold about you.  
  → Use: `GET /api/auth/data-export/`

- **Right to rectification** (Art. 16): Correct inaccurate personal data.  
  → Use: `PUT /api/auth/profile/`

- **Right to erasure** (Art. 17): Delete your account and all associated data.  
  → Use: `DELETE /api/auth/delete-account/` (password confirmation required)

- **Right to data portability** (Art. 20): Download your data in machine-readable format.  
  → The `data-export` endpoint returns JSON.

- **Right to object** (Art. 21): Object to processing based on legitimate interests.  
  → Contact us at privacy@priceintel.dev

- **Right to lodge a complaint**: You may complain to your national supervisory authority.

---

## 8. Data Security

We implement the following security measures:

- Passwords hashed with Django's PBKDF2-SHA256 (bcrypt-compatible strength)
- All API communication over HTTPS/TLS
- HTTP Strict Transport Security (HSTS) enforced
- Input validation and XSS sanitization on all endpoints
- Magic-byte file validation to prevent malicious uploads
- Rate limiting on sensitive endpoints (login, upload, password reset)
- JWT tokens with short lifetimes and rotation-based blacklisting

---

## 9. Third-Party Services

PriceIntel retrieves product data from third-party retailers (Amazon, eBay, Walmart). We do not share your personal data with these services. Price data is fetched server-side on your behalf.

---

## 10. Contact

For privacy concerns, contact:  
**Email:** privacy@priceintel.dev  
**Subject line:** "Privacy Request — [Your Name]"

---

*This document was last reviewed on 13 March 2026.*
