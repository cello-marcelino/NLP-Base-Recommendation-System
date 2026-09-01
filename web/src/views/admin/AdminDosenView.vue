<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../../services/api'
import { useSystemStore } from '../../stores/system'

const systemStore = useSystemStore()
const dosenList = ref([])
const isLoading = ref(true)
const search = ref('')
const selectedProdi = ref('')

// Modals State
const showFormModal = ref(false)
const showDetailModal = ref(false)
const isEditing = ref(false)
const activeTab = ref('utama') // 'utama' | 'publikasi' | 'riwayat'
const isSaving = ref(false)
const formError = ref(null)

const selectedDosenDetail = ref(null)
const editingId = ref(null)

const formData = ref({
  nidn: '',
  nama: '',
  program_studi: 'Teknik Informatika',
  bidang_keahlian: '',
  pendidikan: '',
  publikasiStr: '',
  bimbinganStr: '',
  pengujianStr: ''
})

const parseListItems = (str) => {
  if (!str || typeof str !== 'string') return []
  const trimmed = str.trim()
  if (!trimmed || trimmed === '-' || trimmed.toLowerCase() === 'nan' || trimmed.toLowerCase() === 'null') return []
  
  const matches = trimmed.match(/"([^"]+)"/g)
  if (matches && matches.length > 0) {
    return matches.map(m => m.replace(/(^"|"$)/g, '').trim()).filter(Boolean)
  }
  return trimmed.split(/\n|;|•|\r/).map(s => s.replace(/^[0-9]+[.)]\s*/, '').trim()).filter(Boolean)
}

const fetchDosen = async () => {
  isLoading.value = true
  if (systemStore.isExcelMode && systemStore.dosenList.length > 0) {
    dosenList.value = systemStore.dosenList
    isLoading.value = false
    return
  }

  try {
    const res = await api.get('/admin/dosen')
    dosenList.value = res.data.data || []
  } catch (err) {
    if (systemStore.dosenList.length > 0) {
      dosenList.value = systemStore.dosenList
    } else {
      console.error(err)
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchDosen()
})

const prodiOptions = computed(() => {
  const prodis = new Set(dosenList.value.map(d => d.program_studi).filter(Boolean))
  return Array.from(prodis)
})

const stats = computed(() => {
  let totalPub = 0
  let totalBimb = 0
  let totalUji = 0

  dosenList.value.forEach(d => {
    totalPub += parseListItems(d.jurnal).length
    totalBimb += parseListItems(d.judul_bimbing).length
    totalUji += parseListItems(d.judul_uji).length
  })

  return {
    totalDosen: dosenList.value.length,
    totalPub,
    totalBimb,
    totalUji
  }
})

const filteredDosen = computed(() => {
  return dosenList.value.filter(d => {
    const matchQuery = !search.value || 
      d.nama.toLowerCase().includes(search.value.toLowerCase()) ||
      (d.nidn && d.nidn.includes(search.value)) ||
      (d.bidang_keahlian && d.bidang_keahlian.toLowerCase().includes(search.value.toLowerCase()))
    
    const matchProdi = !selectedProdi.value || d.program_studi === selectedProdi.value
    return matchQuery && matchProdi
  })
})

const openAddModal = () => {
  isEditing.value = false
  editingId.value = null
  activeTab.value = 'utama'
  formData.value = {
    nidn: '',
    nama: '',
    program_studi: 'Teknik Informatika',
    bidang_keahlian: '',
    pendidikan: '',
    publikasiStr: '',
    bimbinganStr: '',
    pengujianStr: ''
  }
  formError.value = null
  showFormModal.value = true
}

const openEditModal = (dosen) => {
  isEditing.value = true
  editingId.value = dosen.id || dosen.nidn
  activeTab.value = 'utama'

  const pubList = parseListItems(dosen.jurnal)
  const bimbList = parseListItems(dosen.judul_bimbing)
  const ujiList = parseListItems(dosen.judul_uji)

  formData.value = {
    nidn: dosen.nidn || '',
    nama: dosen.nama || '',
    program_studi: dosen.program_studi || 'Teknik Informatika',
    bidang_keahlian: dosen.bidang_keahlian || '',
    pendidikan: dosen.pendidikan || '',
    publikasiStr: pubList.join('\n'),
    bimbinganStr: bimbList.join('\n'),
    pengujianStr: ujiList.join('\n')
  }
  formError.value = null
  showFormModal.value = true
}

const openDetailModal = (dosen) => {
  selectedDosenDetail.value = dosen
  showDetailModal.value = true
}

const handleSave = async () => {
  if (!formData.value.nama) {
    formError.value = 'Nama dosen wajib diisi'
    activeTab.value = 'utama'
    return
  }
  isSaving.value = true
  formError.value = null

  const parseInputList = (str) => str.split('\n').map(s => s.trim()).filter(Boolean)

  const payload = {
    nidn: formData.value.nidn,
    nama: formData.value.nama,
    program_studi: formData.value.program_studi,
    bidang_keahlian: formData.value.bidang_keahlian,
    pendidikan: formData.value.pendidikan,
    publikasi: parseInputList(formData.value.publikasiStr),
    riwayat_bimbingan: parseInputList(formData.value.bimbinganStr),
    riwayat_pengujian: parseInputList(formData.value.pengujianStr)
  }

  try {
    if (isEditing.value && editingId.value) {
      await api.put(`/admin/dosen/${editingId.value}`, payload)
    } else {
      await api.post('/admin/dosen', payload)
    }
    showFormModal.value = false
    await fetchDosen()
  } catch (err) {
    formError.value = err.userMessage || 'Gagal menyimpan data dosen'
  } finally {
    isSaving.value = false
  }
}

const handleDelete = async (dosen) => {
  if (!confirm(`Apakah Anda yakin ingin menghapus data dosen "${dosen.nama}"?`)) return
  try {
    await api.delete(`/admin/dosen/${dosen.nidn || dosen.id}`)
    await fetchDosen()
  } catch (err) {
    alert(err.userMessage || 'Gagal menghapus data dosen')
  }
}

const getAvatarBg = (nama) => {
  const colors = ['#0d9488', '#0284c7', '#7c3aed', '#db2777', '#d97706', '#059669']
  let hash = 0
  for (let i = 0; i < nama.length; i++) hash += nama.charCodeAt(i)
  return colors[hash % colors.length]
}
</script>

<template>
  <div class="admin-dosen-page">
    <!-- Header -->
    <div class="page-header">
      <div>
        <span class="page-badge">Admin Data Master</span>
        <h1>Pengelolaan Data Dosen & Portfolio</h1>
        <p>Pusat pengelolaan data dosen, keahlian, publikasi jurnal, serta riwayat bimbingan & pengujian sidang.</p>
      </div>
      <button type="button" class="btn-add" @click="openAddModal">
        <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
        </svg>
        <span>Tambah Dosen Baru</span>
      </button>
    </div>

    <!-- Summary Stats Bar -->
    <div class="stats-bar">
      <div class="stat-item">
        <span class="st-num">{{ stats.totalDosen }}</span>
        <span class="st-lbl">Total Dosen</span>
      </div>
      <div class="stat-sep"></div>
      <div class="stat-item">
        <span class="st-num text-teal">{{ stats.totalPub }}</span>
        <span class="st-lbl">Publikasi Jurnal</span>
      </div>
      <div class="stat-sep"></div>
      <div class="stat-item">
        <span class="st-num text-blue">{{ stats.totalBimb }}</span>
        <span class="st-lbl">Judul Bimbingan</span>
      </div>
      <div class="stat-sep"></div>
      <div class="stat-item">
        <span class="st-num text-purple">{{ stats.totalUji }}</span>
        <span class="st-lbl">Judul Pengujian</span>
      </div>
    </div>

    <!-- Search & Filter Controls -->
    <div class="control-panel">
      <div class="search-box">
        <svg class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input 
          type="text" 
          v-model="search" 
          placeholder="Cari nama dosen, NIDN, atau bidang keahlian..." 
          class="search-input"
        />
      </div>

      <div class="filter-box">
        <label>Filter Prodi:</label>
        <select v-model="selectedProdi" class="prodi-select">
          <option value="">Semua Program Studi</option>
          <option v-for="p in prodiOptions" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-box">
      <div class="spinner"></div>
      <span>Memuat data dosen dan portfolio...</span>
    </div>

    <!-- Table Card -->
    <div v-else class="table-card">
      <table class="dosen-table">
        <thead>
          <tr>
            <th style="width: 50px;">No</th>
            <th>Profil Dosen</th>
            <th>Program Studi</th>
            <th>Bidang Keahlian</th>
            <th style="text-align: center;">Portfolio</th>
            <th style="text-align: center; width: 140px;">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(dosen, idx) in filteredDosen" :key="dosen.id || idx" class="table-row">
            <td class="col-center col-subtle">{{ idx + 1 }}</td>
            <td>
              <div class="dosen-profile-cell">
                <div class="avatar-circle" :style="{ backgroundColor: getAvatarBg(dosen.nama) }">
                  {{ dosen.nama.charAt(0) }}
                </div>
                <div>
                  <div class="dosen-name">{{ dosen.nama }}</div>
                  <div class="dosen-nidn">NIDN: {{ dosen.nidn || '-' }}</div>
                </div>
              </div>
            </td>
            <td>
              <span class="prodi-chip">{{ dosen.program_studi }}</span>
            </td>
            <td>
              <div class="keahlian-tags">
                <span 
                  v-for="(tag, tIdx) in (dosen.bidang_keahlian ? dosen.bidang_keahlian.split(',') : [])" 
                  :key="tIdx"
                  class="keahlian-tag"
                >
                  {{ tag.trim() }}
                </span>
                <span v-if="!dosen.bidang_keahlian" class="text-muted">-</span>
              </div>
            </td>
            <td class="col-center">
              <div class="metrics-flex">
                <span class="metric-badge m-jurnal" title="Jumlah Publikasi Jurnal">
                  Jurnal: {{ parseListItems(dosen.jurnal).length }}
                </span>
                <span class="metric-badge m-bimb" title="Jumlah Bimbingan">
                  Bimbingan: {{ parseListItems(dosen.judul_bimbing).length }}
                </span>
              </div>
            </td>
            <td class="col-center">
              <div class="actions-flex">
                <button type="button" class="act-btn btn-view" @click="openDetailModal(dosen)" title="Lihat Detail Portfolio">
                  Detail
                </button>
                <button type="button" class="act-btn btn-edit" @click="openEditModal(dosen)" title="Edit Dosen">
                  Edit
                </button>
                <button type="button" class="act-btn btn-del" @click="handleDelete(dosen)" title="Hapus Dosen">
                  Hapus
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!filteredDosen.length">
            <td colspan="6" class="empty-state">
              <p>Tidak ada data dosen yang sesuai dengan kriteria pencarian.</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form (Tambah / Edit) -->
    <div v-if="showFormModal" class="modal-backdrop" @click.self="showFormModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>{{ isEditing ? 'Edit Data Dosen' : 'Tambah Dosen Pembimbing Baru' }}</h3>
          <button @click="showFormModal = false" class="close-btn">×</button>
        </div>

        <!-- Form Navigation Tabs -->
        <div class="tab-nav">
          <button 
            type="button" 
            class="tab-btn" 
            :class="{ active: activeTab === 'utama' }"
            @click="activeTab = 'utama'"
          >
            Data Utama
          </button>
          <button 
            type="button" 
            class="tab-btn" 
            :class="{ active: activeTab === 'publikasi' }"
            @click="activeTab = 'publikasi'"
          >
            Publikasi Jurnal
          </button>
          <button 
            type="button" 
            class="tab-btn" 
            :class="{ active: activeTab === 'riwayat' }"
            @click="activeTab = 'riwayat'"
          >
            Bimbingan & Sidang
          </button>
        </div>

        <form @submit.prevent="handleSave" class="modal-body">
          <div v-if="formError" class="error-banner">[ERROR] {{ formError }}</div>

          <!-- Tab 1: Data Utama -->
          <div v-if="activeTab === 'utama'" class="tab-pane">
            <div class="fg-grid-2">
              <div class="fg">
                <label>Nama Lengkap & Gelar *</label>
                <input type="text" v-model="formData.nama" placeholder="Contoh: Dr. Supardianto, S.ST., M.Eng" required />
              </div>
              <div class="fg">
                <label>NIDN / Kode Dosen</label>
                <input type="text" v-model="formData.nidn" placeholder="Masukkan NIDN dosen..." />
              </div>
            </div>

            <div class="fg-grid-2">
              <div class="fg">
                <label>Program Studi</label>
                <input type="text" v-model="formData.program_studi" placeholder="Contoh: TRPL / Teknik Informatika..." />
              </div>
              <div class="fg">
                <label>Riwayat Pendidikan</label>
                <input type="text" v-model="formData.pendidikan" placeholder="Contoh: S1 Teknik Informatika, S2 Ilmu Komputer..." />
              </div>
            </div>

            <div class="fg">
              <label>Bidang Keahlian (Pisahkan dengan koma)</label>
              <input type="text" v-model="formData.bidang_keahlian" placeholder="Contoh: Artificial Intelligence, Machine Learning, Data Science" />
            </div>
          </div>

          <!-- Tab 2: Publikasi Jurnal -->
          <div v-if="activeTab === 'publikasi'" class="tab-pane">
            <div class="fg">
              <label>Daftar Publikasi Jurnal Relevan</label>
              <p class="field-hint">Masukkan 1 judul publikasi jurnal per baris.</p>
              <textarea v-model="formData.publikasiStr" rows="8" placeholder="Judul Jurnal 1&#10;Judul Jurnal 2&#10;Judul Jurnal 3..."></textarea>
            </div>
          </div>

          <!-- Tab 3: Bimbingan & Sidang -->
          <div v-if="activeTab === 'riwayat'" class="tab-pane">
            <div class="fg mb-4">
              <label>Riwayat Bimbingan Tugas Akhir / Skripsi</label>
              <p class="field-hint">Masukkan 1 judul bimbingan mahasiswa per baris.</p>
              <textarea v-model="formData.bimbinganStr" rows="4" placeholder="Judul Bimbingan 1&#10;Judul Bimbingan 2..."></textarea>
            </div>

            <div class="fg">
              <label>Riwayat Pengujian Sidang Skripsi</label>
              <p class="field-hint">Masukkan 1 judul pengujian sidang per baris.</p>
              <textarea v-model="formData.pengujianStr" rows="4" placeholder="Judul Pengujian 1&#10;Judul Pengujian 2..."></textarea>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" @click="showFormModal = false" class="btn-cancel">Batal</button>
            <button type="submit" :disabled="isSaving" class="btn-save">
              {{ isSaving ? 'Menyimpan...' : (isEditing ? 'Simpan Perubahan' : 'Tambah Dosen') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Detail Portfolio View -->
    <div v-if="showDetailModal && selectedDosenDetail" class="modal-backdrop" @click.self="showDetailModal = false">
      <div class="detail-card">
        <div class="detail-header">
          <div class="dosen-profile-cell">
            <div class="avatar-circle lg" :style="{ backgroundColor: getAvatarBg(selectedDosenDetail.nama) }">
              {{ selectedDosenDetail.nama.charAt(0) }}
            </div>
            <div>
              <h3>{{ selectedDosenDetail.nama }}</h3>
              <div class="detail-badges">
                <span class="prodi-chip">{{ selectedDosenDetail.program_studi }}</span>
                <span v-if="selectedDosenDetail.nidn" class="nidn-chip">NIDN: {{ selectedDosenDetail.nidn }}</span>
              </div>
            </div>
          </div>
          <button @click="showDetailModal = false" class="close-btn">×</button>
        </div>

        <div class="detail-body">
          <!-- Section 1: Keahlian -->
          <div class="detail-sec">
            <label class="sec-lbl">Bidang Keahlian Utama</label>
            <p class="sec-text font-medium">{{ selectedDosenDetail.bidang_keahlian || '-' }}</p>
          </div>

          <!-- Section 2: Publikasi -->
          <div class="detail-sec">
            <div class="sec-hdr">
              <label class="sec-lbl">Publikasi Jurnal ({{ parseListItems(selectedDosenDetail.jurnal).length }})</label>
            </div>
            <ol v-if="parseListItems(selectedDosenDetail.jurnal).length" class="detail-list">
              <li v-for="(j, idx) in parseListItems(selectedDosenDetail.jurnal)" :key="idx">{{ j }}</li>
            </ol>
            <p v-else class="text-subtle">Belum ada riwayat publikasi jurnal.</p>
          </div>

          <!-- Section 3: Bimbingan -->
          <div class="detail-sec">
            <div class="sec-hdr">
              <label class="sec-lbl">Riwayat Bimbingan Skripsi ({{ parseListItems(selectedDosenDetail.judul_bimbing).length }})</label>
            </div>
            <ol v-if="parseListItems(selectedDosenDetail.judul_bimbing).length" class="detail-list">
              <li v-for="(b, idx) in parseListItems(selectedDosenDetail.judul_bimbing)" :key="idx">{{ b }}</li>
            </ol>
            <p v-else class="text-subtle">Belum ada riwayat bimbingan mahasiswa.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dosen-page { padding: 2rem 2.5rem; width: 100%; max-width: 100%; box-sizing: border-box; }
.page-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 1.5rem; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: #ccfbf1; color: #0f766e; padding: 3px 10px; border-radius: 99px; margin-bottom: 0.75rem; }
.page-header h1 { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0 0 0.4rem; letter-spacing: -0.02em; }
.page-header p { font-size: 0.9rem; color: #64748b; margin: 0; }

.btn-add {
  display: flex; align-items: center; gap: 0.5rem; background: #0d9488; color: white;
  padding: 0.65rem 1.25rem; font-size: 0.875rem; font-weight: 600; border: none; border-radius: 8px; cursor: pointer; transition: background 0.15s;
  box-shadow: 0 2px 4px rgba(13, 148, 136, 0.2);
}
.btn-add:hover { background: #0f766e; }

/* Stats Bar */
.stats-bar {
  display: flex; align-items: center; gap: 1.5rem;
  background: white; border: 1px solid #e2e8f0; border-radius: 10px;
  padding: 1rem 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.stat-item { display: flex; flex-direction: column; }
.st-num { font-size: 1.35rem; font-weight: 700; font-family: var(--font-mono, monospace); color: #0f172a; line-height: 1; }
.st-lbl { font-size: 0.75rem; font-weight: 600; color: #64748b; margin-top: 0.25rem; }
.stat-sep { width: 1px; height: 28px; background: #e2e8f0; }
.text-teal { color: #0d9488; }
.text-blue { color: #0284c7; }
.text-purple { color: #7c3aed; }

/* Control Panel */
.control-panel { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: 1.25rem; }
.search-box { position: relative; flex: 1; max-width: 420px; }
.search-icon { position: absolute; left: 0.85rem; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; color: #94a3b8; }
.search-input { width: 100%; padding: 0.6rem 0.85rem 0.6rem 2.5rem; font-size: 0.875rem; border: 1px solid #cbd5e1; border-radius: 8px; background: white; }
.search-input:focus { outline: none; border-color: #0d9488; box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15); }

.filter-box { display: flex; align-items: center; gap: 0.5rem; font-size: 0.83rem; color: #475569; font-weight: 600; }
.prodi-select { padding: 0.55rem 0.85rem; font-size: 0.85rem; border: 1px solid #cbd5e1; border-radius: 8px; background: white; color: #0f172a; }

/* Table */
.table-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.dosen-table { width: 100%; border-collapse: collapse; text-align: left; }
.dosen-table th { background: #f8fafc; padding: 0.85rem 1.25rem; font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid #e2e8f0; }
.table-row { border-bottom: 1px solid #f1f5f9; transition: background 0.15s; }
.table-row:hover { background: #f8fafc; }
.dosen-table td { padding: 1rem 1.25rem; vertical-align: middle; font-size: 0.875rem; }

.dosen-profile-cell { display: flex; align-items: center; gap: 0.85rem; }
.avatar-circle { width: 38px; height: 38px; border-radius: 50%; color: white; font-weight: 700; font-size: 1rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.avatar-circle.lg { width: 48px; height: 48px; font-size: 1.25rem; }
.dosen-name { font-weight: 600; color: #0f172a; }
.dosen-nidn { font-size: 0.72rem; font-family: var(--font-mono, monospace); color: #64748b; margin-top: 2px; }

.prodi-chip { font-size: 0.72rem; font-weight: 600; background: #e0f2fe; color: #0369a1; padding: 3px 10px; border-radius: 99px; }
.keahlian-tags { display: flex; flex-wrap: wrap; gap: 4px; max-width: 280px; }
.keahlian-tag { font-size: 0.72rem; background: #f1f5f9; color: #334155; padding: 2px 8px; border-radius: 4px; border: 1px solid #e2e8f0; }

.metrics-flex { display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.metric-badge { font-size: 0.75rem; font-family: var(--font-mono, monospace); font-weight: 600; padding: 3px 8px; border-radius: 6px; }
.m-jurnal { background: #ccfbf1; color: #0f766e; }
.m-bimb { background: #e0f2fe; color: #0284c7; }

.actions-flex { display: flex; align-items: center; justify-content: center; gap: 0.4rem; }
.act-btn { border: none; padding: 0.35rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: all 0.15s; }
.btn-view { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }
.btn-view:hover { background: #166534; color: white; }
.btn-edit { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.btn-edit:hover { background: #1d4ed8; color: white; }
.btn-del { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; }
.btn-del:hover { background: #dc2626; color: white; }

.empty-state { text-align: center; padding: 3rem; color: #94a3b8; }
.loading-box { display: flex; align-items: center; gap: 0.75rem; color: #64748b; padding: 3rem 0; }
.spinner { width: 20px; height: 20px; border: 2px solid #cbd5e1; border-top-color: #0d9488; border-radius: 50%; animation: spin 0.7s linear infinite; }

/* Modals */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 1.5rem; }
.modal-card { background: white; border-radius: 12px; width: 100%; max-width: 680px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 40px rgba(0,0,0,0.25); }
.modal-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; }
.modal-header h3 { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin: 0; }
.close-btn { background: none; border: none; font-size: 1.5rem; color: #94a3b8; cursor: pointer; }

.tab-nav { display: flex; border-bottom: 1px solid #e2e8f0; background: #f8fafc; padding: 0 1.5rem; }
.tab-btn { background: none; border: none; padding: 0.75rem 1.25rem; font-size: 0.85rem; font-weight: 600; color: #64748b; border-bottom: 2px solid transparent; cursor: pointer; }
.tab-btn.active { color: #0d9488; border-bottom-color: #0d9488; background: white; }

.modal-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.fg-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.fg { display: flex; flex-direction: column; gap: 0.35rem; }
.fg label { font-size: 0.8rem; font-weight: 600; color: #334155; }
.field-hint { font-size: 0.75rem; color: #94a3b8; margin: 0 0 0.25rem; }
.fg input, .fg textarea { padding: 0.65rem 0.85rem; font-size: 0.875rem; border: 1px solid #cbd5e1; border-radius: 6px; background: #f8fafc; }
.fg input:focus, .fg textarea:focus { outline: none; border-color: #0d9488; background: white; box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15); }

.error-banner { background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; padding: 0.65rem; border-radius: 6px; font-size: 0.83rem; text-align: center; }

.modal-footer { display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem; }
.btn-cancel { background: #f1f5f9; color: #475569; border: none; padding: 0.6rem 1.25rem; border-radius: 6px; font-weight: 600; cursor: pointer; }
.btn-save { background: #0d9488; color: white; border: none; padding: 0.6rem 1.25rem; border-radius: 6px; font-weight: 600; cursor: pointer; }

/* Detail Card */
.detail-card { background: white; border-radius: 12px; width: 100%; max-width: 650px; max-height: 85vh; overflow-y: auto; padding: 1.75rem; box-shadow: 0 25px 50px rgba(0,0,0,0.25); }
.detail-header { display: flex; align-items: flex-start; justify-content: space-between; border-bottom: 1px solid #e2e8f0; padding-bottom: 1.25rem; margin-bottom: 1.25rem; }
.detail-badges { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.35rem; }
.nidn-chip { font-size: 0.72rem; font-family: var(--font-mono, monospace); background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 4px; }

.detail-body { display: flex; flex-direction: column; gap: 1.25rem; }
.detail-sec { display: flex; flex-direction: column; gap: 0.4rem; }
.sec-lbl { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }
.sec-text { font-size: 0.9rem; color: #0f172a; margin: 0; }
.detail-list { padding-left: 1.25rem; margin: 0; display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.85rem; color: #334155; line-height: 1.5; }
.text-subtle { font-size: 0.83rem; color: #94a3b8; font-style: italic; margin: 0; }
</style>
