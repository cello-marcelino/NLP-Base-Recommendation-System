# 🚀 SIREDO (Sistem Rekomendasi Dosen) - v2.0 Production Ready

[cite_start]SIREDO adalah mesin pencari dan sistem rekomendasi berbasis Artificial Intelligence (AI) dan Natural Language Processing (NLP)[cite: 2, 120]. [cite_start]Aplikasi ini dirancang khusus untuk membantu mahasiswa menemukan dosen pembimbing skripsi yang paling relevan dengan memetakan judul dan abstrak ke rekam jejak penelitian dosen[cite: 3, 57]. 

## 🧠 Metode yang Digunakan

Aplikasi ini menggunakan pendekatan hibrida (gabungan) agar rekomendasi yang dihasilkan sangat presisi:
1. [cite_start]**Metode Leksikal (BM25):** Mencari kecocokan kata kunci (istilah teknis) secara persis antara input mahasiswa dan profil dosen[cite: 58].
2. [cite_start]**Metode Semantik (SBERT):** Memahami kedekatan makna dan konteks topik (berbasis vektor) meskipun menggunakan pilihan diksi yang berbeda[cite: 59].
3. [cite_start]**Pembobotan Adaptif (Adaptive Weighting):** Mesin AI secara otomatis menyeimbangkan persentase skor Leksikal dan Semantik berdasarkan evaluasi kelangkaan (IDF) kosakata pada judul pengguna[cite: 8, 60].

## 🏗️ Layer Aplikasi

Sistem SIREDO dibangun dengan arsitektur *Full-Stack* berkinerja tinggi:
* [cite_start]**Antarmuka Pengguna (Frontend - Vue 3):** Menyediakan fitur *Client-Side Pagination*, animasi interaktif, dan pencarian instan[cite: 133].
* [cite_start]**Server & Komunikasi (Backend - Flask):** API tangguh yang menangani *multithreading* dan memberikan manajemen eror (HTTP 503) saat server menginisialisasi AI[cite: 16, 109].
* [cite_start]**Pangkalan Data (MySQL & Excel Fallback):** Relational Database untuk pengelolaan dosen harian, didukung pembacaan Excel sebagai *seeder* otomatis jika pangkalan data utama kosong[cite: 106, 123].
* [cite_start]**Layer Keamanan (JWT Auth):** Melindungi integritas akses API menggunakan standar *JSON Web Tokens* terenkripsi[cite: 126].

## 🛠️ Cara Instalasi & Menjalankan Aplikasi

**Persyaratan Sistem:**
* [cite_start]Python 3.9 atau lebih baru [cite: 139]
* [cite_start]Node.js v16 atau lebih baru [cite: 139]
* [cite_start]XAMPP / MySQL Server [cite: 139]

### Langkah 1: Setup Pangkalan Data (Database) & Autentikasi
1. [cite_start]Nyalakan modul **MySQL** melalui XAMPP[cite: 140].
2. [cite_start]Buka phpMyAdmin, lalu buat database baru dengan nama `db_siredo`[cite: 140].
3. Lakukan migrasi data awal. Masuk ke direktori basis data lalu jalankan skrip migrasi untuk mengekstrak data dari Excel menjadi baris SQL secara otomatis:
   ```bash
   cd server/database
   python migrate.py

```

*(Catatan: Migrasi ini juga akan mendaftarkan akun admin *default* dengan sandi yang terenkripsi menggunakan `werkzeug.security`)*.

### Langkah 2: Menyalakan Peladen AI (Backend)

1. Buka Terminal baru dan masuk ke dalam folder `server`.


2. Aktifkan *virtual environment* Python:
```bash
.venv\Scripts\activate

```


3. Instal semua pustaka dan dependencies (termasuk modul JWT dan MySQL):
```bash
pip install -r requirements.txt

```


4. Nyalakan mesin peladen utama:
```bash
python app.py

```



*(Catatan Cold Start: Saat pertama kali menyala, AI membutuhkan waktu komputasi untuk merangkum vektor matriks menjadi cache `vektor_dosen.npy` dan `vektor_dosen.npy.fingerprint`. Setelah ini selesai, proses booting sistem ke depannya hanya membutuhkan waktu ~0.1 detik)*.



### Langkah 3: Menyalakan Antarmuka Pengguna (Frontend)

1. Buka Terminal baru dan arahkan ke folder `client`.


2. Instal dependensi antarmuka sistem:
```bash
npm install

```


3. Jalankan server lokal antarmuka web:
```bash
npm run dev

```


4. Buka tautan di peramban web Anda (umumnya `http://localhost:5173`) untuk melihat dan menggunakan SIREDO secara langsung.



```

```