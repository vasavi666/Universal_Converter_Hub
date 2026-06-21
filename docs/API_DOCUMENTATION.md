# Universal Converter Hub — API Documentation

> **Base URL:** `http://localhost:8080/api`  
> **Authentication:** Bearer JWT Token  
> **Content-Type:** `application/json`

---

## Standard API Response Format

All endpoints return a consistent response envelope:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... },
  "timestamp": "2026-06-17T22:00:00Z",
  "path": "/api/converters"
}
```

### Error Response

```json
{
  "success": false,
  "message": "Resource not found",
  "data": null,
  "timestamp": "2026-06-17T22:00:00Z",
  "path": "/api/converters/invalid-slug"
}
```

### Paginated Response

```json
{
  "success": true,
  "message": "Fetched successfully",
  "data": {
    "content": [ ... ],
    "page": 0,
    "size": 20,
    "totalElements": 150,
    "totalPages": 8,
    "last": false
  },
  "timestamp": "2026-06-17T22:00:00Z",
  "path": "/api/converters"
}
```

---

## 🔐 Authentication

### POST `/api/auth/register`
Register a new user account.

**Request Body:**
| Field | Type | Validation | Required |
|-------|------|-----------|----------|
| `firstName` | string | 2-50 chars | ✅ |
| `lastName` | string | 2-50 chars | ✅ |
| `username` | string | 3-30 chars, alphanumeric | ✅ |
| `email` | string | Valid email | ✅ |
| `password` | string | 8+ chars, uppercase, lowercase, number, special | ✅ |

**Response:** `201 Created`
```json
{
  "data": {
    "accessToken": "eyJhbGciOi...",
    "refreshToken": "eyJhbGciOi...",
    "tokenType": "Bearer",
    "expiresIn": 900000,
    "user": {
      "id": "uuid",
      "username": "johndoe",
      "email": "john@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "USER"
    }
  }
}
```

---

### POST `/api/auth/login`
Authenticate and receive tokens.

**Request Body:**
| Field | Type | Required |
|-------|------|----------|
| `email` | string | ✅ |
| `password` | string | ✅ |

**Response:** `200 OK` — Same structure as register.

---

### POST `/api/auth/refresh-token`
Refresh an expired access token.

**Request Body:**
| Field | Type | Required |
|-------|------|----------|
| `refreshToken` | string | ✅ |

**Response:** `200 OK`
```json
{
  "data": {
    "accessToken": "eyJhbGciOi...",
    "tokenType": "Bearer",
    "expiresIn": 900000
  }
}
```

---

### POST `/api/auth/forgot-password`
Request a password reset (logs token to console in dev).

**Request Body:**
| Field | Type | Required |
|-------|------|----------|
| `email` | string | ✅ |

**Response:** `200 OK`

---

## 📁 Categories

### GET `/api/categories`
Get all active categories, sorted by `displayOrder`.

**Auth:** None  
**Caching:** Redis (5 min TTL)  
**Response:** `200 OK` — Array of categories.

### GET `/api/categories/{slug}`
Get a single category by slug.

**Auth:** None

### POST `/api/categories` 🔒 Admin
Create a new category.

### PUT `/api/categories/{id}` 🔒 Admin
Update a category.

### DELETE `/api/categories/{id}` 🔒 Admin
Soft-delete a category.

---

## 🔄 Converters

### GET `/api/converters`
Get all converters with pagination and sorting.

**Auth:** None  
**Query Params:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 0 | Page number |
| `size` | int | 20 | Page size (max 100) |
| `sort` | string | `name,asc` | Sort field and direction |

### GET `/api/converters/{slug}`
Get converter by slug. Cached in Redis.

### GET `/api/converters/category/{categorySlug}`
Get converters by category. Paginated.

### GET `/api/converters/popular?limit=10`
Get most popular converters by conversion count.

### GET `/api/converters/trending`
Get trending converters (most conversions in last 7 days).

### POST `/api/converters/{slug}/track`
Increment conversion count for a converter.

### POST `/api/converters` 🔒 Admin
### PUT `/api/converters/{id}` 🔒 Admin
### DELETE `/api/converters/{id}` 🔒 Admin (soft delete)

---

## 🔍 Search

### GET `/api/search?q={query}`
Search across converters, categories, and tools.

**Query Params:**
| Param | Type | Default |
|-------|------|---------|
| `q` | string | — (required) |
| `page` | int | 0 |
| `size` | int | 20 |

---

## ⭐ Favorites

All endpoints require authentication.

### GET `/api/favorites` 🔒
Get user's favorites. Paginated.

### POST `/api/favorites` 🔒
Add a converter to favorites.

**Request Body:**
```json
{ "converterSlug": "kg-to-g" }
```

### GET `/api/favorites/check/{converterSlug}` 🔒
Check if a converter is favorited.

### DELETE `/api/favorites/{converterSlug}` 🔒
Remove from favorites.

---

## 📜 History

All endpoints require authentication.

### GET `/api/history` 🔒
Get conversion history, newest first. Paginated.

### POST `/api/history` 🔒
Save a conversion to history.

**Request Body:**
```json
{
  "converterSlug": "kg-to-g",
  "inputValue": "5",
  "outputValue": "5000",
  "fromUnit": "Kilogram",
  "toUnit": "Gram"
}
```

### DELETE `/api/history/{id}` 🔒
Delete a specific history entry.

### DELETE `/api/history/clear` 🔒
Clear all history for the authenticated user.

---

## 💱 Currency

### GET `/api/currency/rates/{base}`
Get exchange rates for a base currency.

### GET `/api/currency/convert?from={FROM}&to={TO}&amount={AMOUNT}`
Convert between currencies.

### GET `/api/currency/currencies`
Get list of supported currencies.

---

## 📊 Analytics

### POST `/api/analytics/track`
Track a page visit or conversion event.

### GET `/api/analytics/popular?limit=10`
Get most popular converters.

### GET `/api/analytics/dashboard` 🔒 Admin
Get dashboard analytics (total users, visits, conversions, trends).

---

## 👤 User Profile

### GET `/api/user/profile` 🔒
Get authenticated user's profile.

### PUT `/api/user/profile` 🔒
Update profile (firstName, lastName).

### PUT `/api/user/change-password` 🔒
Change password.

---

## 🛡️ Admin

### GET `/api/admin/users` 🔒 Admin
Get all users. Paginated.

### PUT `/api/admin/users/{id}/toggle-status` 🔒 Admin
Enable/disable a user.

### DELETE `/api/admin/users/{id}` 🔒 Admin
Soft-delete a user.

### GET `/api/admin/analytics` 🔒 Admin
Get comprehensive admin analytics.

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Created |
| `204` | No Content (successful delete) |
| `400` | Bad Request (validation errors) |
| `401` | Unauthorized (missing/invalid token) |
| `403` | Forbidden (insufficient role) |
| `404` | Not Found |
| `409` | Conflict (duplicate resource) |
| `429` | Too Many Requests (rate limited) |
| `500` | Internal Server Error |

---

## Rate Limiting

- **Default:** 100 requests per minute per IP
- **Auth endpoints:** 20 requests per minute per IP
- **Response Header:** `X-Rate-Limit-Remaining`
- **When exceeded:** `429 Too Many Requests`

---

## Swagger UI

Interactive API documentation is available at:

- **Swagger UI:** `http://localhost:8080/swagger-ui.html`
- **OpenAPI JSON:** `http://localhost:8080/v3/api-docs`
