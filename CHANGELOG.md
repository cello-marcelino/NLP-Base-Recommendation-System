# Changelog - Siredo v3

## [3.0.0] - 2026-07-31

### 🔥 Major Updates & Open Source Vision
Siredo v3 secara resmi dirilis ulang dan direstrukturisasi dari versi-versi sebelumnya untuk menjadi **Web Documented Version**. Pembaruan ini merupakan langkah besar dalam menjadikan Siredo sebagai **Open Source Sistem Rekomendasi Dosen** pertama dan terlengkap, khususnya untuk lingkungan akademik Politeknik Negeri Batam.

Versi ini merombak total antarmuka (UI) dan arsitektur (Backend) agar tidak hanya berfungsi sebagai aplikasi, melainkan sebagai platform pembelajaran dan integrasi yang menyediakan **API terstruktur yang lengkap dan terdokumentasi**. Pengembang maupun institusi akademik lain kini dapat dengan mudah mempelajari, menggunakan, maupun mengintegrasikan sistem *Hybrid NLP* (BM25 + SBERT) ini ke dalam infrastruktur internal mereka sendiri.

### ✨ Fitur Baru & Peningkatan
- **Layered Architecture & Clean Code**: Refaktor besar-besaran untuk memisahkan logika antarmuka (*Client/Web*) dan logika mesin cerdas (*Server/Backend*).
- **Interactive API Documentation Page**: Penyediaan halaman Web interaktif khusus yang mendokumentasikan setiap rute REST API (Single Recommendation, Batch Processing, Data Dosen, System Stats, dan Config).
- **Unified Global Configuration**: Parameter krusial seperti Top K-Rank, ambang batas kesamaan (Threshold), serta opsi Mode AI Adaptif (Hybrid Alpha/Beta tuning otomatis) kini diatur secara terpusat tanpa perlu mengubah satu baris kode pun.
- **Explainable AI (XAI)**: Setiap hasil rekomendasi kini menyertakan rincian transparan (pencocokan kata kunci dan penanda topik SBERT) yang memudahkan dewan prodi memahami *mengapa* seorang dosen direkomendasikan.
- **Premium User Interface**: Modernisasi UI berbasis Vue 3 dengan paduan estetika warna premium, responsivitas penuh, serta pemisahan komponen spasial.

Siredo v3 membuka pintu lebar-lebar bagi kontributor open-source. Semua siap digunakan, dipelajari, dan dikembangkan!
