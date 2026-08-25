---
name: write-tests
description: Gunakan skill ini ketika user minta menulis test, menambah test coverage, atau setelah bug ditemukan dan butuh regression test.
---

# Write Tests

## Langkah
1. Tentukan level test yang sesuai: unit, integration, API, atau end-to-end (`rules/testing.md`)
2. Tulis test dengan pola: given input, execute behavior, verify hasil
3. Uji lewat public interface, hindari bergantung pada implementation detail
4. Kalau ini regression test dari bug, tulis dulu test yang gagal sebelum fix diterapkan, lalu pastikan lolos setelah fix
5. Pastikan test deterministic, tidak flaky

## Larangan
Jangan menghapus atau skip test yang sudah ada hanya supaya build menjadi hijau.
