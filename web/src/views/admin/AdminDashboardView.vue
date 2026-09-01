<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '../../services/api'

// --- State Models ---
const serverState = ref({
  online: false,
  status: 'offline', // 'offline' | 'warming_up' | 'reloading' | 'ready' | 'idle' | 'error'
  cacheReady: false,
  totalDosen: 0,
  device: 'CPU',
  message: 'Menghubungkan ke server...',
  detail: 'Memeriksa status port 5000...',
  progressPct: 0,
  currentStep: 0,
  totalSteps: 5,
  elapsedSeconds: 0,
  startedAt: null,
  completedAt: null,
  steps: [
    { id: 1, code: 'loading_data', title: '1. Load Data Dosen', desc: 'Mengambil data dari Storage/DB', status: 'pending', duration_ms: 0, detail: 'Menghubungkan ke database...' },
    { id: 2, code: 'preprocessing', title: '2. Preprocessing Korpus', desc: 'Case folding, stopword, n-gram', status: 'pending', duration_ms: 0, detail: 'Tokenisasi teks profil dosen...' },
    { id: 3, code: 'vektoring', title: '3. BM25 Vektoring', desc: 'Lexical inverted index & IDF', status: 'pending', duration_ms: 0, detail: 'Fitting BM25Okapi Engine...' },
    { id: 4, code: 'embedding', title: '4. SBERT Embedding', desc: 'Dense 384-dim & KeyBERT XAI', status: 'pending', duration_ms: 0, detail: 'Semantic encoding & topic extraction...' },
    { id: 5, code: 'persisting', title: '5. Simpan Cache Disk', desc: 'Snapshot embedding .npy/pkl', status: 'pending', duration_ms: 0, detail: 'Menyimpan snapshot cache...' }
  ]
})

const stats = ref({
  totalDosen: 0,
  threshold: 0.3,
  isAdaptive: true
})

const isReloading = ref(false)
const lastChecked = ref(new Date().toLocaleTimeString())
let pollTimer = null

// --- Computed Status Properties ---
const statusBadgeClass = computed(() => {
  if (!serverState.value.online) return 'badge-offline'
  if (serverState.value.status === 'warming_up') return 'badge-warming'
  if (serverState.value.status === 'reloading') return 'badge-reloading'
  if (serverState.value.status === 'error') return 'badge-error'
  return 'badge-ready'
})

const statusLabel = computed(() => {
  if (!serverState.value.online) return 'Server Offline (Mati)'
  if (serverState.value.status === 'warming_up') return 'Warming Up (Inisialisasi)'
  if (serverState.value.status === 'reloading') return 'Reloading (Re-Indexing)'
  if (serverState.value.status === 'error') return 'Error Inisialisasi'
  return 'Ready & Idle (Siap)'
})

// --- Status Polling Logic ---
const fetchStatus = async () => {
  lastChecked.value = new Date().toLocaleTimeString()
  try {
    const res = await api.get('/status', { timeout: 3000 })
    const data = res.data?.data || {}
    
    serverState.value.online = true
    serverState.value.cacheReady = Boolean(data.cache_ready)
    serverState.value.totalDosen = data.total_dosen || 0
    serverState.value.device = data.device || 'CPU'
    
    const ws = data.warmup_status
    if (ws) {
      serverState.value.status = ws.state || (data.cache_ready ? 'ready' : 'warming_up')
      serverState.value.currentStep = ws.current_step || 0
      serverState.value.totalSteps = ws.total_steps || 5
      serverState.value.message = ws.message || (data.cache_ready ? 'SiReDo v3 is running' : 'Warming up...')
      serverState.value.detail = ws.detail || ''
      serverState.value.progressPct = ws.progress_pct ?? (data.cache_ready ? 100 : (ws.current_step / 5) * 100)
      serverState.value.elapsedSeconds = ws.elapsed_seconds || 0
      serverState.value.startedAt = ws.started_at
      serverState.value.completedAt = ws.completed_at
      
      if (Array.isArray(ws.steps) && ws.steps.length > 0) {
        serverState.value.steps = ws.steps
      }
    } else {
      serverState.value.status = data.cache_ready ? 'ready' : 'warming_up'
      serverState.value.progressPct = data.cache_ready ? 100 : 50
    }
    
    if (serverState.value.cacheReady) {
      isReloading.value = false
    }
  } catch (err) {
    // Server is unreachable (offline / down)
    serverState.value.online = false
    serverState.value.status = 'offline'
    serverState.value.cacheReady = false
    serverState.value.message = 'Koneksi ke backend server gagal (Port 5000 offline)'
    serverState.value.detail = 'Server Python belum aktif. Jalankan "python siredo serve" di terminal.'
    serverState.value.progressPct = 0
    serverState.value.steps.forEach(s => { s.status = 'pending' })
  }
}

const fetchDashboardStats = async () => {
  if (!serverState.value.online) return
  try {
    const [dosenRes, configRes] = await Promise.allSettled([
      api.get('/admin/dosen'),
      api.get('/admin/config')
    ])
    
    if (dosenRes.status === 'fulfilled') {
      stats.value.totalDosen = dosenRes.value.data.meta?.total || dosenRes.value.data.data?.length || 0
    }
    if (configRes.status === 'fulfilled') {
      stats.value.threshold = configRes.value.data.data?.threshold ?? 0.3
      stats.value.isAdaptive = configRes.value.data.data?.is_adaptive ?? true
    }
  } catch (err) {
    console.warn('Gagal memuat statistik admin:', err)
  }
}

// Adaptive scheduler based on server activity
const scheduleNextPoll = () => {
  if (pollTimer) clearTimeout(pollTimer)
  
  let intervalMs = 3000
  if (!serverState.value.online) {
    intervalMs = 1500 // fast poll when offline to catch server boot instantly
  } else if (['warming_up', 'reloading'].includes(serverState.value.status) || isReloading.value) {
    intervalMs = 450 // ultra-fast poll for fluid animation during warmup/reload
  }
  
  pollTimer = setTimeout(async () => {
    await fetchStatus()
    scheduleNextPoll()
  }, intervalMs)
}

// Manual trigger for testing real-time warm-up / re-indexing
const triggerReload = async () => {
  if (isReloading.value) return
  isReloading.value = true
  serverState.value.status = 'reloading'
  serverState.value.message = 'Memulai proses reload NLP engine...'
  serverState.value.progressPct = 5
  
  try {
    await api.post('/system/reload', {}, {
      headers: { 'X-API-Key': localStorage.getItem('siredo_admin_key') || 'siredo-admin-secret-key' }
    })
  } catch (err) {
    console.error('Trigger reload error:', err)
  } finally {
    scheduleNextPoll()
  }
}

onMounted(async () => {
  await fetchStatus()
  await fetchDashboardStats()
  scheduleNextPoll()
})

onUnmounted(() => {
  if (pollTimer) clearTimeout(pollTimer)
})
</script>

<template>
  <div class="admin-dashboard-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <span class="page-badge">Admin Dashboard</span>
        <h1>Ringkasan Pengelolaan SiReDo</h1>
        <p>Pusat kendali data master dosen, publikasi jurnal, riwayat bimbingan/pengujian, serta parameter NLP Engine.</p>
      </div>
    </div>

    <!-- ======================================================== -->
    <!-- DYNAMIC CLEAN SERVER STATUS BAR -->
    <!-- ======================================================== -->
    <div class="server-status-bar" :class="`state-${serverState.status}`">
      <div class="status-main-info">
        <div class="pulse-indicator" :class="`pulse-${serverState.status}`"></div>
        <div class="status-text-group">
          <div class="status-title-row">
            <span class="status-badge" :class="statusBadgeClass">{{ statusLabel }}</span>
            <span class="status-message">{{ serverState.message }}</span>
          </div>
          <div class="status-subdetail" v-if="serverState.detail && serverState.status !== 'ready'">
            {{ serverState.detail }}
          </div>
        </div>
      </div>

      <!-- Real-time dynamic progress bar (active during warmup/reload) -->
      <div class="status-progress-inline" v-if="['warming_up', 'reloading'].includes(serverState.status)">
        <div class="progress-track-mini">
          <div class="progress-fill-mini" :style="{ width: `${serverState.progressPct}%` }"></div>
        </div>
        <span class="progress-pct-mini">{{ Math.round(serverState.progressPct) }}%</span>
      </div>

      <div class="status-meta-group">
        <span class="meta-pill" v-if="serverState.online">
          <span class="pill-dot"></span> {{ serverState.device }}
        </span>
        <button 
          class="btn-reload-mini" 
          title="Muat ulang dan sinkronisasi cache model AI"
          :disabled="!serverState.online || isReloading || ['warming_up', 'reloading'].includes(serverState.status)"
          @click="triggerReload"
        >
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" :class="{ 'spin-icon': isReloading || ['warming_up', 'reloading'].includes(serverState.status) }">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>{{ ['warming_up', 'reloading'].includes(serverState.status) ? 'Syncing...' : 'Sync Engine' }}</span>
        </button>
      </div>
    </div>

    <!-- ======================================================== -->
    <!-- METRIC STAT CARDS (MAIN DATA FOCUS) -->
    <!-- ======================================================== -->
    <div class="dashboard-grid">
      <!-- Stat Card 1 -->
      <div class="stat-card">
        <div class="stat-icon icon-teal">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <div class="stat-content">
          <span class="stat-label">Total Dosen Pembimbing</span>
          <span class="stat-value">{{ stats.totalDosen || serverState.totalDosen }}</span>
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
          <span class="stat-desc">BM25 Hard Filter Relevansi</span>
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
          <span class="stat-desc">Hybrid BM25 + SBERT Semantic Mode</span>
        </div>
      </div>
    </div>

    <!-- ======================================================== -->
    <!-- SHORTCUT CARDS -->
    <!-- ======================================================== -->
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
.admin-dashboard-page {
  padding: 2rem 2.5rem;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

/* Page Header */
.page-header {
  margin-bottom: 1.5rem;
}
.header-left { flex: 1; }
.page-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: #ccfbf1;
  color: #0f766e;
  padding: 3px 10px;
  border-radius: 99px;
  margin-bottom: 0.75rem;
}
.page-header h1 {
  font-size: 1.85rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
}
.page-header p {
  font-size: 0.925rem;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

/* ======================================================== */
/* CLEAN & COMPACT SERVER STATUS BAR */
/* ======================================================== */
.server-status-bar {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.85rem 1.25rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  transition: all 0.2s ease;
  flex-wrap: wrap;
}

.server-status-bar.state-ready {
  border-left: 4px solid #10b981;
}
.server-status-bar.state-warming_up {
  border-left: 4px solid #f59e0b;
  background: #fffdfa;
}
.server-status-bar.state-reloading {
  border-left: 4px solid #3b82f6;
  background: #f8faff;
}
.server-status-bar.state-offline {
  border-left: 4px solid #ef4444;
  background: #fef8f8;
}

.status-main-info {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  min-width: 240px;
}

/* Pulse indicator */
.pulse-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.pulse-ready {
  background: #10b981;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: pulse-ring-green 2s infinite;
}
.pulse-warming {
  background: #f59e0b;
  box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7);
  animation: pulse-ring-amber 1.5s infinite;
}
.pulse-reloading {
  background: #3b82f6;
  box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
  animation: pulse-ring-blue 1.5s infinite;
}
.pulse-offline {
  background: #ef4444;
  box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  animation: pulse-ring-red 2s infinite;
}

@keyframes pulse-ring-green {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
@keyframes pulse-ring-amber {
  0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(245, 158, 11, 0); }
  100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
}
@keyframes pulse-ring-blue {
  0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(59, 130, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}
@keyframes pulse-ring-red {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.status-text-group {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.status-title-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}
.status-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 99px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.badge-ready { background: #d1fae5; color: #059669; }
.badge-warming { background: #fef3c7; color: #b45309; }
.badge-reloading { background: #dbeafe; color: #1d4ed8; }
.badge-offline { background: #fee2e2; color: #dc2626; }
.badge-error { background: #fee2e2; color: #991b1b; }

.status-message {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e293b;
}
.status-subdetail {
  font-size: 0.75rem;
  color: #64748b;
}

/* Mini Progress for inline bar */
.status-progress-inline {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  max-width: 220px;
}
.progress-track-mini {
  flex: 1;
  height: 6px;
  background: #e2e8f0;
  border-radius: 99px;
  overflow: hidden;
}
.progress-fill-mini {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #0d9488);
  transition: width 0.3s ease;
}
.progress-pct-mini {
  font-size: 0.75rem;
  font-weight: 700;
  color: #334155;
  font-family: var(--font-mono, monospace);
}

/* Meta & Action */
.status-meta-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.meta-pill {
  font-size: 0.72rem;
  font-weight: 600;
  color: #475569;
  background: #f1f5f9;
  padding: 3px 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}
.pill-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #0d9488;
}

.btn-reload-mini {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.35rem 0.7rem;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #334155;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-reload-mini:hover:not(:disabled) {
  background: #0f766e;
  border-color: #0f766e;
  color: white;
}
.btn-reload-mini:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-reload-mini svg {
  width: 14px;
  height: 14px;
}
.spin-icon {
  animation: spin 1s linear infinite;
}

/* ======================================================== */
/* DASHBOARD GRID & STATS (MAIN FOCUS) */
/* ======================================================== */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 2.5rem;
}
.stat-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.03);
}
.stat-icon {
  width: 46px;
  height: 46px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stat-icon svg { width: 24px; height: 24px; }
.icon-teal { background: #ccfbf1; color: #0d9488; }
.icon-emerald { background: #d1fae5; color: #059669; }
.icon-blue { background: #dbeafe; color: #2563eb; }

.stat-content { display: flex; flex-direction: column; }
.stat-label { font-size: 0.8rem; font-weight: 600; color: #64748b; margin-bottom: 0.25rem; }
.stat-value { font-size: 1.75rem; font-weight: 700; color: #0f172a; font-family: var(--font-mono, monospace); line-height: 1.2; }
.stat-desc { font-size: 0.75rem; color: #94a3b8; margin-top: 0.35rem; }

/* ======================================================== */
/* SHORTCUTS */
/* ======================================================== */
.shortcuts-section h3 { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0 0 1rem; }
.shortcuts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; }
.shortcut-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1.5rem;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}
.shortcut-card:hover {
  border-color: #0d9488;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(13, 148, 136, 0.08);
}
.sc-title { font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 0.4rem; }
.sc-desc { font-size: 0.83rem; color: #64748b; line-height: 1.5; flex: 1; margin-bottom: 1rem; }
.sc-arrow { font-size: 0.8rem; font-weight: 600; color: #0d9488; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>
