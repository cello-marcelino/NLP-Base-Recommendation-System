# Security Rules

Aturan keamanan. Selalu berlaku, prioritas tertinggi kalau bentrok dengan rule lain.

---

Minimal cakupan: Input Validation, Authentication, Authorization, Password Hashing, HTTPS, Secret Management, Rate Limiting, CORS, SQL Injection Protection, XSS Protection, CSRF Protection, Dependency Security.

- Authentication menjawab: siapa kamu
- Authorization menjawab: apa yang boleh kamu lakukan
- Jangan anggap authenticated user otomatis punya semua permission

Tambahan:
- Jangan pernah menulis, mengubah, atau menampilkan isi file `.env` atau credential apa pun
- Jangan hardcode API key, password, atau token, termasuk di contoh atau dummy data
- Jangan ubah migration yang sudah berjalan di production
- Aksi berikut wajib konfirmasi user dulu sebelum dijalankan: menghapus data, drop table, force push, deploy ke production
