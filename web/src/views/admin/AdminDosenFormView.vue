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

const fetchLecturerForEdit = async () => {
  if (!isEditMode.value) return
  isLoading.value = true
  errorMessage.value = null
  try {
    const res = await api.get(`/admin/dosen/${dosenId}`)
    const d = res.data.data
    if (d) {
      const pubList = parseListItems(d.jurnal)
      const bimbList = parseListItems(d.judul_bimbing)
      const ujiList = parseListItems(d.judul_uji)

      formData.value = {
        nidn: d.nidn || '',
        nama: d.nama || '',
        program_studi: d.program_studi || 'Teknik Informatika',
        bidang_keahlian: d.bidang_keahlian || '',
        pendidikan: d.pendidikan || '',
        publikasiStr: pubList.join('\n'),
        bimbinganStr: bimbList.join('\n'),
        pengujianStr: ujiList.join('\n')
      }
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

const handleSubmit = async () => {
  if (!formData.value.nama) {
    errorMessage.value = 'Nama lengkap dosen wajib diisi'
    return
  }

  isSaving.value = true
  errorMessage.value = null

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
              <label for="pendidikan">Riwayat Pendidikan</label>
              <input id="pendidikan" type="text" v-model="formData.pendidikan" placeholder="Contoh: S1 Teknik Informatika, S2 Ilmu Komputer" />
            </div>
          </div>

          <div class="fg">
            <label for="keahlian">Bidang Keahlian Utama (Pisahkan dengan koma)</label>
            <input id="keahlian" type="text" v-model="formData.bidang_keahlian" placeholder="Contoh: Artificial Intelligence, Machine Learning, Data Science" />
          </div>
        </div>
      </div>

      <!-- Section 2: Publikasi Jurnal -->
      <div class="form-card">
        <div class="card-title">2. Portfolio Publikasi Jurnal</div>
        <div class="card-body">
          <div class="fg">
            <label for="jurnal">Daftar Judul Publikasi Jurnal Relevan</label>
            <p class="field-hint">Tuliskan 1 judul publikasi jurnal per baris. Teks ini akan diolah oleh engine BM25 dan Sentence-BERT.</p>
            <textarea id="jurnal" v-model="formData.publikasiStr" rows="6" placeholder="Judul Jurnal 1&#10;Judul Jurnal 2&#10;Judul Jurnal 3..."></textarea>
          </div>
        </div>
      </div>

      <!-- Section 3: Bimbingan & Sidang -->
      <div class="form-card">
        <div class="card-title">3. Riwayat Bimbingan & Pengujian Sidang Skripsi</div>
        <div class="card-body">
          <div class="fg mb-4">
            <label for="bimbingan">Riwayat Bimbingan Tugas Akhir / Skripsi</label>
            <p class="field-hint">Tuliskan 1 judul bimbingan mahasiswa per baris.</p>
            <textarea id="bimbingan" v-model="formData.bimbinganStr" rows="5" placeholder="Judul Bimbingan 1&#10;Judul Bimbingan 2..."></textarea>
          </div>

          <div class="fg">
            <label for="pengujian">Riwayat Pengujian Sidang Skripsi</label>
            <p class="field-hint">Tuliskan 1 judul pengujian sidang per baris.</p>
            <textarea id="pengujian" v-model="formData.pengujianStr" rows="5" placeholder="Judul Pengujian 1&#10;Judul Pengujian 2..."></textarea>
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
.mb-4 { margin-bottom: 1.25rem; }

.loading-box { display: flex; align-items: center; gap: 0.75rem; color: #64748b; padding: 3rem 0; }
.spinner { width: 20px; height: 20px; border: 2px solid #cbd5e1; border-top-color: #0d9488; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.form-container { display: flex; flex-direction: column; gap: 1.75rem; }
.error-banner { background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; padding: 0.85rem 1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 600; }

.form-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.card-title { padding: 1.1rem 1.5rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; font-weight: 700; color: #0f172a; }
.card-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1.25rem; }

.fg-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
@media (max-width: 640px) { .fg-grid-2 { grid-template-columns: 1fr; } }

.fg { display: flex; flex-direction: column; gap: 0.35rem; }
.fg label { font-size: 0.83rem; font-weight: 600; color: #334155; }
.field-hint { font-size: 0.75rem; color: #94a3b8; margin: 0 0 0.25rem; }
.fg input, .fg textarea { padding: 0.65rem 0.85rem; font-size: 0.875rem; border: 1px solid #cbd5e1; border-radius: 8px; background: #f8fafc; color: #0f172a; transition: all 0.15s; }
.fg input:focus, .fg textarea:focus { outline: none; border-color: #0d9488; background: white; box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15); }

.form-footer { display: flex; align-items: center; justify-content: flex-end; gap: 1rem; padding-top: 0.5rem; }
.btn-cancel { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; padding: 0.75rem 1.5rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; text-decoration: none; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-submit { background: #0d9488; color: white; border: none; padding: 0.75rem 1.75rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: background 0.15s; box-shadow: 0 2px 6px rgba(13, 148, 136, 0.25); }
.btn-submit:hover:not(:disabled) { background: #0f766e; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
