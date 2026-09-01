<script setup>
import { ref, onMounted, computed } from 'vue'
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
const activePortfolioTab = ref('jurnal') // 'jurnal' | 'bimbingan' | 'pengujian'

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

const parseEducationList = (str) => {
  if (!str || typeof str !== 'string') return []
  const trimmed = str.trim()
  if (!trimmed || trimmed === '-' || trimmed.toLowerCase() === 'nan' || trimmed.toLowerCase() === 'null') return []
  
  const regex = /(?=Sarjana|Magister|Doktor|Diploma|S1|S2|S3|D3|D4)/i
  let items = []
  if (trimmed.includes('\n')) {
    items = trimmed.split('\n')
  } else if (trimmed.includes(', ') && regex.test(trimmed)) {
    items = trimmed.split(/,\s*(?=Sarjana|Magister|Doktor|Diploma|S1|S2|S3|D3|D4)/i)
  } else {
    items = trimmed.split(/,|;/)
  }
  return items.map(s => s.trim()).filter(Boolean)
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

const educationList = computed(() => parseEducationList(dosen.value?.pendidikan))
const jurnalList = computed(() => parseListItems(dosen.value?.jurnal))
const bimbinganList = computed(() => parseListItems(dosen.value?.judul_bimbing))
const pengujianList = computed(() => parseListItems(dosen.value?.judul_uji))
</script>

<template>
  <div class="admin-dosen-detail-page">
    <!-- Header Navigation -->
    <div class="page-header">
      <div>
        <router-link to="/admin/dosen" class="btn-back">← Kembali ke Daftar Dosen</router-link>
        <span class="page-badge mt-2">Detail Portfolio Akademik</span>
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
      <div class="profile-col">
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

          <!-- Summary Metric Counts -->
          <div class="metrics-grid">
            <div class="metric-card-sm m-teal" @click="activePortfolioTab = 'jurnal'">
              <span class="mc-num">{{ jurnalList.length }}</span>
              <span class="mc-lbl">Publikasi Jurnal</span>
            </div>
            <div class="metric-card-sm m-blue" @click="activePortfolioTab = 'bimbingan'">
              <span class="mc-num">{{ bimbinganList.length }}</span>
              <span class="mc-lbl">Judul Bimbingan</span>
            </div>
            <div class="metric-card-sm m-purple" @click="activePortfolioTab = 'pengujian'">
              <span class="mc-num">{{ pengujianList.length }}</span>
              <span class="mc-lbl">Judul Pengujian</span>
            </div>
          </div>

          <div class="profile-divider"></div>

          <!-- Enhanced Education Timeline Section -->
          <div class="info-sec">
            <label>Riwayat Pendidikan</label>
            <div v-if="educationList.length" class="edu-timeline">
              <div v-for="(edu, idx) in educationList" :key="idx" class="edu-item">
                <div class="edu-dot"></div>
                <div class="edu-content">
                  <span class="edu-title">{{ edu }}</span>
                </div>
              </div>
            </div>
            <p v-else class="text-subtle">Belum ada data riwayat pendidikan.</p>
          </div>

          <div class="profile-divider"></div>

          <!-- Expertise Section -->
          <div class="info-sec">
            <label>Bidang Keahlian Spesifik</label>
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
      </div>

      <!-- Right Column: Portfolios with Clear Distinct Sections -->
      <div class="portfolio-col">
        <!-- Control & Tab Switcher Bar (Without Search) -->
        <div class="portfolio-nav-bar">
          <div class="portfolio-tabs">
            <button 
              type="button" 
              class="ptab-btn tab-teal" 
              :class="{ active: activePortfolioTab === 'jurnal' }"
              @click="activePortfolioTab = 'jurnal'"
            >
              Publikasi Jurnal ({{ jurnalList.length }})
            </button>
            <button 
              type="button" 
              class="ptab-btn tab-blue" 
              :class="{ active: activePortfolioTab === 'bimbingan' }"
              @click="activePortfolioTab = 'bimbingan'"
            >
              Bimbingan Skripsi ({{ bimbinganList.length }})
            </button>
            <button 
              type="button" 
              class="ptab-btn tab-purple" 
              :class="{ active: activePortfolioTab === 'pengujian' }"
              @click="activePortfolioTab = 'pengujian'"
            >
              Pengujian Sidang ({{ pengujianList.length }})
            </button>
          </div>
        </div>

        <!-- Section 1: Publikasi Jurnal -->
        <div 
          v-if="activePortfolioTab === 'jurnal'" 
          class="portfolio-section card-jurnal"
        >
          <div class="sec-header header-jurnal">
            <div class="sec-title-group">
              <span class="category-badge badge-teal">Kategori 1</span>
              <h3>Publikasi Jurnal & Makalah Ilmiah</h3>
            </div>
            <span class="count-pill pill-teal">{{ jurnalList.length }} Judul</span>
          </div>

          <div class="sec-body">
            <div v-if="jurnalList.length" class="items-grid">
              <div v-for="(j, idx) in jurnalList" :key="idx" class="item-card item-jurnal">
                <span class="item-num num-teal">#{{ idx + 1 }}</span>
                <div class="item-content">
                  <p class="item-title">{{ j }}</p>
                  <span class="item-type-tag tag-teal">Publikasi Jurnal / Paper</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-box">
              <p>Tidak ada data publikasi jurnal yang terdaftar.</p>
            </div>
          </div>
        </div>

        <!-- Section 2: Riwayat Bimbingan Skripsi -->
        <div 
          v-if="activePortfolioTab === 'bimbingan'" 
          class="portfolio-section card-bimbingan"
        >
          <div class="sec-header header-bimbingan">
            <div class="sec-title-group">
              <span class="category-badge badge-blue">Kategori 2</span>
              <h3>Riwayat Bimbingan Tugas Akhir / Skripsi</h3>
            </div>
            <span class="count-pill pill-blue">{{ bimbinganList.length }} Judul</span>
          </div>

          <div class="sec-body">
            <div v-if="bimbinganList.length" class="items-grid">
              <div v-for="(b, idx) in bimbinganList" :key="idx" class="item-card item-bimbingan">
                <span class="item-num num-blue">#{{ idx + 1 }}</span>
                <div class="item-content">
                  <p class="item-title">{{ b }}</p>
                  <span class="item-type-tag tag-blue">Peran: Pembimbing Utama / Anggota</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-box">
              <p>Tidak ada riwayat bimbingan mahasiswa yang terdaftar.</p>
            </div>
          </div>
        </div>

        <!-- Section 3: Riwayat Pengujian Sidang -->
        <div 
          v-if="activePortfolioTab === 'pengujian'" 
          class="portfolio-section card-pengujian"
        >
          <div class="sec-header header-pengujian">
            <div class="sec-title-group">
              <span class="category-badge badge-purple">Kategori 3</span>
              <h3>Riwayat Pengujian Sidang Skripsi</h3>
            </div>
            <span class="count-pill pill-purple">{{ pengujianList.length }} Judul</span>
          </div>

          <div class="sec-body">
            <div v-if="pengujianList.length" class="items-grid">
              <div v-for="(u, idx) in pengujianList" :key="idx" class="item-card item-pengujian">
                <span class="item-num num-purple">#{{ idx + 1 }}</span>
                <div class="item-content">
                  <p class="item-title">{{ u }}</p>
                  <span class="item-type-tag tag-purple">Peran: Penguji Sidang Mahasiswa</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-box">
              <p>Tidak ada riwayat pengujian sidang skripsi yang terdaftar.</p>
            </div>
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
.detail-grid { display: grid; grid-template-columns: 360px 1fr; gap: 2rem; align-items: start; }
@media (max-width: 960px) { .detail-grid { grid-template-columns: 1fr; } }

.profile-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.profile-header { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 1rem; }
.avatar-circle { width: 72px; height: 72px; border-radius: 50%; color: white; font-size: 2rem; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.profile-info h2 { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem; }
.chips-row { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 0.4rem; }
.chip { font-size: 0.72rem; font-weight: 600; padding: 3px 10px; border-radius: 99px; }
.prodi-chip { background: #e0f2fe; color: #0369a1; }
.nidn-chip { background: #f1f5f9; color: #475569; font-family: var(--font-mono, monospace); }

.profile-divider { height: 1px; background: #e2e8f0; margin: 1.25rem 0; }

/* Mini Metric Cards in Profile */
.metrics-grid { display: grid; grid-template-columns: 1fr; gap: 0.65rem; }
.metric-card-sm { padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid; display: flex; align-items: center; justify-content: space-between; cursor: pointer; transition: transform 0.15s; }
.metric-card-sm:hover { transform: translateY(-1px); }
.m-teal { background: #f0fdfa; border-color: #99f6e4; }
.m-teal .mc-num { color: #0f766e; }
.m-blue { background: #f0f9ff; border-color: #bae6fd; }
.m-blue .mc-num { color: #0369a1; }
.m-purple { background: #faf5ff; border-color: #e9d5ff; }
.m-purple .mc-num { color: #7e22ce; }

.mc-num { font-size: 1.25rem; font-weight: 700; font-family: var(--font-mono, monospace); }
.mc-lbl { font-size: 0.8rem; font-weight: 600; color: #475569; }

.info-sec { display: flex; flex-direction: column; gap: 0.5rem; }
.info-sec label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }

/* Education Timeline Component */
.edu-timeline { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 0.25rem; }
.edu-item { display: flex; align-items: flex-start; gap: 0.75rem; }
.edu-dot { width: 8px; height: 8px; border-radius: 50%; background: #0d9488; margin-top: 6px; flex-shrink: 0; box-shadow: 0 0 0 3px #ccfbf1; }
.edu-content { flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.5rem 0.75rem; }
.edu-title { font-size: 0.825rem; font-weight: 600; color: #1e293b; line-height: 1.45; display: block; }

.keahlian-flex { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.25rem; }
.tag-item { font-size: 0.75rem; background: #ccfbf1; color: #0f766e; border: 1px solid #99f6e4; padding: 3px 10px; border-radius: 6px; font-weight: 600; }
.text-subtle { font-size: 0.83rem; color: #94a3b8; font-style: italic; margin: 0; }

/* Portfolio Column & Tabs */
.portfolio-col { display: flex; flex-direction: column; gap: 1.5rem; }

.portfolio-nav-bar { display: flex; align-items: center; background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.65rem 0.85rem; }
.portfolio-tabs { display: flex; flex-wrap: wrap; gap: 0.4rem; width: 100%; }
.ptab-btn { background: none; border: 1px solid transparent; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.825rem; font-weight: 600; color: #64748b; cursor: pointer; transition: all 0.15s; }
.ptab-btn:hover { background: #f8fafc; color: #0f172a; }
.ptab-btn.tab-teal.active { background: #0d9488; border-color: #0d9488; color: white; }
.ptab-btn.tab-blue.active { background: #0284c7; border-color: #0284c7; color: white; }
.ptab-btn.tab-purple.active { background: #7c3aed; border-color: #7c3aed; color: white; }

/* Distinct Section Cards */
.portfolio-section { background: white; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }

.card-jurnal { border-top: 4px solid #0d9488; }
.card-bimbingan { border-top: 4px solid #0284c7; }
.card-pengujian { border-top: 4px solid #7c3aed; }

.sec-header { padding: 1.15rem 1.5rem; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; justify-content: space-between; }
.header-jurnal { background: #f0fdfa; }
.header-bimbingan { background: #f0f9ff; }
.header-pengujian { background: #faf5ff; }

.sec-title-group { display: flex; flex-direction: column; gap: 0.2rem; }
.category-badge { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; display: inline-block; }
.badge-teal { color: #0f766e; }
.badge-blue { color: #0369a1; }
.badge-purple { color: #7e22ce; }

.sec-title-group h3 { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin: 0; }

.count-pill { font-size: 0.75rem; font-family: var(--font-mono, monospace); font-weight: 700; padding: 4px 12px; border-radius: 99px; }
.pill-teal { background: #ccfbf1; color: #0f766e; border: 1px solid #99f6e4; }
.pill-blue { background: #e0f2fe; color: #0284c7; border: 1px solid #bae6fd; }
.pill-purple { background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff; }

.sec-body { padding: 1.25rem 1.5rem; }
.items-grid { display: flex; flex-direction: column; gap: 0.75rem; }

.item-card { display: flex; align-items: flex-start; gap: 1rem; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; background: #ffffff; transition: all 0.15s; }
.item-card:hover { border-color: #cbd5e1; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }

.item-num { font-size: 0.75rem; font-family: var(--font-mono, monospace); font-weight: 700; padding: 3px 8px; border-radius: 6px; flex-shrink: 0; }
.num-teal { background: #ccfbf1; color: #0f766e; }
.num-blue { background: #e0f2fe; color: #0284c7; }
.num-purple { background: #f3e8ff; color: #7e22ce; }

.item-content { flex: 1; display: flex; flex-direction: column; gap: 0.35rem; }
.item-title { font-size: 0.885rem; font-weight: 600; color: #0f172a; line-height: 1.5; margin: 0; }

.item-type-tag { font-size: 0.7rem; font-weight: 600; display: inline-block; }
.tag-teal { color: #0f766e; }
.tag-blue { color: #0284c7; }
.tag-purple { color: #7e22ce; }

.empty-box { text-align: center; padding: 2rem; color: #94a3b8; font-size: 0.85rem; font-style: italic; }
</style>
