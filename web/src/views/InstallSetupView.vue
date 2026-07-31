<script setup>
// Install & Setup View
</script>

<template>
  <div class="install-page">
    <div class="ip-header">
      <span class="ip-badge">Panduan Open Source</span>
      <h1 class="ip-title">Instalasi & Setup</h1>
      <p class="ip-lead">
        Panduan langkah demi langkah untuk melakukan instalasi Siredo v3 di lingkungan lokal (development).
        Sistem ini sepenuhnya open source dan dapat dikembangkan lebih lanjut.
      </p>
      
      <div class="repo-link-card">
        <div class="repo-icon">
          <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
        </div>
        <div class="repo-info">
          <h3>Repositori Resmi</h3>
          <p>Kunjungi repositori GitHub untuk berkontribusi, melaporkan isu, atau melakukan fork proyek ini.</p>
          <a href="https://github.com/cello-marcelino/NLP-Base-Recommendation-System" target="_blank" rel="noopener noreferrer" class="repo-btn">
            Menuju GitHub Repo &rarr;
          </a>
        </div>
      </div>
    </div>

    <div class="ip-content">
      <div class="ip-section">
        <h2>1. Prasyarat Sistem</h2>
        <p>Sebelum memulai, pastikan perangkat Anda telah terpasang perangkat lunak berikut:</p>
        <ul class="ip-list">
          <li><strong>Python 3.9+</strong> (Diperlukan untuk menjalankan Backend AI NLP)</li>
          <li><strong>Node.js 16+</strong> & <strong>npm</strong> (Diperlukan untuk menjalankan Frontend Vue 3)</li>
          <li><strong>Git</strong> (Untuk kloning repositori)</li>
        </ul>
      </div>

      <div class="ip-section">
        <h2>2. Kloning Repositori</h2>
        <div class="code-block">
          <pre><code>git clone https://github.com/cello-marcelino/NLP-Base-Recommendation-System.git
cd NLP-Base-Recommendation-System</code></pre>
        </div>
      </div>

      <div class="ip-section">
        <h2>3. Setup Backend (Server Flask)</h2>
        <p>Backend menggunakan Flask dan library NLP seperti Sentence-Transformers (SBERT). Kami menyarankan penggunaan Virtual Environment.</p>
        <div class="code-block">
          <pre><code># Masuk ke direktori server
cd server

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment (Windows)
venv\Scripts\activate

# Aktifkan virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependensi yang dibutuhkan
pip install -r requirements.txt

# Jalankan server
python run.py</code></pre>
        </div>
        <div class="ip-alert ip-alert--info">
          <strong>Catatan:</strong> Saat pertama kali dijalankan, proses ini mungkin memakan waktu lebih lama karena sistem akan mengunduh model NLP bawaan (seperti indo-sentence-bert-base).
        </div>
      </div>

      <div class="ip-section">
        <h2>4. Setup Frontend (Web Vue)</h2>
        <p>Buka terminal/CMD baru, lalu lakukan instalasi dan jalankan server *development* untuk antarmuka web.</p>
        <div class="code-block">
          <pre><code># Masuk ke direktori web (dari root folder)
cd web

# Install modul Node.js
npm install

# Jalankan server frontend
npm run dev</code></pre>
        </div>
        <p>Setelah berhasil, buka tautan <code>http://localhost:5173</code> di *browser* Anda untuk mengakses aplikasi Siredo v3.</p>
      </div>

      <div class="ip-section">
        <h2>5. Konfigurasi Dataset</h2>
        <p>Sistem ini telah dilengkapi dengan dataset utama Polibatam yang dapat ditemukan di direktori <code>server/data/dataset_profiles_terintegrasi.xlsx</code>. Jika Anda berencana mengganti dengan dataset institusi Anda sendiri, pastikan kolom yang ada setidaknya memiliki header: <code>id</code>, <code>judul</code>, <code>abstrak</code>, <code>nidn</code>, dan <code>nama</code>.</p>
      </div>
      
    </div>
  </div>
</template>

<style scoped>
.install-page { padding: 3rem 2.5rem 5rem; max-width: 900px; margin: 0 auto; }
.ip-header { text-align: center; margin-bottom: 3.5rem; }
.ip-badge { display: inline-block; padding: 0.35rem 1rem; background: var(--brand-light); color: var(--brand); font-size: 0.8rem; font-weight: 700; border-radius: 99px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; }
.ip-title { font-size: 2.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 1rem; letter-spacing: -0.02em; }
.ip-lead { font-size: 1.15rem; color: var(--text-secondary); max-width: 700px; margin: 0 auto 2.5rem; line-height: 1.6; }

.repo-link-card { display: flex; align-items: center; gap: 1.5rem; background: var(--bg); border: 1px solid var(--border-strong); padding: 1.5rem 2rem; border-radius: var(--radius-lg); text-align: left; max-width: 650px; margin: 0 auto; box-shadow: var(--shadow-sm); transition: transform 0.2s, box-shadow 0.2s; }
.repo-link-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); border-color: var(--brand); }
.repo-icon { color: #181717; background: #f1f5f9; padding: 1rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.repo-info h3 { font-size: 1.15rem; font-weight: 700; margin: 0 0 0.25rem 0; color: var(--text-primary); }
.repo-info p { font-size: 0.9rem; color: var(--text-secondary); margin: 0 0 1rem 0; line-height: 1.5; }
.repo-btn { display: inline-block; background: #181717; color: #fff; font-weight: 600; font-size: 0.85rem; padding: 0.6rem 1.25rem; border-radius: var(--radius); text-decoration: none; transition: background 0.2s; }
.repo-btn:hover { background: #333; }

.ip-content { display: flex; flex-direction: column; gap: 3rem; }
.ip-section h2 { font-size: 1.4rem; font-weight: 700; color: var(--brand); margin-bottom: 1rem; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; display: inline-block; }
.ip-section p { font-size: 1rem; color: var(--text-primary); line-height: 1.6; margin-bottom: 1rem; }

.ip-list { margin: 0 0 1.5rem 1.5rem; color: var(--text-primary); line-height: 1.8; font-size: 1rem; }

.code-block { background: #1e1e1e; border-radius: var(--radius-lg); padding: 1.25rem; overflow-x: auto; margin-bottom: 1.5rem; border: 1px solid #333; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2); }
.code-block pre { margin: 0; }
.code-block code { font-family: 'Fira Code', 'Consolas', monospace; font-size: 0.9rem; color: #e5e7eb; line-height: 1.6; }

.ip-alert { padding: 1rem 1.5rem; border-radius: var(--radius); font-size: 0.95rem; line-height: 1.5; margin-bottom: 1.5rem; }
.ip-alert--info { background: var(--blue-bg); border: 1px solid var(--blue-border); color: var(--blue); }
.ip-alert--info strong { color: #1d4ed8; }

@media (max-width: 768px) {
  .install-page { padding: 2rem 1.5rem; }
  .repo-link-card { flex-direction: column; text-align: center; gap: 1rem; }
  .repo-icon { margin: 0 auto; }
}
</style>
