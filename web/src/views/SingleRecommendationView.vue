<script setup>
import { ref } from 'vue'
import api from '../services/api'
import DosenCard from '../components/recommendation/DosenCard.vue'
import ProgressStepper from '../components/recommendation/ProgressStepper.vue'
import XaiModal from '../components/recommendation/XaiModal.vue'

const judul = ref('')
const abstrak = ref('')
const kRank = ref(5)
const recommendations = ref([])
const metadata = ref(null)
const pipeline = ref(null)
const isProcessing = ref(false)
const error = ref('')

const steps = ref([
  { title: 'Preprocessing Teks', desc: 'Case folding, stopword removal, N-Gram', status: 'idle', open: false },
  { title: 'Ekspansi Sinonim', desc: 'Penambahan sinonim via kamus ontologi', status: 'idle', open: false },
  { title: 'Lexical Scoring (BM25)', desc: 'TF-IDF + Z-Score Sigmoid normalization', status: 'idle', open: false },
  { title: 'Semantic Scoring (SBERT)', desc: 'Cosine Similarity pada embedding vektor', status: 'idle', open: false },
  { title: 'Hybrid Ranking', desc: 'Adaptive α·BM25 + β·SBERT aggregation', status: 'idle', open: false }
])

const selectedDosen = ref(null)

const onSubmit = async () => {
  if (!judul.value && !abstrak.value) { error.value = 'Isi minimal judul atau abstrak'; return }
  error.value = ''
  isProcessing.value = true
  recommendations.value = []
  metadata.value = null
  pipeline.value = null
  steps.value.forEach(s => { s.status = 'idle'; s.open = false })

  let currentStep = 0
  steps.value[currentStep].status = 'running'
  steps.value[currentStep].open = true

  const interval = setInterval(() => {
    if (currentStep < steps.value.length - 1) {
      steps.value[currentStep].status = 'done'
      steps.value[currentStep].open = false
      currentStep++
      steps.value[currentStep].status = 'running'
      steps.value[currentStep].open = true
    }
  }, 600)

  try {
    const res = await api.post('/rekomendasi/single', {
      judul: judul.value,
      abstrak: abstrak.value,
      k_rank: kRank.value || null
    })
    clearInterval(interval)
    steps.value.forEach(s => { s.status = 'done'; s.open = false })
    const result = res.data.data
    recommendations.value = result.recommendations
    metadata.value = result.metadata
    pipeline.value = result.pipeline || null
  } catch (err) {
    clearInterval(interval)
    steps.value[currentStep].status = 'error'
    error.value = err.response?.data?.message || err.message
  } finally {
    isProcessing.value = false
  }
}

const openXai = (rec) => { selectedDosen.value = rec }
</script>

<template>
  <div class="sp-wrap">

    <!-- Page header -->
    <div class="sp-header">
      <span class="sp-badge">Live Tool</span>
      <h1 class="sp-title">Single Recommendation</h1>
      <p class="sp-lead">Analisis satu proposal secara real-time — lihat skor <strong>BM25</strong>, <strong>SBERT</strong>, dan <strong>Hybrid</strong> beserta Pipeline Log dan XAI Explanation.</p>
    </div>

    <!-- Two-col layout -->
    <div class="sp-body">

      <!-- ── Left: Input Panel ── -->
      <aside class="sp-left">
        <div class="input-card" :class="{ 'input-card--loading': isProcessing }">
          <div class="input-card__overlay" v-if="isProcessing"></div>

          <div class="ic-section-label">Data Rencana Skripsi</div>

          <form @submit.prevent="onSubmit" class="ic-form">
            <!-- Judul -->
            <div class="ic-field">
              <label class="ic-label">Judul Proposal</label>
              <input
                v-model="judul"
                class="ic-input"
                placeholder="Contoh: Penerapan Deep Learning untuk..."
              />
            </div>

            <!-- Abstrak -->
            <div class="ic-field">
              <label class="ic-label">Abstrak <span class="ic-optional">(opsional)</span></label>
              <textarea
                v-model="abstrak"
                rows="5"
                class="ic-textarea"
                placeholder="Masukkan abstrak proposal..."
              ></textarea>
            </div>

            <!-- Top K -->
            <div class="ic-field">
              <label class="ic-label">Top K-Rank <span class="ic-optional">(opsional, default: 5)</span></label>
              <input
                type="number"
                v-model.number="kRank"
                min="1" max="50"
                class="ic-input"
                placeholder="Misal: 5"
              />
            </div>



            <p v-if="error" class="ic-error">⚠ {{ error }}</p>

            <button type="submit" :disabled="isProcessing" class="ic-submit">
              <svg v-if="isProcessing" class="ic-spin" fill="none" viewBox="0 0 24 24">
                <circle class="op25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              {{ isProcessing ? 'Memproses...' : 'Mulai Analisis AI →' }}
            </button>
          </form>
        </div>
      </aside>

      <!-- ── Right: Results Panel ── -->
      <main class="sp-right">

        <!-- Empty state -->
        <div v-if="!isProcessing && steps[0].status === 'idle'" class="sp-empty">
          <div class="sp-empty__icon">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <p class="sp-empty__title">Panel Analisis AI</p>
          <p class="sp-empty__sub">Isi data proposal di sebelah kiri, lalu klik <em>Mulai Analisis</em>.</p>
        </div>

        <div v-else class="sp-results">

          <!-- Pipeline Log section -->
          <div class="sp-card">
            <div class="sp-section-label">Pipeline Log</div>
            <ProgressStepper :steps="steps">
              <!-- Step 0: Preprocessing -->
              <template #step-0>
              <div v-if="pipeline?.preprocessing" class="plog-body">
                <div class="plog-block">
                  <div class="plog-block-label">Input Query</div>
                  <code class="plog-code">{{ pipeline.preprocessing.raw_query }}</code>
                </div>
                <div class="plog-row">
                  <div class="plog-block">
                    <div class="plog-block-label plog-label--gray">🔡 Setelah Case Fold <span class="plog-count">{{ pipeline.preprocessing.after_case_fold.length }} kata</span></div>
                    <div class="plog-tags">
                      <span v-for="t in pipeline.preprocessing.after_case_fold" :key="t" class="plog-tag plog-tag--gray">{{ t }}</span>
                    </div>
                  </div>
                  <div class="plog-block">
                    <div class="plog-block-label plog-label--red">🚫 Setelah Stopword <span class="plog-count">{{ pipeline.preprocessing.after_stopword.length }} tersisa</span></div>
                    <div class="plog-tags">
                      <span v-for="t in pipeline.preprocessing.after_stopword" :key="t" class="plog-tag plog-tag--red">{{ t }}</span>
                    </div>
                  </div>
                </div>
                <div v-if="pipeline.preprocessing.bigrams.length > 0" class="plog-block">
                  <div class="plog-block-label plog-label--blue">🔗 Bigram Terbentuk</div>
                  <div class="plog-tags">
                    <span v-for="t in pipeline.preprocessing.bigrams" :key="t" class="plog-tag plog-tag--blue">{{ t }}</span>
                  </div>
                </div>
                <div class="plog-footer">Total token BM25: <strong>{{ pipeline.preprocessing.total_tokens }}</strong></div>
              </div>
              <div v-else class="plog-wait">Menunggu data...</div>
            </template>

            <!-- Step 1: Ekspansi -->
            <template #step-1>
              <div v-if="pipeline?.ekspansi" class="plog-body">
                <div v-if="pipeline.ekspansi.num_frasa_ditemukan > 0">
                  <div class="plog-section-title">{{ pipeline.ekspansi.num_frasa_ditemukan }} frasa ditemukan dalam kamus</div>
                  <div class="plog-expand-list">
                    <div v-for="(sinonim, frasa) in pipeline.ekspansi.log" :key="frasa" class="plog-expand-row">
                      <span class="plog-tag plog-tag--amber plog-tag--bold">{{ frasa }}</span>
                      <span class="plog-arrow">→</span>
                      <template v-for="s in sinonim.split(' ')" :key="s">
                        <span class="plog-tag plog-tag--green">+ {{ s }}</span>
                      </template>
                    </div>
                  </div>
                </div>
                <div v-else class="plog-empty-msg">
                  <div class="plog-empty-icon">🔍</div>
                  <p>Tidak ada frasa yang cocok dengan kamus ontologi.</p>
                  <p class="plog-empty-sub">Query diproses tanpa ekspansi sinonim.</p>
                </div>
              </div>
              <div v-else class="plog-wait">Menunggu data...</div>
            </template>

            <!-- Step 2: BM25 -->
            <template #step-2>
              <div v-if="pipeline?.bm25" class="plog-body">
                <div class="plog-stats-row">
                  <div class="plog-stat plog-stat--blue">
                    <div class="plog-stat-val">{{ pipeline.bm25.num_candidates }}</div>
                    <div class="plog-stat-lbl">dosen lolos filter</div>
                  </div>
                  <div class="plog-stat plog-stat--gray">
                    <div class="plog-stat-val">{{ pipeline.bm25.num_total_dosen - pipeline.bm25.num_candidates }}</div>
                    <div class="plog-stat-lbl">BM25 = 0 (difilter)</div>
                  </div>
                </div>
                <div v-if="pipeline.bm25.top_candidates.length > 0" class="plog-ranklist">
                  <div class="plog-ranklist-header">Top Kandidat BM25</div>
                  <div v-for="(c, i) in pipeline.bm25.top_candidates" :key="i" class="plog-rankrow">
                    <span class="plog-rank-num">{{ i+1 }}</span>
                    <span class="plog-rank-name">{{ c.nama }}</span>
                    <div class="plog-score-bar">
                      <div class="plog-score-fill plog-score-fill--blue" :style="`width:${c.skor*100}%`"></div>
                    </div>
                    <span class="plog-score-val plog-score-val--blue">{{ c.skor.toFixed(4) }}</span>
                  </div>
                </div>
              </div>
              <div v-else class="plog-wait">Menunggu data...</div>
            </template>

            <!-- Step 3: SBERT -->
            <template #step-3>
              <div v-if="pipeline?.sbert" class="plog-body">
                <div class="plog-block plog-block--fuchsia">
                  <div class="plog-block-label plog-label--fuchsia">Teks Query yang Di-encode SBERT</div>
                  <code class="plog-code plog-code--fuchsia">{{ pipeline.sbert.query_text || '-' }}</code>
                </div>
                <div class="plog-info-row">
                  Cosine Similarity dihitung untuk <strong>{{ pipeline.sbert.num_computed }} dosen</strong> yang lolos BM25 filter.
                </div>
                <div v-if="pipeline.sbert.top_candidates.length > 0" class="plog-ranklist">
                  <div class="plog-ranklist-header">Top Kandidat SBERT</div>
                  <div v-for="(c, i) in pipeline.sbert.top_candidates" :key="i" class="plog-rankrow">
                    <span class="plog-rank-num">{{ i+1 }}</span>
                    <span class="plog-rank-name">{{ c.nama }}</span>
                    <div class="plog-score-bar">
                      <div class="plog-score-fill plog-score-fill--fuchsia" :style="`width:${c.skor*100}%`"></div>
                    </div>
                    <span class="plog-score-val plog-score-val--fuchsia">{{ c.skor.toFixed(4) }}</span>
                  </div>
                </div>
              </div>
              <div v-else class="plog-wait">Menunggu data...</div>
            </template>

            <!-- Step 4: Hybrid -->
            <template #step-4>
              <div v-if="pipeline?.hybrid" class="plog-body">
                <div class="plog-stats-row plog-stats-row--3">
                  <div class="plog-stat plog-stat--blue">
                    <div class="plog-stat-val">{{ Math.round(pipeline.hybrid.alpha * 100) }}%</div>
                    <div class="plog-stat-lbl">Bobot BM25 (α)</div>
                  </div>
                  <div class="plog-stat plog-stat--fuchsia">
                    <div class="plog-stat-val">{{ Math.round(pipeline.hybrid.beta * 100) }}%</div>
                    <div class="plog-stat-lbl">Bobot SBERT (β)</div>
                  </div>
                  <div class="plog-stat plog-stat--green">
                    <div class="plog-stat-val">{{ pipeline.hybrid.num_results }}</div>
                    <div class="plog-stat-lbl">Hasil Final</div>
                  </div>
                </div>
                <div class="plog-formula">
                  <span class="plog-formula-blue">{{ Math.round(pipeline.hybrid.alpha * 100) }}%</span> × BM25
                  + <span class="plog-formula-fuchsia">{{ Math.round(pipeline.hybrid.beta * 100) }}%</span> × SBERT
                  = <span class="plog-formula-brand">Hybrid Score</span>
                </div>
                <div class="plog-mode-badge" :class="pipeline.hybrid.mode === 'manual' ? 'plog-mode--manual' : (pipeline.hybrid.mode === 'keyword' ? 'plog-mode--blue' : 'plog-mode--fuchsia')">
                  {{ pipeline.hybrid.mode === 'manual' ? '⚙️ Manual Mode' : (pipeline.hybrid.mode === 'keyword' ? '⌨️ Keyword Mode (BM25 dominan)' : '📄 Abstrak Mode (SBERT dominan)') }}
                </div>
              </div>
              <div v-else class="plog-wait">Menunggu data...</div>
            </template>
          </ProgressStepper>
          </div>

          <!-- Results table -->
          <div v-if="recommendations.length > 0" class="sp-card res-section">
            <div class="res-header">
              <div class="sp-section-label" style="margin:0">Hasil Rekomendasi · Top {{ metadata?.k_rank }}</div>
              <div v-if="metadata" class="res-meta-badge">
                α={{ Math.round(metadata.alpha * 100) }}% BM25 · β={{ Math.round(metadata.beta * 100) }}% SBERT
              </div>
            </div>
            <div class="res-table-wrap">
              <table class="res-table">
                <thead>
                  <tr>
                    <th class="res-th res-th--center">#</th>
                    <th class="res-th">Nama Dosen</th>
                    <th class="res-th">Program Studi</th>
                    <th class="res-th res-th--center res-th--blue">BM25</th>
                    <th class="res-th res-th--center res-th--fuchsia">SBERT</th>
                    <th class="res-th res-th--center res-th--brand">Hybrid</th>
                  </tr>
                </thead>
                <tbody>
                  <DosenCard
                    v-for="(rec, index) in recommendations"
                    :key="index"
                    :index="index"
                    :dosen="rec.dosen"
                    :scores="rec.scores"
                    :xai="rec.xai"
                    @click="openXai(rec)"
                  />
                </tbody>
              </table>
            </div>
          </div>

          <!-- No results -->
          <div v-if="recommendations.length === 0 && steps[4].status === 'done'" class="sp-card sp-no-result">
            <div class="sp-no-result__icon">🔍</div>
            <h3>Tidak ada rekomendasi yang relevan</h3>
            <p>Skor BM25 semua dosen = 0. Coba tambahkan kata kunci yang lebih spesifik pada judul atau abstrak.</p>
          </div>

        </div>
      </main>
    </div>

    <XaiModal
      :isOpen="!!selectedDosen"
      :dosen="selectedDosen?.dosen"
      :xai="selectedDosen?.xai"
      @close="selectedDosen = null"
    />
  </div>
</template>

<style scoped>
/* ─── Page layout ─────────────────────────── */
.sp-wrap { display: flex; flex-direction: column; min-height: 100%; }

.sp-header {
  padding: 2.5rem 2.5rem 2rem;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}
.sp-badge {
  display: inline-block; font-size: 0.68rem; font-weight: 700;
  font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--green); background: var(--green-bg); border: 1px solid var(--green-border);
  padding: 2px 10px; border-radius: 99px; margin-bottom: 0.6rem;
}
.sp-title { font-size: 1.85rem; font-weight: 700; letter-spacing: -0.03em; color: var(--text-primary); margin: 0 0 0.5rem; }
.sp-lead { font-size: 1rem; color: var(--text-secondary); line-height: 1.65; margin: 0; max-width: 800px; }
.sp-lead strong { color: var(--text-primary); }

.sp-body {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 2.5rem;
  padding: 2.5rem;
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  align-items: start;
}

/* ─── Left Panel ─────────────────────────── */
.sp-left {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 1.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.input-card { position: relative; }
.input-card--loading { pointer-events: none; opacity: 0.7; }
.input-card__overlay {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(91,75,219,0.05), transparent);
  border-radius: var(--radius-lg);
  z-index: 1;
  pointer-events: none;
}

.ic-section-label {
  font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 1rem;
}
.ic-form { display: flex; flex-direction: column; gap: 1rem; }
.ic-field { display: flex; flex-direction: column; gap: 0.35rem; }
.ic-label { font-size: 0.825rem; font-weight: 600; color: var(--text-primary); }
.ic-optional { font-weight: 400; color: var(--text-muted); font-size: 0.75rem; }
.ic-input, .ic-textarea {
  width: 100%; padding: 0.6rem 0.75rem;
  background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--radius); font-size: 0.85rem; color: var(--text-primary);
  font-family: var(--font-sans); outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  resize: none; box-sizing: border-box;
}
.ic-input:focus, .ic-textarea:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 3px rgba(91,75,219,0.12);
}
.ic-input::placeholder, .ic-textarea::placeholder { color: var(--text-muted); }



.ic-error { font-size: 0.8rem; color: var(--red); font-weight: 500; margin: 0; }

.ic-submit {
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  width: 100%; padding: 0.7rem 1rem;
  background: var(--brand); color: white;
  font-size: 0.875rem; font-weight: 600;
  border: none; border-radius: var(--radius); cursor: pointer;
  transition: background 0.15s, transform 0.1s;
  box-shadow: 0 2px 8px rgba(91,75,219,0.25);
  margin-top: 0.25rem;
}
.ic-submit:hover:not(:disabled) { background: var(--brand-dim); transform: translateY(-1px); }
.ic-submit:disabled { background: var(--bg-muted); color: var(--text-muted); cursor: not-allowed; box-shadow: none; }
.ic-spin { width: 16px; height: 16px; animation: spin 0.7s linear infinite; }
.op25 { opacity: 0.25; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ─── Right Panel ─────────────────────────── */
.sp-right { 
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.sp-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.sp-empty {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  min-height: 320px; border: 2px dashed var(--border-strong); border-radius: var(--radius-xl);
  background: var(--bg-subtle); text-align: center; padding: 3rem 2rem;
}
.sp-empty__icon { width: 56px; height: 56px; color: var(--border-strong); margin-bottom: 1rem; }
.sp-empty__icon svg { width: 100%; height: 100%; }
.sp-empty__title { font-size: 0.95rem; font-weight: 600; color: var(--text-secondary); margin: 0 0 0.35rem; }
.sp-empty__sub { font-size: 0.825rem; color: var(--text-muted); margin: 0; }

.sp-results { display: flex; flex-direction: column; gap: 1.25rem; }
.sp-section-label {
  font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 0.65rem;
}

/* ─── Pipeline Log content ─────────────────────────── */
.plog-body { display: flex; flex-direction: column; gap: 0.75rem; }
.plog-wait { font-size: 0.8rem; color: var(--text-muted); padding: 0.25rem 0; }

.plog-block { display: flex; flex-direction: column; gap: 0.4rem; }
.plog-block--fuchsia { background: #fdf4ff; border: 1px solid #f0abfc; border-radius: var(--radius); padding: 0.65rem 0.85rem; }
.plog-block-label { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: var(--text-muted); display: flex; align-items: center; gap: 0.5rem; }
.plog-label--gray { color: #6b7280; }
.plog-label--red { color: var(--red); }
.plog-label--blue { color: var(--blue); }
.plog-label--fuchsia { color: var(--fuchsia); }
.plog-count { font-weight: 400; font-size: 0.65rem; color: var(--text-muted); }

.plog-code {
  font-family: var(--font-mono); font-size: 0.78rem;
  background: var(--bg-muted); border: 1px solid var(--border);
  border-radius: var(--radius-sm); padding: 0.5rem 0.75rem;
  word-break: break-all; line-height: 1.5; color: var(--text-primary);
}
.plog-code--fuchsia { background: white; border-color: #f0abfc; color: #7e22ce; }

.plog-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; }
.plog-tags { display: flex; flex-wrap: wrap; gap: 4px; }
.plog-tag { font-family: var(--font-mono); font-size: 0.7rem; padding: 2px 6px; border-radius: var(--radius-sm); border: 1px solid; }
.plog-tag--gray { background: var(--bg-muted); border-color: var(--border); color: var(--text-secondary); }
.plog-tag--red { background: var(--red-bg); border-color: var(--red-border); color: var(--red); }
.plog-tag--blue { background: var(--blue-bg); border-color: var(--blue-border); color: var(--blue); }
.plog-tag--amber { background: var(--amber-bg); border-color: var(--amber-border); color: var(--amber); }
.plog-tag--amber.plog-tag--bold { font-weight: 700; }
.plog-tag--green { background: var(--green-bg); border-color: var(--green-border); color: var(--green); }

.plog-footer { font-size: 0.72rem; color: var(--text-muted); text-align: right; font-family: var(--font-mono); }
.plog-footer strong { color: var(--brand); }

.plog-section-title { font-size: 0.78rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.5rem; }
.plog-expand-list { display: flex; flex-direction: column; gap: 0.5rem; }
.plog-expand-row { display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem; background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.5rem 0.75rem; }
.plog-arrow { font-size: 0.8rem; color: var(--border-strong); }

.plog-empty-msg { text-align: center; padding: 1rem; }
.plog-empty-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.plog-empty-msg p { font-size: 0.8rem; color: var(--text-muted); margin: 0 0 0.25rem; }
.plog-empty-sub { font-size: 0.72rem !important; }
.plog-info-row { font-size: 0.8rem; color: var(--text-secondary); background: var(--bg-subtle); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.6rem 0.85rem; }
.plog-info-row strong { color: var(--fuchsia); }

.plog-stats-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; }
.plog-stats-row--3 { grid-template-columns: 1fr 1fr 1fr; }
.plog-stat { border: 1px solid; border-radius: var(--radius); padding: 0.65rem; text-align: center; }
.plog-stat--blue { background: var(--blue-bg); border-color: var(--blue-border); }
.plog-stat--fuchsia { background: var(--fuchsia-bg); border-color: var(--fuchsia-border); }
.plog-stat--gray { background: var(--bg-subtle); border-color: var(--border); }
.plog-stat--green { background: var(--green-bg); border-color: var(--green-border); }
.plog-stat-val { font-size: 1.25rem; font-weight: 800; }
.plog-stat--blue .plog-stat-val { color: var(--blue); }
.plog-stat--fuchsia .plog-stat-val { color: var(--fuchsia); }
.plog-stat--gray .plog-stat-val { color: var(--text-muted); }
.plog-stat--green .plog-stat-val { color: var(--green); }
.plog-stat-lbl { font-size: 0.68rem; color: var(--text-muted); margin-top: 2px; }

.plog-ranklist { border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.plog-ranklist-header { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); padding: 0.5rem 0.75rem; background: var(--bg-subtle); border-bottom: 1px solid var(--border); }
.plog-rankrow { display: flex; align-items: center; gap: 0.6rem; padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--border); }
.plog-rankrow:last-child { border-bottom: none; }
.plog-rank-num { font-size: 0.72rem; font-weight: 700; color: var(--text-muted); width: 14px; text-align: center; flex-shrink: 0; }
.plog-rank-name { font-size: 0.82rem; font-weight: 500; color: var(--text-primary); flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.plog-score-bar { width: 64px; height: 5px; background: var(--bg-muted); border-radius: 99px; overflow: hidden; flex-shrink: 0; }
.plog-score-fill { height: 100%; border-radius: 99px; }
.plog-score-fill--blue { background: var(--blue); }
.plog-score-fill--fuchsia { background: var(--fuchsia); }
.plog-score-val { font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700; width: 46px; text-align: right; flex-shrink: 0; }
.plog-score-val--blue { color: var(--blue); }
.plog-score-val--fuchsia { color: var(--fuchsia); }

.plog-formula {
  font-family: var(--font-mono); font-size: 0.85rem;
  background: #0f0f14; color: #e4e4f0;
  border-radius: var(--radius); padding: 0.75rem 1rem;
  text-align: center;
}
.plog-formula-blue { color: #60a5fa; font-weight: 700; }
.plog-formula-fuchsia { color: #e879f9; font-weight: 700; }
.plog-formula-brand { color: #a78bfa; font-weight: 700; }

.plog-mode-badge {
  font-size: 0.8rem; font-weight: 600;
  padding: 0.5rem 0.85rem;
  border: 1px solid; border-radius: var(--radius);
  text-align: center;
}
.plog-mode--blue { background: var(--blue-bg); border-color: var(--blue-border); color: var(--blue); }
.plog-mode--fuchsia { background: var(--fuchsia-bg); border-color: var(--fuchsia-border); color: var(--fuchsia); }
.plog-mode--manual { background: var(--bg-muted); border-color: var(--border-strong); color: var(--text-primary); }

/* ─── Results ─────────────────────────── */
.res-section { margin-top: 0; }
.res-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.res-meta-badge {
  font-family: var(--font-mono); font-size: 0.72rem; font-weight: 600;
  background: var(--brand-light); color: var(--brand);
  border: 1px solid #c4b5fd; padding: 3px 10px; border-radius: 99px;
}
.res-table-wrap { border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; }
.res-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.res-th {
  background: var(--bg-subtle); border-bottom: 1px solid var(--border);
  padding: 0.6rem 0.85rem;
  font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.07em; color: var(--text-muted); text-align: left;
  white-space: nowrap;
}
.res-th--center { text-align: center; }
.res-th--blue { color: var(--blue); }
.res-th--fuchsia { color: var(--fuchsia); }
.res-th--brand { color: var(--brand); }

.sp-no-result {
  text-align: center; background: var(--bg-subtle);
  border: 1px dashed var(--border-strong); border-radius: var(--radius-xl);
  padding: 2.5rem 2rem;
}
.sp-no-result__icon { font-size: 2rem; margin-bottom: 0.75rem; }
.sp-no-result h3 { font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin: 0 0 0.35rem; }
.sp-no-result p { font-size: 0.825rem; color: var(--text-muted); margin: 0; }

@media (max-width: 900px) {
  .sp-body { grid-template-columns: 1fr; padding: 1.5rem; }
  .sp-header { padding: 1.5rem 1.5rem 1.25rem; }
}
</style>
