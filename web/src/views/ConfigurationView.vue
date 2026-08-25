<script setup>
import { onMounted } from 'vue'
import { useConfigStore } from '../stores/config'

const configStore = useConfigStore()

onMounted(() => {
  configStore.fetchConfig()
})

const onSave = async () => {
  await configStore.saveConfig(configStore.config)
}
</script>

<template>
  <div class="config-page">
    <div class="config-inner">

      <!-- Page header -->
      <div class="page-header">
        <span class="page-badge">Sistem</span>
        <h1>Konfigurasi</h1>
        <p class="page-lead">Atur parameter global mesin rekomendasi. Perubahan akan langsung aktif untuk semua request berikutnya.</p>
      </div>

      <div v-if="configStore.isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <span>Memuat konfigurasi...</span>
      </div>

      <form v-else @submit.prevent="onSave" class="config-form">

        <div class="config-field">
          <div class="cf-header">
            <div>
              <label class="cf-label">BM25 Hard Filter Threshold</label>
              <p class="cf-desc">Skor BM25 mentah minimum agar dosen dihitung skor semantiknya. Nilai 0.0 berarti semua dosen dengan skor mentah &gt; 0 lolos (strict mode). Naikkan untuk lebih selektif.</p>
            </div>
            <span class="cf-value">{{ Number(configStore.config.threshold).toFixed(1) }}</span>
          </div>
          <div class="slider-wrap">
            <span class="slider-tick">0.0</span>
            <input type="range" v-model.number="configStore.config.threshold" min="0" max="5" step="0.1" class="cf-range">
            <span class="slider-tick">5.0</span>
          </div>
        </div>

        <div class="config-divider"></div>

        <!-- Mode Pembobotan AI -->
        <div class="config-field">
          <div class="cf-header">
            <div>
              <label class="cf-label">Mode Pembobotan AI (Hybrid Ranking)</label>
              <p class="cf-desc">Gunakan mode adaptif untuk pembobotan dinamis berdasarkan panjang input, atau atur bobot α (BM25) dan β (SBERT) secara manual.</p>
            </div>
            <button
              type="button"
              class="ic-toggle"
              :class="{ 'ic-toggle--on': configStore.config.is_adaptive }"
              @click="configStore.config.is_adaptive = !configStore.config.is_adaptive"
            >
              <span class="ic-toggle-thumb"></span>
            </button>
          </div>

          <!-- Adaptive Mode Options -->
          <div v-if="configStore.config.is_adaptive" class="adaptive-settings">
            <div class="config-field" style="margin-top:1rem;">
              <div class="cf-header">
                <div>
                  <label class="cf-label" style="font-size:0.8rem">Adaptive Alpha — Token Limit</label>
                  <p class="cf-desc">Batas token query untuk beralih antara Keyword Mode (BM25 dominan) dan Abstrak Mode (SBERT dominan).</p>
                </div>
                <div class="cf-number-wrap">
                  <input type="number" v-model.number="configStore.config.adaptive_alpha_threshold" min="5" max="50" class="cf-number">
                  <span class="cf-number-unit">token</span>
                </div>
              </div>
              <div class="mode-preview">
                <div class="mode-card mode-keyword">
                  <span class="mode-label">⌨️ Keyword Mode</span>
                  <span class="mode-detail">&lt; {{ configStore.config.adaptive_alpha_threshold }} token → α=70% BM25</span>
                </div>
                <div class="mode-sep">↔</div>
                <div class="mode-card mode-abstrak">
                  <span class="mode-label">📄 Abstrak Mode</span>
                  <span class="mode-detail">≥ {{ configStore.config.adaptive_alpha_threshold }} token → β=65% SBERT</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Manual Mode Options -->
          <div v-else class="manual-settings">
            <div class="cf-header" style="margin-top:1rem; margin-bottom:0.5rem">
              <span class="cf-label" style="font-size:0.8rem">Manual Alpha (Bobot BM25)</span>
              <span class="cf-value">{{ Math.round(configStore.config.manual_alpha * 100) }}%</span>
            </div>
            <div class="slider-wrap">
              <span class="slider-tick">0%</span>
              <input type="range" v-model.number="configStore.config.manual_alpha" min="0" max="1" step="0.05" class="cf-range">
              <span class="slider-tick">100%</span>
            </div>
            <p class="cf-desc" style="margin-top:0.5rem">Sisa bobot ({{ Math.round((1 - configStore.config.manual_alpha) * 100) }}%) akan dialokasikan untuk SBERT.</p>
          </div>
        </div>

        <!-- Save Footer -->
        <div class="config-footer">
          <p v-if="configStore.successMessage" class="cf-message cf-success">{{ configStore.successMessage }}</p>
          <p v-if="configStore.error" class="cf-message cf-error">{{ configStore.error }}</p>
          <button type="submit" :disabled="configStore.isSaving" class="btn-save">
            <svg v-if="configStore.isSaving" class="spin-icon" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            {{ configStore.isSaving ? 'Menyimpan...' : 'Simpan Konfigurasi' }}
          </button>
        </div>
      </form>

    </div>
  </div>
</template>

<style scoped>
.config-page { padding: 3rem 2.5rem 5rem; }
.config-inner { max-width: 680px; }

.page-header { margin-bottom: 2.5rem; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--brand); background: var(--brand-light); border: 1px solid #c4b5fd; padding: 3px 10px; border-radius: 99px; margin-bottom: 1rem; }
.page-header h1 { font-size: 1.85rem; font-weight: 700; letter-spacing: -0.03em; color: var(--text-primary); margin: 0 0 0.5rem; }
.page-lead { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.7; margin: 0; }

.loading-state { display: flex; align-items: center; gap: 0.75rem; color: var(--text-muted); font-size: 0.875rem; padding: 2rem 0; }
.loading-spinner { width: 18px; height: 18px; border: 2px solid var(--border); border-top-color: var(--brand); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.config-form {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}
.config-field { padding: 1.75rem 2rem; }
.config-divider { height: 1px; background: var(--border); margin: 0; }

.cf-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1.5rem; margin-bottom: 1.25rem; }
.cf-label { display: block; font-size: 0.925rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.35rem; }
.cf-desc { font-size: 0.83rem; color: var(--text-secondary); line-height: 1.6; margin: 0; }
.cf-value {
  font-family: var(--font-mono);
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--brand);
  background: var(--brand-light);
  min-width: 3rem;
  text-align: center;
  padding: 0.3rem 0.6rem;
  border-radius: var(--radius);
  flex-shrink: 0;
  line-height: 1;
}

.slider-wrap { display: flex; align-items: center; gap: 0.75rem; }
.slider-tick { font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted); width: 2rem; text-align: center; flex-shrink: 0; }
.cf-range {
  flex: 1;
  height: 5px;
  background: var(--border);
  border-radius: 99px;
  appearance: none;
  cursor: pointer;
  accent-color: var(--brand);
}
.cf-range::-webkit-slider-thumb { appearance: none; width: 18px; height: 18px; border-radius: 50%; background: var(--brand); border: 2px solid white; box-shadow: 0 1px 4px rgba(0,0,0,0.2); cursor: pointer; }

.cf-number-wrap { display: flex; align-items: center; gap: 0.4rem; flex-shrink: 0; }
.cf-number {
  width: 64px;
  font-family: var(--font-mono);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--brand);
  background: var(--brand-light);
  border: 1px solid #c4b5fd;
  border-radius: var(--radius);
  padding: 0.4rem 0.6rem;
  text-align: center;
}
.cf-number:focus { outline: 2px solid var(--brand); outline-offset: 1px; }
.cf-number-unit { font-size: 0.75rem; color: var(--text-muted); }

.mode-preview { display: flex; align-items: center; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap; }
.mode-card { flex: 1; min-width: 140px; border: 1px solid var(--border); border-radius: var(--radius); padding: 0.75rem 1rem; display: flex; flex-direction: column; gap: 0.25rem; }
.mode-keyword { background: var(--blue-bg); border-color: var(--blue-border); }
.mode-abstrak { background: var(--fuchsia-bg); border-color: var(--fuchsia-border); }
.mode-label { font-size: 0.8rem; font-weight: 600; color: var(--text-primary); }
.mode-detail { font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-muted); }
.mode-sep { font-size: 1.2rem; color: var(--border-strong); flex-shrink: 0; }

.ic-toggle {
  position: relative; width: 44px; height: 24px;
  background: var(--border-strong); border: none; border-radius: 99px;
  cursor: pointer; transition: background 0.2s; flex-shrink: 0;
}
.ic-toggle--on { background: var(--brand); }
.ic-toggle-thumb {
  position: absolute; top: 2px; left: 2px;
  width: 20px; height: 20px; border-radius: 50%; background: white;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.ic-toggle--on .ic-toggle-thumb { transform: translateX(20px); }

.adaptive-settings {
  background: var(--bg-subtle);
  border: 1px dashed var(--border-strong);
  border-radius: var(--radius-lg);
  padding: 1rem 1.5rem;
  margin-top: 1rem;
}

.manual-settings {
  background: var(--amber-bg);
  border: 1px dashed var(--amber-border);
  border-radius: var(--radius-lg);
  padding: 1rem 1.5rem;
  margin-top: 1rem;
}

.config-footer { padding: 1.25rem 2rem; border-top: 1px solid var(--border); background: var(--bg-subtle); display: flex; align-items: center; justify-content: flex-end; gap: 1rem; }
.cf-message { font-size: 0.85rem; font-weight: 500; margin: 0; flex: 1; }
.cf-success { color: var(--green); }
.cf-error { color: var(--red); }
.btn-save {
  display: flex; align-items: center; gap: 0.5rem;
  background: var(--brand); color: white;
  font-size: 0.875rem; font-weight: 600;
  padding: 0.6rem 1.25rem;
  border: none; border-radius: var(--radius);
  cursor: pointer;
  transition: background 0.15s;
}
.btn-save:hover:not(:disabled) { background: var(--brand-dim); }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
.spin-icon { width: 16px; height: 16px; animation: spin 0.7s linear infinite; }

@media (max-width: 600px) {
  .config-page { padding: 1.5rem 1rem 3rem; }
  .config-field { padding: 1.25rem 1.25rem; }
  .config-footer { padding: 1rem 1.25rem; }
}
</style>
