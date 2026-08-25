---
name: add-api-endpoint
description: Gunakan skill ini ketika user minta membuat endpoint API baru atau mengubah endpoint yang sudah ada.
---

# Add API Endpoint

## Langkah
1. Tentukan resource dan HTTP method sesuai `rules/api-design.md`
2. Buat route tanpa versioning (misal: `/api/users`, `/api/auth/login`)
3. Controller hanya menangani request/response, business logic taruh di Service (`rules/architecture.md`)
4. Tambahkan validasi request input
5. Format response sukses dan error sesuai konvensi standar proyek
6. Tambahkan pagination kalau response berupa collection besar
7. Tulis API test untuk endpoint ini (`rules/testing.md`)
8. Update dokumentasi API (`rules/documentation.md`)

## Sebelum selesai
Jalankan skill `definition-of-done-check`.
