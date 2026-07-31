<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const serverStatus = ref('checking')
const cacheReady = ref(false)

const checkStatus = async () => {
  try {
    const res = await api.get('/status')
    serverStatus.value = 'online'
    cacheReady.value = res.data.data.cache_ready
  } catch {
    serverStatus.value = 'offline'
  }
}
onMounted(checkStatus)
</script>

<template>
  <div class="home">
    <!-- Top bar -->
    <header class="home-topbar">
      <div class="topbar-brand">
        <div class="topbar-logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <span class="topbar-name">SiReDo<span class="topbar-api"> API</span></span>
      </div>
      <div class="topbar-links">
        <router-link to="/docs" class="tl">Dokumentasi</router-link>
        <router-link to="/preprocessing" class="tl">Pipeline</router-link>
        <router-link to="/single" class="tl tl-btn">Coba Sekarang →</router-link>
      </div>
    </header>

    <!-- Hero -->
    <section class="hero-section">
      <div class="hero-inner">
        <div class="hero-badge">
          <span :class="['status-dot', serverStatus === 'online' && cacheReady ? 'dot-green' : serverStatus === 'online' ? 'dot-amber' : 'dot-red']"></span>
          {{ serverStatus === 'online' && cacheReady ? 'Server Online · Model Ready' : serverStatus === 'online' ? 'Server Online · Warming Up' : 'Server Offline' }}
        </div>
        <h1 class="hero-title">
          Sistem Rekomendasi Dosen<br>
          <span class="hero-gradient">Berbasis Hybrid AI</span>
        </h1>
        <p class="hero-desc">
          SiReDo menggunakan algoritma <strong>BM25</strong> (lexical) dan <strong>SBERT</strong> (semantic) 
          untuk menemukan dosen pembimbing atau penguji yang paling relevan 
          berdasarkan judul dan abstrak proposal skripsi mahasiswa.
        </p>
        <div class="hero-actions">
          <router-link to="/single" class="btn-primary">Mulai Analisis →</router-link>
          <router-link to="/docs" class="btn-ghost">Lihat Dokumentasi API</router-link>
        </div>

        <!-- Quick stats -->
        <div class="hero-stats">
          <div class="stat">
            <span class="stat-val">BM25</span>
            <span class="stat-lbl">Lexical Scoring</span>
          </div>
          <div class="stat-div"></div>
          <div class="stat">
            <span class="stat-val">SBERT</span>
            <span class="stat-lbl">Semantic Scoring</span>
          </div>
          <div class="stat-div"></div>
          <div class="stat">
            <span class="stat-val">Hybrid</span>
            <span class="stat-lbl">Adaptive Ranking</span>
          </div>
          <div class="stat-div"></div>
          <div class="stat">
            <span class="stat-val">XAI</span>
            <span class="stat-lbl">Explainability</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Docs cards grid -->
    <section class="docs-section">
      <div class="docs-inner">

        <div class="section-label">Dokumentasi</div>

        <div class="cards-grid">
          <router-link to="/preprocessing" class="doc-card doc-card-feature">
            <div class="card-icon" style="background:#ede9ff;color:#5b4bdb">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
            </div>
            <h3>Pipeline NLP</h3>
            <p>Pelajari bagaimana sistem memproses teks dari preprocessing, ekspansi sinonim, BM25, SBERT, hingga Hybrid Ranking.</p>
            <span class="card-cta">Baca artikel →</span>
          </router-link>

          <router-link to="/docs" class="doc-card">
            <div class="card-icon" style="background:#eff6ff;color:#2563eb">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            </div>
            <h3>API Reference</h3>
            <p>Dokumentasi lengkap endpoint REST untuk integrasi dengan sistem akademik (SIAKAD).</p>
            <span class="card-cta">Lihat referensi →</span>
          </router-link>

          <router-link to="/single" class="doc-card">
            <div class="card-icon" style="background:#f0fdf4;color:#16a34a">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            </div>
            <h3>Single Recommendation</h3>
            <p>Analisis satu proposal secara real-time. Lihat skor BM25, SBERT, dan Hybrid setiap dosen beserta XAI explanation.</p>
            <span class="card-cta">Buka tool →</span>
          </router-link>

          <router-link to="/batch" class="doc-card">
            <div class="card-icon" style="background:#fffbeb;color:#d97706">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M4 6h16M4 10h16M4 14h16M4 18h16"/></svg>
            </div>
            <h3>Batch Recommendation</h3>
            <p>Proses ratusan proposal sekaligus via upload Excel atau JSON payload. Cocok untuk jadwal ujian massal.</p>
            <span class="card-cta">Buka tool →</span>
          </router-link>

          <router-link to="/config" class="doc-card">
            <div class="card-icon" style="background:#fdf4ff;color:#a21caf">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            </div>
            <h3>Konfigurasi Sistem</h3>
            <p>Sesuaikan K-Rank, BM25 threshold, dan batas token adaptive alpha sesuai kebutuhan institusi.</p>
            <span class="card-cta">Buka pengaturan →</span>
          </router-link>
        </div>

        <!-- Quick install / base URL info -->
        <div class="quickstart">
          <div class="qs-label">Base URL</div>
          <pre class="qs-code"><span class="tok-key">POST</span>  http://localhost:5000/api/rekomendasi/single
<span class="tok-key">POST</span>  http://localhost:5000/api/rekomendasi/batch
<span class="tok-key">GET</span>   http://localhost:5000/api/config
<span class="tok-key">GET</span>   http://localhost:5000/api/status</pre>
        </div>
      </div>
    </section>

    <footer class="home-footer">
      <p>SiReDo v3 · Sistem Rekomendasi Dosen · Hybrid BM25 + SBERT</p>
    </footer>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  min-height: 100svh;
  background: var(--bg);
}

/* Top bar */
.home-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.5rem;
  height: 60px;
  border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 10;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(10px);
}
.topbar-brand { display: flex; align-items: center; gap: 0.6rem; }
.topbar-logo {
  width: 28px; height: 28px;
  background: var(--brand);
  border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center;
  color: white;
}
.topbar-logo svg { width: 15px; height: 15px; }
.topbar-name { font-size: 0.95rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em; }
.topbar-api { color: var(--brand); }
.topbar-links { display: flex; align-items: center; gap: 0.25rem; }
.tl {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius);
  transition: background 0.15s, color 0.15s;
}
.tl:hover { background: var(--bg-muted); color: var(--text-primary); }
.tl-btn {
  background: var(--brand);
  color: white !important;
  font-weight: 600;
  margin-left: 0.25rem;
}
.tl-btn:hover { background: var(--brand-dim); }

/* Hero */
.hero-section {
  border-bottom: 1px solid var(--border);
  background: linear-gradient(160deg, #faf9ff 0%, #ffffff 60%);
}
.hero-inner {
  max-width: 760px;
  margin: 0 auto;
  padding: 5rem 2rem 4rem;
  text-align: center;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-muted);
  border: 1px solid var(--border);
  border-radius: 99px;
  padding: 0.3rem 0.9rem;
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 1.75rem;
}
.status-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}
.dot-green { background: var(--green); }
.dot-amber { background: var(--amber); }
.dot-red   { background: var(--red); }

@keyframes pulse {
  0%,100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1.15;
  color: var(--text-primary);
  margin: 0 0 1.25rem;
}
.hero-gradient {
  background: linear-gradient(135deg, var(--brand), #9b59f5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-desc {
  font-size: 1.05rem;
  color: var(--text-secondary);
  line-height: 1.75;
  max-width: 580px;
  margin: 0 auto 2rem;
}
.hero-desc strong { color: var(--text-primary); font-weight: 600; }
.hero-actions {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 3.5rem;
}
.btn-primary {
  background: var(--brand);
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.65rem 1.5rem;
  border-radius: var(--radius);
  text-decoration: none;
  transition: background 0.15s, transform 0.1s;
  box-shadow: 0 2px 12px rgba(91,75,219,0.3);
}
.btn-primary:hover { background: var(--brand-dim); transform: translateY(-1px); }
.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
  padding: 0.65rem 1.5rem;
  border-radius: var(--radius);
  text-decoration: none;
  border: 1px solid var(--border);
  transition: background 0.15s, color 0.15s;
}
.btn-ghost:hover { background: var(--bg-muted); color: var(--text-primary); }

.hero-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.stat { text-align: center; }
.stat-val { display: block; font-size: 0.9rem; font-weight: 700; font-family: var(--font-mono); color: var(--brand); }
.stat-lbl { display: block; font-size: 0.7rem; color: var(--text-muted); margin-top: 2px; }
.stat-div { width: 1px; height: 28px; background: var(--border); }

/* Docs section */
.docs-section {
  flex: 1;
  padding: 3.5rem 0 4rem;
}
.docs-inner {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}
.section-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-bottom: 1.25rem;
}
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  margin-bottom: 2.5rem;
}
.doc-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.4rem;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.doc-card:hover {
  border-color: var(--border-strong);
  box-shadow: 0 4px 20px rgba(0,0,0,0.07);
  transform: translateY(-2px);
}
.doc-card-feature {
  grid-column: span 2;
  background: linear-gradient(135deg, #faf9ff, #f5f0ff);
  border-color: #d4c8ff;
}
.card-icon {
  width: 38px; height: 38px;
  border-radius: var(--radius);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 0.25rem;
}
.card-icon svg { width: 20px; height: 20px; }
.doc-card h3 {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}
.doc-card p {
  font-size: 0.83rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  flex: 1;
}
.card-cta {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--brand);
  margin-top: 0.5rem;
}

/* Quickstart */
.quickstart {
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.qs-label {
  padding: 0.65rem 1rem;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
}
.qs-code {
  margin: 0;
  padding: 1.25rem 1.5rem;
  background: #0f0f14;
  color: #e4e4f0;
  font-family: var(--font-mono);
  font-size: 0.82rem;
  line-height: 1.9;
  overflow-x: auto;
}

/* Footer */
.home-footer {
  border-top: 1px solid var(--border);
  padding: 1.25rem 2rem;
  text-align: center;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.home-footer p { margin: 0; }

@media (max-width: 640px) {
  .home-topbar { padding: 0 1rem; }
  .hero-inner { padding: 3rem 1rem 2.5rem; }
  .doc-card-feature { grid-column: span 1; }
  .topbar-links .tl:not(.tl-btn) { display: none; }
}
</style>
