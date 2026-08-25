# API Rules

Aturan contract dan konsistensi API. Berlaku saat membuat atau mengubah endpoint.

---

Contract yang konsisten (tanpa versioning):
```
/api/users
/api/users/{id}
/api/recommendations
```

Rules:
- Gunakan HTTP method sesuai semantics (GET, POST, PUT, PATCH, DELETE)
- Gunakan status code yang tepat
- Response format harus konsisten
- Error response harus konsisten
- Validasi seluruh request input
- Jangan gunakan versioning pada path/URL API (gunakan endpoint langsung dan bersih)
- Jangan expose internal implementation detail
- Jangan expose stack trace ke client production

Format error standar:
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User not found"
  }
}
```

Gunakan skill `add-api-endpoint` saat membuat endpoint baru.
