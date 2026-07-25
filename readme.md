# SiReDo — Sistem Rekomendasi Dosen (NLP-Base-Recommendation-System)

SiReDo (Sistem Rekomendasi Dosen) adalah aplikasi web berbasis *Machine Learning* yang dirancang untuk membantu mahasiswa menemukan dosen pembimbing skripsi yang paling relevan. Sistem ini bekerja dengan membandingkan teks "Judul" dan "Abstrak" proposal mahasiswa dengan profil, keahlian, dan riwayat penelitian dosen menggunakan pendekatan *Natural Language Processing* (NLP) berarsitektur Hibrida (*Hybrid*).

Pendekatan hibrida mengkombinasikan:
- **Okapi BM25** (Leksikal) untuk pencocokan kemiripan kata kunci secara persis.
- **Sentence-BERT (SBERT)** (Semantik) dengan model `paraphrase-multilingual-MiniLM-L12-v2` untuk memahami konteks dan kemiripan makna.

---

## 🌟 Fitur Utama Terbaru (V2 Refactored)

Sistem telah dirombak (*refactor*) menjadi jauh lebih cepat, modular, dan interaktif:

1. **Rekomendasi Skripsi Hibrida**: Hasil direkomendasikan dengan pencampuran (skor *hybrid*) berdasarkan persentase adaptif atau manual (α BM25 + β SBERT).
2. **Real-time Progress Streaming (SSE)**: UI menampilkan *progress bar* analisis secara waktu nyata (*real-time*), dari prapemrosesan hingga kalkulasi vektor matriks menggunakan *Server-Sent Events*.
3. **Admin Panel Manajemen Dosen**: Administrator dapat menambah, mengedit, dan menghapus dosen.
4. **Penyelarasan Cache Inkremental (Delta Sync)**: Mengubah data dosen sekarang hanya butuh 1-2 detik karena sistem SBERT AI tidak lagi memuat ulang keseluruhan dataset dari awal, melainkan hanya menyisipkan *patch* secara spesifik pada dosen yang dimodifikasi.
5. **Dashboard Riwayat Uji Log**: Panel lengkap untuk melihat riwayat seluruh rekomendasi yang pernah dicari mahasiswa.
6. **XAI (Explainable AI)**: Modal pop-up menjelaskan mengapa AI memilih dosen tersebut (Breakdown skor BM25 dan Semantik).

---

## 🏗️ Struktur Proyek dan Arsitektur

Proyek telah dipisah secara rapi dalam pola arsitektur MVC / *Service-based*:

```text
.
├── client/                     # Frontend Vue 3 + Vite
│   ├── src/components/         # Komponen UI (Navbar, ServerWarmupOverlay, ProgressStepper, XaiModal)
│   ├── src/views/              # Halaman Aplikasi (RecommendationView, AdminDosenView, dll)
│   ├── src/services/           # Integrasi API (api.js) dan SSE (stream.js)
│   └── src/assets/main.css     # Konfigurasi Tailwind CSS v4 Theme
│
└── server/                     # Backend Flask API
    ├── app/
    │   ├── config.py           # Konfigurasi lingkungan & database
    │   ├── routes/             # Blueprint API (recommend, dosen, health)
    │   ├── services/           # Logika AI & Bisnis (BM25, SBERT, Hybrid Engine, Data Loader)
    │   └── utils/              # Pemroses teks, formatter response
    ├── storage/                # Penyimpanan *Cache* AI (Numpy/JSON) dan Kamus NLP
    ├── requirements.txt
    └── run.py                  # Entrypoint peladen (Server)
```

---

## 🚀 Panduan Menjalankan Aplikasi

### 1. Prasyarat (*Prerequisites*)

- **Python 3.10+** (disarankan 3.12)
- **Node.js 20+**
- **MySQL / MariaDB** (Tersedia via XAMPP)

### 2. Pengaturan Basis Data (Database)

Buat database `db_siredo` di MySQL dan impor tabel (atau jalankan script migrasi awal):
```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS db_siredo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p db_siredo -e "CREATE TABLE IF NOT EXISTS dosen (id INT AUTO_INCREMENT PRIMARY KEY, nidn VARCHAR(30) NULL, nama TEXT NOT NULL, program_studi TEXT NOT NULL, bidang_keahlian LONGTEXT, jurnal LONGTEXT, judul_bimbing LONGTEXT, judul_uji LONGTEXT, riwayat_pendidikan LONGTEXT);"
mysql -u root -p db_siredo -e "CREATE TABLE IF NOT EXISTS log_rekomendasi (id_log INT AUTO_INCREMENT PRIMARY KEY, judul_mhs TEXT, abstrak_mhs TEXT, hasil_rekomendasi_json LONGTEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
```
*(Catatan: Kredensial MySQL dapat diubah melalui `server/app/config.py`)*

### 3. Menjalankan Backend (Python Flask)

Buka terminal/PowerShell pertama, masuk ke folder `server`, lalu jalankan:

```powershell
cd server
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt

# Menyalakan API pada http://127.0.0.1:5050
python run.py
```
*(Saat pertama kali `run.py` dijalankan, model AI SBERT akan menghidupkan mesinnya secara otomatis, memuat korpus dari database, dan membuat cache lokal di folder `storage/`)*

### 4. Menjalankan Frontend (Vue 3 + Vite)

Buka terminal/PowerShell kedua, biarkan Backend tetap hidup, masuk ke folder `client`:

```powershell
cd client
npm install
npm run dev
```
Buka tautan lokal yang ditampilkan (biasanya `http://localhost:5173`). UI aplikasi akan menyala dan *Server Warmup Overlay* akan mendeteksi kesiapan mesin AI.

---

## 🧩 Modul Ekstraksi AI

Sistem ini bergantung pada *Natural Language Processing*, dengan metode pra-pemrosesan berikut yang di-handle oleh `server/app/utils/text_preprocessor.py`:
- *Case Folding* (Penyeragaman huruf)
- *Stopwords Removal* (Menghapus kata tidak penting Bahasa Indonesia dari `storage/stopwords.txt`)
- *Synonym Expansion* (Ekspansi makna khusus dari `storage/kamus_ekspansi.json`)
- Pembuatan N-Gram (Unigram & Bigram) untuk meningkatkan pembacaan frasa skripsi.

## ✨ Manajemen Kontribusi
Seluruh basis kode telah dirapihkan. Apabila Anda ingin mengembangkan sistem ini lebih jauh:
- Pastikan tidak mengubah rute `/api/recommend/stream` karena menggunakan spesifikasi `text/event-stream`.
- Jika menambahkan library JS, instal menggunakan `npm install`.
- Jika menambahkan library Python, ingat untuk melakukan `pip freeze > requirements.txt`.
