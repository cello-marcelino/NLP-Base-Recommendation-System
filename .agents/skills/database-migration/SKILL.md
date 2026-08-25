---
name: database-migration
description: Gunakan skill ini ketika user minta membuat tabel baru, mengubah struktur tabel, atau menyebut kata migration, migrasi, atau schema database.
---

# Database Migration

## Langkah
1. Cek struktur tabel terkait yang sudah ada
2. Buat file migration baru, jangan edit migration lama yang sudah pernah berjalan
3. Definisikan constraint yang sesuai: PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, INDEX (`rules/database.md`)
4. Pisahkan dari seeder, factory, dan importer, jangan dicampur
5. Jalankan migration di environment lokal untuk verifikasi
6. Jangan jalankan migration langsung ke production, ikuti `rules/security.md`

## Catatan
Kalau migration menyentuh tabel data user, wajib konfirmasi ke user dulu sebelum lanjut.
