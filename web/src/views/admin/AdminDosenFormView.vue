<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../services/api'

const route = useRoute()
const router = useRouter()

const isEditMode = computed(() => !!route.params.id)
const dosenId = route.params.id

const isLoading = ref(false)
const isSaving = ref(false)
const errorMessage = ref(null)

const formData = ref({
  nidn: '',
  nama: '',
  program_studi: 'Teknik Informatika',
  bidang_keahlian: '',
  pendidikan_d3: '',
  pendidikan_s1_d4: '',
  pendidikan_s2: '',
  pendidikan_s3: ''
})

const publikasiList = ref([''])
const bimbinganList = ref([''])
const pengujianList = ref([''])

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

const parseEducationToFields = (str) => {
  if (!str || typeof str !== 'string') return
  const trimmed = str.trim()
  if (!trimmed || trimmed === '-' || trimmed.toLowerCase() === 'nan') return

  let items = []
  if (trimmed.includes('\n')) {
    items = trimmed.split('\n')
  } else if (trimmed.includes(', ') && /(?=Sarjana|Magister|Doktor|Diploma|S1|S2|S3|D3|D4)/i.test(trimmed)) {
    items = trimmed.split(/,\s*(?=Sarjana|Magister|Doktor|Diploma|S1|S2|S3|D3|D4)/i)
  } else {
    items = trimmed.split(/,|;/)
  }

  items.forEach(item => {
    const s = item.trim()
    if (/d3|diploma\s*(3|iii)/i.test(s)) {
      formData.value.pendidikan_d3 = s
    } else if (/s3|doktor|ph\.?d/i.test(s)) {
      formData.value.pendidikan_s3 = s
    } else if (/s2|magister|master/i.test(s)) {
      formData.value.pendidikan_s2 = s
    } else if (/s1|sarjana|d4|div|diploma\s*(4|iv)/i.test(s)) {
      formData.value.pendidikan_s1_d4 = s
    } else {
      if (!formData.value.pendidikan_s1_d4) {
        formData.value.pendidikan_s1_d4 = s
      } else if (!formData.value.pendidikan_s2) {
        formData.value.pendidikan_s2 = s
      }
    }
  })
}

const fetchLecturerForEdit = async () => {
  if (!isEditMode.value) return
  isLoading.value = true
  errorMessage.value = null
  try {
    const res = await api.get(`/admin/dosen/${dosenId}`)
    const d = res.data.data
    if (d) {
      formData.value.nidn = d.nidn || ''
      formData.value.nama = d.nama || ''
      formData.value.program_studi = d.program_studi || 'Teknik Informatika'
      formData.value.bidang_keahlian = d.bidang_keahlian || ''
      
      parseEducationToFields(d.pendidikan)

      const pubs = parseListItems(d.jurnal)
      publikasiList.value = pubs.length > 0 ? pubs : ['']

      const bimbs = parseListItems(d.judul_bimbing)
      bimbinganList.value = bimbs.length > 0 ? bimbs : ['']

      const ujis = parseListItems(d.judul_uji)
      pengujianList.value = ujis.length > 0 ? ujis : ['']
    }
  } catch (err) {
    errorMessage.value = err.userMessage || 'Gagal memuat data dosen untuk diedit'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchLecturerForEdit()
})

// Dynamic Array Helpers
const addPublikasi = () => publikasiList.value.push('')
const removePublikasi = (idx) => {
  publikasiList.value.splice(idx, 1)
  if (publikasiList.value.length === 0) publikasiList.value.push('')
}

const addBimbingan = () => bimbinganList.value.push('')
const removeBimbingan = (idx) => {
  bimbinganList.value.splice(idx, 1)
  if (bimbinganList.value.length === 0) bimbinganList.value.push('')
}

const addPengujian = () => pengujianList.value.push('')
const removePengujian = (idx) => {
  pengujianList.value.splice(idx, 1)
  if (pengujianList.value.length === 0) pengujianList.value.push('')
}

const handleSubmit = async () => {
  if (!formData.value.nama) {
    errorMessage.value = 'Nama lengkap dosen wajib diisi'
    return
  }

  isSaving.value = true
  errorMessage.value = null

  // Combine education levels
  const eduParts = []
  if (formData.value.pendidikan_d3?.trim()) eduParts.push(formData.value.pendidikan_d3.trim())
  if (formData.value.pendidikan_s1_d4?.trim()) eduParts.push(formData.value.pendidikan_s1_d4.trim())
  if (formData.value.pendidikan_s2?.trim()) eduParts.push(formData.value.pendidikan_s2.trim())
  if (formData.value.pendidikan_s3?.trim()) eduParts.push(formData.value.pendidikan_s3.trim())
  const combinedPendidikan = eduParts.join(', ')

  const cleanList = (arr) => arr.map(s => s.trim()).filter(Boolean)

  const payload = {
    nidn: formData.value.nidn,
    nama: formData.value.nama,
    program_studi: formData.value.program_studi,
    bidang_keahlian: formData.value.bidang_keahlian,
    pendidikan: combinedPendidikan,
    publikasi: cleanList(publikasiList.value),
    riwayat_bimbingan: cleanList(bimbinganList.value),
    riwayat_pengujian: cleanList(pengujianList.value)
  }

  try {
    if (isEditMode.value) {
      await api.put(`/admin/dosen/${dosenId}`, payload)
    } else {
      await api.post('/admin/dosen', payload)
    }
    router.push('/admin/dosen')
  } catch (err) {
    errorMessage.value = err.userMessage || 'Gagal menyimpan data dosen'
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div class="admin-dosen-form-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <router-link to="/admin/dosen" class="btn-back">← Kembali ke Daftar Dosen</router-link>
        <span class="page-badge mt-2">Formulir Pengelolaan Data Dosen</span>
        <h1>{{ isEditMode ? 'Edit Data Dosen' : 'Tambah Dosen Pembimbing Baru' }}</h1>
        <p>Lengkapi formulir di bawah ini untuk menyimpan data master dosen dan riwayat karya ilmiahnnya.</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-box">
      <div class="spinner"></div>
      <span>Memuat formulir...</span>
    </div>

    <!-- Form Body -->
    <form v-else @submit.prevent="handleSubmit" class="form-container">
      <div v-if="errorMessage" class="error-banner">[ERROR] {{ errorMessage }}</div>

      <!-- Section 1: Data Utama -->
      <div class="form-card">
        <div class="card-title">1. Identitas & Keahlian Utama</div>
        <div class="card-body">
          <div class="fg-grid-2">
            <div class="fg">
              <label for="nama">Nama Lengkap & Gelar *</label>
              <input id="nama" type="text" v-model="formData.nama" placeholder="Contoh: Dr. Supardianto, S.ST., M.Eng" required />
            </div>

            <div class="fg">
              <label for="nidn">NIDN / Kode Dosen</label>
              <input id="nidn" type="text" v-model="formData.nidn" placeholder="Contoh: 0012058901" />
            </div>
          </div>

          <div class="fg-grid-2">
            <div class="fg">
              <label for="prodi">Program Studi</label>
              <input id="prodi" type="text" v-model="formData.program_studi" placeholder="Contoh: TRPL / Teknik Informatika / Geomatika" />
            </div>

            <div class="fg">
              <label for="keahlian">Bidang Keahlian Utama (Pisahkan dengan koma)</label>
              <input id="keahlian" type="text" v-model="formData.bidang_keahlian" placeholder="Contoh: Artificial Intelligence, Machine Learning, Data Science" />
            </div>
          </div>
        </div>
      </div>

      <!-- Section 2: Riwayat Pendidikan Berjenjang -->
      <div class="form-card">
        <div class="card-title">2. Riwayat Pendidikan Formal</div>
        <div class="card-body">
          <div class="fg-grid-2">
            <div class="fg">
              <label for="edu-d3">Diploma 3 (D3)</label>
              <input id="edu-d3" type="text" v-model="formData.pendidikan_d3" placeholder="Contoh: D3 Teknik Informatika Politeknik Negeri Batam" />
            </div>

            <div class="fg">
              <label for="edu-s1">Sarjana / Terapan (S1 / D4)</label>
              <input id="edu-s1" type="text" v-model="formData.pendidikan_s1_d4" placeholder="Contoh: S1 Ilmu Komputer Universitas Indonesia" />
            </div>
          </div>

          <div class="fg-grid-2">
            <div class="fg">
              <label for="edu-s2">Magister (S2)</label>
              <input id="edu-s2" type="text" v-model="formData.pendidikan_s2" placeholder="Contoh: S2 Teknik Elektro & Informatika Institut Teknologi Bandung" />
            </div>

            <div class="fg">
              <label for="edu-s3">Doktor (S3 / Ph.D)</label>
              <input id="edu-s3" type="text" v-model="formData.pendidikan_s3" placeholder="Contoh: S3 Computer Science Universite Grenoble Alpes" />
            </div>
          </div>
        </div>
      </div>

      <!-- Section 3: Publikasi Jurnal (Multi Field) -->
      <div class="form-card">
        <div class="card-title-flex header-teal">
          <span>3. Portfolio Publikasi Jurnal & Makalah Ilmiah ({{ publikasiList.filter(Boolean).length }} Judul)</span>
          <button type="button" @click="addPublikasi" class="btn-add-item btn-add-teal">+ Tambah Judul Jurnal</button>
        </div>
        <div class="card-body">
          <div class="multi-list">
            <div v-for="(item, idx) in publikasiList" :key="idx" class="multi-row">
              <span class="row-num num-teal">#{{ idx + 1 }}</span>
              <input 
                type="text" 
                v-model="publikasiList[idx]" 
                placeholder="Masukkan judul publikasi jurnal atau paper ilmiah..." 
                class="row-input"
              />
              <button type="button" @click="removePublikasi(idx)" class="btn-del-row" title="Hapus baris ini">Hapus</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Section 4: Riwayat Bimbingan Skripsi (Multi Field) -->
      <div class="form-card">
        <div class="card-title-flex header-blue">
          <span>4. Riwayat Bimbingan Tugas Akhir / Skripsi ({{ bimbinganList.filter(Boolean).length }} Judul)</span>
          <button type="button" @click="addBimbingan" class="btn-add-item btn-add-blue">+ Tambah Judul Bimbingan</button>
        </div>
        <div class="card-body">
          <div class="multi-list">
            <div v-for="(item, idx) in bimbinganList" :key="idx" class="multi-row">
              <span class="row-num num-blue">#{{ idx + 1 }}</span>
              <input 
                type="text" 
                v-model="bimbinganList[idx]" 
                placeholder="Masukkan judul tugas akhir / skripsi mahasiswa yang dibimbing..." 
                class="row-input"
              />
              <button type="button" @click="removeBimbingan(idx)" class="btn-del-row" title="Hapus baris ini">Hapus</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Section 5: Riwayat Pengujian Sidang (Multi Field) -->
      <div class="form-card">
        <div class="card-title-flex header-purple">
          <span>5. Riwayat Pengujian Sidang Skripsi ({{ pengujianList.filter(Boolean).length }} Judul)</span>
          <button type="button" @click="addPengujian" class="btn-add-item btn-add-purple">+ Tambah Judul Pengujian</button>
        </div>
        <div class="card-body">
          <div class="multi-list">
            <div v-for="(item, idx) in pengujianList" :key="idx" class="multi-row">
              <span class="row-num num-purple">#{{ idx + 1 }}</span>
              <input 
                type="text" 
                v-model="pengujianList[idx]" 
                placeholder="Masukkan judul sidang skripsi yang diuji..." 
                class="row-input"
              />
              <button type="button" @click="removePengujian(idx)" class="btn-del-row" title="Hapus baris ini">Hapus</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Footer -->
      <div class="form-footer">
        <router-link to="/admin/dosen" class="btn-cancel">Batal</router-link>
        <button type="submit" :disabled="isSaving" class="btn-submit">
          {{ isSaving ? 'Menyimpan Data...' : (isEditMode ? 'Simpan Perubahan Dosen' : 'Tambah Data Dosen') }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.admin-dosen-form-page { padding: 2rem 2.5rem; width: 100%; max-width: 1000px; box-sizing: border-box; }
.page-header { margin-bottom: 2rem; }
.btn-back { font-size: 0.83rem; font-weight: 600; color: #0d9488; text-decoration: none; display: inline-block; }
.btn-back:hover { text-decoration: underline; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: #ccfbf1; color: #0f766e; padding: 3px 10px; border-radius: 99px; }
.page-header h1 { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0.4rem 0 0.25rem; }
.page-header p { font-size: 0.9rem; color: #64748b; margin: 0; }

.mt-2 { margin-top: 0.5rem; }

.loading-box { display: flex; align-items: center; gap: 0.75rem; color: #64748b; padding: 3rem 0; }
.spinner { width: 20px; height: 20px; border: 2px solid #cbd5e1; border-top-color: #0d9488; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.form-container { display: flex; flex-direction: column; gap: 1.75rem; }
.error-banner { background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; padding: 0.85rem 1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 600; }

.form-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.card-title { padding: 1.1rem 1.5rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; font-weight: 700; color: #0f172a; }

.card-title-flex { padding: 0.85rem 1.5rem; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; font-weight: 700; display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.header-teal { background: #f0fdfa; color: #0f766e; }
.header-blue { background: #f0f9ff; color: #0369a1; }
.header-purple { background: #faf5ff; color: #7e22ce; }

.btn-add-item { border: none; padding: 0.4rem 0.85rem; border-radius: 6px; font-size: 0.8rem; font-weight: 700; cursor: pointer; transition: background 0.15s; }
.btn-add-teal { background: #ccfbf1; color: #0f766e; }
.btn-add-teal:hover { background: #0d9488; color: white; }
.btn-add-blue { background: #e0f2fe; color: #0284c7; }
.btn-add-blue:hover { background: #0284c7; color: white; }
.btn-add-purple { background: #f3e8ff; color: #7e22ce; }
.btn-add-purple:hover { background: #7e22ce; color: white; }

.card-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1.25rem; }

.fg-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
@media (max-width: 640px) { .fg-grid-2 { grid-template-columns: 1fr; } }

.fg { display: flex; flex-direction: column; gap: 0.35rem; }
.fg label { font-size: 0.83rem; font-weight: 600; color: #334155; }
.fg input { padding: 0.65rem 0.85rem; font-size: 0.875rem; border: 1px solid #cbd5e1; border-radius: 8px; background: #f8fafc; color: #0f172a; transition: all 0.15s; }
.fg input:focus { outline: none; border-color: #0d9488; background: white; box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15); }

/* Multi-row dynamic lists */
.multi-list { display: flex; flex-direction: column; gap: 0.75rem; }
.multi-row { display: flex; align-items: center; gap: 0.75rem; }

.row-num { font-size: 0.75rem; font-family: var(--font-mono, monospace); font-weight: 700; padding: 4px 8px; border-radius: 6px; flex-shrink: 0; }
.num-teal { background: #ccfbf1; color: #0f766e; }
.num-blue { background: #e0f2fe; color: #0284c7; }
.num-purple { background: #f3e8ff; color: #7e22ce; }

.row-input { flex: 1; padding: 0.65rem 0.85rem; font-size: 0.875rem; border: 1px solid #cbd5e1; border-radius: 8px; background: #f8fafc; color: #0f172a; transition: all 0.15s; }
.row-input:focus { outline: none; border-color: #0d9488; background: white; box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15); }

.btn-del-row { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; padding: 0.55rem 0.85rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: all 0.15s; }
.btn-del-row:hover { background: #dc2626; color: white; }

.form-footer { display: flex; align-items: center; justify-content: flex-end; gap: 1rem; padding-top: 0.5rem; }
.btn-cancel { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; padding: 0.75rem 1.5rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; text-decoration: none; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-submit { background: #0d9488; color: white; border: none; padding: 0.75rem 1.75rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: background 0.15s; box-shadow: 0 2px 6px rgba(13, 148, 136, 0.25); }
.btn-submit:hover:not(:disabled) { background: #0f766e; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
