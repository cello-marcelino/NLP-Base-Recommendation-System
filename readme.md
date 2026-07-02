# 🚀 SIREDO (Sistem Rekomendasi Dosen) - v2.0 Production Ready

SIREDO adalah mesin pencari dan sistem rekomendasi berbasis *Artificial Intelligence* (AI) dan *Natural Language Processing* (NLP). Aplikasi ini dirancang khusus untuk membantu mahasiswa menemukan dosen pembimbing skripsi yang paling relevan dengan memetakan abstrak dan judul rencana skripsi ke daftar dosen berdasarkan rekam jejak penelitian mereka.

---

## 🧠 Metode dan Logika (AI Core)

Sistem ini menggunakan pendekatan Hibrida yang canggih untuk memberikan rekomendasi dosen yang akurat, dengan alur pemrosesan sebagai berikut:

* **Pendekatan Leksikal (BM25):** Menghitung skor kecocokan persis antara kata pada input mahasiswa dan profil dosen menggunakan pembobotan berbasis TF-IDF.
* **Pendekatan Semantik (SBERT):** Mengonversi teks ke dalam matriks vektor untuk mengevaluasi jarak kesamaan makna (*Cosine Similarity*) sehingga topik relevan tetap terdeteksi meski kosakatanya berbeda.
* **Pembobotan Hibrida Adaptif:** Sistem memanfaatkan nilai *Inverse Document Frequency* (IDF) secara dinamis.
* **Peningkatan Bobot Otomatis:** Bobot Leksikal akan ditingkatkan jika kueri mengandung istilah teknis atau langka, dan bobot Semantik ditingkatkan jika kueri menggunakan bahasa umum.
* **Pemeringkatan Akhir:** Sistem menggabungkan kedua perhitungan tersebut menjadi *Hybrid Score* lalu mengurutkan hasilnya secara menurun.
* **Optimalisasi dan Caching Vektor:** Sistem melakukan komputasi matriks SBERT dan menyimpannya secara lokal menggunakan file `.npy`.
* **Peningkatan Kecepatan:** Hal ini memangkas waktu *booting* peladen secara radikal dari sekitar 30 menit menjadi hanya 0.1 detik.
* **Validasi Keamanan Hash:** Sistem juga membangkitkan file `.fingerprint` berbasis *hash* (MD5) untuk mendeteksi apabila ada perubahan data dosen di pangkalan data sebelum memutuskan untuk membangun ulang matriks.

---

## 🏗️ Layer Aplikasi

Arsitektur sistem dibangun di atas kerangka kerja *Full-Stack* (Vue.js dan Flask) dengan prinsip *Separation of Concerns* (SoC):

* **Layer Antarmuka Pengguna (Frontend - Vue.js):** Berada di direktori `client/`, menangani stat animasi visualisasi proses pemikiran AI, pencarian *real-time*, dan paginasi sisi klien agar tidak membebani server. Komunikasi HTTP ke *backend* dijembatani oleh file `api.js`.
* **Layer API (Backend - Flask Python):** Berada di `app.py`, mengekspos *endpoint* seperti `/api/rekomendasi` dan mengimplementasikan *multithreading* di latar belakang saat memuat model AI. Isu *race condition* telah diperbaiki sehingga server akan secara elegan mengembalikan status HTTP 503 jika diakses sebelum model siap.
* **Layer Kecerdasan Buatan (AI Core):** Terisolasi di file `rekomendasi.py`, mengelola prapemrosesan teks seperti ekspansi kueri dan penghapusan *stopwords*, proses *AdaptiveWeighting*, serta perhitungan matriks vektor menggunakan *Min-Max Scaling*.
* **Layer Pangkalan Data:** Berfokus pada direktori `database/`, beralih ke arsitektur relasional (MySQL) untuk efisiensi CRUD. File Excel kini murni digunakan sebagai penyemai cadangan (*seeder*) otomatis apabila koneksi MySQL gagal atau tabel masih kosong.
* **Layer Keamanan (Autentikasi):** Sistem memiliki modul `auth.py` yang menggunakan pustaka `flask-jwt-extended` untuk manajemen *JSON Web Tokens* (JWT) dan `werkzeug.security` untuk enkripsi kata sandi guna mengamankan jalur API.

---

## 🛠️ Cara Instalasi & Menjalankan Aplikasi

**Persyaratan Sistem:**
* Python 3.9 atau lebih baru.
* Node.js v16 atau lebih baru.
* XAMPP / MySQL Server.

### Langkah 1: Setup Pangkalan Data (Database) & Autentikasi
1. Nyalakan modul MySQL melalui aplikasi XAMPP.
2. Buka phpMyAdmin di peramban, lalu buat database baru dengan nama `db_siredo`.
3. Masuk ke direktori `server/database` lalu jalankan skrip `python migrate.py` untuk mengekstrak data dari Excel menjadi baris SQL secara otomatis. **Catatan:** Migrasi ini juga mendaftarkan akun admin *default* dengan sandi terenkripsi menggunakan `werkzeug.security`.

### Langkah 2: Menyalakan Peladen AI (Backend)
1. Buka Terminal baru dan masuk ke dalam folder `server`.
2. Aktifkan *virtual environment* Python dengan perintah `.venv\Scripts\activate`.
3. Instal semua pustaka dan dependensi (termasuk modul JWT dan MySQL) menggunakan `pip install -r requirements.txt`.
4. Nyalakan mesin peladen utama dengan mengeksekusi `python app.py`. **Catatan *Cold Start*:** Saat pertama kali menyala, AI membutuhkan waktu komputasi untuk merangkum vektor matriks menjadi *cache* `vektor_dosen.npy` dan `vektor_dosen.npy.fingerprint`, namun *booting* ke depannya hanya memakan waktu 0.1 detik.

### Langkah 3: Menyalakan Antarmuka Pengguna (Frontend)
1. Buka Terminal baru dan arahkan ke folder `client`.
2. Instal dependensi antarmuka sistem dengan menjalankan `npm install`.
3. Jalankan server lokal antarmuka web dengan perintah `npm run dev`.
4. Buka tautan di peramban web Anda (umumnya `http://localhost:5173` atau sesuai info terminal) untuk melihat dan menggunakan SIREDO secara langsung.