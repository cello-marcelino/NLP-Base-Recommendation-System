<script setup>
import { ref } from 'vue'

const props = defineProps({
  pipeline: {
    type: Object,
    required: true
  }
})

const activeTab = ref('all') // 'all', 'preproc', 'expansion', 'bm25', 'sbert', 'hybrid'
const isExpandedAll = ref(true)

const openSteps = ref({
  preproc: true,
  expansion: true,
  bm25: true,
  sbert: true,
  hybrid: true
})

const toggleStep = (stepKey) => {
  openSteps.value[stepKey] = !openSteps.value[stepKey]
}

const toggleExpandAll = () => {
  const nextState = !isExpandedAll.value
  isExpandedAll.value = nextState
  Object.keys(openSteps.value).forEach(key => {
    openSteps.value[key] = nextState
  })
}
</script>

<template>
  <div class="pipeline-card">
    <!-- Header with Visual Pipeline Summary & Filter Tabs -->
    <div class="pipeline-header">
      <div class="ph-left">
        <div class="ph-icon-box">
          <svg class="w-5 h-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <div>
          <h2 class="ph-title">Transparansi Pipeline Analisis NLP</h2>
          <p class="ph-subtitle">Rincian tahapan transformasi query dari teks mentah hingga perankingan hibrida dosen.</p>
        </div>
      </div>

      <div class="ph-actions">
        <button type="button" @click="toggleExpandAll" class="ph-toggle-btn">
          <span>{{ isExpandedAll ? 'Tutup Semua' : 'Buka Semua' }}</span>
          <svg class="w-3.5 h-3.5 transition-transform" :class="{ 'rotate-180': isExpandedAll }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Interactive Pipeline Steps Overview Flow -->
    <div class="pipeline-overview-bar">
      <!-- Step 1 Metric -->
      <div class="ov-item" @click="openSteps.preproc = true">
        <div class="ov-dot bg-slate-500">1</div>
        <div class="ov-text">
          <div class="ov-label">Tokens BM25</div>
          <div class="ov-value text-slate-800">{{ pipeline.preprocessing?.total_tokens || 0 }} Kata</div>
        </div>
      </div>
      <div class="ov-arrow">→</div>

      <!-- Step 2 Metric -->
      <div class="ov-item" @click="openSteps.expansion = true">
        <div class="ov-dot bg-amber-500">2</div>
        <div class="ov-text">
          <div class="ov-label">Ekspansi Sinonim</div>
          <div class="ov-value text-amber-700">{{ pipeline.ekspansi?.num_frasa_ditemukan || 0 }} Frasa</div>
        </div>
      </div>
      <div class="ov-arrow">→</div>

      <!-- Step 3 Metric -->
      <div class="ov-item" @click="openSteps.bm25 = true">
        <div class="ov-dot bg-blue-500">3</div>
        <div class="ov-text">
          <div class="ov-label">Kandidat Lolos</div>
          <div class="ov-value text-blue-700">{{ pipeline.bm25?.num_candidates || 0 }} Dosen</div>
        </div>
      </div>
      <div class="ov-arrow">→</div>

      <!-- Step 4 Metric -->
      <div class="ov-item" @click="openSteps.sbert = true">
        <div class="ov-dot bg-fuchsia-500">4</div>
        <div class="ov-text">
          <div class="ov-label">Vektor SBERT</div>
          <div class="ov-value text-fuchsia-700">384-D Cosine</div>
        </div>
      </div>
      <div class="ov-arrow">→</div>

      <!-- Step 5 Metric -->
      <div class="ov-item" @click="openSteps.hybrid = true">
        <div class="ov-dot bg-indigo-600">5</div>
        <div class="ov-text">
          <div class="ov-label">Bobot α / β</div>
          <div class="ov-value text-indigo-700">{{ pipeline.hybrid?.alpha }} / {{ pipeline.hybrid?.beta }}</div>
        </div>
      </div>
    </div>

    <!-- Step-by-Step Detailed Cards -->
    <div class="pipeline-steps-list">

      <!-- ─── STEP 1: PREPROCESSING ─── -->
      <div v-if="pipeline.preprocessing" class="step-card" :class="{ 'step-card--closed': !openSteps.preproc }">
        <div class="step-header" @click="toggleStep('preproc')">
          <div class="step-badge step-badge--slate">
            <span class="step-num">01</span>
            <span>Preprocessing & Tokenisasi Teks</span>
          </div>
          <div class="step-summary">
            <span class="chip chip--slate">{{ pipeline.preprocessing.total_tokens }} Token Bersih</span>
            <svg class="chevron-icon" :class="{ 'chevron-icon--open': openSteps.preproc }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <div v-if="openSteps.preproc" class="step-body">
          <div class="step-desc-text">
            Teks dibersihkan melalui case folding (huruf kecil), pembuangan karakter non-alfanumerik, penyaringan kata henti (*stopword removal*), serta pembentukan unigram dan bigram (N-gram).
          </div>

          <div class="preproc-grid">
            <!-- Raw Query -->
            <div class="p-card">
              <div class="p-card-title">📝 Teks Masukan (Raw Query)</div>
              <div class="p-card-content p-quote font-sans">
                "{{ pipeline.preprocessing.raw_query }}"
              </div>
            </div>

            <!-- Stopword Filtered -->
            <div class="p-card">
              <div class="p-card-title">🧹 Setelah Stopword Removal (20 Kata Pertama)</div>
              <div class="p-tags-wrap">
                <span v-for="word in pipeline.preprocessing.after_stopword" :key="word" class="tag tag--slate">
                  {{ word }}
                </span>
                <span v-if="!pipeline.preprocessing.after_stopword?.length" class="text-xs text-slate-400 italic">Tidak ada token tersisa</span>
              </div>
            </div>

            <!-- Bigrams N-Grams -->
            <div class="p-card">
              <div class="p-card-title">🔗 Frasa Bigram (N-Grams Rekayasa Recall)</div>
              <div class="p-tags-wrap">
                <span v-for="bg in pipeline.preprocessing.bigrams" :key="bg" class="tag tag--blue">
                  {{ bg.replace('_', ' ') }}
                </span>
                <span v-if="!pipeline.preprocessing.bigrams?.length" class="text-xs text-slate-400 italic">Tidak ada frasa bigram (input terlalu pendek)</span>
              </div>
            </div>

            <!-- Final BM25 Vocabulary Tokens -->
            <div class="p-card">
              <div class="p-card-title">🏷️ Token Unik Leksikal BM25</div>
              <div class="p-tags-wrap">
                <span v-for="tok in pipeline.preprocessing.final_tokens" :key="tok" class="tag tag--brand">
                  {{ tok }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ─── STEP 2: EKSPANSI SINONIM ONTOLOGI ─── -->
      <div v-if="pipeline.ekspansi" class="step-card" :class="{ 'step-card--closed': !openSteps.expansion }">
        <div class="step-header" @click="toggleStep('expansion')">
          <div class="step-badge step-badge--amber">
            <span class="step-num">02</span>
            <span>Ekspansi Kata Kunci Ontologi (Query Expansion)</span>
          </div>
          <div class="step-summary">
            <span class="chip" :class="pipeline.ekspansi.num_frasa_ditemukan > 0 ? 'chip--amber' : 'chip--slate'">
              {{ pipeline.ekspansi.num_frasa_ditemukan }} Frasa Ditemukan
            </span>
            <svg class="chevron-icon" :class="{ 'chevron-icon--open': openSteps.expansion }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <div v-if="openSteps.expansion" class="step-body">
          <div class="step-desc-text">
            Mendeteksi istilah domain ilmu komputer/informatika (misal: *natural language processing*, *machine learning*, *computer vision*) dan memperkaya query dengan sinonim domain agar menjangkau kepakaran dosen yang menggunakan istilah alternatif.
          </div>

          <div v-if="pipeline.ekspansi.num_frasa_ditemukan > 0" class="expansion-cards-grid">
            <div v-for="(syn, phrase) in pipeline.ekspansi.log" :key="phrase" class="exp-card">
              <div class="exp-phrase">
                <span class="exp-label">Kata Kunci Input</span>
                <span class="exp-val text-amber-900 font-bold">"{{ phrase }}"</span>
              </div>
              <div class="exp-arrow">
                <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </div>
              <div class="exp-synonyms">
                <span class="exp-label">Sinonim Ditambahkan</span>
                <div class="p-tags-wrap">
                  <span v-for="s in syn.split(' ')" :key="s" class="tag tag--amber font-mono font-medium">
                    + {{ s }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="empty-notice">
            <svg class="w-5 h-5 text-slate-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Tidak ada frasa spesifik ontologi yang terdeteksi. Sistem melanjutkan dengan token kata asli.</span>
          </div>
        </div>
      </div>

      <!-- ─── STEP 3: BM25 LEXICAL SCORING & PRUNING ─── -->
      <div v-if="pipeline.bm25" class="step-card" :class="{ 'step-card--closed': !openSteps.bm25 }">
        <div class="step-header" @click="toggleStep('bm25')">
          <div class="step-badge step-badge--blue">
            <span class="step-num">03</span>
            <span>Penyaringan Leksikal BM25 (Hard Constraint Pruning)</span>
          </div>
          <div class="step-summary">
            <span class="chip chip--blue">{{ pipeline.bm25.num_candidates }} dari {{ pipeline.bm25.num_total_dosen }} Dosen Lolos</span>
            <svg class="chevron-icon" :class="{ 'chevron-icon--open': openSteps.bm25 }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <div v-if="openSteps.bm25" class="step-body">
          <div class="step-desc-text">
            BM25Okapi menghitung kecocokan frekuensi istilah leksikal terhadap korpus terbobot dosen (Keahlian $\times 5$, Jurnal $\times 2$, Bimbingan $\times 1$, Ujian $\times 1$), lalu dinormalisasi dengan <strong>Z-Score Sigmoid</strong>. Dosen dengan kecocokan 0 dipangkas (*pruned*) untuk efisiensi komputasi semantik.
          </div>

          <div class="candidates-table-card">
            <div class="ct-header">
              <span>Top Kandidat Leksikal BM25 Teratas</span>
              <span class="text-xs font-mono text-blue-600 font-semibold">Z-Score Sigmoid Normalized</span>
            </div>
            <div class="candidates-grid">
              <div v-for="(cand, idx) in pipeline.bm25.top_candidates" :key="idx" class="cand-row cand-row--blue">
                <div class="cand-rank">#{{ idx + 1 }}</div>
                <div class="cand-info">
                  <div class="cand-name">{{ cand.nama }}</div>
                  <div class="cand-bar-wrap">
                    <div class="cand-bar-fill bg-blue-500" :style="`width: ${Math.min(100, Math.round(cand.skor * 100))}%`"></div>
                  </div>
                </div>
                <div class="cand-score text-blue-700">
                  {{ (cand.skor * 100).toFixed(1) }}%
                  <span class="cand-score-raw">({{ cand.skor }})</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ─── STEP 4: SBERT SEMANTIC SCORING ─── -->
      <div v-if="pipeline.sbert" class="step-card" :class="{ 'step-card--closed': !openSteps.sbert }">
        <div class="step-header" @click="toggleStep('sbert')">
          <div class="step-badge step-badge--fuchsia">
            <span class="step-num">04</span>
            <span>Pencocokan Semantik Vektor (Sentence-BERT Embedding)</span>
          </div>
          <div class="step-summary">
            <span class="chip chip--fuchsia">{{ pipeline.sbert.num_computed }} Vektor Dihitung</span>
            <svg class="chevron-icon" :class="{ 'chevron-icon--open': openSteps.sbert }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <div v-if="openSteps.sbert" class="step-body">
          <div class="step-desc-text">
            Sentence-BERT (`paraphrase-multilingual-MiniLM-L12-v2`) memetakan makna kontekstual query ke ruang vektor 384 dimensi dan menghitung <strong>Cosine Similarity</strong> terhadap embedding profil dosen yang lolos tahap leksikal.
          </div>

          <div class="candidates-table-card">
            <div class="ct-header">
              <span>Top Kandidat Semantik SBERT Teratas</span>
              <span class="text-xs font-mono text-fuchsia-600 font-semibold">Cosine Similarity [0.0 - 1.0]</span>
            </div>
            <div class="candidates-grid">
              <div v-for="(cand, idx) in pipeline.sbert.top_candidates" :key="idx" class="cand-row cand-row--fuchsia">
                <div class="cand-rank cand-rank--fuchsia">#{{ idx + 1 }}</div>
                <div class="cand-info">
                  <div class="cand-name">{{ cand.nama }}</div>
                  <div class="cand-bar-wrap">
                    <div class="cand-bar-fill bg-fuchsia-500" :style="`width: ${Math.min(100, Math.round(cand.skor * 100))}%`"></div>
                  </div>
                </div>
                <div class="cand-score text-fuchsia-700">
                  {{ (cand.skor * 100).toFixed(1) }}%
                  <span class="cand-score-raw">({{ cand.skor }})</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ─── STEP 5: HYBRID AGGREGATION & ADAPTIVE WEIGHTS ─── -->
      <div v-if="pipeline.hybrid" class="step-card step-card--brand" :class="{ 'step-card--closed': !openSteps.hybrid }">
        <div class="step-header" @click="toggleStep('hybrid')">
          <div class="step-badge step-badge--brand">
            <span class="step-num">05</span>
            <span>Penggabungan Hibrida & Pembobotan Adaptif (Top-K Ranking)</span>
          </div>
          <div class="step-summary">
            <span class="chip chip--brand">Mode: {{ pipeline.hybrid.mode === 'keyword' ? 'Keyword Dominan' : pipeline.hybrid.mode === 'abstrak' ? 'Abstrak Dominan' : 'Manual' }}</span>
            <svg class="chevron-icon" :class="{ 'chevron-icon--open': openSteps.hybrid }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <div v-if="openSteps.hybrid" class="step-body">
          <div class="step-desc-text">
            Skor akhir dihitung dengan rumus hibrida: $\text{Skor} = (\alpha \times \text{BM25}) + (\beta \times \text{SBERT})$. Bobot otomatis disesuaikan berdasarkan panjang token query mahasiswa.
          </div>

          <div class="hybrid-visual-box">
            <div class="hv-ratio-bar">
              <div class="hv-part hv-part--bm25" :style="`width: ${pipeline.hybrid.alpha * 100}%`">
                <span>α BM25: {{ Math.round(pipeline.hybrid.alpha * 100) }}%</span>
              </div>
              <div class="hv-part hv-part--sbert" :style="`width: ${pipeline.hybrid.beta * 100}%`">
                <span>β SBERT: {{ Math.round(pipeline.hybrid.beta * 100) }}%</span>
              </div>
            </div>

            <div class="hv-cards-grid">
              <div class="hv-card hv-card--blue">
                <div class="hv-label">Bobot Leksikal (α)</div>
                <div class="hv-value text-blue-700">{{ pipeline.hybrid.alpha }}</div>
                <div class="hv-sub">Mengutamakan kecocokan kata kunci eksak</div>
              </div>
              <div class="hv-card hv-card--fuchsia">
                <div class="hv-label">Bobot Semantik (β)</div>
                <div class="hv-value text-fuchsia-700">{{ pipeline.hybrid.beta }}</div>
                <div class="hv-sub">Mengutamakan kedekatan konteks kalimat</div>
              </div>
              <div class="hv-card hv-card--brand">
                <div class="hv-label">Kompleksitas Perankingan</div>
                <div class="hv-value text-indigo-700">O(n + k log k)</div>
                <div class="hv-sub">Menggunakan numpy argpartition efisien</div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.pipeline-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* Header */
.pipeline-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.ph-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}
.ph-icon-box {
  width: 38px;
  height: 38px;
  background: var(--brand-light);
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.ph-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}
.ph-subtitle {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin: 0.15rem 0 0;
}

.ph-toggle-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--brand);
  background: var(--brand-light);
  border: 1px solid rgba(91, 75, 219, 0.2);
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.15s;
}
.ph-toggle-btn:hover {
  background: #e0d8ff;
}

/* Pipeline Overview Bar */
.pipeline-overview-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: var(--bg-subtle);
  border-bottom: 1px solid var(--border);
  overflow-x: auto;
  gap: 0.75rem;
}

.ov-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  padding: 0.35rem 0.6rem;
  border-radius: var(--radius);
  transition: background 0.15s;
  flex-shrink: 0;
}
.ov-item:hover {
  background: var(--bg-muted);
}
.ov-dot {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  color: white;
  font-size: 0.7rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
}
.ov-text {
  display: flex;
  flex-direction: column;
}
.ov-label {
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}
.ov-value {
  font-size: 0.8rem;
  font-weight: 700;
  font-family: var(--font-mono);
}
.ov-arrow {
  color: var(--border-strong);
  font-size: 0.9rem;
  font-weight: 700;
}

/* Steps List */
.pipeline-steps-list {
  display: flex;
  flex-direction: column;
  padding: 1.25rem 1.5rem;
  gap: 1rem;
  background: var(--bg-subtle);
}

.step-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.step-card--brand {
  border-color: rgba(91, 75, 219, 0.3);
}

.step-header {
  padding: 0.85rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  background: var(--bg);
  user-select: none;
  transition: background 0.15s;
}
.step-header:hover {
  background: var(--bg-muted);
}

.step-badge {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-primary);
}
.step-num {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  background: var(--bg-muted);
  color: var(--text-secondary);
}
.step-badge--slate .step-num { background: #f1f5f9; color: #475569; }
.step-badge--amber .step-num { background: #fef3c7; color: #b45309; }
.step-badge--blue .step-num { background: var(--blue-bg); color: var(--blue); }
.step-badge--fuchsia .step-num { background: var(--fuchsia-bg); color: var(--fuchsia); }
.step-badge--brand .step-num { background: var(--brand-light); color: var(--brand); }

.step-summary {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.chevron-icon {
  width: 18px;
  height: 18px;
  color: var(--text-muted);
  transition: transform 0.25s ease;
}
.chevron-icon--open {
  transform: rotate(180deg);
}

.step-body {
  padding: 1.25rem;
  border-top: 1px solid var(--border);
  background: var(--bg);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.step-desc-text {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.55;
}

/* Chips & Tags */
.chip {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 99px;
}
.chip--slate { background: var(--bg-muted); color: var(--text-secondary); }
.chip--amber { background: #fef3c7; color: #b45309; }
.chip--blue { background: var(--blue-bg); color: var(--blue); }
.chip--fuchsia { background: var(--fuchsia-bg); color: var(--fuchsia); }
.chip--brand { background: var(--brand-light); color: var(--brand); }

.p-tags-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.tag {
  font-size: 0.72rem;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
}
.tag--slate { background: var(--bg-muted); color: var(--text-secondary); border-color: var(--border); }
.tag--blue { background: var(--blue-bg); color: var(--blue); border-color: var(--blue-border); font-weight: 600; }
.tag--amber { background: #fffbeb; color: #b45309; border-color: #fde68a; }
.tag--brand { background: var(--brand-light); color: var(--brand); border-color: #ddd6fe; font-weight: 600; font-family: var(--font-mono); }

/* Preprocessing Layout */
.preproc-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
}
.p-card {
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.p-card-title {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.p-quote {
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-style: italic;
  line-height: 1.4;
}

/* Expansion Cards */
.expansion-cards-grid {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.exp-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fffdf5;
  border: 1px solid #fde68a;
  border-radius: var(--radius);
  padding: 0.75rem 1rem;
  gap: 1rem;
}
.exp-phrase, .exp-synonyms {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.exp-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}
.exp-arrow { flex-shrink: 0; }

.empty-notice {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.75rem 1rem;
  background: var(--bg-subtle);
  border: 1px dashed var(--border-strong);
  border-radius: var(--radius);
  font-size: 0.78rem;
  color: var(--text-secondary);
}

/* Candidate Score List */
.candidates-table-card {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}
.ct-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.85rem;
  background: var(--bg-subtle);
  border-bottom: 1px solid var(--border);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-primary);
}
.candidates-grid {
  display: flex;
  flex-direction: column;
}
.cand-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0.85rem;
  border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}
.cand-row:last-child { border-bottom: none; }
.cand-row:hover { background: var(--bg-subtle); }

.cand-rank {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-muted);
  width: 24px;
}
.cand-rank--fuchsia { color: var(--fuchsia); }

.cand-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.cand-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
}
.cand-bar-wrap {
  width: 100%;
  height: 4px;
  background: var(--bg-muted);
  border-radius: 99px;
  overflow: hidden;
}
.cand-bar-fill {
  height: 100%;
  border-radius: 99px;
}

.cand-score {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 800;
  text-align: right;
}
.cand-score-raw {
  display: block;
  font-size: 0.65rem;
  font-weight: 500;
  color: var(--text-muted);
}

/* Hybrid Visual */
.hybrid-visual-box {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.hv-ratio-bar {
  display: flex;
  height: 28px;
  border-radius: var(--radius);
  overflow: hidden;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  color: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.hv-part {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: width 0.3s;
}
.hv-part--bm25 { background: #3b82f6; }
.hv-part--sbert { background: #d946ef; }

.hv-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}
.hv-card {
  padding: 0.85rem;
  border-radius: var(--radius);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.hv-card--blue { background: var(--blue-bg); border: 1px solid var(--blue-border); }
.hv-card--fuchsia { background: var(--fuchsia-bg); border: 1px solid var(--fuchsia-border); }
.hv-card--brand { background: var(--brand-light); border: 1px solid #c4b5fd; }

.hv-label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
}
.hv-value {
  font-family: var(--font-mono);
  font-size: 1.25rem;
  font-weight: 800;
}
.hv-sub {
  font-size: 0.68rem;
  color: var(--text-secondary);
}

@media (max-width: 900px) {
  .preproc-grid { grid-template-columns: 1fr; }
  .hv-cards-grid { grid-template-columns: 1fr; }
  .exp-card { flex-direction: column; align-items: flex-start; }
}
</style>
