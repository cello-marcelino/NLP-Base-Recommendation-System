# NLP Recommendation Quality - Audits & Fixes

Direktori ini berisi riwayat lengkap dari pengujian, audit kualitas, dan catatan perbaikan (changelog) untuk mesin rekomendasi NLP berbasis Hybrid (BM25 + SBERT).

## Siklus Audit & Perbaikan (Agustus 2026)

Proses optimalisasi dilakukan dalam beberapa tahap iteratif: Pengujian kualitas awal, perbaikan algoritma, dan pengujian ulang.

### 1. Temuan Masalah (Issue)
* **Dokumen:** [`issue-recommendation-quality.md`](./issue-recommendation-quality.md)
* **Deskripsi:** Merupakan audit komprehensif pertama terhadap output model (berdasarkan data `recommendation_top5_results.json`). Menemukan beberapa *false-positive* yang fatal (misal: dosen animasi 3D direkomendasikan pada tesis DSS karena bias leksikal).
* **Temuan Utama:**
  * Pengaruh skor SBERT tenggelam karena dominasi skor BM25.
  * Stopword teknis/akademis ("menggunakan", "berbasis", "sistem") belum difilter.
  * Kamus ekspansi kurang kaya.

### 2. Implementasi Perbaikan (Fix)
* **Dokumen:** [`fix-recommendation-quality.md`](./fix-recommendation-quality.md)
* **Deskripsi:** Catatan teknis perbaikan arsitektur dan algoritma yang merespon temuan Issue di atas. Perbaikan ini diuji menggunakan suite otomatis (PyTest) melalui test case integrasi dan unit.
* **Perbaikan Utama:**
  * Penambahan 12 stopword teknis.
  * Implementasi *Min-Max Normalization* pada skor BM25 dan SBERT sehingga rentangnya berimbang di `[0, 1]`.
  * Deduplikasi *n-gram* dan perbaikan threshold.
  * Normalisasi data (bidang keahlian dosen) saat import dataset.
* **Test Suite:** Perubahan ini menyebabkan penyesuaian pada 34 unit & integration test untuk memastikan tidak ada regresi dan batas threshold berjalan dengan benar.

### 3. Validasi & Pengujian Ulang (Validation)
* **Dokumen:** [`validation-recommendation-quality.md`](./validation-recommendation-quality.md)
* **Deskripsi:** Hasil evaluasi ulang setelah perbaikan di atas diterapkan dan dataset di-*rebuild*.
* **Hasil Akhir:**
  * *False-positive* berhasil dieleminasi sepenuhnya.
  * Kualitas ranking membaik secara drastis, dengan pakar AI, Cyber Security, dan DSS yang tepat berada di Rank 1 pada skenario pengujiannya masing-masing.

## Struktur Direktori

```text
docs/audits/
├── README.md                              # Indeks dan ringkasan audit
├── issue-recommendation-quality.md        # Laporan temuan masalah (Issue)
├── fix-recommendation-quality.md          # Changelog perbaikan teknis (Fix)
└── validation-recommendation-quality.md   # Laporan validasi setelah perbaikan (Validation)
```

Semua pengujian dan laporan kualitas pada direktori ini dilakukan dengan prinsip observabilitas dan validasi berbasis data sebelum model NLP dinaikkan ke lingkungan produksi.
