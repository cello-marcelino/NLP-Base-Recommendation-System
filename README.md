# SiReDo v3 — Sistem Rekomendasi Dosen (Politeknik Negeri Batam)

**SiReDo (Sistem Rekomendasi Dosen) v3** adalah platform dan **Penyedia Mesin Rekomendasi (*Recommendation Engine Provider*)** berbasis kecerdasan artifisial (*Natural Language Processing*) yang dirancang untuk memetakan dan merekomendasikan dosen pembimbing maupun dosen penguji secara akurat, objektif, dan terukur berdasarkan kesesuaian judul serta abstrak proyek/skripsi/PBL mahasiswa di lingkungan **Politeknik Negeri Batam (Polibatam)**.

SiReDo v3 dirancang dengan prinsip **arsitektur terpisah (*Decoupled / Headless Architecture*)** dan menyediakan **REST API yang lengkap, modular, serta terdokumentasi secara interaktif**. Hal ini memungkinkan SiReDo v3 tidak hanya digunakan sebagai aplikasi web mandiri, tetapi juga sangat mudah diintegrasikan (*plug-and-play*) ke dalam sistem informasi akademik kampus (seperti SIAKAD, SIM-TA, sistem penjadwalan sidang PBL), maupun aplikasi *frontend* pihak ketiga lainnya (React, Next.js, Mobile App, dll).

---

## 🎯 Cakupan & Target Pengguna (*Scope*)

1. **Mahasiswa**: Membantu menemukan calon **Dosen Pembimbing** yang paling relevan dengan topik riset, tugas akhir, atau proyek *Project-Based Learning* (PBL).
2. **Admin & Koordinator Penjadwalan Akademik**: Membantu mencocokkan dan menyelaraskan topik proyek/PBL mahasiswa dengan **Dosen Penguji** yang memiliki kepakaran sesuai saat pelaksanaan sidang ujian/evaluasi.
3. **Pengembang & Institusi Kampus Lain (*Engine Provider*)**: Menyediakan infrastruktur API inferensi NLP Hibrida yang siap dikonsumsi oleh subsistem akademik kampus lain yang membutuhkan modul rekomendasi kepakaran dosen.

---

## 🌟 Fitur Utama SiReDo v3

1. **Mesin Rekomendasi NLP Hibrida (BM25 + SBERT)**:
   - Menggabungkan pencocokan leksikal berbasis kata kunci (*Okapi BM25*) dan kedekatan konteks semantik (*Sentence-BERT* 768-D `paraphrase-multilingual-MiniLM-L12-v2`).
   - Dilengkapi *Hard Constraint Pruning* untuk mengeliminasi hasil yang tidak relevan secara leksikal.
2. **Single Recommendation & Explainable AI (XAI)**:
   - Rekomendasi dosen perorangan disertai penjelasan transparan (*XAI Modal*): irisan kata kunci persis, ekstraksi frasa representatif dosen via **KeyBERT**, serta rincian skor leksikal vs semantik.
3. **Batch Recommendation (Massal)**:
   - Memproses puluhan hingga ratusan proposal proyek mahasiswa sekaligus melalui unggahan berkas Excel untuk otomatisasi alokasi pembimbing/penguji massal.
4. **Halaman Dokumentasi API Interaktif (`/api-docs`)**:
   - Dokumentasi antarmuka REST API lengkap langsung di dalam web (katalog *endpoint*, contoh cURL, format request/response JSON, dan penanganan kode galat).
5. **Manajemen Konfigurasi Global Dinamis (`/config`)**:
   - Pengaturan parameter krusial (Top K-Rank, Similarity Threshold, Bobot Alpha & Beta, serta Mode AI Adaptif vs Manual) langsung dari antarmuka Web tanpa mengubah kode sumber.
6. **Preprocessing Playground (`/preprocessing`)**:
   - Modul pengujian interaktif untuk melihat tahapan prapemrosesan teks (*Case Folding*, *Stopwords Filtering*, *Synonym Expansion*, dan *N-Gram Tokenization*) secara langsung.
7. **Katalog Data Dosen & Profil Akademik (`/dosen`)**:
   - Pencarian dan eksplorasi data profil kepakaran dosen, bidang keahlian, publikasi ilmiah, dan riwayat bimbingan/pengujian.
8. **Real-time Server Status Badge**:
   - Indikator status detak jantung (*heartbeat*) dan kesiapan mesin inferensi backend.

---

## 🔄 Perbandingan Arsitektur: SiReDo v2 vs SiReDo v3

| Aspek | SiReDo v2 | SiReDo v3 (Versi Terbaru) |
| :--- | :--- | :--- |
| **Peran Sistem** | Aplikasi Web Rekomendasi Terikat | **Recommendation Engine Provider & Headless REST API** |
| **Struktur Folder** | `client/` + `server/` | **`web/`** (Frontend UI & Docs) + **`server/`** (Backend Engine) |
| **Arsitektur Backend** | Flat Route-Service Blueprint | **Layered Controller - Service - NLP Engine - Storage** |
| **Rekomendasi Batch** | Belum terintegrasi | **Didukung Penuh** (Single & Multi-Upload Excel via `POST /api/batch`) |
| **Dokumentasi API** | Markdown Static | **Halaman Interaktif di Web (`ApiDocsView.vue`)** + Playground |
| **Konfigurasi Global** | Hardcoded / Config File | **Dynamic Config API (`GET/PATCH /api/config`)** via UI |
| **Interoperabilitas** | Tertutup untuk klien bawaan | **Terbuka & Siap Diintegrasikan** ke SIAKAD / Frontend Eksternal |

---

## 🏗️ Struktur Direktori Proyek

```text
NLP-Base-Recommendation-System/
├── web/                             # Frontend Layer (Vue 3 + Vite)
│   ├── public/                      # Static Assets & Icons
│   ├── src/
│   │   ├── assets/                  # CSS Global & Design Tokens (@theme)
│   │   ├── components/
│   │   │   ├── layout/              # AppSidebar.vue, ServerStatusBadge.vue
│   │   │   └── recommendation/      # DosenCard.vue, ProgressStepper.vue, XaiModal.vue
│   │   ├── router/                  # Vue Router (Page Routing)
│   │   ├── services/                # Axios API Client (api.js)
│   │   └── views/                   # Halaman Antarmuka:
│   │       ├── HomeView.vue         # Dashboard Utama
│   │       ├── SingleRecommendationView.vue # Rekomendasi Proposal Tunggal
│   │       ├── BatchRecommendationView.vue  # Rekomendasi Batch Excel
│   │       ├── DosenDataView.vue    # Direktori Profil Dosen
│   │       ├── PreprocessingView.vue# Playground Prapemrosesan NLP
│   │       ├── ConfigurationView.vue# Pengaturan Parameter Global
│   │       ├── ApiDocsView.vue      # Dokumentasi Interaktif REST API
│   │       └── InstallSetupView.vue # Panduan Instalasi Lokal
│   ├── package.json
│   └── vite.config.js
│
├── server/                          # Backend Layer & NLP Engine (Flask API)
│   ├── app/
│   │   ├── config/                  # Settings & Environment Config
│   │   ├── controllers/             # Request Handlers (Recommendation, Batch, System)
│   │   ├── routes/                  # API Routing Blueprint (recommendation, batch, system)
│   │   ├── services/
│   │   │   ├── nlp/                 # Core NLP Modules (BM25, SBERT, Preprocessor, Hybrid Scorer)
│   │   │   ├── batch_service.py     # Logika Pemrosesan Rekomendasi Massal
│   │   │   ├── cache_service.py     # Singleton Warmup & Cache Manager
│   │   │   └── recommendation_service.py # Logika Rekomendasi & XAI Generator
│   │   ├── storage/                 # Data Persistence & Config Manager (config.json, dataset Excel)
│   │   └── utils/                   # Stopwords, Kamus Ekspansi, & Response Formatter
│   ├── data/                        # Dataset Master Excel Dosen Polibatam
│   ├── requirements.txt             # Dependensi Python
│   └── run.py                       # Server Entry Point (Port 5000)
│
├── CHANGELOG.md                     # Riwayat Perubahan dan Rilis
└── README.md                        # Dokumentasi Utama Proyek
```

---

## 📡 REST API Reference (Untuk Integrasi Sistem Lain)

SiReDo v3 menyediakan endpoint standar berformat **JSON Envelope**:

```json
{
  "status": "success",
  "data": { ... },
  "message": "Operasi berhasil dieksekusi"
}
```

### Ringkasan Endpoint Utama:
- `POST /api/single`: Mencari rekomendasi dosen untuk 1 proposal (Judul + Abstrak).
- `POST /api/batch`: Mencari rekomendasi dosen untuk banyak data proposal dalam 1 request JSON.
- `POST /api/batch/upload`: Memproses file Excel proposal mahasiswa dan mengembalikan hasil alokasi dosen.
- `GET /api/status`: Memeriksa kesehatan server dan kesiapan mesin NLP.
- `GET /api/config`: Mengambil parameter konfigurasi inferensi yang sedang aktif.
- `PATCH /api/config`: Memperbarui bobot $\alpha/\beta$, threshold, atau Top-K secara langsung.
- `GET /api/dosen`: Mengambil daftar profil lengkap seluruh dosen.

*(Dokumentasi interaktif lengkap dapat diakses melalui antarmuka web pada menu **API Reference**).*

---

## 🚀 Panduan Menjalankan Aplikasi (Lokal)

### 1. Menjalankan Backend (Server)
Pastikan perangkat telah terpasang **Python 3.10+** (disarankan 3.11 atau 3.12).

```powershell
# 1. Masuk ke direktori server
cd server

# 2. Buat dan aktifkan virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
# source venv/bin/activate    # Linux / macOS

# 3. Pasang dependensi
pip install --upgrade pip
pip install -r requirements.txt

# 4. Jalankan server Flask
python run.py
```
*Backend akan berjalan aktif pada `http://localhost:5000` (atau `http://127.0.0.1:5000`).*

---

### 2. Menjalankan Frontend (Web)
Pastikan perangkat telah terpasang **Node.js (v18+ atau v20+)**.

```powershell
# 1. Masuk ke direktori web
cd web

# 2. Pasang dependensi Node
npm install

# 3. Jalankan server pengembangan Vite
npm run dev
```
*Akses antarmuka web melalui browser pada `http://localhost:5173`.*

---

## 👥 Tim Pengembang (Developers)

Proyek ini dikembangkan untuk kemajuan ekosistem riset dan akademik di lingkungan **Politeknik Negeri Batam**:
- **Hamdan Azmi** (NIM: 331241004)
- **Christian Marcelino** (NIM: 3312411008)

---

*SiReDo v3 — Open, Decoupled & Intelligent Lecturer Recommendation Engine.*
