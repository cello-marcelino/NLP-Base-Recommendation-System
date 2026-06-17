# 🚀 SIREDO (Sistem Rekomendasi Dosen) - Pembaruan Teknis v2.0

SIREDO adalah mesin pencari dan sistem rekomendasi berbasis *Artificial Intelligence* (AI) dan *Natural Language Processing* (NLP) yang dirancang untuk memetakan abstrak rencana skripsi mahasiswa ke daftar dosen pembimbing yang paling relevan.

Pembaruan versi 2.0 ini membawa perombakan masif dari purwarupa (*prototype*) akademik menjadi perangkat lunak berskala produksi (*Production-Ready*).

---

## 🌟 Pembaruan Teknis Utama (Changelog)

### 1. Arsitektur Peladen & Pangkalan Data (Backend)
* **Migrasi MySQL:** Meninggalkan file Excel statis dan beralih ke *Relational Database* (MySQL) penuh, memungkinkan operasi CRUD yang efisien.
* **Vector Caching (Optimalisasi Cold Start):** Menerapkan serialisasi NumPy (`.npy`) untuk menyimpan matriks vektor berdimensi tinggi SBERT ke penyimpanan lokal. Memangkas waktu *booting* peladen dari **~30 menit menjadi hanya 0.1 detik**.
* **Keamanan JWT (JSON Web Tokens):** Mengimplementasikan otentikasi API yang aman menggunakan `flask-jwt-extended` dan enkripsi kata sandi `werkzeug.security`.
* **Arsitektur Modular:** Memisahkan logika koneksi, otentikasi, dan pengambilan data ke dalam paket (*package*) internal `database/` untuk memastikan prinsip *Separation of Concerns* (SoC).

### 2. Algoritma Pencarian Hibrida (AI Core)
* **Pembobotan Hibrida Adaptif (Adaptive Hybrid Weighting):** Mesin tidak lagi bergantung pada persentase statis. Menggunakan **Inverse Document Frequency (IDF)**, AI kini mampu secara dinamis menaikkan bobot Leksikal (BM25) jika mendeteksi kueri yang berisi istilah teknis/langka, dan menaikkan bobot Semantik (SBERT) untuk kueri konseptual/bahasa umum.
* **Penilaian Absolut (Absolute Honest Scoring):** Mengganti *Min-Max Normalization* menjadi perhitungan skor absolut berbasis "Skor Sempurna Teoretis". Sistem kini menampilkan persentase kecocokan yang 100% jujur, merepresentasikan tingkat kualitas ketersediaan penelitian pangkalan data kampus.
* **Ekspansi Kueri & Transparansi Token:** Logika prapemrosesan (*preprocessing*) diisolasi murni di sisi peladen demi menjaga integritas *Single Source of Truth* untuk SBERT dan BM25.

### 3. Antarmuka Pengguna (Frontend Vue.js)
* **Client-Side Pagination & Real-time Search:** Tabel pangkalan data dosen kini dilengkapi fitur paginasi sisi klien yang super cepat dan kotak pencarian langsung (nama, prodi, keahlian) tanpa membebani *server*.
* **UX Copywriting Bahasa Indonesia Baku:** Menstandardisasi seluruh bahasa antarmuka (UI) dengan terminologi akademis dan profesional (Misal: "Kecocokan Leksikal", "Jarak Cosine", "Ekspansi Kueri").
* **Perbaikan Stale-State (Race Condition):** Memperbaiki anomali injeksi parameter yang tertinggal di memori (*State Management*) dengan mengatur ulang *Payload Echo* sebelum peladen merespons.
* **Indikator Proses AI:** Mengubah konsep tombol "Refresh" menjadi "Sinkronisasi Data AI" yang lebih intuitif, lengkap dengan animasi dan visualisasi "How AI Thinks" yang elegan dan interaktif.

---

## 📂 Struktur Direktori Proyek

```text
SIREDO/
│
├── client/                     # Antarmuka Pengguna (Vue 3)
│   ├── src/
│   │   ├── components/         # Komponen UI (Modal, Toast, dsb)
│   │   ├── views/              # Halaman Dosen & Halaman Rekomendasi
│   │   └── services/           # Konfigurasi Axios API
│   └── package.json
│
└── server/                     # Peladen Mesin AI (Flask Python)
    ├── database/               # (BARU) Paket Pangkalan Data
    │   ├── __init__.py
    │   ├── auth.py             # Layer Keamanan & JWT
    │   ├── config.py           # Koneksi MySQL
    │   ├── data_layer.py       # Pemasok Data Mesin AI
    │   └── migrate.py          # Script Otomatis Excel ke MySQL
    │
    ├── data/
    │   └── vektor_dosen.npy    # (BARU) Cache Memori Vektor SBERT
    │
    ├── app.py                  # Routing Utama & API Endpoint
    ├── rekomendasi.py          # Mesin SBERT, BM25, & Pipeline Hibrida
    ├── utils.py                # Kamus Ekspansi Kueri & Stopwords
    └── requirements.txt

```

---

## 🛠️ Cara Instalasi & Menjalankan Aplikasi

### Persyaratan Sistem:

* Python 3.9+
* Node.js v16+
* XAMPP / MySQL Server

### Langkah 1: Persiapan Database

1. Nyalakan modul MySQL di XAMPP Anda.
2. Buka phpMyAdmin, buat database baru dengan nama `db_siredo`.
3. (Opsional) Jika Anda memiliki data Excel lama, jalankan migrasi otomatis:
```bash
cd server/database
python migrate.py

```


### Langkah 2: Menyalakan Peladen (Backend)

1. Buka terminal di folder `server`.
2. Aktifkan *virtual environment*:
```bash
.venv\Scripts\activate

```


3. Instal pustaka terbaru (termasuk MySQL Connector & JWT):
```bash
pip install -r requirements.txt

```


4. Nyalakan mesin:
```bash
python app.py

```


*(Catatan: Saat peladen menyala pertama kali setelah migrasi data, mesin akan membangun file cache `vektor_dosen.npy`. Booting berikutnya hanya memakan waktu 0.1 detik).*

### Langkah 3: Menyalakan Antarmuka (Frontend)

1. Buka terminal baru di folder `client`.
2. Instal dependensi Vue:
```bash
npm install

```


3. Jalankan *development server*:
```bash
npm run dev

```


4. Buka tautan `http://localhost:5173` (atau sesuai yang tertera di terminal) pada *browser* Anda.

---

**Dibuat dengan dedikasi untuk riset *Information Retrieval* | © 2026**