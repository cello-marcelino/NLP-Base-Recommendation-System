# Desain Sistem & Alur Kerja (System Flow) — SiReDo v3

Dokumentasi ini menyajikan rancangan arsitektur sistem (*System Design*) dan alur kerja data (*System Flow*) secara sistematis, detail, dan komprehensif pada platform **SiReDo v3**.

---

## 1. Topologi Arsitektur Sistem

SiReDo v3 mengusung pola arsitektur **Decoupled Fullstack** dengan pemisahan tegas antara Client Presentation, Backend Application Engine, Multi-Tier Caching, dan Relational Persistence:

```mermaid
graph TD
    subgraph Frontend_Client ["Frontend Client Layer (Vue 3 + Vite)"]
        UI["Vue Components (Views, Stepper, DosenCard, XaiModal)"]
        Pinia["Pinia Stores (SystemStore, RecommendationStore, ConfigStore)"]
        AxiosClient["Axios Client (Interceptors, SSE Stream Handler)"]
        UI <--> Pinia
        Pinia <--> AxiosClient
    end

    subgraph Backend_Server ["Backend Application Layer (Flask 3.0)"]
        Routes["Routes / Blueprints (/api/*)"]
        MW["Middleware (Security Auth, Structured Request Logger)"]
        Controllers["Controllers (DTO Mapping & Response Formatter)"]
        Services["Services (RecommendationService, BatchService, DosenService)"]
        Routes --> MW --> Controllers --> Services
    end

    subgraph Caching_NLP ["Multi-Tier Caching & Hybrid NLP Engine"]
        CacheMem["Tier 1: In-Memory Cache (RAM Singleton CacheService)"]
        NLP_Engine["NLP Engine (Preprocessor, BM25Okapi, SBERT, KeyBERT XAI)"]
        CacheDisk["Tier 2: Persistent Disk Cache (.npy, .json, .pkl)"]
        Services <--> CacheMem
        CacheMem <--> NLP_Engine
        CacheMem <--> CacheDisk
    end

    subgraph Persistence ["Persistence Layer (Database & Storage)"]
        Repo["SQLDosenRepository (Zero N+1 Batch Queries)"]
        DBManager["DatabaseManager (SQLite / MySQL Driver)"]
        DB[(Database: SQLite / MySQL)]
        Services --> Repo --> DBManager --> DB
    end

    AxiosClient <== "HTTP REST / Server-Sent Events" ==> Routes
```

---

## 2. Diagram Alur Kerja Utama Sistem (Core System Flows)

---

### Alur 1: Inisialisasi Server & Asynchronous Cache Warm-Up (Server Startup Flow)

Alur yang dieksekusi saat perintah `python siredo serve` dijalankan:

```mermaid
sequenceDiagram
    autonumber
    actor CLI as Developer / Admin
    participant ServerCmd as CLI Server Manager (server/siredo)
    participant App as Flask Application (Port 5000)
    participant Worker as Background Warm-Up Worker (Thread)
    participant Cache as CacheService (Singleton)
    participant Repo as SQLDosenRepository
    participant DB as SQLite / MySQL
    participant Disk as Storage Cache (.npy / .pkl)

    CLI->>ServerCmd: python siredo serve
    ServerCmd->>Cache: initialize_cache_async()
    ServerCmd->>App: create_app() & Jalankan HTTP Server (Non-blocking)
    Note over App: Port 5000 LANGSUNG TERBUKA (<50ms) & siap melayani /status

    par Background Warm-Up Running
        Worker->>Cache: _warm_up(5 Tahap Real-Time)
        Cache->>Cache: Update State -> warming_up (Progress 0%)
        
        Note over Cache: [1/5] Load Data Dosen
        Cache->>Repo: get_all()
        Repo->>DB: Fetch Dosen + 3 Flat Child Queries (No N+1)
        DB-->>Repo: Dataset Relasional
        Repo-->>Cache: List[Dosen] Entity Models (89 Dosen)

        Note over Cache: [2/5] Preprocessing Teks
        Cache->>Cache: Case folding, stopword removal & bigram

        Note over Cache: [3/5] BM25 Vektoring
        Cache->>Cache: Tokenisasi & Fit BM25Okapi Inverted Index

        Note over Cache: [4/5] SBERT & KeyBERT Embedding
        alt Cache Embeddings Ada di Disk
            Cache->>Disk: np.load(sbert_embeddings.npy) & load(keybert.json)
            Disk-->>Cache: Matriks Vektor 384-D Dense (<0.2s)
        else Cache Belum Ada
            Cache->>Cache: SBERT forward pass encode 89 dosen (Neural Network)
            Cache->>Disk: Simpan sbert_embeddings.npy & keybert_dosen.json
        end

        Note over Cache: [5/5] Simpan Snapshot Disk
        Cache->>Disk: pickle.dump(dosen_data.pkl)
        Cache->>Cache: Set is_ready = True & State = ready (100%)
    and Frontend Client Monitoring
        loop Polling Real-Time (/api/status)
            App-->>CLI: State: warming_up (Tahap 1..5, Progress %, duration_ms)
        end
    end
    Note over App: AI Engine Siap Melayani Query Rekomendasi (Sub-50ms)
```

---

### Alur 2: Rekomendasi Single Proposal (Recommendation Pipeline Flow)

Alur pemrosesan saat mahasiswa mengirimkan judul dan abstrak penelitian:

```mermaid
sequenceDiagram
    autonumber
    actor User as Mahasiswa / Pengguna
    participant View as RecommendationView.vue
    participant Store as useRecommendationStore
    participant API as RecommendationController
    participant Service as RecommendationService
    participant NLP as Preprocessor & Kamus Ontologi
    participant BM25 as BM25 Engine
    participant SBERT as SBERT Engine
    participant Scorer as Hybrid Scorer (Argpartition)

    User->>View: Masukkan Judul, Abstrak, & Klik "Analisis Rekomendasi"
    View->>Store: getRecommendation(payload)
    Store->>API: POST /api/recommendations {judul, abstrak, k_rank}
    API->>API: Validasi Request DTO (Judul/Abstrak tidak boleh kosong)
    API->>Service: get_recommendations(judul, abstrak, k_rank)

    Service->>NLP: clean_text() & remove_stopwords()
    NLP-->>Service: Unigrams + Bigrams Tokens
    Service->>NLP: ekspansi_query_dengan_log()
    NLP-->>Service: Query Ter-ekspansi (Sinonim IT) + Log Ekspansi

    Service->>BM25: get_scores(query_tokens)
    BM25->>BM25: Z-Score Sigmoid Normalization & Hard Reset (Skor 0 -> 0.0)
    BM25-->>Service: Matriks Skor Leksikal & Indeks Lolos Pruning

    Service->>SBERT: encode_query(query_ekspansi)
    SBERT-->>Service: Vektor Query 768-D
    Service->>SBERT: cosine_similarity(query_emb, valid_indices)
    SBERT-->>Service: Matriks Skor Semantik

    Service->>Scorer: compute_adaptive_alpha(token_count)
    Note over Scorer: Query < 15 token: α=0.70 | Query ≥ 15 token: α=0.35
    Service->>Scorer: rank(skor_lex, skor_sem, α, β, k_rank)
    Scorer->>Scorer: Top-K Selection via np.argpartition O(n + k log k)
    Scorer-->>Service: Top-K Dosen Indices & Skor Akhir

    Service->>Service: Enrich XAI Metadata (Irisan Kata + Topik KeyBERT)
    Service-->>API: Result Payload (Recommendations, Metadata, Pipeline Logs)
    API-->>Store: Response 200 OK (ResponseFormatter.success)
    Store-->>View: State Updated -> Render DosenCard & Stepper
    View-->>User: Tampilkan Hasil Rekomendasi Berperingkat
```

---

### Alur 3: Streaming Real-Time Rekomendasi (Server-Sent Events Flow)

Alur eksekusi rekomendasi dengan visualisasi progres tahapan per detik menggunakan SSE:

```mermaid
sequenceDiagram
    autonumber
    actor User as Pengguna
    participant UI as ProgressStepper.vue
    participant API as POST /api/recommendations/stream
    participant Engine as NLP Pipeline Worker

    User->>UI: Submit Form dengan Mode Streaming
    UI->>API: POST /api/recommendations/stream {judul, abstrak}
    Note over API: Inisialisasi HTTP Connection (Content-Type: text/event-stream)

    API-->>UI: data: {"step": 1, "message": "Memulai Text Preprocessing & Cleaning"}
    UI->>UI: Update Stepper -> Tahap 1 Aktif
    Engine->>Engine: Preprocessing & N-Gram Generation

    API-->>UI: data: {"step": 2, "message": "Melakukan Ekspansi Sinonim Ontologi"}
    UI->>UI: Update Stepper -> Tahap 2 Aktif
    Engine->>Engine: Pencocokan Kamus Sinonim IT

    API-->>UI: data: {"step": 3, "message": "Kalkulasi Skor Leksikal BM25"}
    UI->>UI: Update Stepper -> Tahap 3 Aktif
    Engine->>Engine: BM25Okapi & Sigmoid Normalization

    API-->>UI: data: {"step": 4, "message": "Kalkulasi Skor Semantik Sentence-BERT"}
    UI->>UI: Update Stepper -> Tahap 4 Aktif
    Engine->>Engine: SBERT Embedding & Cosine Similarity

    Engine->>Engine: Hybrid Aggregation, Top-K, & XAI Packaging
    API-->>UI: data: {"step": 5, "message": "Selesai", "result": { ... }}
    UI->>UI: Stepper Lengkap -> Render Hasil Rekomendasi
    Note over API: Tutup Koneksi SSE
```

---

### Alur 4: Pemrosesan Batch Proposal & File Spreadsheet

Alur saat memproses banyak proposal penelitian mahasiswa secara massal:

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Akademik / Dosen
    participant Form as BatchView.vue
    participant Controller as RecommendationController
    participant BatchSvc as BatchService
    participant RecSvc as RecommendationService

    alt Input JSON Batch
        Admin->>Form: Submit JSON Array Proposal
        Form->>Controller: POST /api/recommendations/batch {proposals: [...]}
    else Unggah File Excel
        Admin->>Form: Unggah file .xlsx / .xls
        Form->>Controller: POST /api/recommendations/upload (multipart/form-data)
        Controller->>Controller: Ekstraksi kolom id, judul, abstrak via Pandas
    end

    Controller->>BatchSvc: process_batch(proposals, global_k_rank)
    BatchSvc->>BatchSvc: Cek Batas Maksimum (len(proposals) <= MAX_BATCH_SIZE)

    loop Untuk Setiap Proposal
        BatchSvc->>RecSvc: get_recommendations(judul, abstrak, k_rank)
        RecSvc-->>BatchSvc: Hasil Rekomendasi Proposal
    end

    BatchSvc-->>Controller: List of Processed Proposals + Recommendations
    Controller-->>Form: Response 200 OK (meta: {total_processed: N})
    Form-->>Admin: Render Tabel Hasil Rekomendasi Batch (Ekspor Excel siap diunduh)
```

---

### Alur 5: Hot Reload & Pembaruan Konfigurasi (Zero-Downtime Flow)

Alur saat administrator mengubah parameter algoritma atau melakukan re-indexing tanpa mematikan proses server:

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Administrator
    participant Dashboard as AdminDashboardView.vue / CLI
    participant Auth as Security Middleware
    participant SystemCtrl as SystemController
    participant ConfigSvc as ConfigService
    participant Cache as CacheService (Singleton)

    alt Pembaruan Konfigurasi Runtime
        Admin->>Dashboard: Ubah threshold / is_adaptive & Simpan
        Dashboard->>Auth: PATCH /api/system/config (Header: X-API-Key)
        Auth->>Auth: Verifikasi kecocokan ADMIN_API_KEY
        Auth->>SystemCtrl: Delegasi eksekusi request
        SystemCtrl->>ConfigSvc: update_config(payload)
        ConfigSvc->>ConfigSvc: Simpan ke server/storage/data/config.json
        ConfigSvc-->>SystemCtrl: Konfigurasi Baru Tervalidasi
        SystemCtrl-->>Dashboard: Response 200 OK
    else Trigger Async Hot Reload & Re-indexing
        Admin->>Dashboard: Klik "Sync Engine" / POST /api/system/reload
        Dashboard->>Auth: POST /api/system/reload (Header: X-API-Key)
        Auth->>SystemCtrl: Delegasi eksekusi request
        SystemCtrl->>Cache: initialize_cache_async(force_refresh=True)
        Note over Cache: Worker thread menjalankan 5 tahap warm-up di background
        SystemCtrl-->>Dashboard: Response 200 OK (Status: reloading)
        loop Polling Real-Time (450ms)
            Dashboard->>SystemCtrl: GET /api/status
            SystemCtrl-->>Dashboard: warmup_status {current_step, progress_pct, duration_ms}
        end
        Note over Dashboard: Bar status berubah hijau (Ready & Idle) saat 100%
    end
```

---

### Alur 6: Manipulasi Data Dosen (Hybrid Incremental Indexing Flow)

Alur saat administrator melakukan penambahan, pengubahan, atau penghapusan profil dosen tanpa merobohkan seluruh indeks AI:

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Administrator
    participant View as AdminDosenView.vue
    participant Ctrl as AdminDosenController
    participant Repo as SQLDosenRepository
    participant Cache as CacheService
    participant SBERT as SBERTEngine
    participant KeyBERT as KeyBERTExtractor

    Admin->>View: Tambah / Edit / Hapus Profil Dosen
    View->>Ctrl: POST/PUT/DELETE /api/admin/dosen/:id
    Ctrl->>Repo: Simpan perubahan ke Database Relasional
    Repo-->>Ctrl: Entity Dosen Tersimpan

    alt Tambah Dosen Baru (incremental_add)
        Ctrl->>Cache: incremental_add(new_dosen)
        Cache->>Cache: Append ke dosen_list RAM
        Cache->>Cache: Rebuild BM25 Inverted Index (~0.1s)
        Cache->>SBERT: add_single_embedding(new_dosen.text)
        SBERT->>SBERT: np.vstack 1 baris vektor 384-D baru
        Cache->>KeyBERT: Ekstrak 1 topik dosen & append
    else Edit Dosen (incremental_update)
        Ctrl->>Cache: incremental_update(dosen_id, updated_dosen)
        Cache->>Cache: Ganti profil dosen pada index [idx] di RAM
        Cache->>Cache: Rebuild BM25 Inverted Index (~0.1s)
        Cache->>SBERT: update_single_embedding(idx, updated_text)
        SBERT->>SBERT: Timpa baris matrix corpus_embeddings[idx] (Solusi Stale Bug)
        Cache->>KeyBERT: Ekstrak ulang 1 topik dosen pada [idx]
    else Hapus Dosen (incremental_delete)
        Ctrl->>Cache: incremental_delete(dosen_id)
        Cache->>Cache: Pop dosen dari dosen_list RAM
        Cache->>Cache: Rebuild BM25 Inverted Index (~0.1s)
        Cache->>SBERT: delete_single_embedding(idx)
        SBERT->>SBERT: np.delete(corpus_embeddings, idx, axis=0)
        Cache->>KeyBERT: Hapus entri keybert_data[idx]
    end

    Cache->>Cache: Simpan snapshot cache ke disk (.npy & .pkl)
    Cache-->>Ctrl: Update Inkremental Selesai (~0.8 - 3.5s)
    Ctrl-->>View: Response 200 OK (Data Dosen Diperbarui Tanpa Freeze)
```

---

### Alur 7: Manajemen Data & Provisioning Database

Alur provisioning skema dan pemindahan data master:

```mermaid
graph TD
    subgraph Migration_Flow ["1. Alur Migrasi DDL (python siredo db:migrate)"]
        M1["Mulai: python siredo db:migrate"] --> M2["Buka Koneksi via DatabaseManager"]
        M2 --> M3{"MySQL Aktif?"}
        M3 -- Ya --> M4["CREATE DATABASE IF NOT EXISTS db_siredo"]
        M3 -- Tidak / Error --> M5["Fallback ke SQLite lokal"]
        M4 --> M6["Buat Tabel migrations (Tracking)"]
        M5 --> M6
        M6 --> M7["Eksekusi 001_create_dosen_tables.py (up)"]
        M7 --> M8["Catat riwayat ke tabel migrations"]
    end

    subgraph Import_Flow ["2. Alur Impor Dataset (python siredo db:import)"]
        I1["Mulai: python siredo db:import"] --> I2["Baca dataset_profiles_terintegrasi.xlsx"]
        I2 --> I3["DosenImporter.validate_and_transform_row()"]
        I3 --> I4["Parsing Tanda Petik & Titik Koma (Publikasi, Bimbingan, Ujian)"]
        I4 --> I5["SQLDosenRepository.truncate_all()"]
        I5 --> I6["SQLDosenRepository.save_batch() (Atomic Transaction)"]
        I6 --> I7["Commit Database Relasional"]
    end

    subgraph Export_Flow ["3. Alur Ekspor Data (python siredo db:export)"]
        E1["Mulai: python siredo db:export"] --> E2["SQLDosenRepository.get_all()"]
        E2 --> E3["4 Flat Batch Queries (Master Dosen + 3 Child Tables)"]
        E3 --> E4["In-Memory Grouping via defaultdict (Zero N+1)"]
        E4 --> E5["Konversi ke DataFrame Pandas"]
        E5 --> E6["Simpan ke server/storage/data/dataset_profiles_exported.xlsx / .json"]
    end
```

---

## 3. Penanganan Error Terpusat & Ketahanan Sistem (Resilience Flow)

Semua error pada level aplikasi ditangani melalui arsitektur terpusat (*Centralized Error Handling*):

```mermaid
graph TD
    Req["Incoming HTTP Request"] --> Try{"Try Execution"}
    Try -- Sukses --> SuccessResp["ResponseFormatter.success() -> HTTP 200/201"]
    
    Try -- AppException (ValidationError, NotFoundError, dll) --> HandleAppErr["@app.errorhandler(AppException)"]
    HandleAppErr --> AppErrResp["ResponseFormatter.error(code, message) -> HTTP 400/401/403/404/503"]
    
    Try -- Unhandled Exception (RuntimeError, DB Error) --> HandleFatalErr["@app.errorhandler(Exception)"]
    HandleFatalErr --> LogErr["Structured Logger: logger.error(exc_info=True)"]
    LogErr --> FatalErrResp["ResponseFormatter.error('INTERNAL_SERVER_ERROR', status=500)"]

    SuccessResp --> LogMW["Logging Middleware: Log duration_ms & X-Request-ID"]
    AppErrResp --> LogMW
    FatalErrResp --> LogMW
    LogMW --> Client["Kirim Respon JSON ke Klien"]
```

---

## 4. Matriks Ringkasan Latensi Tiap Alur Sistem
 
| Alur Sistem | Rata-Rata Latensi | Karakteristik Operasi | Komponen Utama |
|---|---|---|---|
| **Health Check & Status** | $< 2\text{ ms}$ | Status real-time 5-tahap dari RAM | `GET /api/status` |
| **Katalog Dosen** | $< 10\text{ ms}$ | JSON serialization dari RAM | `GET /api/dosen` |
| **Rekomendasi Single** | $20\text{--}40\text{ ms}$ | In-memory BM25 + SBERT 1 query + SIMD Cosine | `POST /api/recommendations` |
| **Rekomendasi SSE Stream**| Real-time step ($\sim 0.5\text{ s}$) | 5 tahapan event berurutan | `POST /api/recommendations/stream`|
| **Rekomendasi Batch (10 Proposal)** | $200\text{--}350\text{ ms}$ | Iterasi in-memory batch | `POST /api/recommendations/batch` |
| **CRUD Dosen (Inkremental)** | $0.8\text{--}3.5\text{ s}$ | In-memory append/modify + SBERT row update | `POST/PUT/DELETE /api/admin/dosen` |
| **Hot Reload Asinkron** | $< 50\text{ ms}$ (ACK) / $\sim 11\text{ s}$ (BG) | Trigger async worker & live poll status | `POST /api/system/reload` |
| **Warm-Up Startup Server** | $< 50\text{ ms}$ (Port Open) / $\sim 11\text{ s}$ (Background) | Non-blocking Flask startup + background AI warmup | `python siredo serve` |
