<script setup>
import { ref } from 'vue'
import { useRecommendationStore } from '../stores/recommendation'
import RecommendationInputForm from '../components/recommendation/RecommendationInputForm.vue'
import ProgressStepper from '../components/recommendation/ProgressStepper.vue'
import DosenCard from '../components/recommendation/DosenCard.vue'
import XaiModal from '../components/recommendation/XaiModal.vue'

const recStore = useRecommendationStore()
const isXaiModalOpen = ref(false)

const openXai = (rec) => {
  recStore.selectedDosenXai = rec
  isXaiModalOpen.value = true
}

const closeXai = () => {
  isXaiModalOpen.value = false
  recStore.selectedDosenXai = null
}
</script>

<template>
  <div class="single-page">
    <!-- Header -->
    <div class="sp-header">
      <div class="sp-header__inner">
        <span class="page-badge">Live Tool</span>
        <h1 class="sp-title">Single Recommendation</h1>
        <p class="sp-lead">
          Analisis satu topik penelitian secara real-time — lihat skor <strong>BM25</strong>, <strong>SBERT</strong>, dan <strong>Hybrid</strong> beserta Pipeline Log dan XAI Explanation.
        </p>
      </div>
    </div>

    <!-- Body Layout -->
    <div class="sp-body">
      <!-- Left: Input Panel -->
      <aside class="sp-left">
        <RecommendationInputForm @submit="recStore.executeSingleRecommendation()" />
      </aside>

      <!-- Right: Results Panel -->
      <main class="sp-right">
        <!-- Empty State -->
        <div v-if="!recStore.isProcessing && recStore.recommendations.length === 0" class="sp-empty">
          <div class="sp-empty__icon">
            <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <p class="sp-empty__title">Panel Analisis AI</p>
          <p class="sp-empty__sub">Isi data penelitian di sebelah kiri, lalu klik <em>Mulai Analisis</em>.</p>
        </div>

        <div v-else class="sp-results">
          <!-- Pipeline Log section (Legacy Visual Style) -->
          <div class="sp-card">
            <div class="sp-section-label">Pipeline Log</div>
            <ProgressStepper :steps="recStore.steps">
              <!-- Step 0: Preprocessing -->
              <template #step-0>
                <div v-if="recStore.pipeline?.preprocessing" class="plog-body">
                  <div class="plog-block">
                    <div class="plog-block-label">Input Query</div>
                    <code class="plog-code">{{ recStore.pipeline.preprocessing.raw_query }}</code>
                  </div>
                  <div class="plog-row">
                    <div class="plog-block">
                      <div class="plog-block-label plog-label--gray">🔡 Setelah Case Fold <span class="plog-count">{{ recStore.pipeline.preprocessing.after_case_fold?.length || 0 }} kata</span></div>
                      <div class="plog-tags">
                        <span v-for="t in recStore.pipeline.preprocessing.after_case_fold" :key="t" class="plog-tag plog-tag--gray">{{ t }}</span>
                      </div>
                    </div>
                    <div class="plog-block">
                      <div class="plog-block-label plog-label--red">🚫 Setelah Stopword <span class="plog-count">{{ recStore.pipeline.preprocessing.after_stopword?.length || 0 }} tersisa</span></div>
                      <div class="plog-tags">
                        <span v-for="t in recStore.pipeline.preprocessing.after_stopword" :key="t" class="plog-tag plog-tag--red">{{ t }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-if="recStore.pipeline.preprocessing.bigrams?.length > 0" class="plog-block">
                    <div class="plog-block-label plog-label--blue">🔗 Bigram Terbentuk</div>
                    <div class="plog-tags">
                      <span v-for="t in recStore.pipeline.preprocessing.bigrams" :key="t" class="plog-tag plog-tag--blue">{{ t }}</span>
                    </div>
                  </div>
                  <div class="plog-footer">Total token BM25: <strong>{{ recStore.pipeline.preprocessing.total_tokens }}</strong></div>
                </div>
                <div v-else class="plog-wait">Menunggu data...</div>
              </template>

              <!-- Step 1: Ekspansi -->
              <template #step-1>
                <div v-if="recStore.pipeline?.ekspansi" class="plog-body">
                  <div v-if="recStore.pipeline.ekspansi.num_frasa_ditemukan > 0">
                    <div class="plog-section-title">{{ recStore.pipeline.ekspansi.num_frasa_ditemukan }} frasa ditemukan dalam kamus</div>
                    <div class="plog-expand-list">
                      <div v-for="(sinonim, frasa) in recStore.pipeline.ekspansi.log" :key="frasa" class="plog-expand-row">
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
                <div v-if="recStore.pipeline?.bm25" class="plog-body">
                  <div class="plog-stats-row">
                    <div class="plog-stat plog-stat--blue">
                      <div class="plog-stat-val">{{ recStore.pipeline.bm25.num_candidates }}</div>
                      <div class="plog-stat-lbl">dosen lolos filter</div>
                    </div>
                    <div class="plog-stat plog-stat--gray">
                      <div class="plog-stat-val">{{ recStore.pipeline.bm25.num_total_dosen - recStore.pipeline.bm25.num_candidates }}</div>
                      <div class="plog-stat-lbl">BM25 = 0 (difilter)</div>
                    </div>
                  </div>
                  <div v-if="recStore.pipeline.bm25.top_candidates?.length > 0" class="plog-ranklist">
                    <div class="plog-ranklist-header">Top Kandidat BM25</div>
                    <div v-for="(c, i) in recStore.pipeline.bm25.top_candidates" :key="i" class="plog-rankrow">
                      <span class="plog-rank-num">{{ i + 1 }}</span>
                      <span class="plog-rank-name">{{ c.nama }}</span>
                      <div class="plog-score-bar">
                        <div class="plog-score-fill plog-score-fill--blue" :style="`width:${c.skor * 100}%`"></div>
                      </div>
                      <span class="plog-score-val plog-score-val--blue">{{ c.skor.toFixed(4) }}</span>
                    </div>
                  </div>
                </div>
                <div v-else class="plog-wait">Menunggu data...</div>
              </template>

              <!-- Step 3: SBERT -->
              <template #step-3>
                <div v-if="recStore.pipeline?.sbert" class="plog-body">
                  <div class="plog-block plog-block--fuchsia">
                    <div class="plog-block-label plog-label--fuchsia">Teks Query yang Di-encode SBERT</div>
                    <code class="plog-code plog-code--fuchsia">{{ recStore.pipeline.sbert.query_text || '-' }}</code>
                  </div>
                  <div class="plog-info-row">
                    Cosine Similarity dihitung untuk <strong>{{ recStore.pipeline.sbert.num_computed }} dosen</strong> yang lolos BM25 filter.
                  </div>
                  <div v-if="recStore.pipeline.sbert.top_candidates?.length > 0" class="plog-ranklist">
                    <div class="plog-ranklist-header">Top Kandidat SBERT</div>
                    <div v-for="(c, i) in recStore.pipeline.sbert.top_candidates" :key="i" class="plog-rankrow">
                      <span class="plog-rank-num">{{ i + 1 }}</span>
                      <span class="plog-rank-name">{{ c.nama }}</span>
                      <div class="plog-score-bar">
                        <div class="plog-score-fill plog-score-fill--fuchsia" :style="`width:${c.skor * 100}%`"></div>
                      </div>
                      <span class="plog-score-val plog-score-val--fuchsia">{{ c.skor.toFixed(4) }}</span>
                    </div>
                  </div>
                </div>
                <div v-else class="plog-wait">Menunggu data...</div>
              </template>

              <!-- Step 4: Hybrid -->
              <template #step-4>
                <div v-if="recStore.pipeline?.hybrid" class="plog-body">
                  <div class="plog-stats-row plog-stats-row--3">
                    <div class="plog-stat plog-stat--blue">
                      <div class="plog-stat-val">{{ Math.round(recStore.pipeline.hybrid.alpha * 100) }}%</div>
                      <div class="plog-stat-lbl">Bobot BM25 (α)</div>
                    </div>
                    <div class="plog-stat plog-stat--fuchsia">
                      <div class="plog-stat-val">{{ Math.round(recStore.pipeline.hybrid.beta * 100) }}%</div>
                      <div class="plog-stat-lbl">Bobot SBERT (β)</div>
                    </div>
                    <div class="plog-stat plog-stat--green">
                      <div class="plog-stat-val">{{ recStore.pipeline.hybrid.num_results }}</div>
                      <div class="plog-stat-lbl">Hasil Final</div>
                    </div>
                  </div>
                  <div class="plog-formula">
                    <span class="plog-formula-blue">{{ Math.round(recStore.pipeline.hybrid.alpha * 100) }}%</span> × BM25
                    + <span class="plog-formula-fuchsia">{{ Math.round(recStore.pipeline.hybrid.beta * 100) }}%</span> × SBERT
                    = <span class="plog-formula-brand">Hybrid Score</span>
                  </div>
                  <div class="plog-mode-badge" :class="recStore.pipeline.hybrid.mode === 'manual' ? 'plog-mode--manual' : (recStore.pipeline.hybrid.mode === 'keyword' ? 'plog-mode--blue' : 'plog-mode--fuchsia')">
                    {{ recStore.pipeline.hybrid.mode === 'manual' ? '⚙️ Manual Mode' : (recStore.pipeline.hybrid.mode === 'keyword' ? '⌨️ Keyword Mode (BM25 dominan)' : '📄 Abstrak Mode (SBERT dominan)') }}
                  </div>
                </div>
                <div v-else class="plog-wait">Menunggu data...</div>
              </template>
            </ProgressStepper>
          </div>

          <!-- Results table -->
          <div v-if="recStore.recommendations.length > 0" class="sp-card res-section">
            <div class="res-header">
              <div class="sp-section-label" style="margin:0">Hasil Rekomendasi · Top {{ recStore.metadata?.k_rank }}</div>
              <div v-if="recStore.metadata" class="res-meta-badge">
                α={{ Math.round(recStore.metadata.alpha * 100) }}% BM25 · β={{ Math.round(recStore.metadata.beta * 100) }}% SBERT
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
                    v-for="(rec, index) in recStore.recommendations"
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
        </div>
      </main>
    </div>

    <!-- XAI Modal -->
    <XaiModal
      :isOpen="isXaiModalOpen"
      :dosen="recStore.selectedDosenXai?.dosen"
      :xai="recStore.selectedDosenXai?.xai"
      @close="closeXai"
    />
  </div>
</template>

<style scoped>
.single-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

/* ─── Header ─────────────────────────── */
.sp-header {
  padding: 2.5rem 2.5rem 2rem;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.sp-header__inner {
  max-width: 1400px;
  margin: 0 auto;
}
.page-badge {
  display: inline-block; font-size: 0.68rem; font-weight: 700;
  font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--green); background: var(--green-bg); border: 1px solid var(--green-border);
  padding: 2px 10px; border-radius: 99px; margin-bottom: 0.75rem;
}
.sp-title {
  font-size: 1.85rem; font-weight: 700; letter-spacing: -0.03em;
  color: var(--text-primary); margin: 0 0 0.5rem;
}
.sp-lead {
  font-size: 1rem; color: var(--text-secondary); line-height: 1.65; margin: 0;
  max-width: 800px;
}

/* ─── Body ─────────────────────────── */
.sp-body {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 2rem;
  padding: 2.5rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  align-items: start;
  box-sizing: border-box;
}

.sp-left {
  position: sticky;
  top: 2rem;
}

.sp-right {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  min-width: 0;
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

/* ─── Pipeline Log content (Legacy Styling) ─────────────────────────── */
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

/* ─── Results Table ─────────────────────────── */
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

@media (max-width: 900px) {
  .sp-body { grid-template-columns: 1fr; padding: 1.5rem; }
  .sp-header { padding: 1.5rem 1.5rem 1.25rem; }
}
</style>
