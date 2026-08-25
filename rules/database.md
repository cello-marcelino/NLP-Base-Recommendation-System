# Database Rules

Aturan migration, seeding, dan query database. Berlaku saat mengubah schema atau menulis query.

---

## Migration
Seluruh perubahan schema harus melalui migration. Jangan mengandalkan perubahan manual pada production database.

## Responsibility
- Migration -> database structure
- Seeder -> initial/reference data
- Factory -> dummy/test data
- Importer -> external data import

Jangan mencampurkan keempat responsibility ini dalam satu file atau proses.

## Query
- Hindari N+1 query
- Gunakan index berdasarkan kebutuhan query
- Jangan ambil seluruh column kalau hanya butuh beberapa column
- Gunakan pagination untuk dataset besar
- Gunakan transaction untuk operasi yang harus atomic
- Hindari query database di dalam loop, gunakan batch query kalau memungkinkan

## Data Integrity
Gunakan database constraint sebagai lapisan perlindungan tambahan: `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `INDEX`. Jangan hanya mengandalkan validation di application layer.

Gunakan skill `database-migration` saat membuat migration baru.
