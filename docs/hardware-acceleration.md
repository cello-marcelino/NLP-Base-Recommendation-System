# Akselerasi Hardware (GPU & CPU) — SiReDo v3

Dokumentasi ini menjelaskan modul-modul Python pada SiReDo v3 yang mendukung akselerasi hardware berbasis Graphical Processing Unit (GPU), komparasi karakteristik performa antara CPU dan GPU, mekanisme konfigurasi flag, serta panduan instalasi/setup untuk lingkungan CPU-only vs GPU.

---

## 1. Modul Python yang Mendukung Akselerasi GPU

SiReDo memanfaatkan arsitektur Deep Learning (Transformer) untuk pencocokan semantik dan ekstraksi topik Explainable AI (XAI). Modul-modul berikut mendukung akselerasi hardware via NVIDIA CUDA (PyTorch):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DEEP LEARNING & GPU-ENABLED STACK                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. sentence-transformers  : Model paraphrase-multilingual-MiniLM-L12-v2   │
│  2. keybert                : Ekstraksi Topik Semantik Dosen (XAI Layer)     │
│  3. transformers           : Hugging Face Transformer Neural Architecture    │
│  4. PyTorch (torch)        : Tensor Computation & CUDA Acceleration Engine  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Rincian Peran Modul:

| Modul | Komponen SiReDo | Operasi Komputasi Berat | Dukungan GPU |
|---|---|---|---|
| **`torch` (PyTorch)** | Backend Komputasi Tensor | Eksekusi operasi matriks perkalian dense, forward pass neural network, dan alokasi memory GPU (VRAM) | **Penuh (NVIDIA CUDA / ROCm / Apple MPS)** |
| **`sentence-transformers`** | [`SBERTEngine`](server/src/services/nlp/sbert_engine.py) | Meng-encode teks korpus profil dosen dan teks query proposal ke dalam vektor dense 768 dimensi | **Penuh** (Otomatis dialokasikan ke GPU) |
| **`keybert`** | [`SBERTEngine`](server/src/services/nlp/sbert_engine.py) | Ekstraksi frasa kunci representatif kandidat dosen menggunakan cosine similarity embedding frasa n-gram | **Penuh** |
| **`transformers`** | Layer Arsitektur SBERT | Multi-Head Self-Attention layers dan Feed-Forward Network | **Penuh** |

---

## 2. Modul Non-GPU (Berjalan Murni di CPU)

Tidak seluruh komponen pipeline NLP memerlukan atau diuntungkan oleh GPU. Komponen berikut murni berjalan di CPU secara optimal:

| Modul | Alasan Berjalan di CPU |
|---|---|
| **`rank-bm25` (BM25Okapi)** | Algoritma leksikal berbasis *inverted index* dan penghitungan frekuensi kemunculan term (*term frequency / IDF*) yang bersifat *sparse*. Operasi ini sangat efisien di RAM/CPU dan tidak memiliki karakteristik komputasi matriks paralel masif. |
| **`preprocessor` (Regex & Stopwords)** | Operasi manipulasi string (case folding, pembersihan tanda baca, penghapusan kata hubung, n-gram) beroperasi langsung pada *CPU memory stream*. |
| **`kamus_ekspansi` (Ontologi IT)** | Pencocokan string kamus berbasis kamus hash (*dictionary hash lookup*) $O(1)$ di memori RAM. |

---

## 3. Komparasi Performa: CPU vs GPU pada Siklus SiReDo

```
                     Perbandingan Waktu Eksekusi (Benchmark Estimasi)
                     ────────────────────────────────────────────────
Operasi                                CPU Only (8-Core)        GPU (NVIDIA RTX/GTX)
────────────────────────────────────────────────────────────────────────────────────
1. Initial Corpus Warm-Up (86 Dosen)   ~15 – 30 detik           ~1 – 2 detik (15x lebih cepat)
2. Single Query Recommendation         ~20 – 35 ms              ~10 – 15 ms
3. Batch Processing (50 Proposal)      ~2.5 – 4.0 detik         ~0.3 – 0.5 detik (8x lebih cepat)
4. Batch Processing (100 Proposal)     ~5.0 – 8.0 detik         ~0.6 – 0.9 detik (10x lebih cepat)
```

### Analisis Karakteristik:

1. **Fase Inisialisasi & Warm-Up Awal (Keuntungan Terbesar GPU)**:
   - Saat database dosen baru diimpor atau cache dibersihkan (`python siredo cache:clear`), sistem harus meng-encode seluruh teks korpus dosen.
   - GPU memproses puluhan dokumen secara paralel (*batched tensor operations*), memangkas waktu kalkulasi dari puluhan detik menjadi 1–2 detik.
   - *Catatan*: Berkat arsitektur Tier-2 disk cache SiReDo (`sbert_embeddings.npy`), setelah proses warm-up selesai, pembacaan vektor berikutnya instan ($<0.1$ detik) baik pada lingkungan CPU maupun GPU.

2. **Fase Rekomendasi Single Query**:
   - Pada request tunggal, neural network hanya meng-encode 1 teks query.
   - CPU modern (Intel Core i5/i7/i9 atau AMD Ryzen) sudah sangat cepat ($20\text{--}35\text{ms}$).
   - GPU sedikit lebih cepat, namun terdapat *overhead* kecil untuk transfer tensor antara CPU RAM (*Host*) dan GPU VRAM (*Device*).

3. **Fase Rekomendasi Batch Proposal (Keuntungan Signifikan GPU)**:
   - Pada pemrosesan massal (unggahan file Excel berisi puluhan hingga ratusan judul proposal mahasiswa), GPU dapat melakukan inferensi secara paralel dalam satu kali *batch matrix multiplication*, menghasilkan peningkatan kecepatan hingga **$8\times\text{--}10\times$**.

---

## 4. Konfigurasi Flag & Kontrol Perangkat

Sistem SiReDo secara default berjalan pada **CPU** untuk menjamin kompatibilitas instan di semua perangkat tanpa memerlukan kartu grafis eksternal:

### A. Melalui Argumen Perintah CLI
```powershell
# 1. Default (CPU Mode)
python siredo serve

# 2. Aktifkan Akselerasi GPU (CUDA)
python siredo serve --device cuda

# 3. Mode Otomatis (Gunakan GPU jika ada, fallback ke CPU jika tidak ada)
python siredo serve --device auto
```

### B. Melalui File Konfigurasi `.env`
```ini
# Target komputasi AI/NLP: 'cpu' (default) | 'cuda' | 'auto'
TORCH_DEVICE=cpu
```

---

## 5. Skenario Setup Lingkungan (CPU Only vs GPU CUDA)

### Skenario A: Setup Lingkungan CPU-Only (Default)
Cocok untuk laptop standar, komputer lab tanpa kartu grafis NVIDIA, atau container server minimalis:

```powershell
# 1. Buat virtual environment
cd server
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Pasang dependensi standar
pip install -r requirements.txt
cd ..

# 3. Jalankan server SiReDo (otomatis menggunakan CPU)
python siredo serve
```

### Skenario B: Setup Lingkungan GPU (NVIDIA CUDA)
Untuk mesin dengan kartu grafis NVIDIA (GeForce GTX/RTX, Quadro, atau Tesla) dan driver CUDA terpasang:

```powershell
# 1. Buat virtual environment
cd server
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Pasang PyTorch dengan dukungan CUDA (contoh: CUDA 12.1)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 3. Pasang paket dependensi SiReDo lainnya
pip install -r requirements.txt
cd ..

# 4. Jalankan server SiReDo dengan flag --device cuda
python siredo serve --device cuda
```

*Verifikasi GPU Aktif*: Saat server menyala di foreground (`python siredo serve --device cuda --foreground`), output terminal akan menampilkan `Compute Device : CUDA`. Jika driver CUDA belum terpasang atau GPU tidak terdeteksi, sistem secara otomatis memberikan peringatan log dan melakukan *graceful fallback* ke mode CPU tanpa crash.
