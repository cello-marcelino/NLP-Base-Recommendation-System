# Arsitektur & Desain Sistem — SiReDo v3

## 1. Konsep Desain & Pola Arsitektur

Backend SiReDo mengadopsi **Layered Architecture with Domain Grouping (Monolith-First, Microservice-Ready)** sesuai spesifikasi `rules/architecture.md`.

Setiap level layer terisolasi dengan tanggung jawab tunggal (*Single Responsibility*) dan arah dependensi satu arah yang tegas:

```
Presentation / Routes / CLI Entrypoint
                   │
                   ▼
Controllers (Parsing HTTP/DTO, Validasi, Response Formatting — Tanpa Business Logic)
                   │
                   ▼
Services (Orkestrasi Logika Bisnis Domain, Hybrid NLP Pipeline, System State)
                   │
                   ▼
Repositories (Akses Data Relasional Runtime, Zero N+1 Queries)
                   │
                   ▼
Database / Persistence Storage (SQLite / MySQL)
```

---

## 2. Struktur Repositori Backend (`server/`)

```
server/
├── src/                          # Application Core Layer (Runtime)
│   ├── controllers/              # Presentation Layer: Controller HTTP
│   │   ├── recommendation/       # Controller endpoint rekomendasi
│   │   ├── dosen/                # Controller endpoint katalog dosen
│   │   └── system/               # Controller health, status, config, reload
│   ├── routes/                   # Routing Layer: Blueprint & URL mapping
│   │   ├── recommendation/       # /api/recommendations*
│   │   ├── dosen/                # /api/dosen
│   │   └── system/               # /api/system/*, /health
│   ├── services/                 # Business Logic Layer
│   │   ├── recommendation/       # RecommendationService & BatchService
│   │   ├── dosen/                # DosenService
│   │   ├── nlp/                  # BM25Engine, SBERTEngine, HybridEngine, Preprocessor
│   │   └── system/               # CacheService (Singleton) & ConfigService
│   ├── repositories/             # Data Access Layer
│   │   ├── dosen/                # SQLDosenRepository, ExcelDosenRepository, CompositeDosenRepository
│   │   └── cache/                # CacheRepository (Disk cache .npy & .json)
│   ├── models/                   # Domain Entities
│   │   ├── dosen/                # Dosen, Publikasi, RiwayatBimbingan, RiwayatPengujian
│   │   ├── recommendation/       # RecommendationItem, RecommendationResult
│   │   └── system/               # SystemConfig
│   ├── dtos/                     # Data Transfer Objects
│   │   ├── recommendation/       # SingleRecommendationRequestDTO, BatchRecommendationRequestDTO
│   │   └── system/               # ConfigUpdateDTO
│   ├── middleware/               # Cross-Cutting Middleware
│   │   ├── security_middleware.py # Autentikasi ADMIN_API_KEY
│   │   └── logging_middleware.py  # Request tracing & structured request logging
│   ├── exceptions/               # Application Exceptions
│   │   └── app_exceptions.py     # AppException, ValidationError, NotFoundError, etc.
│   ├── config/                   # Configuration & Infrastructure
│   │   ├── config.py             # Config object dari root .env
│   │   ├── logging_config.py     # Setup structured RotatingFileHandler
│   │   └── response.py           # Standard response envelope

│   ├── cli/                      # SiReDo CLI Framework Handlers
│   └── app.py                    # Application factory (CORS, Error Handlers, Blueprints)
│
├── database/                     # Database Tooling & Lifecycle (Non-Runtime Management)
│   ├── connection/               # Koneksi & lifecycle database murni
│   ├── migrations/               # Schema migrations berversi & migration runner
│   ├── seeders/                  # Seeder data awal & konfigurasi referensi
│   ├── factories/                # Mock data factory untuk automated testing
│   └── importers/                # Pipeline import Excel ke database relasional
│
├── storage/                      # Penyimpanan Runtime
│   ├── cache/                    # Disk cache embedding SBERT (.npy) & KeyBERT (.json)
│   ├── data/                     # Database SQLite (.db), Dataset Excel (.xlsx), config.json
│   └── logs/                     # File log terdedikasi (siredo.log)
│
└── tests/                        # Test Suite
    ├── unit/                     # Pengujian unit logic & engine
    ├── integration/              # Pengujian integrasi API & database
    └── feature/                  # Pengujian flow skenario pengguna
```

---

## 3. Batasan Antar Layer (Layer Boundary Rules)

1. **Controller**:
   - Hanya membaca input request (JSON, form-data, query param).
   - Memetakan input ke DTO atau parameter Service.
   - Mengembalikan respon menggunakan `ResponseFormatter`.
   - Dilarang menjalankan query database langsung atau memproses kalkulasi NLP.

2. **Service**:
   - Mengorkestrasi seluruh business logic.
   - Menggabungkan pipeline NLP leksikal (BM25) dan semantik (SBERT).
   - Memanggil Repository untuk kebutuhan data dan tidak menyentuh driver database mentah.

3. **Repository**:
   - Menangani operasi query ke SQLite atau MySQL.
   - Mengambil relasi (publikasi, bimbingan, pengujian) menggunakan *batch queries* flat untuk mencegah bottleneck N+1 query.
   - Menyediakan metode transaksi atomik untuk persistensi batch.

4. **Database Tooling (`database/`)**:
   - Berdiri independen di luar application runtime.
   - Bertanggung jawab atas migrasi skema, seeding konfigurasi, pembuatan dummy data testing, dan eksekusi pipeline impor file Excel.

---

## 4. Pipeline Natural Language Processing (NLP)

SiReDo mengimplementasikan arsitektur *Hybrid Information Retrieval* yang menggabungkan pencarian leksikal (BM25Okapi) dan pencocokan semantik (Sentence-BERT) dengan pembobotan dinamis dan Explainable AI (XAI).

Tahapan inti pipeline:
1. **Preprocessing & N-Grams**: Case folding, stopword removal, dan pembuatan unigram + bigram.
2. **Sinonim Ekspansi**: Pencocokan ontologi sinonim IT berbasis *longest-first matching*.
3. **Lexical Scoring & Pruning**: Perhitungan BM25Okapi, normalisasi Z-Score Sigmoid, dan pemangkasan kandidat ber-skor nol (*hard pruning*).
4. **Semantic Scoring**: Vektorisasi Sentence-BERT (768-D) dan kalkulasi *Cosine Similarity*.
5. **Adaptive Hybrid Aggregation**: Perhitungan bobot dinamis ($\alpha$ & $\beta$) berdasarkan panjang query dan perangkingan Top-K $O(n + k \log k)$.
6. **Explainable AI (XAI)**: Transparansi irisan kata kunci leksikal dan ekstraksi topik KeyBERT.

> Penjelasan detail formula matematis, kamus ontologi, pseudocode, dan strategi optimasi komputasi didokumentasikan secara mandiri di **[Dokumentasi Pipeline NLP](nlp-pipeline.md)**.


---

## 5. Logging & Observabilitas

- **Dedicated Structured File Log**: `server/storage/logs/siredo.log` dikelola oleh `RotatingFileHandler` (kapasitas 10 MB, 5 file rotasi).
- **Request Tracing**: Setiap request diberikan `X-Request-ID` dan dicatat durasi prosesnya dalam milidetik (`duration=...ms`).
- **Terminal Isolation**: Eksekusi server berjalan silent di background pada lingkungan Windows via `pythonw.exe` dan `CREATE_NO_WINDOW`, terminal bebas digunakan untuk operasi lain.

---

## 6. Arsitektur Frontend (Vue 3 + Pinia)

- **Komponen Presentasi**:
  - `InputForm`: Formulir masukan judul, abstrak, dan pemilihan parameter algoritma.
  - `Stepper`: Indikator progres multi-step pipeline NLP.
  - `DosenCard`: Tampilan kartu hasil peringkat dosen beserta indikator skor dan badge keahlian.
  - `XaiModal`: Modal visualisasi transparansi keputusan rekomendasi.
- **Manajemen State (Pinia)**:
  - `useSystemStore`: Status konektivitas, ketersediaan cache memori, dan katalog dosen.
  - `useRecommendationStore`: State input, riwayat pemrosesan, SSE streaming, dan hasil rekomendasi.
  - `useConfigStore`: State konfigurasi parameter dinamis.
- **Client HTTP**: Axios terkonfigurasi dengan interceptor error unwrapping dan timeout handling.
