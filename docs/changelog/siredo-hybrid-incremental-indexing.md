# SiReDo Hybrid Incremental Indexing Changelog

Dokumen ini merangkum penyelesaian masalah performa kritis pada operasi CRUD (Create, Read, Update, Delete) dosen di aplikasi SiReDo, akar masalah (bottleneck pipeline NLP), solusi arsitektural yang diimplementasikan, dan perbandingan performa akhir.

---

## 1. Problem (Masalah pada Versi Sebelumnya)

Saat pengguna (Admin) melakukan manipulasi data dosen (baik itu Tambah, Edit, atau Hapus dosen), server mengalami *freeze* (membeku) hingga beberapa menit sebelum memberikan respons. Proses CRUD terasa sangat lambat dan memberatkan server. 

### Detail & Akar Masalah Utama:

1. **Full Rebuild NLP Pipeline**: Setiap operasi CRUD memanggil `CacheService.get_instance().initialize_cache(force_refresh=True)`. Hal ini memicu "Warm-up" ulang secara total yang melibatkan:
   - Pemanggilan ulang seluruh 89 data dosen dari database.
   - Pembangunan ulang korpus teks untuk seluruh dosen.
   - Pembangunan ulang indeks lexikal (BM25) secara penuh.
   - **Proses encoding SBERT untuk ke-89 dosen ulang dari nol**, memakan waktu ~5-15 detik.
   - **Ekstraksi KeyBERT (XAI) untuk ke-89 dosen ulang dari nol secara sekuensial**, memakan waktu ~1 hingga 5 menit.
2. **Stale SBERT Embedding Bug**: Pada operasi **Update/Edit**, meskipun admin mengubah spesifikasi dosen (misalnya mengubah Bidang Keahlian), karena jumlah total dosen tetap sama (`len(embeddings) == len(corpus_texts)`), kode di `SBERTEngine` langsung memuat cache `.npy` lama dari disk tanpa menghitung ulang. Akibatnya:
   - Operasi edit **TIDAK** memperbarui embedding SBERT dosen tersebut.
   - Sistem rekomendasi tetap menggunakan representasi semantik lama (stale cache) sampai admin menekan "Reset Cache" manual.
3. **Imbas Performa pada Testing**: Menjalankan 1 test skenario siklus CRUD dosen (`test_admin_dosen_crud.py`) memakan waktu hingga **1281 detik (21 Menit)** karena mesin ML melakukan komputasi *full rebuild* 4 kali berturut-turut.

---

## 2. Solution (Perubahan yang Dilakukan & Pengaruhnya)

Untuk mengatasi bottleneck dan bug tersebut, arsitektur diubah dari **Full Rebuild** menjadi **Hybrid Incremental Indexing**.

| Komponen Terpengaruh | Apa yang Diubah? | Kenapa Diubah? | Bagaimana Pengaruhnya? |
|---|---|---|---|
| **`cache_service.py`** | Menambahkan metode `incremental_add`, `incremental_update`, `incremental_delete`. | Memungkinkan cache diperbarui per-record tanpa merobohkan seluruh indeks in-memory yang sudah ada. | Manipulasi data dosen menjadi instan karena operasi iteratif berat (seperti ekstraksi KeyBERT) hanya dilakukan pada **1 dosen**, bukan 89 dosen. |
| **`sbert_engine.py`** | 1. Memperbaiki bug validasi `force_refresh` saat me-load `.npy`.<br>2. Menambahkan `add_single_embedding`, `update_single_embedding`, dan `delete_single_embedding`. | Memperbaiki masalah stale embedding. Men-support modifikasi *row-wise* pada matrix NumPy `corpus_embeddings` secara aman (append, modify, delete). | Perubahan keahlian dosen kini langsung terefleksi ke embedding SBERT secara realtime. |
| **`admin_dosen_controller.py`** | Mengganti trigger `initialize_cache(force_refresh=True)` menjadi pemanggilan `incremental_add`, `incremental_update`, dan `incremental_delete` secara parsial. | Mengeliminasi beban komputasi masif tiap operasi CRUD. | Response API kembali normal (<3 detik). Server tidak lagi mengalami RAM & CPU *spike*. |

> *Catatan Arsitektur: Proses pembangunan BM25 tetap dipertahankan full-rebuild karena *engine* `rank_bm25` tidak mendukung penambahan IDF dokumen secara inkremental. Namun beban komputasinya sangat ringan (~0.1 detik untuk 89 dosen), sehingga tetap digolongkan hybrid yang efisien.*

---

## 3. Result (Hasil Akhir Perubahan)

Penerapan *Hybrid Incremental Indexing* sukses memangkas waktu komputasi secara radikal dengan skala perbaikan ~80-100x lipat kecepatan operasi sebelumnya.

### Ringkasan Hasil Akhir:
- **Respon CRUD Instan**: Menyelesaikan operasi CRUD dalam rentang waktu **~0.8 hingga 3.5 detik**, turun secara masif dari **65 - 315 detik**.
- **Bug Stale Embeddings Tuntas**: Dosen yang di-edit secara spesifik akan di-*re-encode* embedding-nya lalu ditimpa ke matrix utama. Hasil rekomendasi langsung merefleksikan keahlian barunya.
- **Dampak pada Test Suite**:
  - Test skenario siklus penuh CRUD Dosen (`test_admin_dosen_crud_full_lifecycle`) kini memakan waktu **15.64 detik** (turun tajam dari **1281 detik**!).
  - **Keseluruhan Test Project** (35 test) kini diselesaikan dalam rekor **19.44 detik**.

---

## Kesimpulan
Pergeseran ke pendekatan pembaruan indeks inkremental berhasil menyelesaikan *bottleneck* performa sistem secara permanen. Pengguna admin kini dapat memodifikasi data sebanyak mungkin tanpa harus membekukan komputasi web server.
