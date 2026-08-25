# Logging & Observability

Aturan structured logging dan observability. Berlaku saat menambah logging atau endpoint monitoring.

---

## Logging
Gunakan structured logging. Minimal field: `timestamp`, `level`, `request_id`, `service`, `endpoint`, `status`, `duration`, `error`.

```
request_id=abc123 endpoint=/api/recommendation duration=245ms status=200
```

Rules:
- Jangan log password
- Jangan log API key
- Jangan log token authentication
- Jangan log sensitive user data tanpa alasan
- Gunakan log level yang sesuai
- Error production harus bisa ditelusuri

## Observability
Production system minimal punya: Logs, Metrics, Health Check (`GET /health`). Kalau kompleksitas sistem meningkat, tambahkan Distributed Tracing.
