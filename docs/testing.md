# Panduan & Strategi Pengujian (Testing Layer) — SiReDo v3

Dokumentasi ini menjelaskan hierarki pengujian (*testing hierarchy*), isolasi lingkungan uji, struktur test suite, dan standar penulisan tes otomatis pada sistem SiReDo v3 sesuai dengan pedoman `rules/testing.md`.

---

## 1. Hierarki & Piramida Pengujian

Sistem mengadopsi hierarki pengujian 3 lapis untuk menjamin correctness, keandalan, dan stabilitas regresi:

```
                  ┌────────────────────────┐
                  │      Feature Test      │  ◄── End-to-End User Flow (Katalog -> Input -> Hasil)
                  └───────────┬────────────┘
                              │
                 ┌────────────┴────────────┐
                 │    Integration Test     │  ◄── API Endpoints & Multi-Layer Contracts
                 └────────────┬────────────┘
                              │
             ┌────────────────┴────────────────┐
             │            Unit Test            │  ◄── NLP Engines, Services, Tooling & Models
             └─────────────────────────────────┘
```

| Level | Direktori | Tanggung Jawab & Cakupan | Sifat |
|---|---|---|---|
| **Feature Test** | `server/tests/feature/` | Menguji alur fungsional end-to-end dari sudut pandang pengguna (Health check $\rightarrow$ Akses katalog dosen $\rightarrow$ Rekomendasi) | Realistis & Komprehensif |
| **Integration Test** | `server/tests/integration/` | Menguji kontrak publik HTTP REST API, validasi request/response envelope, status code, dan penanganan error | Black-box API Contract |
| **Unit Test** | `server/tests/unit/` | Menguji logika bisnis terkecil (Preprocessing, ekspansi ontologi, BM25, Hybrid Scorer, Factory, Importer, Migrasi skema) | Terisolasi & Cepat |

---

## 2. Struktur Repositori Pengujian (`server/tests/`)

```
server/tests/
├── conftest.py                   # Global pytest fixtures, mock data in-memory, isolasi tmp_path
├── feature/                      # Feature & End-to-End Tests
│   └── test_recommendation_flow.py # Skenario utuh alur rekomendasi sistem
├── integration/                  # API & Component Integration Tests
│   ├── test_recommendation_api.py # Kontrak endpoint single, batch, dan limit validation
│   └── test_system_api.py         # Kontrak endpoint health, status, config, dan autentikasi
└── unit/                         # Unit Tests
    ├── test_bm25_engine.py       # Fitting & normalisasi skor leksikal BM25
    ├── test_config_service.py    # Validasi whitelist konfigurasi runtime
    ├── test_dosen_factory.py     # Pembangkitan dummy model dosen
    ├── test_dosen_importer.py    # Pipeline ekstraksi & transformasi data Excel
    ├── test_hybrid_scorer.py     # Pembobotan adaptif, perangkingan, dan XAI enrichment
    ├── test_migrations.py        # Lifecycle DDL migrasi up/down & tracking
    └── test_preprocessor.py      # Case fold, regex, stopword, n-gram, & ekspansi
```

---

## 3. Isolasi Lingkungan Uji & Determinisme

Untuk memastikan seluruh pengujian bersifat **deterministik**, **bebas efek samping (*side-effect free*)**, dan **tidak meninggalkan file sampah**:

1. **Penyimpanan Virtual Dinamis (`tmp_path`)**:
   Pengujian tidak menggunakan folder fisik statis, melainkan fixture bawaan pytest `tmp_path`. Direktori storage sementara (`storage/cache/`, `storage/data/`, `storage/logs/`) dibuat di memori temporary OS dan otomatis dimusnahkan setelah pengujian selesai.
2. **In-Memory NLP State Fixture**:
   Model kalkulasi vektor SBERT dan KeyBERT pada `conftest.py` diinisialisasi menggunakan matriks tensor deterministik berdimensi 384-D, sehingga pengujian berjalan instan tanpa perlu mengunduh bobot neural network dari internet.
3. **Database In-Memory**:
   Pengujian DDL skema migrasi dan SQLite repository menggunakan database in-memory (`:memory:`).

---

## 4. Katalog Kasus Uji Eksisting (34 Test Cases)

### A. Feature Tests
| File | Nama Fungsi Test | Verifikasi Perilaku |
|---|---|---|
| `test_recommendation_flow.py` | `test_full_recommendation_feature_flow` | Memverifikasi alur penuh: cek kesehatan server $\rightarrow$ ambil daftar dosen $\rightarrow$ submit proposal $\rightarrow$ terima rekomendasi berperingkat + skor + XAI. |

### B. Integration Tests (API Contract)
| File | Nama Fungsi Test | Verifikasi Perilaku |
|---|---|---|
| `test_recommendation_api.py` | `test_single_recommendation_success` | Response 200 dengan struktur `data.recommendations`, `metadata`, dan `pipeline`. |
| `test_recommendation_api.py` | `test_single_recommendation_empty_input` | Response 400 `VALIDATION_ERROR` jika judul dan abstrak kosong. |
| `test_recommendation_api.py` | `test_batch_recommendation_success` | Response 200 untuk pemrosesan proposal ganda. |
| `test_recommendation_api.py` | `test_batch_recommendation_limit_exceeded` | Response 400 `BATCH_LIMIT_EXCEEDED` jika jumlah proposal melebihi batas `MAX_BATCH_SIZE`. |
| `test_recommendation_top5_json.py` | `test_collect_top5_recommendations_for_all_theses_json` | Mengumpulkan rekomendasi Top-5 lengkap per topik tesis hardcode dan memvalidasi struktur JSON utuh. |
| `test_recommendation_top5_json.py` | `test_batch_collect_top5_recommendations_json` | Memproses seluruh dataset tesis hardcoded via batch endpoint dan memverifikasi kelengkapan Top-5. |
| `test_system_api.py` | `test_get_health` | Endpoint `GET /health` mengembalikan status kesehatan sistem. |
| `test_system_api.py` | `test_get_system_status` | Endpoint `GET /api/system/status` mengembalikan status online dan jumlah dosen. |
| `test_system_api.py` | `test_get_dosen_list` | Endpoint `GET /api/dosen` mengembalikan katalog dosen lengkap. |
| `test_system_api.py` | `test_get_and_patch_config` | Endpoint `GET /api/system/config` dan `PATCH /api/system/config` dengan header `X-API-Key` valid. |
| `test_system_api.py` | `test_patch_config_unauthorized` | Response 401 `UNAUTHENTICATED` saat `PATCH /api/system/config` dengan API Key salah. |


### C. Unit Tests
| File | Nama Fungsi Test | Verifikasi Perilaku |
|---|---|---|
| `test_bm25_engine.py` | `test_bm25_fit_and_get_scores` | Kalkulasi skor relevansi leksikal dan pemangkasan skor nol (*hard reset* ke $0.0$). |
| `test_bm25_engine.py` | `test_bm25_empty_query` | Query kosong mengembalikan array kosong tanpa error. |
| `test_config_service.py` | `test_validate_and_sanitize_valid_config` | Validasi payload konfigurasi yang benar. |
| `test_config_service.py` | `test_validate_and_sanitize_discards_unknown_keys` | Pembersihan (*sanitization*) key asing yang tidak terdaftar di whitelist. |
| `test_config_service.py` | `test_validate_and_sanitize_invalid_values` | Pelemparan `ValidationError` pada nilai threshold / alpha di luar batas. |
| `test_dosen_factory.py` | `test_dosen_factory_make_dosen` | Pembuatan satu objek entity Dosen dummy valid. |
| `test_dosen_factory.py` | `test_dosen_factory_make_batch` | Pembuatan batch $N$ data dosen dengan NIDN unik. |
| `test_dosen_factory.py` | `test_dosen_factory_make_dict_record` | Pembuatan representasi dictionary format importer. |
| `test_dosen_importer.py` | `test_parse_quoted_items` | Parsing teks publikasi ber-tanda petik ganda. |
| `test_dosen_importer.py` | `test_parse_quoted_items_empty_and_nan` | Penanganan data kosong, `-`, dan string `nan`. |
| `test_dosen_importer.py` | `test_validate_and_transform_row` | Transformasi satu baris pandas Series menjadi dictionary terstruktur. |
| `test_hybrid_scorer.py` | `test_compute_adaptive_alpha_short_query` | Query $< 15$ token menghasilkan $\alpha=0.70$ (Mode Keyword). |
| `test_hybrid_scorer.py` | `test_compute_adaptive_alpha_long_query` | Query $\ge 15$ token menghasilkan $\alpha=0.35$ (Mode Abstrak). |
| `test_hybrid_scorer.py` | `test_hybrid_rank` | Perangkingan Top-K mengurutkan skor tertinggi secara benar. |
| `test_hybrid_scorer.py` | `test_enrich_xai` | Ekstraksi irisan kata kunci leksikal dan topik semantik KeyBERT. |
| `test_migrations.py` | `test_migration_001_sqlite_lifecycle` | Eksekusi DDL `up()` (buat tabel) dan `down()` (drop tabel). |
| `test_migrations.py` | `test_migrations_tracking_table` | Pencatatan riwayat migrasi pada tabel `migrations`. |
| `test_preprocessor.py` | `test_clean_text` | Case folding dan pembersihan tanda baca. |
| `test_preprocessor.py` | `test_remove_stopwords` | Penyaringan stopwords bahasa Indonesia. |
| `test_preprocessor.py` | `test_create_ngrams` | Pembentukan unigram dan bigram (`kata1_kata2`). |
| `test_preprocessor.py` | `test_ekspansi_query_dengan_log` | Pencocokan sinonim ontologi dan pencatatan log ekspansi. |
| `test_preprocessor.py` | `test_build_corpus_text` | Pembobotan repetisi korpus teks dosen. |

---

## 5. Cara Menjalankan Automated Test

### A. Menjalankan Seluruh Test Suite
```powershell
& "server/.venv/Scripts/pytest.exe" server/tests/ -v
```

### B. Menjalankan Berdasarkan Level Pengujian
```powershell
# Hanya Unit Tests
& "server/.venv/Scripts/pytest.exe" server/tests/unit/ -v

# Hanya Integration Tests
& "server/.venv/Scripts/pytest.exe" server/tests/integration/ -v

# Hanya Feature Tests
& "server/.venv/Scripts/pytest.exe" server/tests/feature/ -v
```

### C. Menjalankan File atau Fungsi Tes Tertentu
```powershell
# Menjalankan spesifik file
& "server/.venv/Scripts/pytest.exe" server/tests/unit/test_hybrid_scorer.py -v

# Menjalankan spesifik fungsi test
& "server/.venv/Scripts/pytest.exe" server/tests/unit/test_hybrid_scorer.py -k "test_compute_adaptive_alpha_short_query" -v
```

---

## 6. Prinsip & Standar Penulisan Tes Baru

Saat menambahkan fitur baru atau memperbaiki bug (*regression testing*), patuhi aturan berikut:

1. **Uji Behavior, Bukan Detail Implementasi**:
   Gunakan pola *Given - When - Then*:
   ```python
   # Given: Kondisi awal atau input data
   payload = {"judul": "AI", "abstrak": "Machine Learning"}

   # When: Eksekusi fungsi publik / request endpoint
   response = client.post('/api/recommendations', json=payload)

   # Then: Verifikasi hasil keluaran (status code & payload contracts)
   assert response.status_code == 200
   assert response.get_json()["success"] is True
   ```
2. **Deterministic & Network Independent**:
   Tes dilarang bergantung pada jaringan eksternal (misal mengunduh model dari HuggingFace atau memanggil server eksternal). Semua model dan state harus di-mock atau diinisialisasi melalui fixture.
3. **Regression Test untuk Setiap Bug**:
   Setiap kali menemukan bug pada algoritma atau endpoint, tulis minimal 1 unit/integration test baru untuk mencegah terulangnya regresi di masa depan.
