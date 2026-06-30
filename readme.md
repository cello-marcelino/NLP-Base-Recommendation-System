# 🚀 SIREDO (Sistem Rekomendasi Dosen) - v2.0 Production Ready

[cite_start]SIREDO adalah mesin pencari dan sistem rekomendasi berbasis *Artificial Intelligence* (AI) dan *Natural Language Processing* (NLP)[cite: 28]. [cite_start]Aplikasi ini dirancang khusus untuk membantu mahasiswa menemukan dosen pembimbing skripsi yang paling relevan dengan memetakan abstrak dan judul rencana skripsi ke daftar dosen berdasarkan rekam jejak penelitian mereka[cite: 29].

---

## 🧠 Metode dan Logika (AI Core)

[cite_start]Sistem ini menggunakan pendekatan Hibrida yang canggih untuk memberikan rekomendasi dosen yang akurat, dengan alur pemrosesan sebagai berikut[cite: 30]:

* [cite_start]**Pendekatan Leksikal (BM25):** Menghitung skor kecocokan persis antara kata pada input mahasiswa dan profil dosen menggunakan pembobotan berbasis TF-IDF[cite: 30].
* [cite_start]**Pendekatan Semantik (SBERT):** Mengonversi teks ke dalam matriks vektor untuk mengevaluasi jarak kesamaan makna (*Cosine Similarity*) sehingga topik relevan tetap terdeteksi meski kosakatanya berbeda[cite: 31].
* [cite_start]**Pembobotan Hibrida Adaptif:** Sistem memanfaatkan nilai *Inverse Document Frequency* (IDF) secara dinamis[cite: 32].
* [cite_start]**Peningkatan Bobot Otomatis:** Bobot Leksikal akan ditingkatkan jika kueri mengandung istilah teknis atau langka, dan bobot Semantik ditingkatkan jika kueri menggunakan bahasa umum[cite: 33].
* [cite_start]**Pemeringkatan Akhir:** Sistem menggabungkan kedua perhitungan tersebut menjadi *Hybrid Score* lalu mengurutkan hasilnya secara menurun[cite: 34].
* [cite_start]**Optimalisasi dan Caching Vektor:** Sistem melakukan komputasi matriks SBERT dan menyimpannya secara lokal menggunakan file `.npy`[cite: 35].
* [cite_start]**Peningkatan Kecepatan:** Hal ini memangkas waktu *booting* peladen secara radikal dari sekitar 30 menit menjadi hanya 0.1 detik[cite: 36].
* [cite_start]**Validasi Keamanan Hash:** Sistem juga membangkitkan file `.fingerprint` berbasis *hash* (MD5) untuk mendeteksi apabila ada perubahan data dosen di pangkalan data sebelum memutuskan untuk membangun ulang matriks[cite: 37].

---

## 🏗️ Layer Aplikasi

[cite_start]Arsitektur sistem dibangun di atas kerangka kerja *Full-Stack* (Vue.js dan Flask) dengan prinsip *Separation of Concerns* (SoC)[cite: 38]:

* [cite_start]**Layer Antarmuka Pengguna (Frontend - Vue.js):** Berada di direktori `client/`, menangani stat animasi visualisasi proses pemikiran AI, pencarian *real-time*, dan paginasi sisi klien agar tidak membebani server[cite: 38]. [cite_start]Komunikasi HTTP ke *backend* dijembatani oleh file `api.js`[cite: 39].
* [cite_start]**Layer API (Backend - Flask Python):** Berada di `app.py`, mengekspos *endpoint* seperti `/api/rekomendasi` dan mengimplementasikan *multithreading* di latar belakang saat memuat model AI[cite: 40]. [cite_start]Isu *race condition* telah diperbaiki sehingga server akan secara elegan mengembalikan status HTTP 503 jika diakses sebelum model siap[cite: 41].
* [cite_start]**Layer Kecerdasan Buatan (AI Core):** Terisolasi di file `rekomendasi.py`, mengelola prapemrosesan teks seperti ekspansi kueri dan penghapusan *stopwords*, proses *AdaptiveWeighting*, serta perhitungan matriks vektor menggunakan *Min-Max Scaling*[cite: 42].
* [cite_start]**Layer Pangkalan Data:** Berfokus pada direktori `database/`, beralih ke arsitektur relasional (MySQL) untuk efisiensi CRUD[cite: 43]. [cite_start]File Excel kini murni digunakan sebagai penyemai cadangan (*seeder*) otomatis apabila koneksi MySQL gagal atau tabel masih kosong[cite: 44].
* [cite_start]**Layer Keamanan (Autentikasi):** Sistem memiliki modul `auth.py` yang menggunakan pustaka `flask-jwt-extended` untuk manajemen *JSON Web Tokens* (JWT) dan `werkzeug.security` untuk enkripsi kata sandi guna mengamankan jalur API[cite: 45].

---

## 🛠️ Cara Instalasi & Menjalankan Aplikasi

**Persyaratan Sistem:**
* [cite_start]Python 3.9 atau lebih baru[cite: 46].
* [cite_start]Node.js v16 atau lebih baru[cite: 47].
* [cite_start]XAMPP / MySQL Server[cite: 47].

### Langkah 1: Setup Pangkalan Data (Database) & Autentikasi
1.  [cite_start]Nyalakan modul MySQL melalui aplikasi XAMPP[cite: 48].
2.  [cite_start]Buka phpMyAdmin di peramban, lalu buat database baru dengan nama `db_siredo`[cite: 49].
3.  [cite_start]Masuk ke direktori `server/database` lalu jalankan skrip `python migrate.py` untuk mengekstrak data dari Excel menjadi baris SQL secara otomatis[cite: 50]. [cite_start]**Catatan:** Migrasi ini juga mendaftarkan akun admin *default* dengan sandi terenkripsi menggunakan `werkzeug.security`[cite: 51].

### Langkah 2: Menyalakan Peladen AI (Backend)
1.  [cite_start]Buka Terminal baru dan masuk ke dalam folder `server`[cite: 52].
2.  [cite_start]Aktifkan *virtual environment* Python dengan perintah `.venv\Scripts\activate`[cite: 53].
3.  [cite_start]Instal semua pustaka dan dependensi (termasuk modul JWT dan MySQL) menggunakan `pip install -r requirements.txt`[cite: 54].
4.  [cite_start]Nyalakan mesin peladen utama dengan mengeksekusi `python app.py`[cite: 55]. [cite_start]**Catatan *Cold Start*:** Saat pertama kali menyala, AI membutuhkan waktu komputasi untuk merangkum vektor matriks menjadi *cache* `vektor_dosen.npy` dan `vektor_dosen.npy.fingerprint`, namun *booting* ke depannya hanya memakan waktu 0.1 detik[cite: 56].

### Langkah 3: Menyalakan Antarmuka Pengguna (Frontend)
1.  [cite_start]Buka Terminal baru dan arahkan ke folder `client`[cite: 57].
2.  [cite_start]Instal dependensi antarmuka sistem dengan menjalankan `npm install`[cite: 58].
3.  [cite_start]Jalankan server lokal antarmuka web dengan perintah `npm run dev`[cite: 59].
4.  [cite_start]Buka tautan di peramban web Anda (umumnya `http://localhost:5173` atau sesuai info terminal) untuk melihat dan menggunakan SIREDO secara langsung[cite: 60].
