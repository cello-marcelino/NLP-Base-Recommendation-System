---
description: Aturan struktur database tooling (connection, migration, seeder, factory, importer) dan query. Berlaku saat mengubah schema, koneksi, importer, atau menulis query.
---

# Database Rules

## Folder Structure

`database/` terpisah dari `app/`. Model tetap di `app/models/`, bukan di `database/`, karena Model adalah domain/persistence representation (bagian dari application layer), sedangkan `database/` isinya tooling dan lifecycle database.

```
app/
├── controllers/
├── services/
├── repositories/
├── models/
└── schemas/

database/
├── connection/
│   └── database.py
├── migrations/
│   ├── 001_create_dosen.py
│   ├── 002_create_mahasiswa.py
│   └── 003_create_thesis.py
├── seeders/
│   └── database_seeder.py
├── factories/
│   └── dosen_factory.py
└── importers/
    └── dosen_importer.py
```

## Repository vs Database Management (Independent)

Jangan masukkan `migrations`, `seeders`, `factories`, atau `importers` ke dalam `repositories/`. Keduanya independent, tapi boleh saling menggunakan dependency.

```
Application                          Database Management
────────────                          ────────────────────
Controller                            Migrations
    ↓                                 Seeders
Service / Use Case                    Factories
    ↓                                 Importers
Repository
    ↓
Persistence
    ↓
Database
```

Prinsipnya:
```
repositories/  = akses data saat aplikasi berjalan (runtime)
database/      = management & provisioning database (bukan runtime)
```

Jangan sebut `migrations`, `seeders`, `factories`, `importers` sebagai "database layer" seolah bagian dari Repository Layer. Sebutan yang lebih tepat: **database tooling / data management**. Ini yang bikin boundary arsitekturnya jelas.

| Komponen | Tanggung jawab | Runtime? |
|---|---|---|
| Repository | CRUD/query data aplikasi | Ya |
| Model | Representasi entity/database | Ya |
| Migration | Membentuk/mengubah schema | Tidak langsung |
| Seeder | Memasukkan initial/reference data | Tidak |
| Factory | Membuat dummy/test data | Tidak |
| Importer | Import data eksternal | Biasanya command/job |

## Importer Boleh Pakai Repository, Tapi Bukan Repository

Importer dan Seeder boleh memanggil Repository untuk menyimpan data, tapi mereka bukan bagian dari Repository:

```
Importer    ───────→ Repository ───────→ Database
Seeder      ───────→ Repository ───────→ Database
Application ───────→ Repository ───────→ Database
```

Contoh alur importer:
```
Excel -> DosenImporter -> Validation -> DosenRepository -> Database
```

```python
class DosenImporter:

    def import_file(self, file):
        rows = read_excel(file)

        for row in rows:
            dosen = validate(row)
            self.repository.save(dosen)
```

## Responsibility (5 komponen, jangan dicampur satu sama lain)

| Folder | Tugas |
|---|---|
| `connection/` | Koneksi dan lifecycle database saja, jangan taruh query bisnis di sini |
| `migrations/` | Struktur schema, versioned dan incremental |
| `seeders/` | Data awal/statis (roles, admin, default config) |
| `factories/` | Data dummy untuk testing/load testing |
| `importers/` | Data nyata dari sumber eksternal (Excel, dsb) |

## Connection
Hanya mengurus koneksi dan lifecycle, tidak boleh berisi query bisnis.
```python
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
```

## Migration
Seluruh perubahan schema harus melalui migration, bersifat versioned dan incremental:
```
v1 -> migration 001 -> v2 -> migration 002 -> v3
```
Jangan mengubah migration lama yang sudah dipakai di production, buat migration baru.

## Seeder vs Factory vs Importer
Ketiganya sering tertukar, padahal tujuannya beda:
- **Seeder**: data awal/statis yang memang harus ada (default role, default admin), bukan tempat utama untuk data production dari Excel
- **Factory**: menghasilkan data dummy dalam jumlah banyak untuk testing (`DosenFactory.create()`)
- **Importer**: memasukkan data nyata dari sumber eksternal lewat pipeline dengan validasi (lihat diagram di atas)

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