<script setup>
import { ref } from 'vue'
import { useRecommendationStore } from '../stores/recommendation'
import RecommendationInputForm from '../components/recommendation/RecommendationInputForm.vue'
import ProgressStepper from '../components/recommendation/ProgressStepper.vue'
import PipelineLogAccordion from '../components/recommendation/PipelineLogAccordion.vue'
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
  <div class="sp-wrap">
    <!-- Page header -->
    <div class="sp-header">
      <span class="sp-badge">Live Tool</span>
      <h1 class="sp-title">Single Recommendation</h1>
      <p class="sp-lead">
        Analisis satu topik penelitian secara real-time — lihat skor <strong>BM25</strong>, <strong>SBERT</strong>, dan <strong>Hybrid</strong> beserta Pipeline Log dan XAI Explanation.
      </p>
    </div>

    <!-- Two-column layout -->
    <div class="sp-body">
      <!-- Left: Input Panel -->
      <aside class="sp-left">
        <RecommendationInputForm @submit="recStore.executeSingleRecommendation()" />
      </aside>

      <!-- Right: Processing & Results Panel -->
      <main class="sp-right">
        <!-- Initial empty state -->
        <div v-if="!recStore.isProcessing && recStore.recommendations.length === 0" class="sp-placeholder">
          <div class="sp-ph-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
          </div>
          <div class="sp-ph-title">Belum Ada Analisis Berjalan</div>
          <div class="sp-ph-desc">Masukkan judul atau rencana penelitian pada formulir di sebelah kiri, lalu tekan tombol <strong>Analisis & Rekomendasikan</strong>.</div>
        </div>

        <!-- Processing Stepper Progress -->
        <div v-if="recStore.isProcessing || recStore.recommendations.length > 0" class="sp-stepper-container">
          <ProgressStepper :steps="recStore.steps">
            <template #step-0>
              <div v-if="recStore.pipeline?.preprocessing" class="text-xs space-y-1">
                <div><strong>Tokens:</strong> {{ recStore.pipeline.preprocessing.total_tokens }} token terdeteksi.</div>
                <div class="text-gray-500 font-mono">{{ recStore.pipeline.preprocessing.final_tokens?.join(', ') }}</div>
              </div>
            </template>
            <template #step-1>
              <div v-if="recStore.pipeline?.ekspansi" class="text-xs">
                <div><strong>Frasa ditemukan:</strong> {{ recStore.pipeline.ekspansi.num_frasa_ditemukan }}</div>
              </div>
            </template>
            <template #step-2>
              <div v-if="recStore.pipeline?.bm25" class="text-xs">
                <div><strong>Kandidat lolos BM25:</strong> {{ recStore.pipeline.bm25.num_candidates }} dosen.</div>
              </div>
            </template>
            <template #step-3>
              <div v-if="recStore.pipeline?.sbert" class="text-xs">
                <div><strong>SBERT dihitung:</strong> {{ recStore.pipeline.sbert.num_computed }} embeddings.</div>
              </div>
            </template>
            <template #step-4>
              <div v-if="recStore.pipeline?.hybrid" class="text-xs">
                <div><strong>Mode:</strong> {{ recStore.pipeline.hybrid.mode }} (α: {{ recStore.pipeline.hybrid.alpha }}, β: {{ recStore.pipeline.hybrid.beta }})</div>
              </div>
            </template>
          </ProgressStepper>
        </div>

        <!-- Pipeline Log Accordion -->
        <div v-if="recStore.pipeline" class="mt-6">
          <PipelineLogAccordion :pipeline="recStore.pipeline" />
        </div>

        <!-- Recommendation Results Table -->
        <div v-if="recStore.recommendations.length > 0" class="sp-results-card mt-6">
          <div class="sp-results-header">
            <div>
              <h2 class="sp-results-title">Peringkat Rekomendasi Dosen</h2>
              <p class="sp-results-subtitle">Klik baris dosen untuk melihat detail Explainable AI (XAI) & Riwayat.</p>
            </div>
            <div v-if="recStore.metadata" class="sp-results-meta">
              <span class="sp-meta-tag">Top-{{ recStore.metadata.k_rank }}</span>
              <span class="sp-meta-tag sp-meta-tag--brand">α: {{ recStore.metadata.alpha }} / β: {{ recStore.metadata.beta }}</span>
            </div>
          </div>

          <div class="sp-table-wrap">
            <table class="sp-table">
              <thead>
                <tr>
                  <th style="width: 50px; text-align: center;">Rank</th>
                  <th>Dosen & Keyword Irisan</th>
                  <th>Program Studi</th>
                  <th style="text-align: center;">BM25</th>
                  <th style="text-align: center;">SBERT</th>
                  <th style="text-align: center; width: 120px;">Hybrid</th>
                </tr>
              </thead>
              <tbody>
                <DosenCard
                  v-for="(rec, idx) in recStore.recommendations"
                  :key="idx"
                  :index="idx"
                  :dosen="rec.dosen"
                  :scores="rec.scores"
                  :xai="rec.xai"
                  @click="openXai(rec)"
                />
              </tbody>
            </table>
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
.sp-wrap {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sp-header {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.sp-badge {
  align-self: flex-start;
  font-size: 0.68rem;
  font-weight: 700;
  color: #16a34a;
  background: #dcfce7;
  padding: 3px 8px;
  border-radius: 99px;
  font-family: var(--font-mono);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.sp-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin: 0;
}
.sp-lead {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.sp-body {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 1.5rem;
  align-items: start;
}

.sp-left {
  position: sticky;
  top: 1.5rem;
}

.sp-right {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.sp-placeholder {
  background: var(--bg);
  border: 2px dashed var(--border-strong);
  border-radius: var(--radius-xl);
  padding: 4rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
}
.sp-ph-icon {
  width: 56px; height: 56px;
  background: var(--bg-muted);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-muted);
}
.sp-ph-icon svg { width: 28px; height: 28px; }
.sp-ph-title { font-size: 1.05rem; font-weight: 700; color: var(--text-primary); }
.sp-ph-desc { font-size: 0.85rem; color: var(--text-secondary); max-width: 420px; line-height: 1.5; }

.sp-results-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.sp-results-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.sp-results-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}
.sp-results-subtitle {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin: 0.15rem 0 0;
}

.sp-results-meta { display: flex; gap: 0.5rem; }
.sp-meta-tag {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  background: var(--bg-muted);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}
.sp-meta-tag--brand {
  background: var(--brand-light);
  color: var(--brand);
}

.sp-table-wrap {
  overflow-x: auto;
}
.sp-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}
.sp-table th {
  padding: 0.75rem 0.75rem;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  background: var(--bg-subtle);
  border-bottom: 1px solid var(--border);
}

@media (max-width: 1024px) {
  .sp-body {
    grid-template-columns: 1fr;
  }
  .sp-left {
    position: static;
  }
}
</style>
