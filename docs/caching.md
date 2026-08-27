# Arsitektur Caching Layer — SiReDo v3

Dokumentasi ini menjelaskan secara mendalam desain **Multi-Tier Caching Layer** yang memungkinkan SiReDo v3 menghasilkan rekomendasi dosen secara instan (sub-50ms) tanpa membebani database dan tanpa melakukan kalkulasi ulang model Transformer pada setiap request.

---

## 1. Motivasi & Kebutuhan Caching

Dalam sistem temu balik informasi berbasis Deep Learning (*Sentence-BERT*), operasi ekstraksi fitur vektor (forward pass neural network) terhadap puluhan profil dosen membutuhkan komputasi CPU/GPU yang signifikan jika dilakukan secara on-the-fly pada setiap request pengguna.

Caching Layer pada SiReDo dirancang untuk:
1. **Menghilangkan Latensi Model Transformer**: Komputasi embedding korpus dosen hanya dilakukan satu kali, bukan berulang-ulang di setiap query.
2. **Menghilangkan Beban Query Database Berulang**: Data rekam jejak akademik dosen siap pakai langsung dari memori RAM.
3. **Mencapai Waktu Respon Sub-50ms**: Menggabungkan pencarian BM25 in-memory dengan komputasi vektor tensor SIMD Cosine Similarity berkecepatan tinggi.

---

## 2. Arsitektur Caching Dua Lapis (Multi-Tier Caching)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      TIER 1: IN-MEMORY SINGLETON CACHE                      │
│                                (CacheService)                               │
│  - In-Memory Dosen Object Models (RAM)                                      │
│  - Fitted BM25 Inverted Index & Token Tables                                │
│  - In-Memory Preloaded SBERT PyTorch Tensor Embeddings                      │
│  - In-Memory KeyBERT Topik Cache                                            │
│  - Thread-Safe Reentrant Lock (threading.RLock)                             │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │ Load Instan saat Startup (<0.5s)
                                       │ / Simpan saat Warm-up
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                       TIER 2: PERSISTENT DISK CACHE                         │
│                           (server/storage/cache/)                           │
│  - sbert_embeddings.npy  : Matriks biner NumPy vektor 768-D dense           │
│  - keybert_dosen.json     : Metadata topik ekstraksi XAI KeyBERT            │
│  - dosen_data.pkl         : Snapshot serialisasi objek profil dosen         │
└──────────────────────────────────────▲──────────────────────────────────────┘
                                       │ Invalidation / Regen
┌──────────────────────────────────────┴──────────────────────────────────────┐
│                         SOURCE OF TRUTH (DATABASE)                          │
│               Database Relasional SQLite / MySQL / Master Dataset           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Komponen & Detail Artefak Cache

### A. Tier 1: In-Memory Cache ([`server/src/services/system/cache_service.py`])

Dikelola sebagai **Thread-Safe Singleton** di memori aplikasi:

| Objek di Memori | Tipe Data | Deskripsi |
|---|---|---|
| `dosen_list` | `List[Dosen]` | Seluruh entitas profil dosen lengkap beserta riwayat publikasi & bimbingan |
| `bm25.bm25` | `BM25Okapi` | Inverted index leksikal siap query dengan token term frequency terhitung |
| `sbert.corpus_embeddings` | `np.ndarray (N × 768)` | Matriks embedding dense seluruh korpus dosen siap kalkulasi Cosine Similarity |
| `sbert.keybert_data` | `List[List[Tuple]]` | Daftar kata kunci topik dosen untuk pengayaan metadata XAI |
| `is_ready` | `bool` | Flag status kesiapan cache untuk health check |

### B. Tier 2: Disk Cache Storage (`server/storage/cache/`)

| File Cache | Format | Peran & Alasan Penggunaan |
|---|---|---|
| `sbert_embeddings.npy` | NumPy Binary | Menyimpan matriks tensor float32. Format biner NumPy memungkinkan pemuatan memori ultra-cepat (*memory-mapped I/O*) tanpa overhead parsing teks |
| `keybert_dosen.json` | JSON UTF-8 | Menyimpan daftar topik XAI hasil ekstraksi KeyBERT agar tidak perlu menjalankan algoritma MaxSum/MMR di setiap request |
| `dosen_data.pkl` | Python Pickle | Snapshot serialisasi model Python untuk pemulihan instan saat inisialisasi cepat |

---

## 4. Siklus Hidup & Alur Kerja Cache (Cache Lifecycle)

### A. Proses Warm-Up Saat Server Dimulai (`_warm_up`)

Saat perintah `python siredo serve` dijalankan, server secara otomatis menjalankan prosedur inisialisasi 5 tahap:

```
[1/5] Memuat Data Dosen dari Database
      └── Ambil data dari SQLite/MySQL via CompositeDosenRepository.
[2/5] Konstruksi Korpus & Preprocessing Teks
      └── Pembangunan teks terbobot (Bidang Keahlian ×5, Jurnal ×2, Riwayat ×1).
[3/5] Fitting BM25 Engine
      └── Tokenisasi n-gram dan fitting inverted index BM25Okapi.
[4/5] Menyiapkan SBERT & KeyBERT Engine
      ├── Cek keberadaan sbert_embeddings.npy di disk:
      │   ├── JIKA ADA: Muat langsung via np.load (< 0.1 detik).
      │   └── JIKA BELUM ADA: Lakukan encoding neural network dan simpan ke disk.
      └── Cek keberadaan keybert_dosen.json di disk (muat atau regenerasi).
[5/5] Menyimpan Snapshot Memori & Set is_ready = True
      └── Server siap menerima request rekomendasi (Health check -> 200 OK).
```

### B. Alur Eksekusi Rekomendasi Instan (Runtime Execution)

Ketika request `POST /api/recommendations` masuk:
1. **Preprocessing Query**: Membersihkan teks masukan dan tokenisasi ($< 2\text{ms}$).
2. **Ekspansi Sinonim**: Pencocokan kamus ontologi in-memory ($< 1\text{ms}$).
3. **BM25 In-Memory Lookup**: Menghitung skor leksikal dan menerapkan *Hard Constraint Pruning* ($< 5\text{ms}$).
4. **Vektorisasi Query Tunggal**: Sentence-BERT hanya meng-encode 1 query masukan ($15\text{--}25\text{ms}$).
5. **In-Memory Cosine Similarity**: Mengalikan vektor query terhadap baris kandidat pada matriks embedding yang sudah ada di RAM via operasi vektor SIMD ($< 2\text{ms}$).
6. **Adaptive Top-K Argpartition**: Perangkingan $O(n + k \log k)$ ($< 1\text{ms}$).
7. **XAI Lookup**: Pengambilan topik dari cache in-memory ($< 1\text{ms}$).

> **Total Waktu Pemrosesan**: Rata-rata **$20\text{--}40\text{ms}$** per request, dibandingkan $\ge 1500\text{ms}$ jika tanpa caching layer.

---

## 5. Strategi Invalidasi & Pembaruan Cache (Cache Invalidation)

Untuk menjaga konsistensi antara data di Database/Dataset dengan data di Caching Layer:

```
                       Event Pembaruan Data
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
Skenario 1: Hot Reload (Tanpa Restart)    Skenario 2: Hard Cache Reset
─────────────────────────────────────     ────────────────────────────
1. Admin update konfigurasi / DB          1. python siredo cache:clear
2. python siredo reload                   2. python siredo db:import
   (atau POST /api/system/reload)         3. python siredo serve
3. In-memory cache di-refresh langsung    4. Cache disk di-generate ulang
```

### 1. Hot Reload via API / CLI
- **Perintah CLI**: `python siredo reload`
- **Endpoint**: `POST /api/system/reload` (terotentikasi `X-API-Key`)
- **Mekanisme**: Memanggil `CacheService.get_instance().initialize_cache(force_refresh=True)`, memuat ulang data dari database, dan memperbarui inverted index BM25 di RAM tanpa *downtime*.

### 2. Pembersihan Disk Cache
- **Perintah CLI**: `python siredo cache:clear`
- **Mekanisme**: Menghapus seluruh file `.npy`, `.json`, dan `.pkl` di `server/storage/cache/`. Pada eksekusi berikutnya, sistem otomatis meng-generate ulang embedding baru dari database.

---

## 6. Ketahanan Sistem & Graceful Degradation

1. **Proteksi Akses Sebelum Siap (*Warm-Up Guard*)**:
   Jika ada request rekomendasi masuk saat proses warm-up sedang berlangsung (`cache.is_ready == False`), sistem mengembalikan respon HTTP 503 `SERVICE_UNAVAILABLE` dengan pesan deskriptif dan tidak mengalami *crash*.
2. **Deteksi Perubahan Jumlah Data (*Cache Invalidation Check*)**:
   Jika file `sbert_embeddings.npy` ditemukan di disk namun jumlah barisnya tidak sesuai dengan jumlah dosen di database, SBERTEngine otomatis mendeteksi ketidakcocokan tersebut dan meregenerasi embedding baru.
3. **Penanganan Thread-Safety**:
   Inisialisasi cache dilindungi oleh `threading.RLock()` sehingga aman dari *race condition* pada lingkungan multi-threaded Flask server.
