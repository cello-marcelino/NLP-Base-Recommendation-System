<script setup>
import { ref } from 'vue'
import api from '../services/api'

const file = ref(null)
const kRank = ref(5)
const isUploading = ref(false)
const results = ref([])
const error = ref('')

const handleFileChange = (e) => { file.value = e.target.files[0] }

const submitExcel = async () => {
  if (!file.value) { error.value = 'Pilih file Excel terlebih dahulu'; return }
  error.value = ''
  isUploading.value = true
  results.value = []
  const formData = new FormData()
  formData.append('file', file.value)
  if (kRank.value) formData.append('k_rank', kRank.value)
  try {
    const res = await api.post('/rekomendasi/batch/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    results.value = res.data.data
  } catch (err) {
    error.value = err.response?.data?.message || err.message
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div class="batch-page">

    <!-- Page header -->
    <div class="bp-header">
      <span class="bp-badge">Live Tool</span>
      <h1 class="bp-title">Batch Recommendation</h1>
      <p class="bp-lead">Proses banyak proposal sekaligus via upload Excel atau JSON payload. Cocok untuk otomatisasi penjadwalan dosen penguji massal.</p>
    </div>

    <!-- Main Content -->
    <div class="bp-body">

      <!-- Upload Section -->
      <div class="bp-card mb-8">
        <div class="bp-card-content">
          
          <div class="upload-instructions">
            <h4>Format Header Kolom Excel</h4>
            <p>Pastikan file Excel Anda (.xlsx) memiliki baris pertama (header) dengan nama kolom berikut dalam huruf kecil:</p>
            <div class="header-format">
              <span class="col-badge">id</span>
              <span class="col-badge">judul</span>
              <span class="col-badge">abstrak</span>
            </div>
          </div>

          <!-- Excel Upload -->
          <div class="bp-excel-area">
            <div 
              class="upload-dropzone"
              :class="{ 'upload-dropzone--has-file': file }"
            >
              <div class="upload-icon">
                <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <div class="upload-text">
                <label class="upload-btn">
                  <span>{{ file ? file.name : 'Pilih file Excel (.xlsx)' }}</span>
                  <input type="file" class="sr-only" accept=".xlsx, .xls" @change="handleFileChange">
                </label>
              </div>
              <p class="upload-text">atau seret ke sini</p>
              <p class="upload-hint">Ukuran maksimum file 10MB.</p>
            </div>

            <div class="bp-options">
              <label class="bp-opt-label">Top K-Rank <span class="bp-opt-hint">(opsional, default: 5)</span></label>
              <input type="number" v-model.number="kRank" min="1" max="50" class="bp-opt-input" placeholder="Misal: 5">
            </div>
            
            <button 
              @click="submitExcel"
              :disabled="!file || isUploading"
              class="bp-submit-btn"
            >
              <svg v-if="isUploading" class="ic-spin" fill="none" viewBox="0 0 24 24">
                <circle class="op25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              {{ isUploading ? 'Memproses Batch...' : 'Mulai Proses Batch' }}
            </button>
          </div>
          
          <p v-if="error" class="bp-error mt-4 text-center">⚠ {{ error }}</p>
        </div>
      </div>
      
      <!-- Results Section -->
      <div v-if="results.length > 0" class="bp-card bp-results-card">
        <div class="bp-results-header">
          <h3 class="bp-results-title">Hasil Pemrosesan Batch ({{ results.length }} Item)</h3>
          <button class="bp-download-btn">Download JSON</button>
        </div>
        
        <div class="bp-table-wrap">
          <table class="bp-table">
            <thead>
              <tr>
                <th class="bp-th w-1/3">ID / Proposal</th>
                <th class="bp-th">Top Rekomendasi (Dosen & Skor Hybrid)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="res in results" :key="res.id" class="bp-tr">
                <td class="bp-td">
                  <div class="bp-td-id">ID: {{ res.id }}</div>
                  <div class="bp-td-title" :title="res.judul">{{ res.judul || '(Tanpa Judul)' }}</div>
                </td>
                <td class="bp-td">
                  <div class="bp-rec-list">
                    <div v-for="(rec, i) in res.rekomendasi?.recommendations || []" :key="i" class="bp-rec-item">
                      <span class="bp-rec-num">{{ i + 1 }}</span>
                      <span class="bp-rec-name">{{ rec.dosen.nama }}</span>
                      <span class="bp-rec-score">{{ (rec.scores.hybrid * 100).toFixed(1) }}%</span>
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
/* ─── Page layout ─────────────────────────── */
.batch-page { display: flex; flex-direction: column; min-height: 100%; }

.bp-header {
  padding: 2.5rem 2.5rem 2rem;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}
.bp-badge {
  display: inline-block; font-size: 0.68rem; font-weight: 700;
  font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--green); background: var(--green-bg); border: 1px solid var(--green-border);
  padding: 2px 10px; border-radius: 99px; margin-bottom: 0.75rem;
}
.bp-title { font-size: 1.85rem; font-weight: 700; letter-spacing: -0.03em; color: var(--text-primary); margin: 0 0 0.5rem; }
.bp-lead { font-size: 1rem; color: var(--text-secondary); line-height: 1.65; margin: 0; max-width: 800px; }

.bp-body {
  padding: 2.5rem;
  flex: 1;
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
}

/* ─── Cards & Tabs ─────────────────────────── */
.bp-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.mb-8 { margin-bottom: 2rem; }
.mt-4 { margin-top: 1rem; }
.text-center { text-align: center; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border-width: 0; }

.bp-card-content { padding: 1.5rem; }

/* ─── Excel Upload ─────────────────────────── */
.upload-instructions {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px dashed var(--border-strong);
  text-align: center;
}
.upload-instructions h4 {
  font-size: 0.95rem; font-weight: 700; color: var(--text-primary); margin: 0 0 0.5rem;
}
.upload-instructions p {
  font-size: 0.825rem; color: var(--text-secondary); margin: 0 0 1rem;
}
.header-format {
  display: flex; gap: 0.75rem; justify-content: center;
}
.col-badge {
  font-family: var(--font-mono); font-size: 0.75rem; font-weight: 600;
  color: var(--brand); background: var(--brand-light);
  padding: 4px 10px; border-radius: var(--radius-sm);
  border: 1px solid #c4b5fd;
}

.bp-excel-area { max-width: 600px; margin: 0 auto; text-align: center; }

.upload-dropzone {
  padding: 2rem 1.5rem;
  border: 2px dashed var(--border-strong);
  border-radius: var(--radius-lg);
  background: var(--bg-subtle);
  transition: all 0.2s;
}
.upload-dropzone:hover { background: var(--bg-muted); }
.upload-dropzone--has-file {
  background: var(--brand-light);
  border-color: #c4b5fd;
  border-style: solid;
}

.upload-icon { width: 48px; height: 48px; margin: 0 auto 1rem; color: var(--text-muted); }
.upload-icon svg { width: 100%; height: 100%; }

.upload-text { font-size: 0.875rem; color: var(--text-secondary); display: flex; align-items: center; justify-content: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.75rem; }
.upload-btn {
  cursor: pointer;
  background: var(--bg);
  color: var(--brand);
  font-weight: 600;
  padding: 0.35rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  transition: all 0.15s;
}
.upload-btn:hover { border-color: var(--brand); color: var(--brand-dim); }

.upload-hint { font-size: 0.75rem; color: var(--text-muted); margin: 0; }

.bp-options { margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: center; gap: 0.75rem; }
.bp-opt-label { font-size: 0.85rem; font-weight: 600; color: var(--text-primary); }
.bp-opt-hint { font-weight: 400; color: var(--text-muted); font-size: 0.75rem; }
.bp-opt-input { width: 80px; padding: 0.4rem 0.6rem; border: 1px solid var(--border); border-radius: var(--radius-sm); font-size: 0.85rem; font-family: var(--font-mono); text-align: center; }

.bp-submit-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  width: 100%; margin-top: 1.5rem; padding: 0.85rem 1.5rem;
  background: var(--brand); color: white;
  font-size: 0.925rem; font-weight: 600;
  border: none; border-radius: var(--radius);
  cursor: pointer; transition: background 0.15s, transform 0.1s;
  box-shadow: 0 2px 8px rgba(91,75,219,0.25);
}
.bp-submit-btn:hover:not(:disabled) { background: var(--brand-dim); transform: translateY(-1px); }
.bp-submit-btn:disabled { background: var(--bg-muted); color: var(--text-muted); cursor: not-allowed; box-shadow: none; }
.ic-spin { width: 18px; height: 18px; animation: spin 0.7s linear infinite; }
.op25 { opacity: 0.25; }
@keyframes spin { to { transform: rotate(360deg); } }

.bp-error { font-size: 0.85rem; color: var(--red); font-weight: 500; }


/* ─── Results Table ─────────────────────────── */
.bp-results-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg-subtle);
  display: flex; align-items: center; justify-content: space-between;
}
.bp-results-title { font-size: 1.05rem; font-weight: 700; color: var(--text-primary); margin: 0; }
.bp-download-btn {
  font-size: 0.75rem; font-weight: 600;
  color: var(--brand); background: var(--brand-light);
  border: none; border-radius: var(--radius-sm);
  padding: 0.4rem 0.85rem; cursor: pointer; transition: opacity 0.15s;
}
.bp-download-btn:hover { opacity: 0.8; }

.bp-table-wrap { overflow-x: auto; }
.bp-table { width: 100%; border-collapse: collapse; }
.bp-th {
  padding: 0.85rem 1.5rem; text-align: left;
  font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--text-muted);
  background: var(--bg-subtle); border-bottom: 1px solid var(--border);
}
.bp-tr { border-bottom: 1px solid var(--border); transition: background 0.15s; }
.bp-tr:hover { background: var(--bg-muted); }
.bp-tr:last-child { border-bottom: none; }
.bp-td { padding: 1.25rem 1.5rem; vertical-align: top; }

.bp-td-id { font-size: 0.72rem; font-weight: 700; font-family: var(--font-mono); color: var(--text-muted); margin-bottom: 0.35rem; }
.bp-td-title { font-size: 0.875rem; font-weight: 600; color: var(--text-primary); line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

.bp-rec-list { display: flex; flex-direction: column; gap: 0.5rem; }
.bp-rec-item { display: flex; align-items: center; gap: 0.75rem; font-size: 0.85rem; }
.bp-rec-num {
  display: flex; align-items: center; justify-content: center;
  width: 1.25rem; height: 1.25rem; border-radius: 50%;
  background: var(--bg-muted); color: var(--text-muted);
  font-size: 0.65rem; font-weight: 700;
}
.bp-rec-name { font-weight: 500; color: var(--text-primary); flex: 1; }
.bp-rec-score {
  font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700;
  color: var(--brand); background: var(--brand-light);
  padding: 2px 6px; border-radius: var(--radius-sm);
}

@media (max-width: 768px) {
  .bp-header { padding: 1.5rem 1.25rem; }
  .bp-body { padding: 1.25rem; }
  .bp-td { padding: 1rem; }
  .w-1\/3 { width: auto; }
}
</style>
