<template>
  <div class="docs-layout">
    <!-- TOC Sidebar -->
    <aside class="toc-sidebar">
      <div class="toc-title">Pipeline NLP</div>
      <nav class="toc-nav">
        <a href="#intro" class="toc-link">Pengantar</a>
        <a href="#arsitektur" class="toc-link">Arsitektur Sistem</a>
        <a href="#preprocessing" class="toc-link">1. Preprocessing</a>
        <a href="#ekspansi" class="toc-link">2. Ekspansi Sinonim</a>
        <a href="#bm25" class="toc-link">3. BM25 Scoring</a>
        <a href="#sbert" class="toc-link">4. SBERT Semantic</a>
        <a href="#hybrid" class="toc-link">5. Hybrid Ranking</a>
        <a href="#xai" class="toc-link">6. Explainability (XAI)</a>
        <a href="#skenario" class="toc-link">Skenario Mitigasi</a>
      </nav>
    </aside>

    <!-- Main article -->
    <main class="docs-main">
      <div class="prose docs-prose">

        <div class="page-header">
          <span class="page-badge">Technical Deep Dive</span>
          <h1>Pipeline NLP SiReDo</h1>
          <p class="page-lead">
            Dokumentasi teknis lengkap tentang bagaimana SiReDo memproses query proposal skripsi
            menjadi rekomendasi dosen yang relevan dan dapat dijelaskan (explainable).
          </p>
        </div>

        <!-- Arsitektur visual -->
        <section id="arsitektur">
          <h2>Arsitektur Sistem</h2>
          <p>
            SiReDo menggunakan pendekatan <strong>Hybrid Retrieval</strong> yang menggabungkan
            dua paradigma pencarian: leksikal berbasis frekuensi kata (BM25) dan semantik berbasis
            representasi vektor (SBERT). Keduanya digabung dengan bobot adaptif.
          </p>

          <div class="pipeline-flow">
            <div class="pf-step">
              <div class="pf-icon" style="background:#ede9ff;color:#5b4bdb">📝</div>
              <div class="pf-label">Input Query</div>
              <div class="pf-sub">Judul + Abstrak</div>
            </div>
            <div class="pf-arrow">→</div>
            <div class="pf-step">
              <div class="pf-icon" style="background:#fef9c3;color:#854d0e">🧹</div>
              <div class="pf-label">Preprocessing</div>
              <div class="pf-sub">Case Fold · Stopword · N-Gram</div>
            </div>
            <div class="pf-arrow">→</div>
            <div class="pf-fork">
              <div class="pf-step pf-step-blue">
                <div class="pf-icon" style="background:#eff6ff;color:#2563eb">📊</div>
                <div class="pf-label">BM25</div>
                <div class="pf-sub">Lexical Scoring</div>
              </div>
              <div class="pf-step pf-step-fuchsia">
                <div class="pf-icon" style="background:#fdf4ff;color:#a21caf">🧠</div>
                <div class="pf-label">SBERT</div>
                <div class="pf-sub">Semantic Vector</div>
              </div>
            </div>
            <div class="pf-arrow">→</div>
            <div class="pf-step">
              <div class="pf-icon" style="background:#f0fdf4;color:#16a34a">🏆</div>
              <div class="pf-label">Hybrid Ranking</div>
              <div class="pf-sub">α·BM25 + β·SBERT</div>
            </div>
          </div>
        </section>

        <!-- Preprocessing -->
        <section id="preprocessing">
          <h2>1. Preprocessing Teks</h2>
          <p>
            Sebelum query dan corpus dosen dapat dibandingkan, teks mentah harus distandarisasi.
            SiReDo menerapkan tiga tahap preprocessing secara berurutan:
          </p>

          <h3>Case Folding</h3>
          <p>
            Seluruh teks dikonversi ke huruf kecil dan karakter non-alfanumerik dihapus.
            Hanya token dengan panjang ≥ 2 karakter yang dipertahankan.
          </p>
          <div class="example-transform">
            <div class="et-before"><span class="et-label">Input</span><code>"Penerapan Deep Learning untuk Deteksi Penyakit Daun"</code></div>
            <div class="et-arrow">↓</div>
            <div class="et-after"><span class="et-label">Output</span><code>"penerapan deep learning untuk deteksi penyakit daun"</code></div>
          </div>

          <h3>Stopword Removal</h3>
          <p>
            Kata-kata yang tidak memiliki makna informatif (stopwords) dihapus menggunakan
            daftar kata baku Bahasa Indonesia. Ini meningkatkan signal-to-noise ratio.
          </p>
          <div class="example-transform">
            <div class="et-before"><span class="et-label">Input</span><code>["penerapan", "deep", "learning", "untuk", "deteksi", "penyakit", "daun"]</code></div>
            <div class="et-arrow">↓ hapus: "untuk"</div>
            <div class="et-after"><span class="et-label">Output</span><code>["penerapan", "deep", "learning", "deteksi", "penyakit", "daun"]</code></div>
          </div>

          <h3>N-Gram (Bigram)</h3>
          <p>
            Token unigram digabung dengan bigram (pasangan 2 kata berurutan). Ini memungkinkan
            BM25 mencocokkan frasa multi-kata seperti <code>deep_learning</code> atau
            <code>penyakit_daun</code> sebagai satu unit semantik.
          </p>
          <div class="example-transform">
            <div class="et-before"><span class="et-label">Unigram</span><code>["deep", "learning", "deteksi", "penyakit"]</code></div>
            <div class="et-arrow">↓ + bigram</div>
            <div class="et-after"><span class="et-label">Token BM25</span><code>["deep", "learning", "deteksi", "penyakit", "deep_learning", "learning_deteksi", "deteksi_penyakit"]</code></div>
          </div>

          <h3>Corpus Dosen</h3>
          <p>
            Data dosen juga dipreprocess dengan cara yang sama. Bidang data yang digunakan:
          </p>
          <div class="info-table">
            <table>
              <thead><tr><th>Field</th><th>Bobot Repetisi (BM25)</th><th>Keterangan</th></tr></thead>
              <tbody>
                <tr><td><code>bidang_keahlian</code></td><td>×5</td><td>Paling informatif, direpetisi 5x</td></tr>
                <tr><td><code>jurnal</code></td><td>×2</td><td>Judul jurnal/publikasi</td></tr>
                <tr><td><code>judul_bimbing</code></td><td>×1</td><td>Judul skripsi yang dibimbing</td></tr>
                <tr><td><code>judul_uji</code></td><td>×1</td><td>Judul skripsi yang diuji</td></tr>
                <tr><td><code>pendidikan</code></td><td>×1</td><td>Latar belakang pendidikan</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Ekspansi -->
        <section id="ekspansi">
          <h2>2. Ekspansi Sinonim (Query Expansion)</h2>
          <p>
            Sebelum SBERT encoding, query diekspansi menggunakan <strong>kamus ontologi domain</strong> yang
            dikurasi manual. Tujuannya: meningkatkan recall dengan menambahkan istilah-istilah
            yang setara secara semantik namun berbeda secara leksikal.
          </p>
          <blockquote>
            Ekspansi sinonim <strong>hanya</strong> diterapkan pada jalur SBERT, bukan BM25.
            Ini disengaja agar presisi leksikal BM25 tidak terkontaminasi.
          </blockquote>

          <h3>Mekanisme</h3>
          <p>
            Sistem memindai query dari kiri ke kanan, mencari frasa terpanjang yang cocok
            dengan kunci di kamus. Jika ditemukan, sinonim-sinonimnya ditambahkan ke akhir query.
          </p>
          <div class="example-transform">
            <div class="et-before"><span class="et-label">Query</span><code>"deep learning untuk klasifikasi gambar"</code></div>
            <div class="et-arrow">↓ "deep learning" → dl, neural network, cnn, rnn, lstm</div>
            <div class="et-after"><span class="et-label">Expanded</span><code>"deep learning untuk klasifikasi gambar dl neural network cnn rnn lstm"</code></div>
          </div>
        </section>

        <!-- BM25 -->
        <section id="bm25">
          <h2>3. BM25 — Lexical Scoring</h2>
          <p>
            BM25 (Best Match 25) adalah evolusi dari TF-IDF yang mengatasi kelemahan linearitas
            dan saturasi frekuensi. SiReDo menggunakan implementasi <strong>BM25Okapi</strong>
            dari library <code>rank_bm25</code>.
          </p>

          <h3>Formula BM25</h3>
          <div class="formula-box">
            <div class="formula-text">
              BM25(q, d) = Σ IDF(qᵢ) · <span class="fr-frac"><span class="fr-num">f(qᵢ, d) · (k₁ + 1)</span><span class="fr-den">f(qᵢ, d) + k₁ · (1 - b + b · |d|/avgdl)</span></span>
            </div>
            <div class="formula-legend">
              <span><code>f(qᵢ,d)</code> = frekuensi term di dokumen</span>
              <span><code>|d|</code> = panjang dokumen</span>
              <span><code>avgdl</code> = rata-rata panjang dokumen</span>
              <span><code>k₁=1.5, b=0.75</code> = parameter tuning</span>
            </div>
          </div>

          <h3>Normalisasi Z-Score Sigmoid</h3>
          <p>
            Skor BM25 mentah dinormalisasi ke rentang [0, 1] menggunakan Z-Score Sigmoid
            agar dapat dibandingkan dengan skor SBERT secara adil:
          </p>
          <div class="formula-box">
            <div class="formula-text">
              z = (score − μ) / σ<br>
              score_norm = 1 / (1 + e<sup>−z/2</sup>)
            </div>
          </div>

          <h3>Hard Filter (Skenario A)</h3>
          <p>
            Dosen dengan skor BM25 mentah = 0 (tidak memiliki satu pun kata kunci yang cocok)
            otomatis mendapat skor 0 dan tidak dihitung skor SBERT-nya. Ini mencegah
            rekomendasi dosen <em>out-of-domain</em>.
          </p>
        </section>

        <!-- SBERT -->
        <section id="sbert">
          <h2>4. SBERT — Semantic Scoring</h2>
          <p>
            SBERT (Sentence-BERT) mengubah teks menjadi <strong>dense vector embedding</strong>
            berdimensi tinggi yang merepresentasikan makna semantik. Dua kalimat yang bermakna
            sama akan menghasilkan vektor yang berdekatan di ruang embedding.
          </p>

          <h3>Mengapa SBERT, bukan BERT biasa?</h3>
          <p>
            BERT asli menghasilkan embedding untuk pasangan kalimat (cross-encoding), yang
            memerlukan perbandingan O(n²) — tidak efisien untuk corpus besar. SBERT
            dioptimasi untuk menghasilkan embedding <em>per kalimat</em> (bi-encoding),
            sehingga seluruh corpus dapat di-encode terlebih dahulu dan disimpan dalam cache,
            lalu hanya query yang di-encode saat runtime.
          </p>

          <h3>Cosine Similarity</h3>
          <p>
            Kedekatan semantik diukur menggunakan Cosine Similarity antara vektor query
            dan vektor setiap dosen:
          </p>
          <div class="formula-box">
            <div class="formula-text">
              cos(q, d) = <span class="fr-frac"><span class="fr-num">q · d</span><span class="fr-den">‖q‖ · ‖d‖</span></span>
            </div>
          </div>
          <p>
            Nilai berkisar dari 0 (tidak relevan) hingga 1 (identik secara semantik).
          </p>

          <h3>Cache & Optimasi</h3>
          <p>
            Embedding corpus dosen di-encode sekali saat server startup dan disimpan di file
            <code>sbert_embeddings.npy</code>. Saat ada query baru, hanya query yang di-encode
            secara real-time. SBERT hanya dijalankan untuk dosen yang lolos BM25 hard filter,
            menghemat komputasi secara signifikan pada corpus besar.
          </p>
        </section>

        <!-- Hybrid -->
        <section id="hybrid">
          <h2>5. Hybrid Ranking</h2>
          <p>
            Skor BM25 dan SBERT digabungkan secara linear dengan bobot adaptif:
          </p>
          <div class="formula-box">
            <div class="formula-text">
              Hybrid Score = <span class="cl-blue">α</span> × BM25_norm + <span class="cl-fuchsia">β</span> × SBERT
            </div>
            <div class="formula-legend">
              <span><code>α + β = 1.0</code> selalu</span>
            </div>
          </div>

          <h3>Adaptive Alpha (Skenario B)</h3>
          <p>
            Bobot α dan β ditentukan otomatis berdasarkan <strong>panjang query</strong>:
          </p>
          <div class="info-table">
            <table>
              <thead><tr><th>Kondisi Query</th><th>α (BM25)</th><th>β (SBERT)</th><th>Alasan</th></tr></thead>
              <tbody>
                <tr>
                  <td>Pendek (&lt; 15 token) — <em>Keyword Mode</em></td>
                  <td><strong>0.70</strong></td>
                  <td>0.30</td>
                  <td>Query singkat lebih cocok untuk exact-match BM25. SBERT kurang akurat dengan input sedikit.</td>
                </tr>
                <tr>
                  <td>Panjang (≥ 15 token) — <em>Abstrak Mode</em></td>
                  <td>0.35</td>
                  <td><strong>0.65</strong></td>
                  <td>Abstrak panjang mengandung konteks kaya → SBERT lebih unggul dalam menangkap makna.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- XAI -->
        <section id="xai">
          <h2>6. Explainability (XAI)</h2>
          <p>
            Setiap hasil rekomendasi dilengkapi dengan lapisan penjelasan (<em>Explainability</em>)
            agar pengguna dapat memverifikasi relevansi rekomendasi secara manual.
          </p>

          <h3>Irisan Kata (BM25 Match)</h3>
          <p>
            Set intersection antara token query dan token corpus dosen. Menunjukkan
            kata kunci mana yang secara eksplisit ditemukan di profil dosen.
          </p>
          <pre><code><span class="tok-comment">// XAI output</span>
{
  <span class="tok-key">"irisan_kata"</span>: [<span class="tok-str">"deep_learning"</span>, <span class="tok-str">"cnn"</span>, <span class="tok-str">"klasifikasi"</span>]
}</code></pre>

          <h3>Topik Dosen (KeyBERT Semantic)</h3>
          <p>
            Topik-topik utama dari corpus dosen yang diekstrak menggunakan KeyBERT
            (keyword extraction berbasis SBERT). Menunjukkan <em>kenapa</em>
            SBERT menganggap dosen ini relevan secara semantik.
          </p>
          <pre><code>{
  <span class="tok-key">"topik_dosen"</span>: [<span class="tok-str">"image classification"</span>, <span class="tok-str">"convolutional neural network"</span>]
}</code></pre>
        </section>

        <!-- Skenario -->
        <section id="skenario">
          <h2>Skenario Mitigasi</h2>
          <p>
            SiReDo mengimplementasikan tiga skenario mitigasi yang bekerja secara simultan
            untuk meningkatkan kualitas rekomendasi:
          </p>

          <div class="scenario-cards">
            <div class="scenario-card" style="border-left-color: var(--brand)">
              <div class="sc-header">
                <span class="sc-badge" style="background:var(--brand-light);color:var(--brand)">A</span>
                <h3>Hard Filter — Mencegah Out-of-Domain</h3>
              </div>
              <p>
                Dosen yang tidak memiliki satu pun kata kunci relevan (BM25 mentah = 0)
                dieksklusi dari ranking. Ini mencegah dosen lintas bidang yang tidak relevan
                masuk ke hasil rekomendasi hanya karena skor SBERT-nya tinggi.
              </p>
              <div class="sc-impact">Dampak: Meningkatkan presisi</div>
            </div>

            <div class="scenario-card" style="border-left-color: var(--green)">
              <div class="sc-header">
                <span class="sc-badge" style="background:var(--green-bg);color:var(--green)">B</span>
                <h3>Adaptive Alpha — Bobot Dinamis</h3>
              </div>
              <p>
                Bobot hybrid disesuaikan secara otomatis berdasarkan panjang query.
                Query keyword pendek → BM25 dominan (70%).
                Query abstrak panjang → SBERT dominan (65%).
              </p>
              <div class="sc-impact">Dampak: Meningkatkan akurasi lintas jenis query</div>
            </div>

            <div class="scenario-card" style="border-left-color: var(--amber)">
              <div class="sc-header">
                <span class="sc-badge" style="background:var(--amber-bg);color:var(--amber)">C</span>
                <h3>Ekspansi Sinonim — Mengatasi Vocabulary Gap</h3>
              </div>
              <p>
                Query diekspansi dengan istilah-istilah domain yang setara namun berbeda
                secara leksikal. Contoh: "deep learning" → ditambahkan "dl neural network cnn rnn lstm".
                Ini menutup celah antara terminologi mahasiswa dan dosen.
              </p>
              <div class="sc-impact">Dampak: Meningkatkan recall untuk SBERT</div>
            </div>
          </div>

          <hr>
          <p>
            <router-link to="/single" style="color:var(--brand);font-weight:600">→ Coba pipeline ini secara langsung di halaman Single Recommendation</router-link>
          </p>
        </section>

      </div>
    </main>
  </div>
</template>

<style scoped>
.docs-layout {
  display: flex;
  min-height: 100svh;
}
.toc-sidebar {
  width: 200px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100svh;
  overflow-y: auto;
  border-right: 1px solid var(--border);
  padding: 2rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.toc-title { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); padding: 0 0.5rem; margin-bottom: 0.5rem; }
.toc-nav { display: flex; flex-direction: column; gap: 1px; }
.toc-link { font-size: 0.825rem; color: var(--text-secondary); text-decoration: none; padding: 0.35rem 0.6rem; border-radius: var(--radius-sm); transition: background 0.12s, color 0.12s; }
.toc-link:hover { background: var(--bg-muted); color: var(--text-primary); }

.docs-main { flex: 1; min-width: 0; padding: 3rem 2.5rem 5rem; }
.docs-prose { max-width: var(--content-max); }

.page-header { margin-bottom: 0; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--brand); background: var(--brand-light); border: 1px solid #c4b5fd; padding: 3px 10px; border-radius: 99px; margin-bottom: 1rem; }
.page-lead { font-size: 1.05rem; color: var(--text-secondary); line-height: 1.75; margin-bottom: 0.5rem !important; }

/* Pipeline flow diagram */
.pipeline-flow {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin: 1.5rem 0;
  padding: 1.5rem;
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}
.pf-step { display: flex; flex-direction: column; align-items: center; gap: 0.35rem; text-align: center; }
.pf-icon { width: 44px; height: 44px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
.pf-label { font-size: 0.8rem; font-weight: 700; color: var(--text-primary); }
.pf-sub { font-size: 0.68rem; color: var(--text-muted); }
.pf-arrow { font-size: 1.1rem; color: var(--border-strong); flex-shrink: 0; }
.pf-fork { display: flex; flex-direction: column; gap: 0.5rem; }

/* Example transforms */
.example-transform {
  margin: 1rem 0 1.5rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  font-size: 0.85rem;
}
.et-before, .et-after {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
}
.et-before { background: var(--bg-subtle); border-bottom: 1px dashed var(--border); }
.et-after { background: var(--green-bg); }
.et-label { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); padding: 2px 6px; background: var(--bg-muted); border-radius: var(--radius-sm); flex-shrink: 0; margin-top: 2px; }
.et-arrow { padding: 0.35rem 1.5rem; font-size: 0.78rem; color: var(--text-muted); background: var(--bg); border-top: 1px dashed var(--border); border-bottom: 1px dashed var(--border); }

/* Formula box */
.formula-box {
  background: #0f0f14;
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem;
  margin: 1rem 0 1.5rem;
  overflow-x: auto;
}
.formula-text {
  font-family: var(--font-mono);
  font-size: 0.92rem;
  color: #e4e4f0;
  line-height: 1.8;
  margin-bottom: 0.75rem;
}
.fr-frac { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 0.25rem; }
.fr-num { border-bottom: 1px solid #6b7280; padding: 0 0.25rem 2px; }
.fr-den { padding: 2px 0.25rem 0; }
.formula-legend { display: flex; flex-wrap: wrap; gap: 0.75rem; }
.formula-legend span { font-size: 0.75rem; color: #9ca3af; }
.formula-legend code { background: #1e1e2e; color: #a6e3a1; border: none; font-size: 0.75rem; }

.cl-blue { color: #60a5fa; font-weight: 700; }
.cl-fuchsia { color: #e879f9; font-weight: 700; }

/* Info table */
.info-table { margin: 1rem 0 1.5rem; overflow-x: auto; }
.info-table table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.info-table th { background: var(--bg-subtle); border: 1px solid var(--border); padding: 0.6rem 0.9rem; text-align: left; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-secondary); }
.info-table td { border: 1px solid var(--border); padding: 0.65rem 0.9rem; color: var(--text-secondary); vertical-align: top; line-height: 1.5; }

/* Scenario cards */
.scenario-cards { display: flex; flex-direction: column; gap: 1rem; margin: 1.5rem 0; }
.scenario-card {
  border: 1px solid var(--border);
  border-left: 4px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.25rem 1rem;
}
.sc-header { display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.5rem; }
.sc-badge { font-size: 0.72rem; font-weight: 800; padding: 3px 9px; border-radius: 99px; font-family: var(--font-mono); }
.sc-header h3 { margin: 0; font-size: 0.95rem; font-weight: 600; color: var(--text-primary); }
.scenario-card p { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.65; margin: 0 0 0.65rem !important; }
.sc-impact { font-size: 0.75rem; font-weight: 600; color: var(--text-muted); }

@media (max-width: 768px) {
  .toc-sidebar { display: none; }
  .docs-main { padding: 2rem 1.25rem 4rem; }
  .pipeline-flow { flex-direction: column; }
  .pf-arrow { transform: rotate(90deg); }
}
</style>
