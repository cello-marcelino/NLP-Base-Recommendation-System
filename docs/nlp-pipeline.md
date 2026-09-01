# Pipeline Natural Language Processing (NLP) — SiReDo v3

Dokumentasi ini menjelaskan secara komprehensif seluruh alur kerja, formula matematis, strategi optimasi komputasi, dan lapisan Explainable AI (XAI) pada **Hybrid NLP Recommendation Engine** SiReDo v3.

---

## 1. Ikhtisar Arsitektur Hybrid NLP

SiReDo memadukan dua paradigma Information Retrieval (IR) komplementer:
1. **Pencarian Leksikal (BM25Okapi)**: Menjamin presisi kata kunci (*exact term matching*), akronim bidang IT, dan istilah teknis khusus.
2. **Pencocokan Semantik (Sentence-BERT)**: Menangkap kedekatan makna kontekstual (*semantic similarity*) dan sinonim laten pada abstrak penelitian mahasiswa.

### Diagram Alur Pipeline End-to-End

```
                      Query Masukan (Judul & Abstrak)
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │ 1. Preprocessing & N-Gram Generation │
                 │    - Case Folding                    │
                 │    - Stopword Removal                │
                 │    - Unigram + Bigram Tokenization   │
                 └──────────────────┬───────────────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │ 2. Ekspansi Sinonim (Ontologi IT)    │
                 │    - Longest-First Matching          │
                 │    - Logging frasa yang diperluas    │
                 └──────────────────┬───────────────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │ 3. Lexical Scoring (BM25 Engine)     │
                 │    - Perhitungan Skor Mentah BM25    │
                 │    - Z-Score Sigmoid Normalization   │
                 │    - Hard Constraint Pruning         │
                 └──────────────────┬───────────────────┘
                                    │
                                    ▼
                     [Kandidat Lolos Pruning BM25]
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │ 4. Semantic Scoring (SBERT Engine)   │
                 │    - Encoding Query ke Vektor 768-D  │
                 │    - Cosine Sim vs Vektor Dosen      │
                 └──────────────────┬───────────────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │ 5. Adaptive Hybrid Fusion            │
                 │    - Hitung Bobot Dinamis (α & β)    │
                 │    - Skor Akhir = (α × Lex) + (β × Sem)│
                 │    - Top-K Selection O(n + k log k)  │
                 └──────────────────┬───────────────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │ 6. Lapisan Explainable AI (XAI)      │
                 │    - Irisan Kata Kunci BM25          │
                 │    - Topik Semantik KeyBERT          │
                 └──────────────────┬───────────────────┘
                                    │
                                    ▼
                      Daftar Rekomendasi + Metadata XAI
```

---

## 2. Tahap 1: Text Preprocessing & Korpus Dosen

Komponen: [`server/src/services/nlp/preprocessor.py`](server/src/services/nlp/preprocessor.py)

### A. Preprocessing Query Mahasiswa
1. **Case Folding**: Mengonversi seluruh teks menjadi huruf kecil (*lowercase*).
2. **Regex Cleansing**: Mengambil token alfanumerik dengan panjang $\ge 2$ karakter (`\b[a-z0-9]{2,}\b`) dan menghapus tanda baca.
3. **Stopword Removal**: Menyaring kata hubung umum bahasa Indonesia (misal: *dan, atau, yang, untuk, pada, ke, dari, di, dalam, adalah, dengan*).
4. **N-Gram Generation**: Menggabungkan unigram dan bigram berurutan untuk menjaga keutuhan frasa teknis dua kata:
   $$\text{Tokens} = [w_1, w_2, \dots, w_m] \cup [w_1\_w_2, w_2\_w_3, \dots, w_{m-1}\_w_m]$$
   *Contoh*: `"machine learning"` $\rightarrow$ `["machine", "learning", "machine_learning"]`.

### B. Konstruksi Korpus Dosen Terbobot
Data profil dosen dikonstruksi menjadi dua representasi teks:
1. **Teks Terbobot (untuk BM25)**: Menerapkan pengulangan berbobot (*repetition weighting*) berdasarkan tingkat otoritas domain:
   - Bidang Keahlian: Bobot $5\times$
   - Publikasi Jurnal: Bobot $2\times$
   - Judul Riwayat Bimbingan: Bobot $1\times$ (maksimal 12 judul unik)
   - Judul Riwayat Pengujian: Bobot $1\times$ (maksimal 8 judul unik)
   - Riwayat Pendidikan: Bobot $1\times$
2. **Teks Normal (untuk SBERT & KeyBERT)**: Rangkaian teks utuh tanpa duplikasi buatan untuk menjaga struktur semantik kalimat alami.

---

## 3. Tahap 2: Ekspansi Sinonim (Ontologi Domain IT)

Komponen: [`server/src/services/nlp/kamus_ekspansi.py`](server/src/services/nlp/kamus_ekspansi.py)

Untuk mengatasi kesenjangan kosakata (*vocabulary mismatch problem*), query mahasiswa dicocokkan dengan kamus ontologi sinonim domain ilmu komputer:

### Aturan Eksekusi (*Longest-First Matching*)
Frasa dicocokkan dari yang terpanjang ke yang terpendek untuk mencegah pemotongan kata parsial (*greedy matching*):

| Kategori Bidang | Frasa Kunci Target | Sinonim & Akronim Terkait |
|---|---|---|
| Natural Language Processing | `natural language processing` | `nlp`, `text mining`, `bert`, `word2vec`, `embedding`, `sentiment analysis` |
| Deep Learning | `deep learning` | `cnn`, `rnn`, `lstm`, `transformer`, `bert`, `mobilenet`, `dl`, `neural network` |
| Machine Learning | `machine learning` | `ml`, `supervised`, `unsupervised`, `klasifikasi`, `regresi`, `svm`, `random forest` |
| Decision Support System | `decision support system` | `dss`, `spk`, `ahp`, `topsis`, `saw`, `moora`, `vikor`, `promethee` |
| Computer Vision | `computer vision` | `cv`, `image processing`, `pengolahan citra`, `object detection`, `yolo` |
| Internet of Things | `internet of things` | `iot`, `sensor`, `arduino`, `raspberry`, `smart home`, `mikrokontroler` |
| Software Engineering | `software engineering` | `rpl`, `agile`, `scrum`, `sdlc`, `waterfall`, `uml`, `black box`, `white box` |
| Data Mining | `data mining` | `kdd`, `association rule`, `apriori`, `fp-growth`, `klastering`, `k-means` |
| Cyber Security | `cyber security` | `keamanan`, `kriptografi`, `aes`, `rsa`, `steganografi`, `malware`, `penetration testing` |
| Expert System | `expert system` | `sistem pakar`, `forward chaining`, `backward chaining`, `certainty factor` |

Setiap sinonim yang ditemukan ditambahkan ke query dan dicatat dalam `pipeline_logs.ekspansi` untuk transparansi XAI.

---

## 4. Tahap 3: Lexical Engine & Hard Constraint Pruning (BM25)

Komponen: [`server/src/services/nlp/bm25_engine.py`](server/src/services/nlp/bm25_engine.py)

### A. Algoritma BM25Okapi
Skor relevansi leksikal dihitung menggunakan formula standar Okapi BM25:
$$\text{BM25}(D, Q) = \sum_{t \in Q} \text{IDF}(t) \cdot \frac{f(t, D) \cdot (k_1 + 1)}{f(t, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
*Parameter default*: $k_1 = 1.5$, $b = 0.75$.

### B. Normalisasi Sigmoid Z-Score
Skor mentah BM25 memiliki rentang tak terbatas ($[0, \infty)$) yang bervariasi tergantung panjang dokumen. Untuk menyelaraskannya dengan rentang skor SBERT ($[0, 1]$), diterapkan **Z-Score Sigmoid Transformation**:
$$z_i = \frac{x_i - \mu}{\sigma}$$
$$\text{Score}_{\text{BM25}}(i) = \frac{1}{1 + e^{-z_i / 2.0}}$$

### C. Hard Constraint Pruning
Jika skor mentah BM25 seorang dosen adalah nol ($x_i \le 10^{-9}$ / tidak memiliki irisan kata kunci sama sekali dengan query):
$$\text{Score}_{\text{BM25}}(i) \leftarrow 0.0$$
**Manfaat Arsitektural**:
1. **Efisiensi Komputasi**: Dosen dengan skor $0$ tidak perlu dihitung vektor Cosine Similarity-nya pada layer semantik SBERT.
2. **Akurasi Domain**: Mencegah dosen di luar rumpun topik mendapatkan rekomendasi semata-mata karena kemiripan vektor semantik yang kabur (*false positive elimination*).

---

## 5. Tahap 4: Semantic Engine (Sentence-BERT)

Komponen: [`server/src/services/nlp/sbert_engine.py`](server/src/services/nlp/sbert_engine.py)

### A. Model & Vector Embeddings
- **Model**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Dimensi Representasi**: 768 dimensi vektor dense (*dense tensor embeddings*).
- **Cakupan Bahasa**: Multilingual (termasuk bahasa Indonesia dan istilah teknis bahasa Inggris).

### B. Caching Embeddings di Disk
Seluruh vektor korpus dosen dihitung sekali saat startup/migrasi dan disimpan ke `server/storage/cache/sbert_embeddings.npy`. Saat server dinyalakan ulang, vektor dimuat instan via `numpy.load` dalam $< 0.1$ detik.

### C. Kalkulasi Cosine Similarity
Vektor query proposal ($\vec{u}$) dibandingkan dengan matriks vektor dosen kandidat lolos pruning ($\vec{v}_i$):
$$\text{Sim}_{\text{Cosine}}(\vec{u}, \vec{v}_i) = \frac{\vec{u} \cdot \vec{v}_i}{\|\vec{u}\| \|\vec{v}_i\|}$$
Skor semantik dibatasi pada rentang non-negatif:
$$\text{Score}_{\text{SBERT}}(i) = \max\left(0.0, \text{Sim}_{\text{Cosine}}(\vec{u}, \vec{v}_i)\right)$$

---

## 6. Tahap 5: Adaptive Hybrid Scoring & Top-K Ranking

Komponen: [`server/src/services/nlp/hybrid_scorer.py`](server/src/services/nlp/hybrid_scorer.py)

### A. Dynamic Adaptive Weighting
Panjang query masukan menentukan karakteristik pencarian yang optimal:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 Panjang Query Masukan                  │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
             Query < 15 Token                                  Query ≥ 15 Token
             (Mode Kata Kunci)                                 (Mode Abstrak Penuh)
             ─────────────────                                 ────────────────────
             α (BM25)  = 0.70                                  α (BM25)  = 0.35
             β (SBERT) = 0.30                                  β (SBERT) = 0.65
```

### B. Formula Agregasi Skor Hybrid
$$\text{Score}_{\text{Hybrid}}(i) = \left(\alpha \times \text{Score}_{\text{BM25}}(i)\right) + \left(\beta \times \text{Score}_{\text{SBERT}}(i)\right)$$
*Catatan*: $\alpha + \beta = 1.0$.

### C. Top-K Selection Berkecepatan Tinggi
Alih-alih mengurutkan seluruh korpus ($O(n \log n)$), sistem menggunakan `np.argpartition` dengan kompleksitas **$O(n + k \log k)$**:
1. Partisi $K$ elemen terbesar: $O(n)$.
2. Urutkan hanya sub-array $K$ kandidat teratas: $O(k \log k)$.
3. Eliminasi kandidat yang memiliki skor akhir di bawah `threshold` (default: $0.0$).

---

## 7. Tahap 6: Lapisan Explainable AI (XAI)

Untuk memberikan transparansi kepada mahasiswa dan dosen mengapa rekomendasi tersebut diberikan, sistem menyertakan metadata XAI di setiap kandidat:

1. **Irisan Kata Kunci Leksikal (`irisan_kata`)**:
   Menampilkan daftar term/kata kunci yang secara eksplisit cocok antara proposal mahasiswa dan rekam jejak penelitian dosen:
   $$\text{XAI}_{\text{lex}} = \text{Tokens}_{\text{Query}} \cap \text{Tokens}_{\text{Dosen}}$$
2. **Topik Semantik Dosen (`topik_dosen`)**:
   Top 5 topik/frasa kunci spesifik dosen yang diekstrak menggunakan algoritma **KeyBERT** (`use_maxsum=True`, n-gram range: 1–3) dan di-cache pada `server/storage/cache/keybert_dosen.json`.

---

## 8. Ringkasan Kompleksitas & Karakteristik Komputasi

| Tahap | Operasi Utama | Kompleksitas Waktu | Karakteristik Cache / Storage |
|---|---|---|---|
| **Preprocessing** | Regex, stopword, n-grams | $O(L)$ ($L$ = panjang teks) | In-memory stream |
| **Sinonim Ekspansi** | Longest-first string matching | $O(M \cdot K)$ ($M$ = kata, $K$ = kamus) | In-memory static dictionary |
| **BM25 Scoring** | Dot product sparse token | $O(|Q| \cdot \text{avg\_postings})$ | In-memory inverted index |
| **SBERT Encoding** | Transformer forward pass | $O(1)$ (query) + Cosine Sim | Disk cache `sbert_embeddings.npy` |
| **Hybrid Ranking** | NumPy argpartition | $O(n + k \log k)$ | Vektorisasi SIMD |
| **XAI Generation** | Set intersection & KeyBERT lookup | $O(|Q| + |D|)$ | Disk cache `keybert_dosen.json` |
