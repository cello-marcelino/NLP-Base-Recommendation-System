# Code Style

Aturan readability, naming, dan struktur function. Berlaku untuk semua kode yang ditulis atau diubah.

---

## Readability First
Kode harus mudah dibaca sebelum dioptimalkan.
```python
user = find_user(user_id)
validate_user(user)
recommend(user)
```
Ini lebih baik daripada satu function yang melakukan banyak operasi sekaligus.

## Naming
Gunakan nama yang descriptive, consistent, domain-specific, dan tidak ambigu.

Hindari: `data`, `temp`, `obj`, `x`, `helper`, `manager`, `utils`, `process`, kecuali nama itu memang menjelaskan tujuan sebenarnya.

Prefer: `user_repository`, `recommendation_service`, `thesis_embedding`, `examiner_score`.

## Function Size
Function harus punya satu tujuan yang jelas. Kalau sebuah function mulai melakukan validation, database access, calculation, formatting, dan logging secara bersamaan, evaluasi kemungkinan pemisahan responsibility. Tidak ada batas jumlah baris absolut, gunakan complexity dan readability sebagai indikator.

## Avoid Hidden Side Effects
Function sebaiknya tidak melakukan perubahan state yang tidak terlihat dari namanya. `getUser()` yang diam-diam update `last_login`, menulis ke database, dan mengirim notifikasi itu menyesatkan. Gunakan nama yang menjelaskan side effect-nya.

## Avoid Magic Values
```python
# Salah
if score > 0.75:

# Benar
RECOMMENDATION_THRESHOLD = 0.75
```
Configuration yang bisa berubah sebaiknya tidak hardcoded, lihat `rules/configuration.md`.
