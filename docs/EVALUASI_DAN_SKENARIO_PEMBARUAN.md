# 📄 Laporan Evaluasi & Skenario Pembaruan Sistem Rekomendasi (SiReDo)

**Tanggal:** Juli 2026  
**Fokus:** Evaluasi metrik Precision@5 dari model Hybrid Scoring (BM25 + SBERT) dan perumusan skenario mitigasi teknis.

---

## 1. Evaluasi Performa (Precision@5)
Evaluasi ini dijalankan menggunakan metrik Precision@5 terhadap 3 studi kasus kueri judul dan abstrak pengajuan skripsi.

### Hasil Eksperimen:
| Kasus Uji | Topik Utama | Precision@5 | Status | Analisis Kesalahan Utama (Error Analysis) |
| :--- | :--- | :---: | :--- | :--- |
| **Kasus 1** | Deep Learning / AI | **0.60** | ⚠️ Suboptimal | Kata kunci spesifik pada abstrak seperti *"citra digital"* menyebabkan model semantik (SBERT) menarik dosen di bidang E-Learning dan Multimedia ke Top-5, menyingkirkan dosen inti AI. |
| **Kasus 2** | Sistem Informasi / Web | **0.60** | ⚠️ Suboptimal | Ada irisan istilah umum (misal: "Sistem"). Dosen *Machine Learning* yang sesekali memiliki proyek "Sistem Deteksi" ikut terambil, menunjukkan ambiguitas semantik pada kata-kata umum. |
| **Kasus 3** | Jaringan Komputer / SDN | **0.80** | ✅ Cukup Baik | Kata *"Software"* pada *Software Defined Network* memicu dosen *Software Engineering* (RPL) masuk rekomendasi. Model semantik pre-trained (multilingual) gagal memahami *SDN* sebagai entitas Jaringan secara utuh. |

---

## 2. Kesimpulan Kegagalan (*Failure Points*)
Model Hybrid saat ini terlalu mudah terdistraksi (*Noise Susceptible*) akibat:
1. **Tidak adanya batas toleransi leksikal (Hard Constraints)**: Dosen yang secara riwayat/bidang keahlian sama sekali tidak berkaitan dengan topik inti, bisa muncul hanya karena ada kemiripan pada tingkat abstrak kalimat.
2. **Keterbatasan Pemahaman Istilah Teknis Lokal**: SBERT (*paraphrase-multilingual-MiniLM-L12-v2*) menggunakan corpus umum, sehingga sering keliru mengkorelasikan istilah spesifik (Contoh: *SDN* diartikan dekat dengan *Software Development*, bukan *Computer Networks*).

---

## 3. Skenario Pembaruan Teknis (Actionable Scenarios)
Berikut adalah langkah-langkah presisi yang **siap untuk dieksekusi** pada iterasi kode berikutnya (terutama di `app/services` atau `run.py` pada backend):

### 🛠️ Skenario A: Implementasi Hard Filter (Pruning Leksikal)
* **Tujuan**: Memastikan dosen memiliki keterkaitan leksikal dasar sebelum diproses secara semantik.
* **Instruksi Eksekusi**:
  1. Pada fungsi agregasi skor (hybrid), jalankan `bm25.get_scores(query)` terlebih dahulu.
  2. Tetapkan nilai *threshold* (contoh: persentil ke-25 atau skor absolut `> 0`).
  3. Filter daftar kandidat dosen. Jika skor BM25 seorang dosen = 0 (tidak ada satupun kata kunci yang cocok), **drop dosen tersebut** dari perhitungan *Cosine Similarity* SBERT.
  4. Lanjutkan penghitungan SBERT hanya untuk kandidat yang lolos tahap filter.
* **Pseudo-code**:
  ```python
  raw_bm25 = bm25_weighted.get_scores(query_tokens)
  # Filter index dengan skor > 0
  valid_indices = np.where(raw_bm25 > 0)[0] 
  
  # Lakukan cosine similarity hanya untuk valid_indices
  corpus_embs_filtered = corpus_embs[valid_indices]
  s_sbert = cosine_similarity(query_emb, corpus_embs_filtered)[0]
  # Kalkulasi Hybrid ...
  ```

### 🛠️ Skenario B: Adaptive Hybrid Weighting (Alpha Dinamis)
* **Tujuan**: Menyesuaikan bobot BM25 ($\alpha$) dan SBERT berdasarkan panjang pendeknya *query*.
* **Instruksi Eksekusi**:
  1. Buat fungsi evaluasi panjang *query* (berdasarkan jumlah karakter atau token).
  2. Jika *query* sangat pendek (mirip kata kunci pencarian biasa, `< 15 kata`), gunakan BM25 lebih dominan ($\alpha = 0.7$).
  3. Jika *query* panjang (berupa proposal/abstrak utuh, `> 15 kata`), gunakan SBERT lebih dominan ($\alpha = 0.35$).
* **Pseudo-code**:
  ```python
  num_tokens = len(query_tokens)
  if num_tokens < 15:
      alpha, beta = 0.7, 0.3 # Fokus pada keyword matching
  else:
      alpha, beta = 0.35, 0.65 # Fokus pada semantic context
  ```

### 🛠️ Skenario C: Ekspansi Corpus dan Domain Specific Fine-Tuning
* **Tujuan**: Membantu SBERT memahami kosakata teknis spesifik jurusan Informatika.
* **Instruksi Eksekusi**:
  1. **Quick Fix**: Perluas variabel `KAMUS_EKSPANSI` di backend. Tambahkan singkatan spesifik seperti `{"sdn": ["software defined network", "jaringan", "routing", "cisco"]}` agar proses BM25 lebih kaya.
  2. **Long-Term**: Kumpulkan data 500+ judul/abstrak skripsi TI sebelumnya beserta dosen pembimbingnya. Gunakan pustaka `sentence-transformers` dengan *MultipleNegativesRankingLoss* untuk melakukan *Fine-Tuning* terhadap bobot model `MiniLM-L12-v2`.

### 🛠️ Skenario D: Penalty Scoring berdasarkan *Out-of-Domain*
* **Tujuan**: Memberikan pinalti (-skor) kepada dosen yang keahliannya sangat bertolak belakang dengan *keyword* dominan yang terdeteksi.
* **Instruksi Eksekusi**:
  1. Buat sistem deteksi label pada input (contoh: kueri berlabel "Sistem Informasi").
  2. Jika label utama kueri berbeda jalur (misal kueri adalah "Jaringan Komputer", namun bidang keahlian dosen murni "RPL / Web"), berikan penalti sebesar `0.2` pada skor akhir hybrid.
