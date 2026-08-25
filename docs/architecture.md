# Arsitektur & Desain Sistem — SiReDo v3

## 1. Konsep Desain
SiReDo v3 dirancang dengan arsitektur **Decoupled Fullstack** yang memisahkan backend engine (*server*) dari frontend presentation (*web*).

### Alur Layering Feature-Module (Backend)
```
Routes / Transport
       │
       ▼
Controller (Validasi DTO & Transport formatting)
       │
       ▼
Service / Use Case (Orkestrasi Logika Bisnis & NLP Pipeline)
       │
       ▼
Repository / Data Access (Komposit MySQL + Fallback Excel)
       │
       ▼
Data Storage (MySQL Database / Excel Spreadsheet)
```

## 2. NLP Pipeline Engineering
1. **Preprocessing**: Case folding, stopword removal, unigram + bigram n-gram generation.
2. **Synonym Expansion**: Longest-first ontology matching dari kamus sinonim domain IT.
3. **Lexical Scoring (BM25Okapi)**:
   - Z-score Sigmoid Normalization: $z = \frac{x - \mu}{\sigma}$, $\text{Score}_{\text{norm}} = \frac{1}{1 + e^{-z/2}}$.
   - Hard Constraint Pruning: Hanya dosen dengan $\text{BM25}_{\text{norm}} > 0$ yang diteruskan ke layer semantik.
4. **Semantic Scoring (Sentence-BERT)**:
   - Model `paraphrase-multilingual-MiniLM-L12-v2` (768-D embeddings).
   - Cosine Similarity komputasi vektor.
5. **Adaptive Hybrid Aggregation**:
   - Jika query $< 15$ token: Keyword Mode ($\alpha=0.70$ BM25, $\beta=0.30$ SBERT).
   - Jika query $\ge 15$ token: Abstrak Mode ($\alpha=0.35$ BM25, $\beta=0.65$ SBERT).
   - Top-K ranking efisien $O(n + k \log k)$ via `np.argpartition`.
6. **Explainable AI (XAI)**:
   - Irisan kata kunci leksikal mahasiswa vs korpus dosen.
   - Ekstraksi topik semantic via KeyBERT.

## 3. Frontend Architecture (Vue 3 + Pinia)
- **Pinia State Management**:
  - `useSystemStore`: Status koneksi server, ketersediaan cache, daftar data dosen.
  - `useRecommendationStore`: State input query, stepper progress, hasil rekomendasi, pipeline logs, dan batch processing.
  - `useConfigStore`: State konfigurasi parameter algoritma.
- **Axios Interceptors**:
  - Base URL dinamis dari `import.meta.env.VITE_API_BASE_URL`.
  - Standardized error unwrapping dan timeout handling.
