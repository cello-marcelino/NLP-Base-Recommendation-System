<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSystemStore } from '../stores/system'

const systemStore = useSystemStore()
const searchQuery = ref('')
const selectedDosenDetail = ref(null)
const activeModalTab = ref('jurnal') // 'jurnal', 'bimbingan', 'uji', 'profil'

const parseListItems = (str) => {
  if (!str || typeof str !== 'string') return []
  const trimmed = str.trim()
  if (!trimmed || trimmed === '-' || trimmed.toLowerCase() === 'nan' || trimmed.toLowerCase() === 'null') {
    return []
  }
  // Quoted items
  const matches = trimmed.match(/"([^"]+)"/g)
  if (matches && matches.length > 0) {
    return matches
      .map(m => m.replace(/(^"|"$)/g, '').trim())
      .filter(j => j.length > 0 && j !== '-')
  }
  // Array-like
  if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
    try {
      const parsed = JSON.parse(trimmed.replace(/'/g, '"'))
      if (Array.isArray(parsed)) return parsed.map(String).filter(Boolean)
    } catch {}
  }
  // Semicolon / newline separated
  return trimmed
    .split(/\n|;|•|\r/)
    .map(s => s.replace(/^[0-9]+[.)]\s*/, '').trim())
    .filter(s => s.length > 0 && s !== '-')
}

const getCount = (str) => parseListItems(str).length

const filteredDosen = computed(() => {
  if (!searchQuery.value) return systemStore.dosenList
  const q = searchQuery.value.toLowerCase()
  return systemStore.dosenList.filter(d => 
    (d.nama && d.nama.toLowerCase().includes(q)) || 
    (d.program_studi && d.program_studi.toLowerCase().includes(q)) ||
    (d.bidang_keahlian && d.bidang_keahlian.toLowerCase().includes(q)) ||
    (d.pendidikan && d.pendidikan.toLowerCase().includes(q))
  )
})

const openDetailModal = (dosen, initialTab = 'jurnal') => {
  selectedDosenDetail.value = dosen
  activeModalTab.value = initialTab
}

onMounted(() => {
  if (systemStore.dosenList.length === 0) {
    systemStore.fetchDosenList()
  }
})
</script>

<template>
  <div class="dosen-page">
    
    <!-- Header -->
    <div class="dp-header">
      <span class="page-badge">Data Master</span>
      <h1 class="dp-title">Data Dosen & Rekam Jejak Akademik</h1>
      <p class="dp-lead">
        Database profil seluruh dosen, keahlian bidang riset, riwayat pendidikan, publikasi jurnal ilmiah, bimbingan tugas akhir, dan riwayat pengujian sidang.
      </p>
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
          placeholder="Cari berdasarkan nama dosen, program studi, keahlian, atau riwayat pendidikan..." 
        />
        <div class="search-badge" v-if="!systemStore.isLoading">{{ filteredDosen.length }} dosen terdaftar</div>
      </div>

      <!-- State: Loading -->
      <div v-if="systemStore.isLoading" class="state-box">
        <div class="spin-icon"></div>
        <p>Memuat data dosen dari server...</p>
      </div>

      <!-- State: Error -->
      <div v-else-if="systemStore.error" class="state-box error-box">
        <div class="error-icon">⚠</div>
        <p>{{ systemStore.error }}</p>
      </div>

      <!-- State: Empty Search -->
      <div v-else-if="filteredDosen.length === 0" class="state-box">
        <div class="empty-icon">🔍</div>
        <p>Tidak ada dosen yang cocok dengan kata kunci "<strong>{{ searchQuery }}</strong>"</p>
      </div>

      <!-- Table -->
      <div v-else class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th class="th-no">No</th>
              <th class="th-nama">Nama & NIDN</th>
              <th class="th-prodi">Program Studi</th>
              <th class="th-keahlian">Bidang Keahlian</th>
              <th class="th-pendidikan">Riwayat Pendidikan</th>
              <th class="th-counts text-center">Rekam Jejak</th>
              <th class="th-action text-center">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(dosen, idx) in filteredDosen" :key="idx" class="data-row">
              <td class="td-no">{{ idx + 1 }}</td>
              
              <!-- Nama & NIDN -->
              <td class="td-nama">
                <div class="dosen-nama">{{ dosen.nama }}</div>
                <div class="dosen-nidn">NIDN: {{ dosen.nidn || dosen.id || '-' }}</div>
              </td>
              
              <!-- Program Studi -->
              <td class="td-prodi">
                <span class="prodi-pill">{{ dosen.program_studi }}</span>
              </td>
              
              <!-- Bidang Keahlian -->
              <td class="td-keahlian">
                <div class="keahlian-text" :title="dosen.bidang_keahlian">{{ dosen.bidang_keahlian || '-' }}</div>
              </td>

              <!-- Riwayat Pendidikan -->
              <td class="td-pendidikan">
                <div class="pendidikan-text" :title="dosen.pendidikan">{{ dosen.pendidikan || '-' }}</div>
              </td>
              
              <!-- Counts Badges -->
              <td class="td-counts">
                <div class="counts-badges-wrap">
                  <span class="badge-mini badge-mini--brand" :title="`${getCount(dosen.jurnal)} Publikasi Jurnal`">
                    📚 {{ getCount(dosen.jurnal) }}
                  </span>
                  <span class="badge-mini badge-mini--green" :title="`${getCount(dosen.judul_bimbing)} Bimbingan Mahasiswa`">
                    👥 {{ getCount(dosen.judul_bimbing) }}
                  </span>
                  <span class="badge-mini badge-mini--blue" :title="`${getCount(dosen.judul_uji)} Pengujian Sidang`">
                    ⚖️ {{ getCount(dosen.judul_uji) }}
                  </span>
                </div>
              </td>

              <!-- Action Button -->
              <td class="td-action">
                <button class="btn-detail" @click="openDetailModal(dosen)">
                  <span>Detail Lengkap</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
    
    <!-- Comprehensive Lecturer Detail Modal -->
    <div v-if="selectedDosenDetail" class="detail-modal-overlay" @click.self="selectedDosenDetail = null">
      <div class="detail-modal-box">
        <!-- Modal Header -->
        <div class="detail-modal-header">
          <div>
            <div class="dm-badges">
              <span class="prodi-pill">{{ selectedDosenDetail.program_studi }}</span>
              <span v-if="selectedDosenDetail.nidn" class="nidn-pill">NIDN: {{ selectedDosenDetail.nidn }}</span>
            </div>
            <h3 class="dm-title">{{ selectedDosenDetail.nama }}</h3>
            <p class="dm-keahlian">🎯 {{ selectedDosenDetail.bidang_keahlian || '-' }}</p>
          </div>
          <button @click="selectedDosenDetail = null" class="dm-close" aria-label="Tutup modal">
            <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Modal Tabs -->
        <div class="dm-tabs">
          <button 
            type="button" 
            class="dm-tab-btn" 
            :class="{ 'dm-tab-btn--active': activeModalTab === 'jurnal' }"
            @click="activeModalTab = 'jurnal'"
          >
            📚 Publikasi Jurnal ({{ getCount(selectedDosenDetail.jurnal) }})
          </button>
          <button 
            type="button" 
            class="dm-tab-btn" 
            :class="{ 'dm-tab-btn--active': activeModalTab === 'bimbingan' }"
            @click="activeModalTab = 'bimbingan'"
          >
            👥 Riwayat Bimbingan ({{ getCount(selectedDosenDetail.judul_bimbing) }})
          </button>
          <button 
            type="button" 
            class="dm-tab-btn" 
            :class="{ 'dm-tab-btn--active': activeModalTab === 'uji' }"
            @click="activeModalTab = 'uji'"
          >
            ⚖️ Riwayat Pengujian ({{ getCount(selectedDosenDetail.judul_uji) }})
          </button>
          <button 
            type="button" 
            class="dm-tab-btn" 
            :class="{ 'dm-tab-btn--active': activeModalTab === 'profil' }"
            @click="activeModalTab = 'profil'"
          >
            🎓 Profil & Pendidikan
          </button>
        </div>

        <!-- Modal Tab Content Body -->
        <div class="detail-modal-body">
          
          <!-- TAB 1: JURNAL -->
          <div v-if="activeModalTab === 'jurnal'">
            <ul v-if="parseListItems(selectedDosenDetail.jurnal).length" class="dm-list">
              <li v-for="(jurnal, idx) in parseListItems(selectedDosenDetail.jurnal)" :key="idx" class="dm-item">
                <div class="dm-number dm-number--brand">{{ idx + 1 }}</div>
                <div class="dm-text">{{ jurnal }}</div>
              </li>
            </ul>
            <div v-else class="dm-empty">Belum ada riwayat publikasi jurnal yang terdata.</div>
          </div>

          <!-- TAB 2: BIMBINGAN -->
          <div v-if="activeModalTab === 'bimbingan'">
            <ul v-if="parseListItems(selectedDosenDetail.judul_bimbing).length" class="dm-list">
              <li v-for="(bimbing, idx) in parseListItems(selectedDosenDetail.judul_bimbing)" :key="idx" class="dm-item">
                <div class="dm-number dm-number--green">{{ idx + 1 }}</div>
                <div class="dm-text">{{ bimbing }}</div>
              </li>
            </ul>
            <div v-else class="dm-empty">Belum ada riwayat bimbingan mahasiswa yang terdata.</div>
          </div>

          <!-- TAB 3: PENGUJIAN -->
          <div v-if="activeModalTab === 'uji'">
            <ul v-if="parseListItems(selectedDosenDetail.judul_uji).length" class="dm-list">
              <li v-for="(uji, idx) in parseListItems(selectedDosenDetail.judul_uji)" :key="idx" class="dm-item">
                <div class="dm-number dm-number--blue">{{ idx + 1 }}</div>
                <div class="dm-text">{{ uji }}</div>
              </li>
            </ul>
            <div v-else class="dm-empty">Belum ada riwayat pengujian sidang yang terdata.</div>
          </div>

          <!-- TAB 4: PROFIL & PENDIDIKAN -->
          <div v-if="activeModalTab === 'profil'" class="dm-profil-view">
            <div class="profil-card">
              <div class="profil-label">🎓 Riwayat Pendidikan</div>
              <div v-if="parseListItems(selectedDosenDetail.pendidikan).length" class="edu-list-wrap">
                <div v-for="(edu, idx) in parseListItems(selectedDosenDetail.pendidikan)" :key="idx" class="edu-item">
                  <span class="edu-dot">•</span>
                  <span>{{ edu }}</span>
                </div>
              </div>
              <div v-else class="dm-empty">Belum ada data riwayat pendidikan.</div>
            </div>

            <div class="profil-card">
              <div class="profil-label">🎯 Bidang Keahlian Utama</div>
              <div class="profil-val">{{ selectedDosenDetail.bidang_keahlian || '-' }}</div>
            </div>
          </div>

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
  max-width: 1400px;
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
.dp-lead { font-size: 1rem; color: var(--text-secondary); line-height: 1.65; margin: 0; max-width: 900px; }

/* Body */
.dp-body {
  padding: 2.5rem;
  flex: 1;
  max-width: 1400px;
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
.th-no { width: 45px; text-align: center; }
.th-nama { width: 22%; }
.th-prodi { width: 15%; }
.th-keahlian { width: 20%; }
.th-pendidikan { width: 20%; }
.th-counts { width: 130px; }
.th-action { width: 110px; }

.data-row {
  border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}
.data-row:last-child { border-bottom: none; }
.data-row:hover { background: var(--bg-muted); }

.data-table td { padding: 0.85rem 1rem; vertical-align: middle; }
.td-no { font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); text-align: center; font-weight: 700; }
.dosen-nama { font-size: 0.875rem; font-weight: 600; color: var(--text-primary); }
.dosen-nidn { font-size: 0.7rem; font-family: var(--font-mono); color: var(--text-muted); margin-top: 0.15rem; }

.prodi-pill {
  font-size: 0.72rem; font-weight: 600;
  color: var(--brand); background: var(--brand-light);
  padding: 2px 8px; border-radius: var(--radius-sm);
}

.keahlian-text, .pendidikan-text {
  font-size: 0.8rem; color: var(--text-secondary);
  line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

.counts-badges-wrap {
  display: flex; gap: 4px; justify-content: center;
}
.badge-mini {
  font-family: var(--font-mono); font-size: 0.7rem; font-weight: 700;
  padding: 2px 6px; border-radius: var(--radius-sm);
}
.badge-mini--brand { background: var(--brand-light); color: var(--brand); }
.badge-mini--green { background: var(--green-bg); color: var(--green); }
.badge-mini--blue { background: var(--blue-bg); color: var(--blue); }

.btn-detail {
  font-size: 0.75rem; font-weight: 600;
  color: var(--brand); background: var(--brand-light);
  border: 1px solid #c4b5fd; border-radius: var(--radius-sm);
  padding: 0.35rem 0.65rem; cursor: pointer; transition: all 0.15s;
  white-space: nowrap;
}
.btn-detail:hover { background: var(--brand); color: white; }

/* States */
.state-box {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 4rem 2rem; background: var(--bg-subtle);
  border: 1px dashed var(--border-strong); border-radius: var(--radius-lg);
  color: var(--text-secondary); text-align: center;
}
.spin-icon {
  width: 28px; height: 28px;
  border: 3px solid var(--border-strong);
  border-top-color: var(--brand);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Detail Modal */
.detail-modal-overlay {
  position: fixed; inset: 0;
  background: rgba(17, 17, 24, 0.45); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  padding: 1.5rem; z-index: 200;
}
.detail-modal-box {
  background: var(--bg); border-radius: var(--radius-xl);
  border: 1px solid var(--border); box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
  width: 100%; max-width: 860px; max-height: 88vh;
  display: flex; flex-direction: column; overflow: hidden;
  animation: modal-up 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes modal-up {
  from { opacity: 0; transform: translateY(16px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.detail-modal-header {
  padding: 1.5rem 2rem; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: flex-start;
  background: var(--bg);
}
.dm-badges { display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.25rem; }
.nidn-pill { font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-muted); background: var(--bg-muted); padding: 2px 6px; border-radius: var(--radius-sm); }
.dm-title { font-size: 1.35rem; font-weight: 800; color: var(--text-primary); margin: 0 0 0.25rem; }
.dm-keahlian { font-size: 0.85rem; color: var(--text-secondary); margin: 0; }

.dm-close {
  background: var(--bg-muted); border: none; border-radius: 50%;
  width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;
  color: var(--text-muted); cursor: pointer; transition: all 0.15s;
}
.dm-close:hover { background: var(--red-bg); color: var(--red); }

.dm-tabs {
  display: flex; background: var(--bg-muted); border-bottom: 1px solid var(--border);
  padding: 4px 1.5rem 0; gap: 4px; overflow-x: auto;
}
.dm-tab-btn {
  padding: 0.65rem 1rem; font-size: 0.78rem; font-weight: 600;
  color: var(--text-secondary); background: transparent; border: none;
  border-bottom: 2px solid transparent; cursor: pointer; transition: all 0.15s;
  white-space: nowrap;
}
.dm-tab-btn:hover { color: var(--text-primary); }
.dm-tab-btn--active {
  color: var(--brand); border-bottom-color: var(--brand); background: var(--bg);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0; font-weight: 700;
}

.detail-modal-body {
  padding: 1.5rem 2rem; overflow-y: auto; background: var(--bg-subtle);
  display: flex; flex-direction: column; gap: 1rem;
}

.dm-list {
  list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.65rem;
}
.dm-item {
  background: var(--bg); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 0.85rem 1rem;
  display: flex; gap: 0.85rem; align-items: flex-start;
}
.dm-number {
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  width: 24px; height: 24px; font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
  border-radius: 50%;
}
.dm-number--brand { background: var(--brand-light); color: var(--brand); }
.dm-number--green { background: var(--green-bg); color: var(--green); }
.dm-number--blue { background: var(--blue-bg); color: var(--blue); }
.dm-text { font-size: 0.85rem; color: var(--text-primary); line-height: 1.5; margin-top: 1px; }

.dm-empty {
  text-align: center; padding: 2rem; color: var(--text-muted); font-size: 0.85rem; font-style: italic;
  background: var(--bg); border: 1px dashed var(--border); border-radius: var(--radius);
}

.dm-profil-view { display: flex; flex-direction: column; gap: 1rem; }
.profil-card {
  background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem;
  display: flex; flex-direction: column; gap: 0.5rem;
}
.profil-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: var(--text-muted); font-family: var(--font-mono); }
.profil-val { font-size: 0.875rem; color: var(--text-primary); font-weight: 500; }
.edu-list-wrap { display: flex; flex-direction: column; gap: 0.4rem; }
.edu-item { display: flex; align-items: flex-start; gap: 0.5rem; font-size: 0.85rem; color: var(--text-secondary); }
.edu-dot { color: var(--brand); font-weight: bold; }

@media (max-width: 900px) {
  .dp-header, .dp-body { padding: 1.5rem 1rem; }
  .search-badge { display: none; }
}
</style>
