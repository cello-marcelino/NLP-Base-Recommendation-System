<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../services/api'
import { useSystemStore } from '../../stores/system'

const route = useRoute()
const router = useRouter()
const systemStore = useSystemStore()

const dosenId = route.params.id
const dosen = ref(null)
const isLoading = ref(true)
const errorMessage = ref(null)

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

const fetchDetail = async () => {
  isLoading.value = true
  errorMessage.value = null

  if (systemStore.isExcelMode && systemStore.dosenList.length > 0) {
    const target = systemStore.dosenList.find(d => String(d.nidn) === String(dosenId) || String(d.id) === String(dosenId))
    if (target) {
      dosen.value = target
      isLoading.value = false
      return
    }
  }

  try {
    const res = await api.get(`/admin/dosen/${dosenId}`)
    dosen.value = res.data.data
  } catch (err) {
    if (systemStore.dosenList.length > 0) {
      const target = systemStore.dosenList.find(d => String(d.nidn) === String(dosenId) || String(d.id) === String(dosenId))
      if (target) {
        dosen.value = target
        return
      }
    }
    errorMessage.value = err.userMessage || 'Gagal memuat detail data dosen'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchDetail()
})

const getAvatarBg = (nama) => {
  if (!nama) return '#0d9488'
  const colors = ['#0d9488', '#0284c7', '#7c3aed', '#db2777', '#d97706', '#059669']
  let hash = 0
  for (let i = 0; i < nama.length; i++) hash += nama.charCodeAt(i)
  return colors[hash % colors.length]
}

const handleDelete = async () => {
  if (!confirm(`Apakah Anda yakin ingin menghapus data dosen "${dosen.value.nama}"?`)) return
  try {
    await api.delete(`/admin/dosen/${dosenId}`)
    router.push('/admin/dosen')
  } catch (err) {
    alert(err.userMessage || 'Gagal menghapus data dosen')
  }
}
</script>

<template>
  <div class="admin-dosen-detail-page">
    <!-- Header Navigation -->
    <div class="page-header">
      <div>
        <router-link to="/admin/dosen" class="btn-back">← Kembali ke Daftar Dosen</router-link>
        <span class="page-badge mt-2">Detail Portfolio Dosen</span>
        <h1 v-if="dosen">{{ dosen.nama }}</h1>
        <h1 v-else>Detail Dosen</h1>
      </div>
      <div v-if="dosen" class="header-actions">
        <router-link :to="`/admin/dosen/${dosenId}/edit`" class="btn-edit">
          Edit Data Dosen
        </router-link>
        <button type="button" @click="handleDelete" class="btn-delete">
          Hapus Dosen
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-box">
      <div class="spinner"></div>
      <span>Memuat rincian data dosen...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="errorMessage" class="error-box">
      <p>[ERROR] {{ errorMessage }}</p>
      <router-link to="/admin/dosen" class="btn-back-link">Kembali ke Daftar Dosen</router-link>
    </div>

    <!-- Detail View Card Grid -->
    <div v-else-if="dosen" class="detail-grid">
      <!-- Left Column: Profile Card & Keahlian -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar-circle" :style="{ backgroundColor: getAvatarBg(dosen.nama) }">
            {{ dosen.nama ? dosen.nama.charAt(0) : 'D' }}
          </div>
          <div class="profile-info">
            <h2>{{ dosen.nama }}</h2>
            <div class="chips-row">
              <span class="chip prodi-chip">{{ dosen.program_studi || 'Teknik Informatika' }}</span>
              <span v-if="dosen.nidn" class="chip nidn-chip">NIDN: {{ dosen.nidn }}</span>
            </div>
          </div>
        </div>

        <div class="profile-divider"></div>

        <div class="info-sec">
          <label>Riwayat Pendidikan</label>
          <p>{{ dosen.pendidikan || 'Belum diisi' }}</p>
        </div>

        <div class="info-sec">
          <label>Bidang Keahlian Utama</label>
          <div class="keahlian-flex">
            <span 
              v-for="(tag, idx) in (dosen.bidang_keahlian ? dosen.bidang_keahlian.split(',') : [])" 
              :key="idx" 
              class="tag-item"
            >
              {{ tag.trim() }}
            </span>
            <span v-if="!dosen.bidang_keahlian" class="text-subtle">-</span>
          </div>
        </div>
      </div>

      <!-- Right Column: Lists & Portfolios -->
      <div class="portfolio-col">
        <!-- Card 1: Publikasi Jurnal -->
        <div class="port-card">
          <div class="port-header">
            <h3>Publikasi Jurnal Relevan</h3>
            <span class="count-badge badge-teal">{{ parseListItems(dosen.jurnal).length }} Judul</span>
          </div>
          <div class="port-body">
            <ol v-if="parseListItems(dosen.jurnal).length" class="item-list">
              <li v-for="(j, idx) in parseListItems(dosen.jurnal)" :key="idx">{{ j }}</li>
            </ol>
            <p v-else class="text-empty">Belum ada data publikasi jurnal yang terdaftar.</p>
          </div>
        </div>

        <!-- Card 2: Riwayat Bimbingan -->
        <div class="port-card">
          <div class="port-header">
            <h3>Riwayat Bimbingan Skripsi</h3>
            <span class="count-badge badge-blue">{{ parseListItems(dosen.judul_bimbing).length }} Judul</span>
          </div>
          <div class="port-body">
            <ol v-if="parseListItems(dosen.judul_bimbing).length" class="item-list">
              <li v-for="(b, idx) in parseListItems(dosen.judul_bimbing)" :key="idx">{{ b }}</li>
            </ol>
            <p v-else class="text-empty">Belum ada riwayat bimbingan mahasiswa.</p>
          </div>
        </div>

        <!-- Card 3: Riwayat Pengujian Sidang -->
        <div class="port-card">
          <div class="port-header">
            <h3>Riwayat Pengujian Sidang Skripsi</h3>
            <span class="count-badge badge-purple">{{ parseListItems(dosen.judul_uji).length }} Judul</span>
          </div>
          <div class="port-body">
            <ol v-if="parseListItems(dosen.judul_uji).length" class="item-list">
              <li v-for="(u, idx) in parseListItems(dosen.judul_uji)" :key="idx">{{ u }}</li>
            </ol>
            <p v-else class="text-empty">Belum ada riwayat pengujian sidang.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dosen-detail-page { padding: 2rem 2.5rem; width: 100%; max-width: 100%; box-sizing: border-box; }
.page-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; margin-bottom: 2rem; }
.btn-back { font-size: 0.83rem; font-weight: 600; color: #0d9488; text-decoration: none; display: inline-block; }
.btn-back:hover { text-decoration: underline; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: #ccfbf1; color: #0f766e; padding: 3px 10px; border-radius: 99px; }
.page-header h1 { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0.4rem 0 0; }

.mt-2 { margin-top: 0.5rem; }

.header-actions { display: flex; align-items: center; gap: 0.75rem; }
.btn-edit { background: #0d9488; color: white; border: none; padding: 0.65rem 1.25rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; text-decoration: none; transition: background 0.15s; }
.btn-edit:hover { background: #0f766e; }
.btn-delete { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; padding: 0.65rem 1.25rem; border-radius: 8px; font-size: 0.875rem; font-weight: 600; cursor: pointer; }
.btn-delete:hover { background: #dc2626; color: white; }

.loading-box { display: flex; align-items: center; gap: 0.75rem; color: #64748b; padding: 3rem 0; }
.spinner { width: 20px; height: 20px; border: 2px solid #cbd5e1; border-top-color: #0d9488; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.error-box { background: #fef2f2; border: 1px solid #fca5a5; color: #991b1b; padding: 1.5rem; border-radius: 8px; text-align: center; }
.btn-back-link { display: inline-block; margin-top: 0.75rem; font-size: 0.85rem; color: #0d9488; font-weight: 600; text-decoration: none; }

/* Grid Layout */
.detail-grid { display: grid; grid-template-columns: 340px 1fr; gap: 2rem; align-items: start; }
@media (max-width: 960px) { .detail-grid { grid-template-columns: 1fr; } }

.profile-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.profile-header { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 1rem; }
.avatar-circle { width: 72px; height: 72px; border-radius: 50%; color: white; font-size: 2rem; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.profile-info h2 { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem; }
.chips-row { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.4rem; }
.chip { font-size: 0.72rem; font-weight: 600; padding: 3px 10px; border-radius: 99px; }
.prodi-chip { background: #e0f2fe; color: #0369a1; }
.nidn-chip { background: #f1f5f9; color: #475569; font-family: var(--font-mono, monospace); }

.profile-divider { height: 1px; background: #e2e8f0; margin: 1.5rem 0; }
.info-sec { display: flex; flex-direction: column; gap: 0.35rem; margin-bottom: 1.25rem; }
.info-sec label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }
.info-sec p { font-size: 0.875rem; color: #0f172a; margin: 0; line-height: 1.5; }

.keahlian-flex { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.25rem; }
.tag-item { font-size: 0.75rem; background: #ccfbf1; color: #0f766e; border: 1px solid #99f6e4; padding: 3px 10px; border-radius: 6px; font-weight: 600; }
.text-subtle { font-size: 0.83rem; color: #94a3b8; font-style: italic; }

/* Portfolio Column */
.portfolio-col { display: flex; flex-direction: column; gap: 1.5rem; }
.port-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.port-header { padding: 1.15rem 1.5rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; }
.port-header h3 { font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0; }
.count-badge { font-size: 0.75rem; font-family: var(--font-mono, monospace); font-weight: 700; padding: 3px 10px; border-radius: 99px; }
.badge-teal { background: #ccfbf1; color: #0f766e; }
.badge-blue { background: #e0f2fe; color: #0284c7; }
.badge-purple { background: #f3e8ff; color: #7e22ce; }

.port-body { padding: 1.5rem; }
.item-list { padding-left: 1.25rem; margin: 0; display: flex; flex-direction: column; gap: 0.6rem; font-size: 0.875rem; color: #334155; line-height: 1.55; }
.text-empty { font-size: 0.85rem; color: #94a3b8; font-style: italic; margin: 0; }
</style>
