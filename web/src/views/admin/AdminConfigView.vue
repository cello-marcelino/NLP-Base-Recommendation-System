<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../../services/api'

const config = ref({
  threshold: 0.3,
  adaptive_alpha_threshold: 15,
  is_adaptive: true,
  manual_alpha: 0.7
})

const initialConfig = ref({})
const isLoading = ref(true)
const isSaving = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const showWarningModal = ref(false)

const DEFAULT_THRESHOLD = 0.3
const DEFAULT_ADAPTIVE = true

const fetchConfig = async () => {
  isLoading.value = true
  try {
    const res = await api.get('/admin/config')
    config.value = res.data.data
    initialConfig.value = JSON.parse(JSON.stringify(res.data.data))
  } catch (err) {
    errorMessage.value = err.userMessage || 'Gagal memuat konfigurasi engine'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchConfig()
})

const isModifiedFromDefault = computed(() => {
  return config.value.threshold !== DEFAULT_THRESHOLD || config.value.is_adaptive !== DEFAULT_ADAPTIVE
})

const promptSave = () => {
  if (isModifiedFromDefault.value) {
    showWarningModal.value = true
  } else {
    executeSave()
  }
}

const executeSave = async () => {
  showWarningModal.value = false
  isSaving.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const res = await api.put('/admin/config', config.value)
    config.value = res.data.data
    initialConfig.value = JSON.parse(JSON.stringify(res.data.data))
    successMessage.value = 'Konfigurasi NLP Engine berhasil diperbarui!'
  } catch (err) {
    errorMessage.value = err.userMessage || 'Gagal menyimpan perubahan konfigurasi'
  } finally {
    isSaving.value = false
  }
}

const resetToDefault = () => {
  config.value.threshold = 0.3
  config.value.adaptive_alpha_threshold = 15
  config.value.is_adaptive = true
  config.value.manual_alpha = 0.7
}
</script>

<template>
  <div class="admin-config-page">
    <div class="page-header">
      <span class="page-badge">NLP Engine Admin</span>
      <h1>Konfigurasi Parametrik Engine</h1>
      <p>Kelola parameter runtime rekomendasi hibrida (BM25 + Sentence-BERT). Perubahan akan langsung aktif untuk request berikutnya.</p>
    </div>

    <div v-if="isLoading" class="loading-box">
      <div class="spinner"></div>
      <span>Memuat konfigurasi engine...</span>
    </div>

    <form v-else @submit.prevent="promptSave" class="config-card">

      <!-- Default Optimization Banner -->
      <div class="opt-info-banner">
        <div class="banner-icon">[INFO]</div>
        <div>
          <strong>Konfigurasi Teroptimasi (Hasil Audit NLP):</strong>
          <p>Mesin SiReDo secara default menggunakan <code>threshold = 0.3</code> dan <code>is_adaptive = True</code> berdasarkan changelog optimasi Min-Max Normalization. Perubahan di luar angka ini dapat mempengaruhi relevansi ranking dosen.</p>
        </div>
      </div>

      <!-- Field 1: Threshold -->
      <div class="cf-section">
        <div class="cf-header">
          <div>
            <label class="cf-label">BM25 Min-Max Threshold Filter</label>
            <p class="cf-desc">Skor kelulusan minimal dosen. Rekomendasi di bawah threshold ini akan difilter out. (Default Teroptimasi: 0.3)</p>
          </div>
          <span class="cf-val">{{ Number(config.threshold).toFixed(2) }}</span>
        </div>
        <div class="slider-row">
          <span>0.0</span>
          <input type="range" v-model.number="config.threshold" min="0" max="1" step="0.05" class="cf-slider" />
          <span>1.0</span>
        </div>
      </div>

      <div class="cf-divider"></div>

      <!-- Field 2: Adaptive Mode -->
      <div class="cf-section">
        <div class="cf-header">
          <div>
            <label class="cf-label">Mode Pembobotan AI (Hybrid Adaptive)</label>
            <p class="cf-desc">Mode adaptif otomatis menyesuaikan bobot BM25 vs SBERT berdasarkan panjang token input (Keyword Mode vs Abstrak Mode).</p>
          </div>
          <button 
            type="button" 
            class="toggle-btn"
            :class="{ active: config.is_adaptive }"
            @click="config.is_adaptive = !config.is_adaptive"
          >
            <span class="toggle-thumb"></span>
          </button>
        </div>

        <!-- Adaptive Settings -->
        <div v-if="config.is_adaptive" class="sub-box adaptive-box">
          <div class="cf-header mb-2">
            <label class="cf-sublabel">Adaptive Token Limit Threshold</label>
            <input type="number" v-model.number="config.adaptive_alpha_threshold" min="5" max="50" class="input-num" />
          </div>
          <div class="adaptive-preview">
            <div class="mode-tag mode-kw">&lt; {{ config.adaptive_alpha_threshold }} Token → Keyword Mode (BM25 Dominan 70%)</div>
            <div class="mode-tag mode-abs">&ge; {{ config.adaptive_alpha_threshold }} Token → Abstrak Mode (SBERT Dominan 65%)</div>
          </div>
        </div>

        <!-- Manual Settings -->
        <div v-else class="sub-box manual-box">
          <div class="cf-header mb-2">
            <label class="cf-sublabel">Manual Alpha (Bobot BM25)</label>
            <span class="cf-subval">{{ Math.round(config.manual_alpha * 100) }}%</span>
          </div>
          <input type="range" v-model.number="config.manual_alpha" min="0" max="1" step="0.05" class="cf-slider" />
          <p class="cf-desc mt-2">Sisa bobot {{ Math.round((1 - config.manual_alpha) * 100) }}% dialokasikan untuk SBERT.</p>
        </div>
      </div>

      <!-- Action Footer -->
      <div class="config-footer">
        <p v-if="successMessage" class="msg msg-success">[OK] {{ successMessage }}</p>
        <p v-if="errorMessage" class="msg msg-error">[ERROR] {{ errorMessage }}</p>
        <div class="btn-group">
          <button type="button" @click="resetToDefault" class="btn-reset">Reset Ke Default (0.3)</button>
          <button type="submit" :disabled="isSaving" class="btn-save">
            {{ isSaving ? 'Menyimpan...' : 'Simpan Konfigurasi Engine' }}
          </button>
        </div>
      </div>
    </form>

    <!-- Warning Modal -->
    <div v-if="showWarningModal" class="modal-backdrop" @click.self="showWarningModal = false">
      <div class="warning-modal-box">
        <div class="warn-icon">[PERINGATAN]</div>
        <h3>Peringatan Perubahan Parameter Engine</h3>
        <p>Anda mencoba mengubah konfigurasi engine dari **nilai default teroptimasi** (Threshold: 0.3, Adaptive Mode: ON).</p>
        <p class="warn-highlight">Perubahan ini dapat mempengaruhi kualitas normalisasi skor Min-Max dan menyebabkan dosen yang tidak relevan masuk ke jajaran Top-5 rekomendasi.</p>
        
        <div class="warn-actions">
          <button type="button" @click="showWarningModal = false" class="btn-warn-cancel">Batal</button>
          <button type="button" @click="executeSave" class="btn-warn-confirm">Tetap Simpan Perubahan</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-config-page { padding: 2rem 2.5rem; width: 100%; max-width: 1200px; box-sizing: border-box; }
.page-header { margin-bottom: 2rem; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: #ccfbf1; color: #0f766e; padding: 3px 10px; border-radius: 99px; margin-bottom: 0.75rem; }
.page-header h1 { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem; }
.page-header p { font-size: 0.9rem; color: #64748b; margin: 0; line-height: 1.6; }

.loading-box { display: flex; align-items: center; gap: 0.75rem; color: #64748b; padding: 3rem 0; }
.spinner { width: 20px; height: 20px; border: 2px solid #cbd5e1; border-top-color: #0d9488; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.config-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.03); }
.opt-info-banner { background: #f0fdf4; border-bottom: 1px solid #bbf7d0; padding: 1.25rem 1.5rem; display: flex; align-items: flex-start; gap: 1rem; color: #166534; font-size: 0.85rem; line-height: 1.5; }
.banner-icon { font-size: 1.25rem; flex-shrink: 0; }
.opt-info-banner code { background: #dcfce7; padding: 2px 6px; border-radius: 4px; font-family: var(--font-mono, monospace); font-weight: 700; }

.cf-section { padding: 1.75rem 2rem; }
.cf-divider { height: 1px; background: #f1f5f9; margin: 0; }
.cf-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1.5rem; margin-bottom: 1rem; }
.cf-label { font-size: 0.95rem; font-weight: 700; color: #0f172a; display: block; margin-bottom: 0.25rem; }
.cf-desc { font-size: 0.83rem; color: #64748b; margin: 0; line-height: 1.5; }
.cf-val { font-family: var(--font-mono, monospace); font-size: 1.25rem; font-weight: 700; color: #0d9488; background: #ccfbf1; padding: 4px 12px; border-radius: 6px; }

.slider-row { display: flex; align-items: center; gap: 0.75rem; font-family: var(--font-mono, monospace); font-size: 0.8rem; color: #94a3b8; }
.cf-slider { flex: 1; accent-color: #0d9488; height: 6px; cursor: pointer; }

.toggle-btn { width: 48px; height: 26px; background: #cbd5e1; border: none; border-radius: 99px; position: relative; cursor: pointer; transition: background 0.2s; flex-shrink: 0; }
.toggle-btn.active { background: #0d9488; }
.toggle-thumb { width: 22px; height: 22px; background: white; border-radius: 50%; position: absolute; top: 2px; left: 2px; transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
.toggle-btn.active .toggle-thumb { transform: translateX(22px); }

.sub-box { border-radius: 8px; padding: 1.25rem; margin-top: 1rem; }
.adaptive-box { background: #f8fafc; border: 1px dashed #cbd5e1; }
.manual-box { background: #fffbebf; border: 1px dashed #fcd34d; }
.cf-sublabel { font-size: 0.85rem; font-weight: 600; color: #334155; }
.input-num { width: 70px; padding: 0.35rem 0.5rem; text-align: center; border: 1px solid #cbd5e1; border-radius: 6px; font-family: var(--font-mono, monospace); font-size: 0.9rem; }
.adaptive-preview { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.75rem; }
.mode-tag { font-size: 0.78rem; font-family: var(--font-mono, monospace); padding: 6px 10px; border-radius: 6px; font-weight: 600; }
.mode-kw { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.mode-abs { background: #fae8ff; color: #a21caf; border: 1px solid #f5d0fe; }

.config-footer { padding: 1.25rem 2rem; background: #f8fafc; border-top: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.btn-group { display: flex; align-items: center; gap: 0.75rem; }
.btn-reset { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-size: 0.85rem; font-weight: 600; padding: 0.65rem 1rem; border-radius: 6px; cursor: pointer; }
.btn-save { background: #0d9488; color: white; border: none; font-size: 0.875rem; font-weight: 600; padding: 0.65rem 1.25rem; border-radius: 6px; cursor: pointer; }
.btn-save:hover { background: #0f766e; }

.msg { font-size: 0.85rem; font-weight: 600; margin: 0; }
.msg-success { color: #166534; }
.msg-error { color: #dc2626; }

/* Warning Modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 300; padding: 1.5rem; }
.warning-modal-box { background: white; border-radius: 12px; max-width: 480px; width: 100%; padding: 2rem; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.25); }
.warn-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.warning-modal-box h3 { font-size: 1.2rem; font-weight: 700; color: #0f172a; margin: 0 0 0.75rem; }
.warning-modal-box p { font-size: 0.875rem; color: #475569; line-height: 1.5; margin: 0 0 0.75rem; }
.warn-highlight { background: #fff7ed; border: 1px solid #fed7aa; color: #c2410c; padding: 0.75rem; border-radius: 8px; font-size: 0.825rem; text-align: left; }

.warn-actions { display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; }
.btn-warn-cancel { background: #f1f5f9; color: #475569; border: none; padding: 0.6rem 1rem; border-radius: 6px; font-weight: 600; cursor: pointer; }
.btn-warn-confirm { background: #dc2626; color: white; border: none; padding: 0.6rem 1rem; border-radius: 6px; font-weight: 600; cursor: pointer; }
</style>
