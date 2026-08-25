# Spesifikasi Kontrak API — SiReDo v3

Seluruh endpoint REST API menggunakan format JSON tanpa versioning pada path URL (`rules/api-design.md`).

---

## 1. Response Envelope Standar

### Sukses
```json
{
  "success": true,
  "message": "Pesan deskriptif",
  "data": { ... },
  "meta": { ... }
}
```

### Error
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Deskripsi kesalahan",
    "details": { ... }
  }
}
```

---

## 2. Ringkasan Endpoint

| Method | Endpoint | Deskripsi | Autentikasi |
|---|---|---|---|
| `GET` | `/health` | Health check ketersediaan sistem | Publik |
| `GET` | `/api/system/status` | Status server, kesiapan cache, dan jumlah dosen | Publik |
| `GET` | `/api/system/config` | Mengambil parameter konfigurasi runtime | Publik |
| `PATCH` | `/api/system/config` | Memperbarui parameter konfigurasi runtime (whitelist) | `X-API-Key` |
| `GET` | `/api/dosen` | Mengambil daftar seluruh profil dosen | Publik |
| `POST` | `/api/recommendations` | Analisis rekomendasi single topik proposal | Publik |
| `POST` | `/api/recommendations/batch` | Pemrosesan batch rekomendasi (max 100) | Publik |
| `POST` | `/api/recommendations/upload`| Pemrosesan batch rekomendasi via file Excel | Publik |
| `POST` | `/api/recommendations/stream`| Analisis rekomendasi via Server-Sent Events (SSE) | Publik |
