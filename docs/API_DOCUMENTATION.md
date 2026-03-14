# PriceIntel — API Documentation

**Version:** 2.0.0 | **Base URL:** `http://localhost:8000` (dev) / `https://your-domain.com` (prod)

---

## Authentication

Most endpoints require a JWT access token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Tokens are obtained by logging in via `POST /api/auth/login/`.

---

## Response Format

All successful responses return JSON. Error responses follow this pattern:

```json
{
  "error": "Human-readable error message"
}
```

HTTP status codes follow REST conventions (200, 201, 400, 401, 403, 404, 429, 500).

---

## Rate Limits

| Endpoint Group | Limit | Window |
|---|---|---|
| Login / Register | 5 requests | Per minute, per IP |
| Image Upload | 10 requests | Per minute, per user |
| Product Recognition | 10 requests | Per minute, per user |
| Price Scraping | 15 requests | Per minute, per user |
| Forgot Password | 3 requests | Per minute, per IP |
| General API | 100 requests | Per minute, per user |

Rate limit exceeded returns HTTP **429 Too Many Requests**.

---

## Endpoints

---

### Health & Status

#### `GET /api/hello/`

Simple connectivity check.

**Authentication:** None

**Response `200`:**
```json
{
  "message": "Hello from Django backend!"
}
```

---

#### `GET /api/health/`

System health check used by Docker healthchecks and monitoring tools.

**Authentication:** None

**Response `200`:**
```json
{
  "status": "healthy",
  "service": "backend-api",
  "version": "2.0.0"
}
```

---

### Authentication (`/api/auth/`)

---

#### `POST /api/auth/register/`

Create a new user account.

**Authentication:** None  
**Rate limit:** 5/min per IP

**Request Body:**
```json
{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!"
}
```

**Response `201 Created`:**
```json
{
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJhbGci...",
    "access": "eyJhbGci..."
  }
}
```

**Error `400`:**
```json
{
  "email": ["A user with this email already exists."],
  "password2": ["Passwords do not match."]
}
```

---

#### `POST /api/auth/login/`

Authenticate and receive JWT tokens.

**Authentication:** None  
**Rate limit:** 5/min per IP

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response `200`:**
```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci..."
}
```

**Error `401`:**
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

#### `POST /api/auth/refresh/`

Exchange a refresh token for a new access token (old refresh token is blacklisted).

**Request Body:**
```json
{
  "refresh": "eyJhbGci..."
}
```

**Response `200`:**
```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci..."
}
```

---

#### `GET /api/auth/profile/`

Get the current user's profile.

**Authentication:** ✅ Required

**Response `200`:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2026-03-13T10:00:00Z"
}
```

---

#### `PUT /api/auth/profile/`

Update profile fields (partial update supported).

**Authentication:** ✅ Required

**Request Body (partial):**
```json
{
  "first_name": "Jonathan"
}
```

**Response `200`:**
```json
{
  "message": "Profile updated.",
  "user": { ... }
}
```

---

#### `POST /api/auth/change-password/`

Change the authenticated user's password.

**Authentication:** ✅ Required

**Request Body:**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewSecurePass456!",
  "new_password2": "NewSecurePass456!"
}
```

**Response `200`:**
```json
{
  "message": "Password changed successfully."
}
```

---

#### `POST /api/auth/forgot-password/`

Request a password reset email.

**Authentication:** None  
**Rate limit:** 3/min per IP  
**Note:** Always returns the same message to prevent user enumeration.

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Response `200`:**
```json
{
  "message": "If that email exists, a reset link has been sent."
}
```

---

#### `POST /api/auth/reset-password/`

Reset password using a token received by email.

**Request Body:**
```json
{
  "token": "abc123xyz...",
  "new_password": "NewSecurePass789!",
  "new_password2": "NewSecurePass789!"
}
```

**Response `200`:**
```json
{
  "message": "Password reset successfully. You can now log in."
}
```

**Error `400`:**
```json
{
  "error": "Invalid or expired reset token."
}
```

---

#### `GET /api/auth/data-export/`

**GDPR** — Export all personal data in machine-readable JSON format.

**Authentication:** ✅ Required

**Response `200`:**
```json
{
  "export_generated_at": "2026-03-13T17:00:00Z",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "first_name": "John",
    "date_joined": "2026-01-01T09:00:00Z"
  },
  "uploaded_images": [
    {
      "image_id": "20260313_abc123",
      "original_filename": "laptop.jpg",
      "file_size_bytes": 1048576,
      "uploaded_at": "2026-03-13T10:30:00Z"
    }
  ]
}
```

---

#### `DELETE /api/auth/delete-account/`

**GDPR** — Permanently delete account and all associated data. Requires password confirmation.

**Authentication:** ✅ Required

**Request Body:**
```json
{
  "password": "SecurePass123!"
}
```

**Response `200`:**
```json
{
  "message": "Your account and all associated data have been permanently deleted."
}
```

---

### Core Image API (`/api/`)

---

#### `POST /api/upload-image/`

Upload a product image for recognition.

**Authentication:** ✅ Required  
**Rate limit:** 10/min per user  
**Content-Type:** `multipart/form-data`

**Request:**
```
file: <binary image file>   (JPEG, PNG, or WebP; max 10MB)
```

**Response `200`:**
```json
{
  "success": true,
  "image_id": "20260313_a1b2c3d4",
  "original_filename": "laptop.jpg",
  "file_size_mb": 2.1,
  "process_path": "media/preprocessed/20260313_a1b2c3d4.jpg",
  "timestamp": "2026-03-13T17:00:00Z",
  "message": "Image uploaded and preprocessed successfully"
}
```

**Error `400`:**
```json
{
  "error": "Invalid image format. Only JPEG, PNG, and WebP files are accepted."
}
```

**Error `429`:**
```json
{
  "detail": "Request was throttled. Expected available in 30 seconds."
}
```

---

#### `POST /api/recognize-product/`

Run AI recognition on a previously uploaded image.

**Authentication:** ✅ Required  
**Rate limit:** 10/min per user

**Request Body:**
```json
{
  "image_id": "20260313_a1b2c3d4"
}
```

**Response `200`:**
```json
{
  "success": true,
  "image_id": "20260313_a1b2c3d4",
  "recognition": {
    "category": "laptops",
    "primary_label": "laptop computer",
    "search_keywords": "laptop computer",
    "top_predictions": [
      {"label": "laptop computer", "confidence": 0.89},
      {"label": "notebook computer", "confidence": 0.07}
    ],
    "confidence": 0.89
  },
  "from_cache": false
}
```

**Error `404`:**
```json
{
  "error": "Image not found. Please upload the image first."
}
```

---

#### `GET /api/price-comparison/{image_id}/`

Complete flow: retrieve recognition results then scrape all platforms.

**Authentication:** ✅ Required  
**Rate limit:** 15/min per user

**URL Parameter:** `image_id` — from the upload response

**Response `200`:**
```json
{
  "success": true,
  "image_id": "20260313_a1b2c3d4",
  "product": {
    "name": "laptop computer",
    "category": "laptops",
    "confidence": 0.89
  },
  "summary": {
    "total_results": 12,
    "platforms_searched": ["Amazon", "eBay", "Walmart"],
    "lowest_price": 349.99,
    "highest_price": 1299.99,
    "average_price": 749.50,
    "best_deal_store": "Walmart",
    "best_deal_price": 349.99
  },
  "offers": [
    {
      "platform": "Walmart",
      "title": "HP Chromebook 14 Laptop",
      "price": 349.99,
      "currency": "USD",
      "product_url": "https://www.walmart.com/...",
      "image_url": "https://i5.walmartimages.com/...",
      "availability": "In Stock",
      "rating": 4.2,
      "shipping": "Free shipping",
      "is_best_deal": true
    },
    {
      "platform": "Amazon",
      "title": "Acer Aspire 3 Laptop",
      "price": 399.00,
      "product_url": "https://www.amazon.com/...",
      "rating": 4.5,
      "is_best_deal": false
    }
  ],
  "from_cache": false
}
```

---

#### `GET /api/compare-prices/`

Text-based synchronous price search across all platforms.

**Authentication:** ✅ Required

**Query Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `product` | ✅ | Product name to search |
| `page` | ❌ | Page number (default: 1) |
| `page_size` | ❌ | Results per page (default: 20) |

**Example:** `GET /api/compare-prices/?product=wireless+headphones&page=1`

**Response `200`:**
```json
{
  "query": "wireless headphones",
  "total_results": 24,
  "page": 1,
  "results": [
    {
      "platform": "Amazon",
      "title": "Sony WH-1000XM5",
      "price": 279.99,
      "rating": 4.7,
      "is_best_deal": true
    }
  ]
}
```

---

#### `GET /api/search-async/`

Launch an asynchronous price search. Returns a task ID immediately.

**Authentication:** ✅ Required

**Query Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `product` | ✅ | Product name |

**Response `202 Accepted`:**
```json
{
  "task_id": "f81d4fae-7dec-11d0-a765",
  "status": "processing",
  "message": "Search started. Poll /api/search-status/?task_id=..."
}
```

---

#### `GET /api/search-status/`

Poll for async search results.

**Authentication:** ✅ Required

**Query Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `task_id` | ✅ | From `/search-async/` response |

**Response `200` (in progress):**
```json
{
  "task_id": "f81d4fae-7dec-11d0-a765",
  "status": "processing"
}
```

**Response `200` (completed):**
```json
{
  "task_id": "f81d4fae-7dec-11d0-a765",
  "status": "completed",
  "results": [ ... ]
}
```

---

#### `GET /api/price-history/`

Price history data for the dashboard chart.

**Authentication:** ✅ Required

**Query Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `product` | ✅ | Product name |
| `days` | ❌ | How many days back (default: 30) |

**Response `200`:**
```json
{
  "product": "Sony WH-1000XM5",
  "data_points": [
    {"timestamp": "2026-02-10T12:00:00Z", "store": "Amazon", "price": 299.99},
    {"timestamp": "2026-02-17T12:00:00Z", "store": "Amazon", "price": 289.99},
    {"timestamp": "2026-03-01T12:00:00Z", "store": "Amazon", "price": 279.99}
  ]
}
```

---

### Advanced Features (`/api/advanced/`)

---

#### `GET /api/advanced/alerts/`

List all price alerts for the authenticated user.

**Authentication:** ✅ Required

**Response `200`:**
```json
[
  {
    "id": 1,
    "product_name": "Sony WH-1000XM5",
    "target_price": "250.00",
    "current_price": "279.99",
    "product_url": "https://www.amazon.com/...",
    "status": "active",
    "created_at": "2026-03-01T10:00:00Z"
  }
]
```

---

#### `POST /api/advanced/alerts/`

Create a new price alert.

**Authentication:** ✅ Required

**Request Body:**
```json
{
  "product_name": "Sony WH-1000XM5",
  "target_price": 250.00,
  "product_url": "https://www.amazon.com/..."
}
```

**Response `201`:**
```json
{
  "id": 2,
  "product_name": "Sony WH-1000XM5",
  "target_price": "250.00",
  "status": "active",
  "created_at": "2026-03-13T17:00:00Z"
}
```

---

#### `DELETE /api/advanced/alerts/{id}/`

Delete a specific price alert.

**Authentication:** ✅ Required

**Response `204 No Content`**

---

#### `GET /api/advanced/search-history/`

Retrieve the user's search history.

**Authentication:** ✅ Required

**Response `200`:**
```json
[
  {
    "id": 5,
    "query": "wireless headphones",
    "timestamp": "2026-03-13T16:00:00Z"
  }
]
```

---

#### `GET /api/advanced/wishlist/`

List saved wishlist items.

**Authentication:** ✅ Required

**Response `200`:**
```json
[
  {
    "id": 3,
    "product_name": "Sony WH-1000XM5",
    "store": "Amazon",
    "price": "279.99",
    "product_url": "https://www.amazon.com/...",
    "image_url": "https://...",
    "added_at": "2026-03-10T09:00:00Z"
  }
]
```

---

#### `POST /api/advanced/wishlist/`

Add a product to the wishlist.

**Authentication:** ✅ Required

**Request Body:**
```json
{
  "product_name": "Sony WH-1000XM5",
  "store": "Amazon",
  "price": 279.99,
  "product_url": "https://www.amazon.com/dp/..."
}
```

**Response `201`:**
```json
{
  "id": 4,
  "product_name": "Sony WH-1000XM5",
  "store": "Amazon",
  "price": "279.99",
  "added_at": "2026-03-13T17:10:00Z"
}
```

**Error `400` (duplicate):**
```json
{
  "error": "This item is already in your wishlist."
}
```

---

#### `DELETE /api/advanced/wishlist/{id}/`

Remove a wishlist item.

**Authentication:** ✅ Required

**Response `204 No Content`**

---

#### `GET /api/advanced/price-history/`

Price history for chart (advanced endpoint with filtering).

**Authentication:** ✅ Required

**Query Parameters:** `product`, `days`

---

#### `GET /api/advanced/recommendations/`

Get product recommendations based on search history.

**Authentication:** ✅ Required

**Response `200`:**
```json
{
  "recommendations": [
    "Sony WH-1000XM4",
    "Bose QuietComfort 45",
    "Apple AirPods Pro"
  ]
}
```

---

## HTTP Status Code Reference

| Code | Meaning |
|---|---|
| `200` | OK — Successful request |
| `201` | Created — Resource created successfully |
| `202` | Accepted — Async task started |
| `204` | No Content — Deleted successfully |
| `400` | Bad Request — Validation error |
| `401` | Unauthorized — Missing or invalid JWT |
| `403` | Forbidden — Valid JWT but insufficient permissions |
| `404` | Not Found — Resource doesn't exist |
| `429` | Too Many Requests — Rate limit exceeded |
| `500` | Internal Server Error — Unexpected server error |
