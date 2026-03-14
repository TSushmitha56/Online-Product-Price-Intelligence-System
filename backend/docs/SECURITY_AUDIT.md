# Security Audit Report — PriceIntel

**Date:** 13 March 2026  
**Auditor:** Automated Review (AI-assisted)  
**Version Audited:** v2.0.0  
**Scope:** Backend API (Django), Frontend (React/Vite), Infrastructure (Docker/nginx)

---

## Executive Summary

This audit identified **6 vulnerabilities** in the original codebase. All have been **remediated** in this release. No critical unresolved issues remain.

---

## Findings & Remediations

### VULN-001 — Hardcoded Secret Key ✅ FIXED
| | |
|---|---|
| **Severity** | Critical |
| **Location** | `config/settings.py` line 13 |
| **Description** | `SECRET_KEY` was hardcoded as a plaintext string in the source file and committed to the repository. Any person with repository access could forge session tokens and JWT signatures. |
| **Remediation** | Moved to `python-decouple` env var. `.env` is gitignored. A unique random key must be generated for each deployment. |

---

### VULN-002 — DEBUG=True in Production ✅ FIXED
| | |
|---|---|
| **Severity** | High |
| **Location** | `config/settings.py` line 16 |
| **Description** | `DEBUG=True` exposes full Python tracebacks, local variable dumps, and the list of installed apps to any unauthenticated user who triggers a 5xx error. |
| **Remediation** | `DEBUG` is now read from an environment variable (defaults to `False`). Production deployments must set `DEBUG=False`. |

---

### VULN-003 — ALLOWED_HOSTS Wildcard ✅ FIXED
| | |
|---|---|
| **Severity** | Medium |
| **Location** | `config/settings.py` line 18 |
| **Description** | `ALLOWED_HOSTS = ['*']` disables Django's Host header validation, enabling HTTP Host header injection attacks which can be used in password-reset link hijacking. |
| **Remediation** | `ALLOWED_HOSTS` now read from env var, defaulting to `['localhost', '127.0.0.1']`. Production deployments must specify exact domain names. |

---

### VULN-004 — No Rate Limiting on Login/Upload ✅ FIXED
| | |
|---|---|
| **Severity** | High |
| **Location** | `users/urls.py`, `api/views.py` |
| **Description** | The login, registration, and image-upload endpoints had only a blanket `user: 60/minute` throttle. This allowed brute-force attacks on login and storage-exhaustion via bulk uploads. |
| **Remediation** | Custom throttle classes applied per endpoint: login 5/min, upload 10/min, recognition 10/min, scraping 15/min, forgot-password 3/min. |

---

### VULN-005 — File Upload: Missing Magic-Byte Validation ✅ FIXED
| | |
|---|---|
| **Severity** | High |
| **Location** | `api/views.py upload_image` |
| **Description** | File type validation relied solely on the `content_type` HTTP header which is attacker-controlled. An attacker could upload a PHP/Python script or executable disguised as `image.jpg`. |
| **Remediation** | Added `validate_image_magic_bytes()` which reads actual binary signatures (JPEG `\xff\xd8\xff`, PNG `\x89PNG`, WebP `RIFF...WEBP`) regardless of stated content type. |

---

### VULN-006 — Stack Traces Exposed in API Responses ✅ FIXED
| | |
|---|---|
| **Severity** | Medium |
| **Location** | `api/views.py` — multiple `except` blocks |
| **Description** | Error handlers returned `f"... Error: {str(e)}"` which included Python exception details, file paths, and internal structure in API responses. This aids attackers in understanding the system. |
| **Remediation** | All exception messages now return generic user-facing strings. Actual exceptions are logged server-side via Django's logging system. |

---

## Security Controls Verified ✅

| Control | Status | Notes |
|---|---|---|
| Password hashing (bcrypt-strength PBKDF2) | ✅ Active | Django's default; enforced via `create_user()` |
| JWT token rotation + blacklisting | ✅ Active | `BLACKLIST_AFTER_ROTATION=True` in SIMPLE_JWT |
| HTTPS enforcement | ✅ Configured | `SECURE_SSL_REDIRECT=True` (production), nginx SSL termination in docker-compose |
| HSTS enabled | ✅ Configured | 1 year max-age, includes subdomains, preload flag |
| Secure cookies | ✅ Configured | `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` (production) |
| XSS filter header | ✅ Active | `SECURE_BROWSER_XSS_FILTER=True` |
| Content type sniffing prevention | ✅ Active | `SECURE_CONTENT_TYPE_NOSNIFF=True` |
| Clickjacking prevention | ✅ Active | `X_FRAME_OPTIONS=DENY` |
| CORS restriction | ✅ Active | `CORS_ALLOW_ALL_ORIGINS=False`, explicit origin allowlist |
| Input sanitization (XSS/SQL) | ✅ Active | `security/validators.py` applied to all text inputs |
| SQL Injection prevention | ✅ Active | Django ORM parameterised queries used throughout |
| Secrets in env vars | ✅ Active | python-decouple; `.env` gitignored |
| File size limit | ✅ Active | 10MB default, configurable via env var |
| Filename sanitization | ✅ Active | Path traversal prevention in `sanitize_filename()` |
| GDPR data export | ✅ Active | `GET /api/auth/data-export/` |
| GDPR account deletion | ✅ Active | `DELETE /api/auth/delete-account/` (password confirmed) |

---

## Remaining Recommendations (Out of Scope for This Release)

| # | Recommendation | Priority |
|---|---|---|
| R-01 | Implement **email verification** on registration | Medium |
| R-02 | Add **multi-factor authentication (MFA/TOTP)** | Medium |
| R-03 | Integrate **Dependabot** or **Snyk** for automated dependency CVE scanning | Medium |
| R-04 | Add **fail2ban** or Cloudflare WAF in front of nginx | Low |
| R-05 | Implement **Content Security Policy (CSP)** header on the frontend | Medium |
| R-06 | Add **audit log** table in DB for security-sensitive actions | Low |

---

## Sign-Off

| Role | Status |
|---|---|
| Security review | ✅ Complete |
| GDPR compliance | ✅ Complete |
| DevOps hardening | ✅ Complete |
| Outstanding critical issues | None |

---

*PriceIntel Security Audit — 13 March 2026*
