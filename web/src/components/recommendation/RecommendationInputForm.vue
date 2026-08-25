<script setup>
import { useRecommendationStore } from '../../stores/recommendation'

const recStore = useRecommendationStore()

const emit = defineEmits(['submit'])

const presetExamples = [
  {
    title: 'Chatbot Akademik berbasis NLP BERT',
    abstract: 'Pengembangan asisten virtual mahasiswa dengan pemrosesan bahasa alami (NLP), ekstraksi intent, dan transformer BERT untuk menjawab pertanyaan akademik.'
  },
  {
    title: 'Deteksi Penyakit Daun Tanaman via Computer Vision',
    abstract: 'Klasifikasi citra daun tanaman menggunakan Convolutional Neural Network (CNN) dan YOLO untuk identifikasi penyakit secara otomatis pada sektor pertanian.'
  },
  {
    title: 'Sistem Pendukung Keputusan Pemilihan Supplier',
    abstract: 'Penerapan metode AHP dan TOPSIS untuk perangkingan dan seleksi pemasok bahan baku terbaik berdasarkan kriteria biaya, kualitas, dan waktu pengiriman.'
  }
]

const loadPreset = (preset) => {
  recStore.judul = preset.title
  recStore.abstrak = preset.abstract
}
</script>

<template>
  <div class="input-card" :class="{ 'input-card--loading': recStore.isProcessing }">
    <div class="input-card__overlay" v-if="recStore.isProcessing"></div>

    <div class="ic-section-label">Data Topik / Rencana Penelitian</div>

    <form @submit.prevent="$emit('submit')" class="ic-form">
      <!-- Judul -->
      <div class="ic-field">
        <label class="ic-label">Judul Penelitian</label>
        <input
          v-model="recStore.judul"
          class="ic-input"
          placeholder="Contoh: Sistem Rekomendasi Tempat Wisata dengan Algoritma Hybrid"
          :disabled="recStore.isProcessing"
        />
      </div>

      <!-- Abstrak -->
      <div class="ic-field">
        <label class="ic-label">
          Abstrak / Rencana Penelitian
          <span class="ic-optional">Opsional tapi disarankan</span>
        </label>
        <textarea
          v-model="recStore.abstrak"
          class="ic-textarea"
          rows="5"
          placeholder="Tuliskan latar belakang, metode, teknologi yang digunakan, serta tujuan penelitian secara ringkas..."
          :disabled="recStore.isProcessing"
        ></textarea>
      </div>

      <!-- K-Rank -->
      <div class="ic-field">
        <div class="ic-k-row">
          <label class="ic-label" style="margin-bottom:0;">Jumlah Rekomendasi (Top-K)</label>
          <span class="ic-k-badge">{{ recStore.kRank }} Dosen</span>
        </div>
        <input
          type="range"
          min="1"
          max="15"
          v-model.number="recStore.kRank"
          class="ic-slider"
          :disabled="recStore.isProcessing"
        />
        <div class="ic-slider-ticks">
          <span>1</span><span>5</span><span>10</span><span>15</span>
        </div>
      </div>

      <!-- Error -->
      <div v-if="recStore.error" class="ic-error">
        <svg class="ic-error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ recStore.error }}</span>
      </div>

      <!-- Actions -->
      <div class="ic-actions">
        <button
          type="submit"
          class="btn-primary w-full"
          :disabled="recStore.isProcessing"
        >
          <svg v-if="!recStore.isProcessing" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <div v-else class="btn-spinner"></div>
          <span>{{ recStore.isProcessing ? 'Menganalisis Korpus...' : 'Analisis & Rekomendasikan' }}</span>
        </button>

        <button
          type="button"
          class="btn-ghost w-full"
          @click="recStore.resetSingle()"
          :disabled="recStore.isProcessing"
        >
          Reset Form
        </button>
      </div>
    </form>

    <!-- Preset Suggestions -->
    <div class="ic-presets">
      <div class="ic-presets-title">Contoh Topik Cepat:</div>
      <div class="ic-presets-list">
        <button
          v-for="(preset, idx) in presetExamples"
          :key="idx"
          type="button"
          class="ic-preset-btn"
          @click="loadPreset(preset)"
          :disabled="recStore.isProcessing"
        >
          {{ preset.title }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.input-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  position: relative;
  box-shadow: var(--shadow-sm);
}
.input-card--loading { opacity: 0.9; }
.input-card__overlay {
  position: absolute; inset: 0;
  background: rgba(255,255,255,0.4);
  border-radius: var(--radius-xl);
  z-index: 10;
}

.ic-section-label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.ic-form { display: flex; flex-direction: column; gap: 1.1rem; }

.ic-field { display: flex; flex-direction: column; gap: 0.4rem; }

.ic-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.ic-optional {
  font-size: 0.72rem;
  font-weight: 400;
  color: var(--text-muted);
}

.ic-input, .ic-textarea {
  width: 100%;
  padding: 0.65rem 0.85rem;
  background: var(--bg-subtle);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  font-size: 0.875rem;
  color: var(--text-primary);
  transition: all 0.15s;
  font-family: var(--font-sans);
}
.ic-input:focus, .ic-textarea:focus {
  outline: none;
  border-color: var(--brand);
  background: var(--bg);
  box-shadow: 0 0 0 3px rgba(91, 75, 219, 0.12);
}

.ic-k-row { display: flex; align-items: center; justify-content: space-between; }
.ic-k-badge {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--brand);
  background: var(--brand-light);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.ic-slider {
  width: 100%;
  accent-color: var(--brand);
  cursor: pointer;
}
.ic-slider-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 0.68rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.ic-error {
  background: var(--red-bg);
  color: var(--red);
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  font-size: 0.8rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.ic-error-icon { width: 18px; height: 18px; flex-shrink: 0; }

.ic-actions { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem; }

.btn-primary {
  background: var(--brand);
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: background 0.15s, transform 0.1s;
}
.btn-primary:hover:not(:disabled) {
  background: var(--brand-dark);
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  padding: 0.5rem;
  border-radius: var(--radius);
  font-size: 0.8rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-ghost:hover:not(:disabled) {
  background: var(--bg-muted);
  color: var(--text-primary);
}

.btn-spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.ic-presets {
  border-top: 1px solid var(--border);
  padding-top: 1rem;
}
.ic-presets-title {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}
.ic-presets-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.ic-preset-btn {
  text-align: left;
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  padding: 0.4rem 0.6rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.ic-preset-btn:hover {
  background: var(--brand-light);
  border-color: var(--brand-dim);
  color: var(--brand);
}
</style>
