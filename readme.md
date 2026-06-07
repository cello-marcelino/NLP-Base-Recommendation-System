======================================================================
README - SISTEM REKOMENDASI DOSEN PEMBIMBING TA
======================================================================

Sistem rekomendasi ini menggunakan metode BM25 (Leksikal) dan SBERT (Semantik) untuk mencocokkan Judul dan Abstrak Tugas Akhir mahasiswa dengan riwayat jurnal dosen. 

Sistem dibangun menggunakan arsitektur terpisah:
- Front-end (Klien): Vue.js, Vite, Tailwind CSS v4
- Back-end (Peladen): Python Flask

STRUKTUR FOLDER UTAMA
----------------------------------------------------------------------
sistem_rekomendasi/
|-- client/               (Folder antarmuka web)
|-- server/               (Folder API dan mesin AI)
|   |-- dataset_dosen.csv (File data riwayat dosen)
|-- jalankan_sistem.bat   (Skrip jalan pintas)


PERSIAPAN & INSTALASI
----------------------------------------------------------------------
Pastikan komputer Anda sudah terinstal Python dan Node.js.

1. Instalasi Backend
Buka terminal, arahkan ke folder "server", buat dan aktifkan virtual environment (env), lalu jalankan perintah instalasi dalam satu baris berikut:
pip install flask flask-cors pandas rank-bm25 sentence-transformers scikit-learn requests openpyxl

2. Instalasi Frontend
Buka terminal, arahkan ke folder "client", lalu jalankan perintah instalasi berikut:
npm install vue-router tailwindcss @tailwindcss/vite


CARA MENJALANKAN APLIKASI
----------------------------------------------------------------------
Anda tidak perlu lagi mengetik perintah manual. Cukup gunakan file jalan pintas yang sudah disediakan:

1. Pastikan Anda berada di direktori root (sistem_rekomendasi).
2. Klik ganda (2x) pada file "recommendation_system.bat".
3. Skrip tersebut akan otomatis membuka dua jendela terminal baru dan menjalankan Backend serta Frontend secara bersamaan.
4. Tunggu beberapa saat, lalu buka alamat http://localhost:5173 di web browser Anda.


CATATAN PENTING
----------------------------------------------------------------------
- Saat Backend dijalankan untuk pertama kalinya, sistem akan mengunduh model bahasa AI SBERT (sekitar 400MB). Pastikan internet stabil pada percobaan pertama.
- Untuk mematikan aplikasi, cukup tutup (silang) kedua jendela terminal hitam yang terbuka oleh file .bat tersebut, atau tekan Ctrl + C di masing-masing terminal.
======================================================================