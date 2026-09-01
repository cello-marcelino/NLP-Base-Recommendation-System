<script setup>
import { ref, onMounted } from 'vue'
import { useSystemStore } from '../../stores/system'

const systemStore = useSystemStore()
const showExcelModal = ref(false)
const isReading = ref(false)
const uploadError = ref(null)

onMounted(() => {
  systemStore.fetchStatus()
  setInterval(() => {
    systemStore.fetchStatus()
  }, 15000)
})

const handleFileUpload = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  isReading.value = true
  uploadError.value = null
  try {
    await systemStore.loadExcelDataset(file)
    showExcelModal.value = false
  } catch (err) {
    uploadError.value = 'Gagal membaca file Excel dataset.'
  } finally {
    isReading.value = false
  }
}
</script>

<template>
  <div class="status-container">
    <div 
      class="status-badge"
      :class="{
        'badge-online': systemStore.isOnline && systemStore.isCacheReady && !systemStore.isExcelMode,
        'badge-warming': systemStore.isOnline && !systemStore.isCacheReady && !systemStore.isExcelMode,
        'badge-excel': systemStore.isExcelMode,
        'badge-offline': !systemStore.isOnline && !systemStore.isExcelMode
      }"
    >
      <div 
        class="status-dot"
        :class="{
          'dot-online': systemStore.isOnline && systemStore.isCacheReady && !systemStore.isExcelMode,
          'dot-warming': systemStore.isOnline && !systemStore.isCacheReady && !systemStore.isExcelMode,
          'dot-excel': systemStore.isExcelMode,
          'dot-offline': !systemStore.isOnline && !systemStore.isExcelMode
        }"
      ></div>

      <span v-if="systemStore.isExcelMode">Excel Mode ({{ systemStore.totalDosen }} Dosen)</span>
      <span v-else-if="systemStore.isOnline && systemStore.isCacheReady">Server Online ({{ systemStore.totalDosen }} Dosen)</span>
      <span v-else-if="systemStore.isOnline && !systemStore.isCacheReady">Server Warming Up...</span>
      <span v-else>Server Offline</span>

      <button 
        v-if="!systemStore.isOnline || systemStore.isExcelMode" 
        @click="showExcelModal = true" 
        class="btn-excel-toggle"
        title="Gunakan Excel Fallback"
      >
        {{ systemStore.isExcelMode ? 'Ganti Excel' : 'Gunakan Excel' }}
      </button>
    </div>

    <!-- Modal Excel File Reader -->
    <div v-if="showExcelModal" class="modal-backdrop" @click.self="showExcelModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Opsi Pembacaan Excel Fallback</h3>
          <button @click="showExcelModal = false" class="btn-close">×</button>
        </div>

        <div class="modal-body">
          <p class="modal-desc">
            Saat server offline atau bermasalah, Anda dapat mengunggah file dataset Excel (<code>dataset_profiles_terintegrasi.xlsx</code>) untuk membaca data dosen, publikasi, dan bimbingan langsung di browser.
          </p>

          <div v-if="uploadError" class="error-msg">{{ uploadError }}</div>

          <label class="drop-area">
            <svg width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <span class="drop-text">{{ isReading ? 'Membaca data Excel...' : 'Pilih File Excel Dataset (.xlsx)' }}</span>
            <input type="file" accept=".xlsx, .xls" @change="handleFileUpload" class="sr-only" :disabled="isReading" />
          </label>
        </div>

        <div class="modal-footer">
          <button v-if="systemStore.isExcelMode" @click="systemStore.clearExcelMode(); showExcelModal = false" class="btn-reset">
            Ganti ke Mode Server
          </button>
          <button @click="showExcelModal = false" class="btn-cancel">Tutup</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.status-container { position: relative; width: 100%; }
.status-badge {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.4rem 0.75rem; border-radius: 99px;
  font-size: 0.72rem; font-weight: 600; border: 1px solid;
  transition: all 0.2s;
}
.badge-online { background: #ecfdf5; border-color: #a7f3d0; color: #047857; }
.badge-warming { background: #fffbe6; border-color: #fde68a; color: #b45309; }
.badge-excel { background: #f0fdfa; border-color: #99f6e4; color: #0f766e; }
.badge-offline { background: #fef2f2; border-color: #fca5a5; color: #b91c1c; }

.status-dot { width: 8px; height: 8px; border-radius: 50%; animation: pulse 1.5s infinite; flex-shrink: 0; }
.dot-online { background: #10b981; }
.dot-warming { background: #f59e0b; }
.dot-excel { background: #0d9488; }
.dot-offline { background: #ef4444; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

.btn-excel-toggle {
  margin-left: auto; background: rgba(0,0,0,0.06); border: none;
  padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: 700;
  cursor: pointer; transition: background 0.15s;
}
.btn-excel-toggle:hover { background: rgba(0,0,0,0.12); }

/* Modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); backdrop-filter: blur(3px); display: flex; align-items: center; justify-content: center; z-index: 300; padding: 1rem; }
.modal-card { background: white; border-radius: 12px; max-width: 440px; width: 100%; padding: 1.5rem; box-shadow: 0 20px 40px rgba(0,0,0,0.25); color: #0f172a; }
.modal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
.modal-header h3 { font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0; }
.btn-close { background: none; border: none; font-size: 1.25rem; color: #94a3b8; cursor: pointer; }

.modal-body { display: flex; flex-direction: column; gap: 1rem; }
.modal-desc { font-size: 0.825rem; color: #475569; line-height: 1.5; margin: 0; }
.modal-desc code { font-family: monospace; background: #f1f5f9; padding: 2px 4px; border-radius: 4px; font-size: 0.78rem; }
.error-msg { background: #fef2f2; color: #991b1b; padding: 0.5rem; border-radius: 6px; font-size: 0.8rem; text-align: center; }

.drop-area { border: 2px dashed #cbd5e1; border-radius: 8px; padding: 1.75rem 1rem; text-align: center; background: #f8fafc; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 0.5rem; transition: background 0.15s; }
.drop-area:hover { background: #f1f5f9; border-color: #0d9488; }
.drop-text { font-size: 0.825rem; font-weight: 600; color: #0d9488; }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }

.modal-footer { display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem; margin-top: 1.25rem; }
.btn-reset { background: #fffbe6; color: #b45309; border: 1px solid #fde68a; padding: 0.4rem 0.85rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
.btn-cancel { background: #f1f5f9; color: #475569; border: none; padding: 0.4rem 0.85rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
</style>
