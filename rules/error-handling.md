# Error Handling

Aturan penanganan error. Selalu berlaku di semua kode.

---

Error harus ditangani secara eksplisit. Jangan silently ignore error.
```python
# Salah
try:
    ...
except:
    pass
```

Gunakan kategori error yang jelas: `ValidationError`, `AuthenticationError`, `AuthorizationError`, `NotFoundError`, `DatabaseError`, `ExternalServiceError`, `InternalServerError`.

Gunakan centralized error handling kalau framework mendukung.
