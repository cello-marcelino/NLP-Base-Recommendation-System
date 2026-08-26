# Arsitektur & Desain Sistem — SiReDo v3

## 1. Konsep Desain
SiReDo v3 dirancang dengan arsitektur **Decoupled Fullstack** yang memisahkan backend engine (*server*) dari frontend presentation (*web*), dilengkapi antarmuka operasional mandiri (**SiReDo CLI Framework**).

### Alur Layering Feature-Module (Backend)
```
Routes / CLI Entrypoint
       │
       ▼
Controller / CLI Command Handler (Validasi DTO, Flag CLI, & Response Formatting)
       │
       ▼
Service / Use Case (Orkestrasi Logika Bisnis, Hybrid NLP Pipeline, Hot Reload)
       │
       ▼
Repository / Data Access (Relational Composite SQL Repository: SQLite / MySQL)
       │
       ▼
Data Storage (SQLite DB / MySQL Engine / Excel Importer & Exporter)
```

---

## 2. SiReDo CLI Framework Architecture

Framework CLI dibangun di atas `server/src/cli/` dengan entrypoint root `siredo` (dieksekusi: `python siredo <command>`):
- **Server Lifecycle**: `serve` (background daemon by default via `pythonw.exe` & `CREATE_NO_WINDOW`, `--foreground` mode), `reload` (hot reload in-memory cache via authenticated API), `shutdown` (graceful PID-based termination).
- **Log Monitoring**: `logs` (real-time stream viewer via `RotatingFileHandler`).
- **Database Engineering**: `db:migrate` (skema DDL SQLite/MySQL dengan `CREATE DATABASE IF NOT EXISTS`), `db:export` (ekspor relasional ke Excel/JSON), `db:import` (impor dataset Excel ke tabel relasional), `db:truncate` (kosongkan data tabel), `db:drop` (hapus database).
- **Cache Maintenance**: `cache:clear` (pembersihan disk embedding cache `.npy` dan `.json`).

---

## 3. Database Architecture (Multi-Driver Relasional)

Skema database dinormalisasi ke dalam 4 tabel relasional:
- `dosen` (Master: `id`, `nidn`, `nama`, `program_studi`, `bidang_keahlian`, `pendidikan`, `timestamps`)
- `publikasi` (Child: `id`, `dosen_id`, `judul`, `tahun`, `penerbit`, `created_at`)
- `riwayat_bimbingan` (Child: `id`, `dosen_id`, `judul_tugas_akhir`, `tahun`, `peran`, `created_at`)
- `riwayat_pengujian` (Child: `id`, `dosen_id`, `judul_sidang`, `tahun`, `peran`, `created_at`)

*Optimalisasi Query*: Menggunakan 4-query flat batch fetch dengan *in-memory grouping* (Zero N+1 Query).

---

## 4. NLP Pipeline Engineering
1. **Preprocessing**: Case folding, stopword removal, unigram + bigram n-gram generation.
2. **Synonym Expansion**: Longest-first ontology matching dari kamus sinonim domain IT.
3. **Lexical Scoring (BM25Okapi)**:
   - Z-score Sigmoid Normalization: $z = \frac{x - \mu}{\sigma}$, $\text{Score}_{\text{norm}} = \frac{1}{1 + e^{-z/2}}$.
   - Hard Constraint Pruning: Hanya dosen dengan $\text{BM25}_{\text{norm}} > 0$ yang diteruskan ke layer semantik.
4. **Semantic Scoring (Sentence-BERT)**:
   - Model `paraphrase-multilingual-MiniLM-L12-v2` (768-D embeddings).
   - Cosine Similarity komputasi vektor.
5. **Adaptive Hybrid Aggregation**:
   - Jika query $< 15$ token: Keyword Mode ($\alpha=0.70$ BM25, $\beta=0.30$ SBERT).
   - Jika query $\ge 15$ token: Abstrak Mode ($\alpha=0.35$ BM25, $\beta=0.65$ SBERT).
   - Top-K ranking efisien $O(n + k \log k)$ via `np.argpartition`.
6. **Explainable AI (XAI)**:
   - Irisan kata kunci leksikal mahasiswa vs korpus dosen.
   - Ekstraksi topik semantic via KeyBERT.

---

## 5. Logging & Observability Architecture
- **Dedicated File Logger**: `server/storage/logs/siredo.log` menggunakan `RotatingFileHandler` (10 MB x 5 backup).
- **Structured Fields**: `timestamp`, `level`, `request_id`, `endpoint`, `status`, `duration`, `error`.
- **Health Monitoring**: Endpoint `GET /health` dan `GET /api/system/status`.

---

## 6. Frontend Architecture (Vue 3 + Pinia)
- **Pinia State Management**:
  - `useSystemStore`: Status koneksi server, ketersediaan cache, daftar data dosen.
  - `useRecommendationStore`: State input query, stepper progress, hasil rekomendasi, pipeline logs, dan batch processing.
  - `useConfigStore`: State konfigurasi parameter algoritma.
- **Axios Interceptors**:
  - Base URL dinamis dari `import.meta.env.VITE_API_BASE_URL`.
  - Standardized error unwrapping dan timeout handling.
