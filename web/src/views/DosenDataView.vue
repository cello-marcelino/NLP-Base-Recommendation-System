<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const dosenList = ref([])
const isLoading = ref(true)
const error = ref('')
const searchQuery = ref('')
const selectedDosenRiwayat = ref(null)
const riwayatType = ref('')

const parsedRiwayatList = computed(() => {
  if (!selectedDosenRiwayat.value) return []
  if (riwayatType.value === 'jurnal') return parseStringList(selectedDosenRiwayat.value.jurnal)
  if (riwayatType.value === 'bimbing') return parseStringList(selectedDosenRiwayat.value.judul_bimbing)
  if (riwayatType.value === 'uji') return parseStringList(selectedDosenRiwayat.value.judul_uji)
  return []
})

const getListCount = (str) => {
  return parseStringList(str).length
}

const openRiwayatModal = (dosen, type) => {
  selectedDosenRiwayat.value = dosen
  riwayatType.value = type
}

const getRiwayatTitle = () => {
  if (riwayatType.value === 'jurnal') return 'Publikasi Jurnal'
  if (riwayatType.value === 'bimbing') return 'Riwayat Bimbingan'
  if (riwayatType.value === 'uji') return 'Riwayat Ujian'
  return 'Riwayat Akademik'
}

const fetchDosen = async () => {
  try {
    const res = await api.get('/dosen')
    dosenList.value = res.data.data
  } catch (err) {
    error.value = err.response?.data?.message || err.message
  } finally {
    isLoading.value = false
  }
}

const filteredDosen = computed(() => {
  if (!searchQuery.value) return dosenList.value
  const q = searchQuery.value.toLowerCase()
  return dosenList.value.filter(d => 
    (d.nama && d.nama.toLowerCase().includes(q)) || 
    (d.program_studi && d.program_studi.toLowerCase().includes(q)) ||
    (d.bidang_keahlian && d.bidang_keahlian.toLowerCase().includes(q))
  )
})

onMounted(() => {
  fetchDosen()
})
</script>

<template>
  <div class="dosen-page">
    
    <!-- Header -->
    <div class="dp-header">
      <span class="page-badge">Data Master</span>
      <h1 class="dp-title">Data Dosen</h1>
      <p class="dp-lead">Lihat dan cari seluruh data dosen yang terdaftar di dalam sistem rekomendasi, lengkap dengan program studi dan bidang keahlian.</p>
    </div>

    <!-- Content -->
    <div class="dp-body">
      
      <!-- Search Bar -->
      <div class="search-wrap">
        <div class="search-icon">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-input" 
          placeholder="Cari nama, program studi, atau keahlian dosen..." 
        />
        <div class="search-badge" v-if="!isLoading">{{ filteredDosen.length }} dosen</div>
      </div>

      <!-- State: Loading -->
      <div v-if="isLoading" class="state-box">
        <div class="spin-icon"></div>
        <p>Memuat data dosen dari server...</p>
      </div>

      <!-- State: Error -->
      <div v-else-if="error" class="state-box error-box">
        <div class="error-icon">⚠</div>
        <p>{{ error }}</p>
      </div>

      <!-- State: Empty Search -->
      <div v-else-if="filteredDosen.length === 0" class="state-box">
        <div class="empty-icon">🔍</div>
        <p>Tidak ada dosen yang cocok dengan pencarian "<strong>{{ searchQuery }}</strong>"</p>
      </div>

      <!-- Table -->
      <div v-else class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th class="th-no">No</th>
              <th class="th-nama">Nama Lengkap</th>
              <th class="th-prodi">Program Studi</th>
              <th class="th-keahlian">Bidang Keahlian</th>
              <th class="th-riwayat">Riwayat Akademik</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(dosen, idx) in filteredDosen" :key="idx" class="data-row">
              <td class="td-no">{{ idx + 1 }}</td>
              <td class="td-nama">
                <div class="dosen-nama">{{ dosen.nama }}</div>
                <div class="dosen-nidn">NIDN: {{ dosen.id || '-' }}</div>
              </td>
              <td class="td-prodi">{{ dosen.program_studi }}</td>
              <td class="td-keahlian">
                <div class="keahlian-text">{{ dosen.bidang_keahlian || '-' }}</div>
              </td>
              <td class="td-riwayat">
                <div class="riwayat-actions">
                  <button class="jurnal-btn" @click="openRiwayatModal(dosen, 'jurnal')" :disabled="getListCount(dosen.jurnal) === 0" title="Publikasi Jurnal">
                    <span class="jurnal-badge" :class="{ 'jurnal-badge--zero': getListCount(dosen.jurnal) === 0 }">{{ getListCount(dosen.jurnal) }}</span>
                    <span class="jurnal-btn-text">Jurnal</span>
                  </button>
                  <button class="jurnal-btn" @click="openRiwayatModal(dosen, 'bimbing')" :disabled="getListCount(dosen.judul_bimbing) === 0" title="Riwayat Bimbingan">
                    <span class="jurnal-badge" :class="{ 'jurnal-badge--zero': getListCount(dosen.judul_bimbing) === 0 }">{{ getListCount(dosen.judul_bimbing) }}</span>
                    <span class="jurnal-btn-text">Bimbing</span>
                  </button>
                  <button class="jurnal-btn" @click="openRiwayatModal(dosen, 'uji')" :disabled="getListCount(dosen.judul_uji) === 0" title="Riwayat Ujian">
                    <span class="jurnal-badge" :class="{ 'jurnal-badge--zero': getListCount(dosen.judul_uji) === 0 }">{{ getListCount(dosen.judul_uji) }}</span>
                    <span class="jurnal-btn-text">Uji</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
    
    <!-- Riwayat Modal -->
    <div v-if="selectedDosenRiwayat" class="jurnal-modal-overlay" @click.self="selectedDosenRiwayat = null">
      <div class="jurnal-modal-box">
        <div class="jurnal-modal-header">
          <div>
            <h3 class="jurnal-modal-title">{{ getRiwayatTitle() }}</h3>
            <p class="jurnal-modal-subtitle">{{ selectedDosenRiwayat.nama }}</p>
          </div>
          <button @click="selectedDosenRiwayat = null" class="jurnal-modal-close">
            <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="jurnal-modal-body">
          <ul class="jurnal-list">
            <li v-for="(riwayat, idx) in parsedRiwayatList" :key="idx" class="jurnal-item">
              <div class="jurnal-number">{{ idx + 1 }}</div>
              <div class="jurnal-text">{{ riwayat }}</div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dosen-page {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

/* Header */
.dp-header {
  padding: 2.5rem 2.5rem 2rem;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}
.page-badge {
  display: inline-block; font-size: 0.68rem; font-weight: 700;
  font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--blue); background: var(--blue-bg); border: 1px solid var(--blue-border);
  padding: 2px 10px; border-radius: 99px; margin-bottom: 0.75rem;
}
.dp-title { font-size: 1.85rem; font-weight: 700; letter-spacing: -0.03em; color: var(--text-primary); margin: 0 0 0.5rem; }
.dp-lead { font-size: 1rem; color: var(--text-secondary); line-height: 1.65; margin: 0; max-width: 800px; }

/* Body */
.dp-body {
  padding: 2.5rem;
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Search */
.search-wrap {
  position: relative;
  display: flex; align-items: center;
}
.search-icon {
  position: absolute; left: 1rem;
  width: 20px; height: 20px;
  color: var(--text-muted);
}
.search-input {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 3rem;
  font-family: var(--font-sans);
  font-size: 0.95rem;
  color: var(--text-primary);
  background: var(--bg);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-lg);
  outline: none;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.search-input:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 3px rgba(91,75,219,0.15);
}
.search-input::placeholder { color: var(--text-muted); }

.search-badge {
  position: absolute; right: 1rem;
  font-size: 0.75rem; font-weight: 600; font-family: var(--font-mono);
  background: var(--bg-muted); color: var(--text-secondary);
  padding: 0.25rem 0.6rem; border-radius: var(--radius-sm);
}

/* States */
.state-box {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 4rem 2rem; background: var(--bg-subtle);
  border: 1px dashed var(--border-strong); border-radius: var(--radius-lg);
  color: var(--text-secondary); text-align: center;
}
.state-box p { margin: 1rem 0 0; font-size: 0.95rem; }
.error-box { border-color: var(--red-border); color: var(--red); background: var(--red-bg); }
.error-icon { font-size: 2rem; }
.empty-icon { font-size: 2rem; }

.spin-icon {
  width: 28px; height: 28px;
  border: 3px solid var(--border-strong);
  border-top-color: var(--brand);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Table */
.table-wrap {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow-x: auto;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th {
  padding: 0.85rem 1rem;
  font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--text-muted);
  background: var(--bg-subtle); border-bottom: 1px solid var(--border);
}
.th-no { width: 60px; text-align: center; }
.th-nama { width: 25%; }
.th-prodi { width: 20%; }
.th-keahlian { width: auto; }
.th-jurnal { width: 120px; text-align: center; }
.th-riwayat { width: 180px; text-align: center; }

.data-row {
  border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}
.data-row:last-child { border-bottom: none; }
.data-row:hover { background: var(--bg-muted); }

.data-table td { padding: 1rem; vertical-align: top; }
.td-no { font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); text-align: center; font-weight: 700; }
.dosen-nama { font-size: 0.875rem; font-weight: 600; color: var(--text-primary); }
.dosen-nidn { font-size: 0.7rem; font-family: var(--font-mono); color: var(--text-muted); margin-top: 0.25rem; }
.td-prodi { font-size: 0.825rem; color: var(--text-secondary); }

.keahlian-text {
  font-size: 0.825rem; color: var(--text-secondary);
  line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

.td-jurnal { text-align: center; }
.td-riwayat { text-align: center; vertical-align: middle; }
.riwayat-actions {
  display: flex; gap: 0.5rem; justify-content: center; align-items: center;
}
.jurnal-btn {
  display: inline-flex; flex-direction: column; align-items: center; gap: 0.25rem;
  background: transparent; border: none; cursor: pointer;
  padding: 0.35rem 0.5rem; border-radius: var(--radius-sm);
  transition: background 0.15s;
}
.jurnal-btn:hover:not(:disabled) { background: var(--bg-muted); }
.jurnal-btn:disabled { cursor: default; opacity: 0.7; }
.jurnal-badge {
  display: inline-block;
  font-family: var(--font-mono); font-size: 0.8rem; font-weight: 700;
  background: var(--brand-light); color: var(--brand);
  padding: 0.2rem 0.75rem; border-radius: 99px;
  border: 1px solid #c4b5fd;
}
.jurnal-badge--zero { background: var(--bg-muted); color: var(--text-muted); border-color: var(--border-strong); }
.jurnal-btn-text { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); }

/* Jurnal Modal */
.jurnal-modal-overlay {
  position: fixed; inset: 0;
  background: rgba(17, 17, 24, 0.4); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  padding: 1.5rem; z-index: 200;
}
.jurnal-modal-box {
  background: var(--bg); border-radius: var(--radius-xl);
  border: 1px solid var(--border); box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  width: 100%; max-width: 800px; max-height: 85vh;
  display: flex; flex-direction: column; overflow: hidden;
  animation: modal-up 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes modal-up {
  from { opacity: 0; transform: translateY(20px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.jurnal-modal-header {
  padding: 1.5rem 2rem; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: flex-start;
  background: var(--bg);
}
.jurnal-modal-title { font-size: 1.25rem; font-weight: 800; color: var(--text-primary); margin: 0 0 0.25rem; }
.jurnal-modal-subtitle { font-size: 0.85rem; font-weight: 600; color: var(--brand); margin: 0; }
.jurnal-modal-close {
  background: var(--bg-muted); border: none; border-radius: 50%;
  width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;
  color: var(--text-muted); cursor: pointer; transition: all 0.15s;
}
.jurnal-modal-close:hover { background: var(--red-bg); color: var(--red); }
.jurnal-modal-body {
  padding: 2rem; overflow-y: auto; background: var(--bg-subtle);
}
.jurnal-list {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 1rem;
}
.jurnal-item {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 1.25rem;
  display: flex; gap: 1rem; align-items: flex-start;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.jurnal-number {
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  width: 28px; height: 28px; background: var(--brand-light); color: var(--brand);
  font-family: var(--font-mono); font-size: 0.75rem; font-weight: 700;
  border-radius: var(--radius);
}
.jurnal-text {
  font-size: 0.875rem; color: var(--text-secondary); line-height: 1.6; margin-top: 2px;
}

@media (max-width: 768px) {
  .dp-header { padding: 1.5rem 1.25rem; }
  .dp-body { padding: 1.25rem; }
  .search-badge { display: none; }
  .jurnal-modal-header { padding: 1.25rem 1.5rem; }
  .jurnal-modal-body { padding: 1.5rem; }
}
</style>
