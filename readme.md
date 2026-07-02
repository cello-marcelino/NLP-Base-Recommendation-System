# 🚀 SIREDO (Sistem Rekomendasi Dosen) - v2.0 Production Ready

SIREDO adalah mesin pencari dan sistem rekomendasi berbasis *Artificial Intelligence* (AI) dan *Natural Language Processing* (NLP). Aplikasi ini dirancang khusus untuk membantu mahasiswa menemukan dosen pembimbing skripsi yang paling relevan dengan memetakan abstrak dan judul rencana skripsi ke daftar dosen berdasarkan rekam jejak penelitian mereka.

---

## 🧠 Metode dan Logika (AI Core) - Optimized Architecture

Sistem ini menggunakan pendekatan Hibrida yang canggih dengan optimasi arsitektur **Pre-computation & O(1) Query Phase** untuk mencapai respons API dalam hitungan milidetik:

* **Pendekatan Leksikal (BM25):** Menghitung skor kecocokan persis antara kata pada input mahasiswa dan profil dosen menggunakan pembobotan berbasis TF-IDF.
* **Pendekatan Semantik (SBERT):** Mengonversi teks ke dalam matriks vektor untuk mengevaluasi jarak kesamaan makna (*Cosine Similarity*).
* **Pembobotan Hibrida Adaptif:** Sistem mengevaluasi *Inverse Document Frequency* (IDF) kueri secara dinamis untuk menentukan rasio bobot Leksikal dan Semantik.
* **Vectorized Ranking:** Pemeringkatan skor dosen tidak lagi menggunakan perulangan (*looping*) konvensional, melainkan murni menggunakan aljabar linier matriks NumPy (`np.argsort`) sehingga komputasi data berskala besar terjadi nyaris instan.
* **KeyBERT Pre-computation:** Ekstraksi frasa kunci keahlian dosen dieksekusi **hanya satu kali** saat peladen (*server*) menyala, menghilangkan beban inferensi AI saat permintaan (*query*) masuk.

---

## 🏗️ Layer Aplikasi (Backend & AI)

* **Layer API (Backend - Flask Python):** Berada di `app.py`. Menjalankan *multithreading* di latar belakang untuk melakukan prapemrosesan AI. 
* **Layer Kecerdasan Buatan (AI Core):** Terisolasi di file `rekomendasi.py`.
* **Sistem Caching Tingkat Lanjut:** Untuk mencegah *bottleneck* komputasi saat peladen dihidupkan ulang, sistem menyimpan status *(state)* AI secara lokal dalam dua format:
  1. `vektor_dosen.npy`: Menyimpan prapemrosesan matriks vektor SBERT.
  2. `keybert_dosen.json`: Menyimpan prapemrosesan ekstraksi topik keahlian dosen dari model KeyBERT.
  Sistem divalidasi menggunakan `.fingerprint` berbasis *hash* (MD5) untuk mendeteksi perubahan data di pangkalan data secara otomatis.

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