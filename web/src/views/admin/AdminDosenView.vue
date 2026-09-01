<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../../services/api'

const dosenList = ref([])
const isLoading = ref(true)
const search = ref('')

// Form State
const showModal = ref(false)
const isSaving = ref(false)
const formError = ref(null)

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

const fetchDosen = async () => {
  isLoading.value = true
  try {
    const res = await api.get('/admin/dosen')
    dosenList.value = res.data.data || []
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchDosen()
})

const filteredDosen = computed(() => {
  if (!search.value) return dosenList.value
  const q = search.value.toLowerCase()
  return dosenList.value.filter(d => 
    d.nama.toLowerCase().includes(q) ||
    d.program_studi.toLowerCase().includes(q) ||
    d.bidang_keahlian.toLowerCase().includes(q)
  )
})

const openAddModal = () => {
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
  showModal.value = true
}

const handleSave = async () => {
  if (!formData.value.nama) {
    formError.value = 'Nama dosen wajib diisi'
    return
  }
  isSaving.value = true
  formError.value = null

  const parseList = (str) => str.split('\n').map(s => s.trim()).filter(Boolean)

  const payload = {
    nidn: formData.value.nidn,
    nama: formData.value.nama,
    program_studi: formData.value.program_studi,
    bidang_keahlian: formData.value.bidang_keahlian,
    pendidikan: formData.value.pendidikan,
    publikasi: parseList(formData.value.publikasiStr),
    riwayat_bimbingan: parseList(formData.value.bimbinganStr),
    riwayat_pengujian: parseList(formData.value.pengujianStr)
  }

  try {
    await api.post('/admin/dosen', payload)
    showModal.value = false
    await fetchDosen()
  } catch (err) {
    formError.value = err.userMessage || 'Gagal menyimpan data dosen'
  } finally {
    isSaving.value = false
  }
}

const handleDelete = async (dosen) => {
  if (!confirm(`Apakah Anda yakin ingin menghapus data dosen ${dosen.nama}?`)) return
  try {
    await api.delete(`/admin/dosen/${dosen.nidn || dosen.id}`)
    await fetchDosen()
  } catch (err) {
    alert(err.userMessage || 'Gagal menghapus data dosen')
  }
}
</script>

<template>
  <div class="admin-dosen-page">
    <div class="page-header">
      <div>
        <span class="page-badge">Admin Master Data</span>
        <h1>Pengelolaan Data Dosen</h1>
        <p>Kelola profil dosen, bidang keahlian, riwayat publikasi jurnal, bimbingan, dan pengujian sidang.</p>
      </div>
      <button type="button" class="btn-add" @click="openAddModal">
        <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        <span>Tambah Dosen Baru</span>
      </button>
    </div>

    <!-- Search & Filter -->
    <div class="filter-bar">
      <input type="text" v-model="search" placeholder="Cari nama dosen, prodi, atau bidang keahlian..." class="search-input" />
      <span class="count-text">Total: {{ filteredDosen.length }} Dosen</span>
    </div>

    <!-- Data Table -->
    <div v-if="isLoading" class="loading-box">
      <div class="spinner"></div>
      <span>Memuat data dosen...</span>
    </div>

    <div v-else class="table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>No</th>
            <th>Nama & NIDN</th>
            <th>Program Studi</th>
            <th>Bidang Keahlian</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(dosen, idx) in filteredDosen" :key="idx">
            <td class="col-num">{{ idx + 1 }}</td>
            <td>
              <div class="dosen-nama">{{ dosen.nama }}</div>
              <div class="dosen-nidn">NIDN: {{ dosen.nidn || '-' }}</div>
            </td>
            <td><span class="prodi-badge">{{ dosen.program_studi }}</span></td>
            <td><div class="keahlian-text">{{ dosen.bidang_keahlian || '-' }}</div></td>
            <td>
              <button type="button" class="btn-del" @click="handleDelete(dosen)" title="Hapus dosen">
                Hapus
              </button>
            </td>
          </tr>
          <tr v-if="!filteredDosen.length">
            <td colspan="5" class="empty-cell">Tidak ada data dosen yang sesuai.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form Tambah Dosen -->
    <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <h3>Tambah Dosen Pembimbing Baru</h3>
          <button @click="showModal = false" class="close-btn">×</button>
        </div>
        <form @submit.prevent="handleSave" class="modal-body">
          <div v-if="formError" class="error-msg">{{ formError }}</div>

          <div class="form-grid-2">
            <div class="fg">
              <label>Nama Lengkap & Gelar *</label>
              <input type="text" v-model="formData.nama" placeholder="Contoh: Dr. Ahmad, M.Kom" required />
            </div>
            <div class="fg">
              <label>NIDN</label>
              <input type="text" v-model="formData.nidn" placeholder="Nomor Induk Dosen Nasional..." />
            </div>
          </div>

          <div class="form-grid-2">
            <div class="fg">
              <label>Program Studi</label>
              <input type="text" v-model="formData.program_studi" placeholder="TRPL / TI / Geomatika..." />
            </div>
            <div class="fg">
              <label>Bidang Keahlian (Pisahkan koma)</label>
              <input type="text" v-model="formData.bidang_keahlian" placeholder="Artificial Intelligence, Machine Learning..." />
            </div>
          </div>

          <div class="fg">
            <label>Riwayat Publikasi Jurnal (1 Judul per baris)</label>
            <textarea v-model="formData.publikasiStr" rows="3" placeholder="Masukan judul publikasi jurnal..."></textarea>
          </div>

          <div class="fg">
            <label>Riwayat Bimbingan Mahasiswa (1 Judul per baris)</label>
            <textarea v-model="formData.bimbinganStr" rows="3" placeholder="Masukan judul bimbingan skripsi..."></textarea>
          </div>

          <div class="modal-footer">
            <button type="button" @click="showModal = false" class="btn-cancel">Batal</button>
            <button type="submit" :disabled="isSaving" class="btn-save">
              {{ isSaving ? 'Menyimpan...' : 'Simpan Dosen' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dosen-page { padding: 2.5rem 2rem; max-width: 1200px; }
.page-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 2rem; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: #ccfbf1; color: #0f766e; padding: 3px 10px; border-radius: 99px; margin-bottom: 0.75rem; }
.page-header h1 { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem; }
.page-header p { font-size: 0.9rem; color: #64748b; margin: 0; }

.btn-add {
  display: flex; align-items: center; gap: 0.5rem; background: #0d9488; color: white;
  padding: 0.65rem 1.2rem; font-size: 0.875rem; font-weight: 600; border: none; border-radius: 8px; cursor: pointer; transition: background 0.15s;
}
.btn-add:hover { background: #0f766e; }

.filter-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; }
.search-input { width: 360px; padding: 0.6rem 0.85rem; font-size: 0.875rem; border: 1px solid #cbd5e1; border-radius: 6px; }
.count-text { font-size: 0.8rem; font-family: var(--font-mono, monospace); color: #64748b; }

.table-card { background: white; border: 1px solid #e2e8f0; border-radius: 10px; overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { background: #f8fafc; padding: 0.85rem 1rem; font-size: 0.8rem; font-weight: 700; color: #475569; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 0.85rem 1rem; font-size: 0.875rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
.col-num { width: 50px; text-align: center; font-family: var(--font-mono, monospace); color: #94a3b8; }
.dosen-nama { font-weight: 600; color: #0f172a; }
.dosen-nidn { font-size: 0.72rem; font-family: var(--font-mono, monospace); color: #64748b; }
.prodi-badge { font-size: 0.72rem; font-weight: 600; background: #f1f5f9; color: #334155; padding: 2px 8px; border-radius: 4px; }
.keahlian-text { font-size: 0.83rem; color: #475569; }

.btn-del { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; padding: 3px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; cursor: pointer; }
.btn-del:hover { background: #dc2626; color: white; }

.empty-cell { text-align: center; padding: 3rem; color: #94a3b8; font-style: italic; }
.loading-box { display: flex; align-items: center; gap: 0.75rem; color: #64748b; padding: 3rem 0; }
.spinner { width: 20px; height: 20px; border: 2px solid #cbd5e1; border-top-color: #0d9488; border-radius: 50%; animation: spin 0.7s linear infinite; }

/* Modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); backdrop-filter: blur(3px); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 1.5rem; }
.modal-box { background: white; border-radius: 12px; width: 100%; max-width: 640px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
.modal-header { padding: 1.25rem 1.5rem; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; }
.modal-header h3 { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin: 0; }
.close-btn { background: none; border: none; font-size: 1.5rem; color: #94a3b8; cursor: pointer; }

.modal-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.form-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.fg { display: flex; flex-direction: column; gap: 0.35rem; }
.fg label { font-size: 0.8rem; font-weight: 600; color: #334155; }
.fg input, .fg textarea { padding: 0.6rem 0.8rem; font-size: 0.875rem; border: 1px solid #cbd5e1; border-radius: 6px; }

.error-msg { background: #fef2f2; color: #991b1b; padding: 0.6rem 0.85rem; border-radius: 6px; font-size: 0.8rem; }
.modal-footer { display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem; }
.btn-cancel { background: #f1f5f9; color: #475569; border: none; padding: 0.6rem 1.2rem; border-radius: 6px; font-weight: 600; cursor: pointer; }
.btn-save { background: #0d9488; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 6px; font-weight: 600; cursor: pointer; }
</style>
