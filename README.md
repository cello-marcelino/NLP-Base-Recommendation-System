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

### 1. Menjalankan Backend (Server)
Pastikan Python 3.9+ telah terpasang.
```bash
cd server
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python run.py
```
Backend akan berjalan di `http://localhost:5000`

### 2. Menjalankan Frontend (Web)
Pastikan Node.js (versi 16+) telah terpasang.
```bash
cd web
npm install
npm run dev
```
Frontend akan berjalan di `http://localhost:5173`

## Fitur Utama
1. **Single Recommendation**: Analisis proposal secara detail beserta *Explainable AI* (XAI) yang memperlihatkan alasan mengapa dosen tertentu direkomendasikan.
2. **Batch Recommendation**: Proses banyak data sekaligus menggunakan unggahan file Excel. Sangat membantu dalam menjadwalkan alokasi dosen pembimbing/penguji secara massal.
3. **Konfigurasi Global**: Atur ambang batas (Threshold), panjang token, serta mode AI (Adaptif vs Manual) langsung dari antarmuka Web tanpa menyentuh kode.

---
*Dibuat untuk memudahkan penentuan dosen pembimbing maupun penguji dengan pendekatan AI yang cerdas dan transparan.*
