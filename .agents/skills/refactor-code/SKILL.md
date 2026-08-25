---
name: refactor-code
description: Gunakan skill ini ketika user minta merapikan, menyederhanakan, atau restrukturisasi kode yang sudah ada.
---

# Refactor Code

## Langkah
1. Understand: pahami behavior dan dependency dari kode yang akan diubah
2. Test: pastikan ada test yang meng-cover behavior saat ini, tulis dulu kalau belum ada
3. Refactor: lakukan perubahan secara incremental, jangan large-scale sekaligus
4. Run test: pastikan semua test masih lolos
5. Review: jelaskan ke user apa yang berubah dan kenapa

## Kalau menemukan technical debt yang tidak bisa langsung dibereskan
Catat sesuai format di `rules/refactoring-and-tech-debt.md`, jangan disembunyikan atau diabaikan begitu saja.
