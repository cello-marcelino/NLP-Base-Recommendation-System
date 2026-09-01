<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const stats = ref({
  totalDosen: 0,
  threshold: 0.3,
  isAdaptive: true,
  status: 'online'
})
const isLoading = ref(true)

onMounted(async () => {
  try {
    const [dosenRes, configRes] = await Promise.all([
      api.get('/admin/dosen'),
      api.get('/admin/config')
    ])
    stats.value.totalDosen = dosenRes.data.meta?.total || dosenRes.data.data?.length || 0
    stats.value.threshold = configRes.data.data?.threshold ?? 0.3
    stats.value.isAdaptive = configRes.data.data?.is_adaptive ?? true
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="admin-dashboard-page">
    <div class="page-header">
      <span class="page-badge">Admin Dashboard</span>
      <h1>Ringkasan Pengelolaan SiReDo</h1>
      <p>Pusat kendali data master dosen, publikasi jurnal, riwayat bimbingan/pengujian, serta parameter NLP Engine.</p>
    </div>

    <div v-if="isLoading" class="loading-box">
      <div class="spinner"></div>
      <span>Memuat data dashboard...</span>
    </div>

    <div v-else class="dashboard-grid">
      <!-- Stat Card 1 -->
      <div class="stat-card">
        <div class="stat-icon icon-teal">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <div class="stat-content">
          <span class="stat-label">Total Dosen Pembimbing</span>
          <span class="stat-value">{{ stats.totalDosen }}</span>
          <span class="stat-desc">Dosen terintegrasi dalam database relasional</span>
        </div>
      </div>

      <!-- Stat Card 2 -->
      <div class="stat-card">
        <div class="stat-icon icon-emerald">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div class="stat-content">
          <span class="stat-label">NLP Engine Threshold</span>
          <span class="stat-value">{{ Number(stats.threshold).toFixed(2) }}</span>
          <span class="stat-desc">Min-Max Normalization Hard Filter</span>
        </div>
      </div>

      <!-- Stat Card 3 -->
      <div class="stat-card">
        <div class="stat-icon icon-blue">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div class="stat-content">
          <span class="stat-label">Mode Pembobotan AI</span>
          <span class="stat-value">{{ stats.isAdaptive ? 'Adaptive' : 'Manual' }}</span>
          <span class="stat-desc">Hybrid BM25 + Sentence-BERT Mode</span>
        </div>
      </div>
    </div>

    <!-- Shortcut Cards -->
    <div class="shortcuts-section">
      <h3>Aksi Cepat Admin</h3>
      <div class="shortcuts-grid">
        <router-link to="/admin/dosen" class="shortcut-card">
          <div class="sc-title">Kelola Data Dosen</div>
          <div class="sc-desc">Tambah, edit, atau hapus data dosen, publikasi jurnal, dan riwayat bimbingan.</div>
          <span class="sc-arrow">Buka Kelola Dosen →</span>
        </router-link>

        <router-link to="/admin/config" class="shortcut-card">
          <div class="sc-title">Konfigurasi Engine NLP</div>
          <div class="sc-desc">Atur threshold filter, alpha manual, dan mode pembobotan adaptif.</div>
          <span class="sc-arrow">Atur Engine →</span>
        </router-link>

        <router-link to="/admin/batch" class="shortcut-card">
          <div class="sc-title">Simulasi Batch Recommendation</div>
          <div class="sc-desc">Uji rekomendasi massal untuk pengujian dataset tesis simultan.</div>
          <span class="sc-arrow">Jalankan Batch →</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard-page { padding: 2.5rem 2rem; max-width: 1100px; }
.page-header { margin-bottom: 2rem; }
.page-badge { display: inline-block; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: #ccfbf1; color: #0f766e; padding: 3px 10px; border-radius: 99px; margin-bottom: 0.75rem; }
.page-header h1 { font-size: 1.85rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem; letter-spacing: -0.02em; }
.page-header p { font-size: 0.925rem; color: #64748b; margin: 0; line-height: 1.6; }

.loading-box { display: flex; align-items: center; gap: 0.75rem; color: #64748b; padding: 3rem 0; }
.spinner { width: 20px; height: 20px; border: 2px solid #cbd5e1; border-top-color: #0d9488; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-bottom: 2.5rem; }
.stat-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; display: flex; align-items: flex-start; gap: 1.25rem; box-shadow: 0 2px 4px rgba(0,0,0,0.03); }
.stat-icon { width: 46px; height: 46px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.stat-icon svg { width: 24px; height: 24px; }
.icon-teal { background: #ccfbf1; color: #0d9488; }
.icon-emerald { background: #d1fae5; color: #059669; }
.icon-blue { background: #dbeafe; color: #2563eb; }

.stat-content { display: flex; flex-direction: column; }
.stat-label { font-size: 0.8rem; font-weight: 600; color: #64748b; margin-bottom: 0.25rem; }
.stat-value { font-size: 1.75rem; font-weight: 700; color: #0f172a; font-family: var(--font-mono, monospace); line-height: 1.2; }
.stat-desc { font-size: 0.75rem; color: #94a3b8; margin-top: 0.35rem; }

.shortcuts-section h3 { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0 0 1rem; }
.shortcuts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; }
.shortcut-card { background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.5rem; text-decoration: none; display: flex; flex-direction: column; transition: all 0.2s; }
.shortcut-card:hover { border-color: #0d9488; transform: translateY(-2px); box-shadow: 0 8px 16px rgba(13, 148, 136, 0.08); }
.sc-title { font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 0.4rem; }
.sc-desc { font-size: 0.83rem; color: #64748b; line-height: 1.5; flex: 1; margin-bottom: 1rem; }
.sc-arrow { font-size: 0.8rem; font-weight: 600; color: #0d9488; }
</style>
