<script setup>
import { ref } from 'vue'
import api from '../../services/api'

const file = ref(null)
const kRank = ref(5)
const isProcessing = ref(false)
const errorMessage = ref(null)
const batchResults = ref([])

const handleFileChange = (e) => {
  file.value = e.target.files[0]
}

const submitExcel = async () => {
  if (!file.value) {
    errorMessage.value = 'Pilih file Excel terlebih dahulu'
    return
  }
  
  isProcessing.value = true
  errorMessage.value = null
  batchResults.value = []

  const formData = new FormData()
  formData.append('file', file.value)
  if (kRank.value) {
    formData.append('k_rank', kRank.value)
  }
  
  try {
    const res = await api.post('/admin/recommendation/batch', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    batchResults.value = res.data.data || []
  } catch (err) {
    errorMessage.value = err.userMessage || 'Gagal memproses batch recommendation'
  } finally {
    isProcessing.value = false
  }
}

const downloadJson = () => {
  if (batchResults.value.length === 0) return
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(batchResults.value, null, 2))
  const downloadAnchor = document.createElement('a')
  downloadAnchor.setAttribute("href", dataStr)
  downloadAnchor.setAttribute("download", `siredo_admin_batch_${new Date().toISOString().slice(0,10)}.json`)
  document.body.appendChild(downloadAnchor)
  downloadAnchor.click()
  downloadAnchor.remove()
}
</script>

<template>
  <div class="admin-batch-page">
    <div class="page-header">
      <span class="page-badge">Admin Tool</span>
      <h1>Simulasi Batch Recommendation</h1>
      <p>Upload dataset proposal skripsi dalam format Excel (.xlsx) untuk memproses rekomendasi pembimbing secara masif.</p>
    </div>

    <div class="batch-content">
      <!-- Upload Card -->
      <div class="card upload-card">
        <div class="upload-instructions">
          <h4>Ketentuan Header Excel (.xlsx)</h4>
          <p>Baris 1 file Excel wajib memuat nama kolom: <code>id</code>, <code>judul</code>, dan <code>abstrak</code>.</p>
        </div>

        <div class="dropzone" :class="{ 'has-file': file }">
          <svg class="drop-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <label class="btn-file-select">
            <span>{{ file ? file.name : 'Pilih File Excel Dataset (.xlsx)' }}</span>
            <input type="file" class="sr-only" accept=".xlsx, .xls" @change="handleFileChange" />
          </label>
        </div>

        <div class="options-row">
          <label>Top K-Rank Rekomendasi:</label>
          <input type="number" v-model.number="kRank" min="1" max="20" class="input-rank" />
        </div>

        <button @click="submitExcel" :disabled="!file || isProcessing" class="btn-process">
          <span v-if="!isProcessing">Jalankan Batch Simulation</span>
          <span v-else>Memproses Dataset...</span>
        </button>

        <p v-if="errorMessage" class="error-msg">[ERROR] {{ errorMessage }}</p>
      </div>

      <!-- Results Table -->
      <div v-if="batchResults.length > 0" class="card results-card">
        <div class="results-header">
          <h3>Hasil Batch Simulation ({{ batchResults.length }} Tesis)</h3>
          <button @click="downloadJson" class="btn-download">Download Format JSON</button>
        </div>

        <div class="table-wrap">
          <table class="res-table">
            <thead>
              <tr>
                <th>ID / Judul Proposal</th>
                <th>Top Rekomendasi Dosen</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="res in batchResults" :key="res.id">
                <td>
                  <div class="res-id">ID: {{ res.id }}</div>
                  <div class="res-title">{{ res.judul || '(Tanpa Judul)' }}</div>
                </td>
                <td>
                  <div class="rec-list">
                    <div v-for="(rec, i) in res.rekomendasi?.recommendations || []" :key="i" class="rec-item">
                      <span class="rec-num">{{ i + 1 }}</span>
                      <span class="rec-name">{{ rec.dosen.nama }}</span>
                      <span class="rec-score">{{ (rec.scores.hybrid * 100).toFixed(1) }}%</span>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-batch-page { padding: 2rem 2.5rem; width: 100%; max-width: 100%; box-sizing: border-box; }
.page-header { margin-bottom: 2rem; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: #ccfbf1; color: #0f766e; padding: 3px 10px; border-radius: 99px; margin-bottom: 0.75rem; }
.page-header h1 { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem; }
.page-header p { font-size: 0.9rem; color: #64748b; margin: 0; }

.card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.75rem; margin-bottom: 2rem; }
.upload-instructions h4 { font-size: 0.95rem; font-weight: 700; color: #0f172a; margin: 0 0 0.35rem; }
.upload-instructions p { font-size: 0.83rem; color: #64748b; margin: 0 0 1.25rem; }
.upload-instructions code { font-family: var(--font-mono, monospace); background: #ccfbf1; color: #0f766e; padding: 2px 6px; border-radius: 4px; }

.dropzone { border: 2px dashed #cbd5e1; border-radius: 10px; background: #f8fafc; padding: 2.5rem 1.5rem; text-align: center; margin-bottom: 1.5rem; }
.dropzone.has-file { background: #f0fdf4; border-color: #0d9488; }
.drop-icon { width: 44px; height: 44px; margin: 0 auto 1rem; color: #94a3b8; }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }

.btn-file-select span { background: white; color: #0d9488; border: 1px solid #0d9488; font-size: 0.875rem; font-weight: 600; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; }
.options-row { display: flex; align-items: center; justify-content: center; gap: 0.75rem; font-size: 0.85rem; font-weight: 600; color: #334155; margin-bottom: 1.5rem; }
.input-rank { width: 70px; padding: 0.4rem; text-align: center; border: 1px solid #cbd5e1; border-radius: 6px; font-family: var(--font-mono, monospace); }

.btn-process { width: 100%; padding: 0.85rem; background: #0d9488; color: white; border: none; border-radius: 8px; font-size: 0.925rem; font-weight: 600; cursor: pointer; }
.btn-process:hover:not(:disabled) { background: #0f766e; }
.btn-process:disabled { opacity: 0.6; cursor: not-allowed; }
.error-msg { font-size: 0.83rem; color: #dc2626; text-align: center; margin-top: 1rem; }

.results-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; }
.results-header h3 { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0; }
.btn-download { background: #ccfbf1; color: #0f766e; border: none; font-size: 0.8rem; font-weight: 600; padding: 0.4rem 0.85rem; border-radius: 6px; cursor: pointer; }

.table-wrap { overflow-x: auto; }
.res-table { width: 100%; border-collapse: collapse; text-align: left; }
.res-table th { background: #f8fafc; padding: 0.75rem 1rem; font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; }
.res-table td { padding: 1rem; border-bottom: 1px solid #f1f5f9; vertical-align: top; }
.res-id { font-size: 0.72rem; font-family: var(--font-mono, monospace); color: #94a3b8; font-weight: 700; margin-bottom: 0.25rem; }
.res-title { font-size: 0.875rem; font-weight: 600; color: #0f172a; }

.rec-list { display: flex; flex-direction: column; gap: 0.4rem; }
.rec-item { display: flex; align-items: center; gap: 0.6rem; font-size: 0.83rem; }
.rec-num { width: 20px; height: 20px; border-radius: 50%; background: #f1f5f9; color: #64748b; font-size: 0.68rem; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.rec-name { font-weight: 500; color: #1e293b; flex: 1; }
.rec-score { font-family: var(--font-mono, monospace); font-size: 0.75rem; font-weight: 700; background: #ccfbf1; color: #0f766e; padding: 2px 6px; border-radius: 4px; }
</style>
