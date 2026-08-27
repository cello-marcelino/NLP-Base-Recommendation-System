# Desain Database & Data Management Tooling — SiReDo v3

Dokumentasi ini menjelaskan desain skema database relasional, konstrain integritas data, dan arsitektur *database tooling* (koneksi, migrasi, seeder, factory, dan importer) pada sistem SiReDo v3 sesuai `rules/database.md`.

---

## 1. Diagram Relasi Entitas (Entity-Relationship Diagram)

Sistem menggunakan skema relasional ter-normalisasi yang memisahkan entitas profil dosen dari data riwayat akademik:

```
┌──────────────────────────────────────────────┐
│                    dosen                     │
├──────────────────────────────────────────────┤
│ PK  id               INT / INTEGER           │
│ UK  nidn             VARCHAR(50) / TEXT      │
│     nama             VARCHAR(255) / TEXT     │
│     program_studi    VARCHAR(150) / TEXT     │
│     bidang_keahlian  TEXT                    │
│     pendidikan       TEXT                    │
│     created_at       TIMESTAMP               │
│     updated_at       TIMESTAMP               │
└──────┬──────────────────────┬──────────────┬─┘
       │ 1:N                  │ 1:N          │ 1:N
       ▼                      ▼              ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│    publikasi     │  │riwayat_bimbingan │  │riwayat_pengujian │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ PK id            │  │ PK id            │  │ PK id            │
│ FK dosen_id (NN) │  │ FK dosen_id (NN) │  │ FK dosen_id (NN) │
│    judul (NN)    │  │    judul_ta (NN) │  │    judul_sidang  │
│    tahun         │  │    tahun         │  │    tahun         │
│    penerbit      │  │    peran         │  │    peran         │
│    created_at    │  │    created_at    │  │    created_at    │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## 2. Definisi Skema Tabel & Konstrain

### A. Tabel `dosen` (Master Profil Dosen)
| Kolom | Tipe SQLite | Tipe MySQL | Konstrain & Deskripsi |
|---|---|---|---|
| `id` | `INTEGER` | `INT` | `PRIMARY KEY AUTOINCREMENT` |
| `nidn` | `TEXT` | `VARCHAR(50)` | `UNIQUE`, Nomor Induk Dosen Nasional |
| `nama` | `TEXT` | `VARCHAR(255)` | `NOT NULL`, Nama lengkap beserta gelar |
| `program_studi` | `TEXT` | `VARCHAR(150)` | `NOT NULL`, Program studi dosen |
| `bidang_keahlian`| `TEXT` | `TEXT` | Bidang keahlian penelitian |
| `pendidikan` | `TEXT` | `TEXT` | Riwayat pendidikan terakhir |
| `created_at` | `TIMESTAMP` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |
| `updated_at` | `TIMESTAMP` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |

### B. Tabel `publikasi` (Child Riwayat Jurnal / Karya Ilmiah)
| Kolom | Tipe SQLite | Tipe MySQL | Konstrain & Deskripsi |
|---|---|---|---|
| `id` | `INTEGER` | `INT` | `PRIMARY KEY AUTOINCREMENT` |
| `dosen_id` | `INTEGER` | `INT` | `FOREIGN KEY REFERENCES dosen(id) ON DELETE CASCADE`, `INDEX` |
| `judul` | `TEXT` | `TEXT` | `NOT NULL`, Judul publikasi atau karya ilmiah |
| `tahun` | `INTEGER` | `INT NULL` | Tahun rilis publikasi |
| `penerbit` | `TEXT` | `VARCHAR(255)` | Nama jurnal atau konferensi penerbit |
| `created_at` | `TIMESTAMP` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |

### C. Tabel `riwayat_bimbingan` (Child Riwayat Tugas Akhir / Skripsi)
| Kolom | Tipe SQLite | Tipe MySQL | Konstrain & Deskripsi |
|---|---|---|---|
| `id` | `INTEGER` | `INT` | `PRIMARY KEY AUTOINCREMENT` |
| `dosen_id` | `INTEGER` | `INT` | `FOREIGN KEY REFERENCES dosen(id) ON DELETE CASCADE`, `INDEX` |
| `judul_tugas_akhir` | `TEXT` | `TEXT` | `NOT NULL`, Judul skripsi/tugas akhir mahasiswa |
| `tahun` | `INTEGER` | `INT NULL` | Tahun kelulusan bimbingan |
| `peran` | `TEXT` | `VARCHAR(100)` | Default `'Pembimbing'` |
| `created_at` | `TIMESTAMP` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |

### D. Tabel `riwayat_pengujian` (Child Riwayat Sidang Skripsi)
| Kolom | Tipe SQLite | Tipe MySQL | Konstrain & Deskripsi |
|---|---|---|---|
| `id` | `INTEGER` | `INT` | `PRIMARY KEY AUTOINCREMENT` |
| `dosen_id` | `INTEGER` | `INT` | `FOREIGN KEY REFERENCES dosen(id) ON DELETE CASCADE`, `INDEX` |
| `judul_sidang` | `TEXT` | `TEXT` | `NOT NULL`, Judul sidang tugas akhir mahasiswa |
| `tahun` | `INTEGER` | `INT NULL` | Tahun pelaksanaan ujian |
| `peran` | `TEXT` | `VARCHAR(100)` | Default `'Penguji'` |
| `created_at` | `TIMESTAMP` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |

### E. Tabel `migrations` (Tracking Migrasi Skema)
| Kolom | Tipe Data | Deskripsi |
|---|---|---|
| `id` | `INTEGER / INT` | `PRIMARY KEY AUTOINCREMENT` |
| `migration` | `TEXT / VARCHAR(255)` | `UNIQUE`, Nama file migrasi yang telah dieksekusi |
| `applied_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |

---

## 3. Arsitektur Database Tooling (`server/database/`)

Database management dipisahkan dari application runtime untuk menjaga isolasi boundary sistem yang jelas:

```
Runtime Application                  Database Management Tooling
───────────────────                  ───────────────────────────
Controller                           Migrations  (001_create_dosen_tables.py)
    ↓                                Seeders     (database_seeder.py)
Service                              Factories   (dosen_factory.py)
    ↓                                Importers   (dosen_importer.py)
Repository (SQLDosenRepository)
    ↓
Database Connection (DatabaseManager)
    ↓
Database Driver (SQLite / MySQL)
```

### Tanggung Jawab Komponen:

| Komponen | Lokasi Direktori | Tanggung Jawab |
|---|---|---|
| **Connection** | `server/database/connection/` | Mengelola siklus koneksi SQLite/MySQL, foreign key pragma, dan graceful fallback |
| **Migrations** | `server/database/migrations/` | Membangun dan mengubah struktur skema database secara berversi & inkremental (`up` & `down`) |
| **Seeders** | `server/database/seeders/` | Memasukkan data awal/statis dan inisialisasi default configuration (`config.json`) |
| **Factories** | `server/database/factories/` | Membangkitkan dummy data realistis untuk pengujian otomatis dan load testing |
| **Importers** | `server/database/importers/` | Menjalankan pipeline ETL dari dataset Excel ke tabel relasional via validasi dan delegasi ke Repository |

---

## 4. Pipeline Import Data (Excel to Database)

Alur impor data master profil dosen dari file spreadsheet `server/storage/data/dataset_profiles_terintegrasi.xlsx`:

```
File Excel (.xlsx)
       │
       ▼
DosenImporter
       │ 1. Parsing Quoted Items & Semicolon Separators
       │ 2. Sanitasi & Validasi Kolom Wajib (Nama, NIDN, Prodi)
       ▼
List of Validated Records
       │
       ▼
SQLDosenRepository.save_batch()
       │ Atomic Transaction (BEGIN TRANSACTION -> INSERT Master & Relations -> COMMIT)
       ▼
Database Relasional (SQLite / MySQL)
```

---

## 5. Optimalisasi Query (Zero N+1 Query)

Pada proses pembacaan seluruh data dosen (`SQLDosenRepository.get_all()`), sistem menghindari eksekusi query relasi di dalam loop (N+1 query) dengan menerapkan teknik **Batch In-Memory Grouping**:

1. **Query 1**: Ambil seluruh data master dosen:
   ```sql
   SELECT id, nidn, nama, program_studi, bidang_keahlian, pendidikan FROM dosen ORDER BY id ASC;
   ```
2. **Query 2**: Ambil seluruh data publikasi dalam 1 query flat:
   ```sql
   SELECT dosen_id, judul FROM publikasi ORDER BY id ASC;
   ```
3. **Query 3**: Ambil seluruh riwayat bimbingan dalam 1 query flat:
   ```sql
   SELECT dosen_id, judul_tugas_akhir FROM riwayat_bimbingan ORDER BY id ASC;
   ```
4. **Query 4**: Ambil seluruh riwayat pengujian dalam 1 query flat:
   ```sql
   SELECT dosen_id, judul_sidang FROM riwayat_pengujian ORDER BY id ASC;
   ```
5. **Grouping**: Memetakan child records ke master dosen secara instan di memori menggunakan `collections.defaultdict(list)`.
   *Total query tetap konstan = 4 query, terlepas dari berapapun jumlah dosen di database.*

---

## 6. Dukungan Dual-Driver (SQLite & MySQL)

Sistem SiReDo mendukung dua driver database relasional yang dapat diganti sewaktu-waktu melalui variabel environment `DB_DRIVER` pada file `.env`:
- **SQLite** (`DB_DRIVER=sqlite`): Zero-setup, disimpan di `server/database/siredo.db`. Cocok untuk development lokal dan pengujian.
- **MySQL** (`DB_DRIVER=mysql`): Menghubungkan ke MySQL server (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_DATABASE`).

- **Resilience Fallback**: Jika konfigurasi diatur ke MySQL namun server MySQL sedang tidak aktif, sistem secara otomatis mengalihkan koneksi ke SQLite lokal agar server tetap dapat beroperasi normal.
