# SiReDo — Sistem Rekomendasi Dosen (Politeknik Negeri Batam)

**SiReDo (Sistem Rekomendasi Dosen)** adalah platform berbasis kecerdasan artifisial (*Natural Language Processing*) yang dirancang khusus untuk memetakan dan merekomendasikan dosen pembimbing serta penguji tugas akhir / skripsi / *Project-Based Learning* (PBL) yang paling relevan dengan topik proyek mahasiswa di lingkungan **Politeknik Negeri Batam (Polibatam)**.

Sistem menganalisis keselarasan antara teks masukan (*Judul* dan *Abstrak* proposal) dengan korpus kepakaran dosen (keahlian, publikasi ilmiah, riwayat bimbingan, riwayat pengujian, dan latar belakang pendidikan) menggunakan pendekatan **Hibrida (*Hybrid Retrieval*)**: **Leksikal (Okapi BM25)** dan **Semantik (Sentence-BERT)**.

---

## 🌟 Fitur Utama

1. **Rekomendasi Hibrida Adaptif & Manual**:
   - Menghitung skor gabungan (*Hybrid Score*) dari kemiripan kata kunci persis (*Lexical*) dan kedekatan makna kontekstual (*Semantic*).
   - Menyediakan mode **Manual** (slider bobot $\alpha$ & $\beta$) serta mode **Adaptif** (sistem otomatis menghitung bobot optimal berdasarkan tingkat kelangkaan istilah teknis pada proposal mahasiswa).
2. **Streaming Progres Real-Time (Server-Sent Events)**:
   - Pelacakan progres pencarian secara *live* dari tahap prapemrosesan teks, kalkulasi BM25, inferensi SBERT, hingga pemeringkatan akhir melalui protokol SSE (`/api/rekomendasi/stream`).
3. **Explainable AI (XAI) Modal**:
   - Transparansi keputusan AI: Menampilkan *breakdown* skor, irisan kata kunci persis (*Lexical Intersections*), serta frasa representatif dosen hasil ekstraksi **KeyBERT**.
4. **Admin Panel & Sinkronisasi Cache Inkremental (*Delta Sync*)**:
   - Manajemen CRUD data dosen secara dinamis.
   - Menggunakan mekanisme *Delta Patching* berorientasi *thread-safe* (`threading.RLock()`) pada matriks vektor `.npy`, sehingga pembaruan data dosen hanya memakan waktu **1–2 detik** tanpa perlu komputasi ulang seluruh dataset.
5. **Dashboard Riwayat & Analisis**:
   - Rekapitulasi histori pencarian mahasiswa lengkap dengan ringkasan statistik (total kueri, topik terbanyak, dan detail hasil rekomendasi).
6. **Direktori & Profil Akademik Dosen**:
   - Katalog pencarian profil dosen Polibatam beserta visualisasi keahlian dan riwayat akademik.
7. **Dynamic Server Status & Data Source Indicator**:
   - *Top bar* cerdas yang memantau kesiapan mesin AI secara *real-time* serta mendeteksi sumber alokasi data yang sedang aktif (**MySQL Database** atau **Excel Fallback**).

---

## 🏗️ Struktur dan Arsitektur Proyek

Aplikasi dibangun dengan arsitektur modular yang memisahkan *Presentation Layer* (Frontend), *API & Business Logic Layer* (Backend), *Storage/Cache Layer*, serta *Testing Layer*:

```text
NLP-Base-Recommendation-System/
├── client/                          # Frontend Application (Vue 3 + Vite)
│   ├── public/                      # Static Assets & Icons
│   ├── src/
│   │   ├── assets/
│   │   │   └── main.css             # Tailwind CSS v4 Theme (@theme Teal/Slate)
│   │   ├── components/              # Komponen Reusable (ProgressStepper, XaiModal, DosenCard)
│   │   ├── router/                  # Vue Router (Page Routing)
│   │   ├── services/
│   │   │   ├── api.js               # Axios REST Client
│   │   │   └── stream.js            # EventSource SSE Client
│   │   ├── utils/                   # Helper & Toast Notifications
│   │   ├── views/                   # Halaman Utama (Recommendation, DosenProfile, Admin, Riwayat)
│   │   ├── App.vue                  # Root Component + Dynamic Server Status Topbar
│   │   └── main.js                  # Entrypoint Frontend
│   ├── package.json
│   └── vite.config.js
│
├── server/                          # Backend Application (Flask REST API)
│   ├── app/
│   │   ├── __init__.py              # Factory Pattern App Initialization
│   │   ├── config.py                # Konfigurasi Environment & Path Storage
│   │   ├── routes/                  # Blueprint Controllers
│   │   │   ├── recommend_routes.py  # Endpoint Rekomendasi (REST & SSE Stream)
│   │   │   ├── dosen_routes.py      # Endpoint CRUD & Profil Dosen
│   │   │   └── health_routes.py     # Endpoint Status Kesiapan Server & Sumber Data
│   │   ├── services/                # Business Logic & NLP Engine
│   │   │   ├── bm25_service.py      # Lexical Matching Engine (Okapi BM25)
│   │   │   ├── sbert_service.py     # Semantic Matching & KeyBERT Service
│   │   │   ├── hybrid_engine.py     # Fusion Engine, Ranking, & Delta Sync
│   │   │   ├── data_loader.py       # Data Access Object (MySQL + Excel Fallback)
│   │   │   └── progress_stream.py   # SSE Event Formatter Helper
│   │   └── utils/                   # Modul Prapemrosesan Teks
│   │       ├── text_preprocessor.py # Pipeline Tokenisasi N-Gram & Ekspansi
│   │       ├── stopwords.py         # Korpus Stopwords Bahasa Indonesia
│   │       ├── kamus_ekspansi.py    # Tesaurus / Kamus Sinonim Domain Khusus
│   │       └── response_formatter.py# Standarisasi JSON Response
│   ├── storage/                     # Penyimpanan Data & Cache Terisolasi
│   │   ├── data/                    # Master Data Excel Fallback
│   │   ├── cache/                   # Cache Vektor Numpy (.npy) & KeyBERT JSON
│   │   └── models/                  # Direktori Model Lokal (opsional)
│   ├── requirements.txt             # Dependensi Python
│   └── run.py                       # Entrypoint Server Flask
│
├── testing/                         # Automated Testing & Benchmark Suite
│   ├── unitest.py                   # Unit Testing Pipeline NLP & Logika
│   ├── test_api.py                  # Integration Testing Endpoint API
│   ├── locustfile.py                # Performance & Load Testing (Locust)
│   └── confest,py                   # Konfigurasi Test Fixtures
│
├── docs/                            # Blueprint & Dokumentasi Arsitektur
└── readme.md                        # Dokumentasi Utama Proyek
```

---

## ⚙️ Pipeline NLP dan Prapemrosesan

```
[ Input Proposal: Judul & Abstrak ]
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Text Preprocessing Pipeline                          │
│    • Case Folding & Pembersihan Karakter Khusus         │
│    • Indonesian Stopword Filtering                      │
│    • Domain Synonym Expansion (kamus_ekspansi.py)       │
│    • N-Gram Tokenizer (Unigram + Bigram)                │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────────────────────┐
        ▼                                 ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│ 2. Lexical Engine (BM25)  │   │ 3. Semantic Engine (SBERT)│
│    • Okapi BM25 Scoring   │   │    • 768-D Dense Vectors  │
│    • Min-Max Normalization│   │    • Cosine Similarity    │
└───────────────┬───────────┘   └─────────────┬─────────────┘
                │                             │
                └──────────────┬──────────────┘
                               ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Hard Constraint & Pruning Layer                      │
│    • Jika Skor BM25 == 0 -> Skor Semantik di-drop ke 0  │
└──────────────────────────────┬──────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Hybrid Fusion & Weighting Scheme                     │
│    • Mode Manual  : Score = (α * Lexical) + (β * Semantic)│
│    • Mode Adaptif : Bobot dihitung dinamis via IDF      │
└──────────────────────────────┬──────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Explainable AI (XAI) & Final K-Ranking               │
│    • Ekstraksi Frasa Representatif Dosen (KeyBERT)      │
│    • Irisan Kata Kunci Persis (Lexical Matching)        │
│    • Top-K Ranked Lecturers Response                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tools dan Library Utama

### Backend
- **Python 3.10+** (disarankan 3.11 atau 3.12)
- **Flask**: Web framework micro untuk REST API dan SSE.
- **sentence-transformers**: Menggunakan model `paraphrase-multilingual-MiniLM-L12-v2` untuk *semantic text embedding*.
- **rank-bm25**: Algoritma Okapi BM25 untuk *lexical keyword matching*.
- **KeyBERT**: Ekstraksi kata kunci kontekstual profil dosen.
- **scikit-learn**: Komputasi *cosine similarity* dan fungsi matriks.
- **NumPy & Pandas**: Pengolahan array multi-dimensi dan parsing data tabel.
- **PyMySQL & Cryptography**: Konektivitas database relasional MySQL.

### Frontend
- **Vue 3** (Composition API `<script setup>`): Reaktif dan terstruktur.
- **Vite**: Build tool modern berkecepatan tinggi.
- **Tailwind CSS v4**: Utility-first CSS framework dengan kustomisasi tema `@theme`.
- **Axios**: HTTP client untuk request data asinkron.
- **Server-Sent Events (EventSource)**: Protokol streaming progres *real-time*.

### Database & Testing
- **MySQL / MariaDB**: Penyimpanan relasional master data profil dosen dan log pencarian.
- **Pytest & Unittest**: Pengujian unit dan integrasi.
- **Locust**: Pengujian beban (*load/stress testing*) konkurensi API.

---

## 🚀 Panduan Menjalankan Aplikasi (Lokal)

### 1. Prasyarat Sistem
Pastikan perangkat Anda telah terinstal:
- **Node.js**: v18+ atau v20+ ([Unduh Node.js](https://nodejs.org/))
- **Python**: v3.10, v3.11, atau v3.12 ([Unduh Python](https://www.python.org/))
- **MySQL Server**: (Bisa menggunakan paket **XAMPP** atau MySQL Community Server)

---

### 2. Konfigurasi Basis Data (Database)

1. Pastikan layanan MySQL Anda aktif (misalnya via *XAMPP Control Panel*).
2. Buka terminal atau konsol MySQL, lalu buat database dan tabel yang diperlukan:

```sql
CREATE DATABASE IF NOT EXISTS db_siredo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_siredo;

-- Tabel Profil Dosen
CREATE TABLE IF NOT EXISTS dosen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nidn VARCHAR(30) NULL,
    nama TEXT NOT NULL,
    program_studi TEXT NOT NULL,
    bidang_keahlian LONGTEXT,
    jurnal LONGTEXT,
    judul_bimbing LONGTEXT,
    judul_uji LONGTEXT,
    riwayat_pendidikan LONGTEXT
);

-- Tabel Log Histori Rekomendasi
CREATE TABLE IF NOT EXISTS log_rekomendasi (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    judul_mhs TEXT,
    abstrak_mhs TEXT,
    hasil_rekomendasi_json LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

> **Catatan Ketersediaan Data (Fallback)**:
> Jika MySQL tidak diaktifkan, backend **secara otomatis beralih** menggunakan dataset cadangan di `server/storage/data/dataset_profiles_terintegrasi.xlsx` sehingga aplikasi tetap dapat berjalan normal.
> Pengaturan koneksi MySQL dapat disesuaikan pada berkas `server/app/config.py` atau `server/app/services/data_loader.py`.

---

### 3. Menjalankan Backend (Flask API)

1. Buka terminal pertama, arahkan ke direktori `server`:
   ```powershell
   cd server
   ```
2. Buat dan aktifkan *Virtual Environment*:
   ```powershell
   python -m venv .venv
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. Pasang seluruh dependensi Python:
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Jalankan server backend:
   ```powershell
   python run.py
   ```
   *Peladen backend akan aktif pada `http://127.0.0.1:5050`. Mesin AI akan memanaskan cache vektor secara otomatis di latar belakang.*

---

### 4. Menjalankan Frontend (Vue 3)

1. Buka terminal kedua, arahkan ke direktori `client`:
   ```powershell
   cd client
   ```
2. Pasang paket dependensi Node.js:
   ```powershell
   npm install
   ```
3. Jalankan server pengembangan Vite:
   ```powershell
   npm run dev
   ```
4. Buka peramban (*browser*) dan akses URL yang tertera (biasanya `http://localhost:5173`).

---

### 5. Menjalankan Pengujian (*Testing Suite*)

Untuk menjalankan rangkaian uji otomatis:
```powershell
# Unit Testing
python -m unittest testing/unitest.py

# API Integration Testing
pytest testing/test_api.py

# Load Testing (Locust Web UI pada http://localhost:8089)
locust -f testing/locustfile.py
```

---

## 👥 Tim Pengembang (Developers)

Proyek ini dikembangkan oleh:
- **Hamdan Azmi** (331241004)
- **Christian Marcelino** (3312411008)

---

## 🔧 Pemeliharaan & Kontribusi

- **Pembaruan Data Dosen**: Disarankan melalui antarmuka **Admin Panel** di web agar cache inkremental (*Delta Sync*) diperbarui secara otomatis.
- **Konsistensi Preprocessing**: Jangan mengubah alur tokenisasi pada `text_preprocessor.py` tanpa menguji dampaknya pada matriks kemiripan leksikal dan semantik.

---

*Dikembangkan untuk Program Studi dan Sivitas Akademika Politeknik Negeri Batam.*

