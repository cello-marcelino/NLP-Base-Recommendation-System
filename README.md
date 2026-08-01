# Siredo v3 - Sistem Rekomendasi Dosen

Siredo (Sistem Rekomendasi Dosen) v3 adalah platform berbasis AI untuk memberikan rekomendasi dosen pembimbing atau penguji terbaik secara otomatis berdasarkan kecocokan abstrak dan judul penelitian/proyek. Sistem ini memadukan kemudahan penggunaan (UI yang dinamis dan premium) dengan performa model hybrid NLP mutakhir.

## Arsitektur & Teknologi (Tech Stack)

Sistem ini dibangun menggunakan arsitektur *Client-Server* terpisah:

### Web (Frontend)
- **Framework**: Vue 3 + Vite
- **Styling**: Vanilla CSS dengan desain modern dan variabel Tailwind-style (`@theme`) di `style.css`.
- **Arsitektur Direktori**: Layered Architecture
  - `src/views/`: Halaman utama aplikasi (Home, Batch, Single, Konfigurasi, Data Dosen, API Docs).
  - `src/components/`: Komponen UI modular terbagi ke dalam *layout*, *recommendation*, dan *shared*.
  - `src/services/`: Modul interaksi API (Axios).
  - `src/assets/`: Berkas statis dan CSS utama.

### Server (Backend)
- **Framework**: Python Flask
- **Machine Learning / NLP**: 
  - SBERT (Sentence-BERT) untuk analisis semantik mendalam.
  - BM25 untuk pencarian berbasis kata kunci (*keyword matching*).
  - Hybrid Engine dengan pembobotan dinamis (Adaptif α & β berdasarkan panjang token).
  - Pengekstraksi topik (KeyBERT/XAI) untuk memberi penjelasan rekomendasi (*Explainable AI*).
- **Data Storage**: 
  - `data/dataset_profiles_terintegrasi.xlsx` (Dataset utama)
  - Penyimpanan konfigurasi global berbasis JSON lokal (`storage/data/config.json`) untuk pengelolaan fleksibel (tanpa DB wajib).
- **Arsitektur Direktori**: MVC Pattern
  - `app/controllers/`: Handler *endpoints* API.
  - `app/services/`: *Business logic* dan *AI engine* (*Batch*, *Recommendation*, *NLP*).
  - `app/storage/`: Manajemen data file dan *cache* lokal.
  - `app/utils/`: Format respons dan *helper* tambahan.

## Cara Menjalankan (Development)

Proyek ini dipisahkan menjadi dua bagian utama (Backend dan Frontend). Silakan merujuk ke masing-masing direktori untuk panduan teknis yang lebih spesifik:

- [Panduan Backend / Server](./server/)
- [Panduan Frontend / Web](./web/README.md)

### Deployment & Hosting
Sistem ini telah disiapkan untuk di-deploy menggunakan kombinasi layanan modern:
- **Frontend (Web):** Menggunakan [Vercel](https://vercel.com) yang menyajikan file SPA (Single Page Application).
- **Backend (Server):** Dapat dijalankan pada server lokal yang di-ekspos ke internet publik menggunakan [Microsoft Dev Tunnels](https://learn.microsoft.com/en-us/azure/developer/dev-tunnels/get-started).

**Catatan Integrasi (VITE_API_URL):**
Saat mengonfigurasi Frontend di Vercel, *Environment Variable* `VITE_API_URL` harus diatur ke URL backend Anda dan **diakhiri dengan `/api`** (contoh: `https://siredo-server-5000.jpe1.devtunnels.ms/api`). Hal ini karena semua *route* pada Flask backend diletakkan di bawah *prefix* `/api`.

## Fitur Utama
1. **Single Recommendation**: Analisis proposal secara detail beserta *Explainable AI* (XAI) yang memperlihatkan alasan mengapa dosen tertentu direkomendasikan.
2. **Batch Recommendation**: Proses banyak data sekaligus menggunakan unggahan file Excel. Sangat membantu dalam menjadwalkan alokasi dosen pembimbing/penguji secara massal.
3. **Konfigurasi Global**: Atur ambang batas (Threshold), panjang token, serta mode AI (Adaptif vs Manual) langsung dari antarmuka Web tanpa menyentuh kode.

---
*Dibuat untuk memudahkan penentuan dosen pembimbing maupun penguji dengan pendekatan AI yang cerdas dan transparan.*
