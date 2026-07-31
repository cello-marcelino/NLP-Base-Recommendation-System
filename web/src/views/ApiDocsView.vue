<script setup>
import { ref } from 'vue'

const activeSection = ref('overview')

const sections = [
  { id: 'overview', label: 'Overview' },
  { id: 'auth', label: 'Autentikasi' },
  { id: 'single', label: 'POST /single' },
  { id: 'batch', label: 'POST /batch' },
  { id: 'batch-upload', label: 'POST /batch/upload' },
  { id: 'config-get', label: 'GET /config' },
  { id: 'config-patch', label: 'PATCH /config' },
  { id: 'status', label: 'GET /status' },
  { id: 'errors', label: 'Error Handling' },
]
</script>

<template>
  <div class="docs-layout">
    <!-- Page TOC sidebar -->
    <aside class="toc-sidebar">
      <div class="toc-title">API Reference</div>
      <nav class="toc-nav">
        <a
          v-for="s in sections" :key="s.id"
          :href="`#${s.id}`"
          class="toc-link"
          :class="{ active: activeSection === s.id }"
          @click.prevent="activeSection = s.id; document.getElementById(s.id)?.scrollIntoView({behavior:'smooth'})"
        >{{ s.label }}</a>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="docs-main">
      <div class="prose docs-prose">

        <!-- Page header -->
        <div class="page-header">
          <span class="page-badge">REST API</span>
          <h1>API Reference</h1>
          <p class="page-lead">
            SiReDo menyediakan REST API untuk integrasi dengan sistem akademik (SIAKAD) maupun aplikasi pihak ketiga.
            Semua request dan response menggunakan format <strong>JSON</strong>.
          </p>
          <div class="base-url-box">
            <span class="bu-label">BASE URL</span>
            <code class="bu-val">http://localhost:5000/api</code>
          </div>
        </div>

        <!-- Overview -->
        <section id="overview">
          <h2>Overview</h2>
          <p>
            API SiReDo dirancang mengikuti prinsip REST. Setiap endpoint mengembalikan respons
            dalam envelope JSON yang konsisten dengan format berikut:
          </p>
          <pre><code><span class="tok-comment">// Respons sukses</span>
{
  <span class="tok-key">"status"</span>: <span class="tok-str">"success"</span>,
  <span class="tok-key">"message"</span>: <span class="tok-str">"Success"</span>,
  <span class="tok-key">"data"</span>: { ... }
}

<span class="tok-comment">// Respons error</span>
{
  <span class="tok-key">"status"</span>: <span class="tok-str">"error"</span>,
  <span class="tok-key">"message"</span>: <span class="tok-str">"Deskripsi error"</span>
}</code></pre>

          <div class="info-table">
            <table>
              <thead><tr><th>Endpoint</th><th>Method</th><th>Deskripsi</th></tr></thead>
              <tbody>
                <tr><td><code>/rekomendasi/single</code></td><td><span class="badge-post">POST</span></td><td>Rekomendasi satu dokumen/penelitian</td></tr>
                <tr><td><code>/rekomendasi/batch</code></td><td><span class="badge-post">POST</span></td><td>Rekomendasi massal via JSON</td></tr>
                <tr><td><code>/rekomendasi/batch/upload</code></td><td><span class="badge-post">POST</span></td><td>Rekomendasi massal via Excel</td></tr>
                <tr><td><code>/config</code></td><td><span class="badge-get">GET</span></td><td>Ambil konfigurasi aktif</td></tr>
                <tr><td><code>/config</code></td><td><span class="badge-patch">PATCH</span></td><td>Update konfigurasi</td></tr>
                <tr><td><code>/status</code></td><td><span class="badge-get">GET</span></td><td>Status server & cache</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Auth -->
        <section id="auth">
          <h2>Autentikasi</h2>
          <p>
            Saat ini API SiReDo <strong>tidak memerlukan autentikasi</strong> dan dirancang untuk
            digunakan di lingkungan jaringan internal kampus. Untuk deployment produksi,
            sangat direkomendasikan untuk menambahkan API key atau token JWT di layer reverse proxy (Nginx/Caddy).
          </p>
          <blockquote>
            ⚠️ Jangan expose endpoint ini ke internet publik tanpa proteksi autentikasi.
          </blockquote>
        </section>

        <!-- Single -->
        <section id="single">
          <h2>POST /rekomendasi/single</h2>
          <p>
            Menjalankan pipeline rekomendasi lengkap (Preprocessing → BM25 → SBERT → Hybrid Ranking)
            untuk satu dokumen penelitian. Mengembalikan top-K dosen beserta skor dan penjelasan XAI.
          </p>

          <h3>Request Body</h3>
          <div class="param-table">
            <table>
              <thead><tr><th>Parameter</th><th>Tipe</th><th>Wajib</th><th>Keterangan</th></tr></thead>
              <tbody>
                <tr><td><code>judul</code></td><td>string</td><td>✓*</td><td>Judul penelitian/dokumen</td></tr>
                <tr><td><code>abstrak</code></td><td>string</td><td>✓*</td><td>Abstrak penelitian (opsional jika judul diisi)</td></tr>
                <tr><td><code>k_rank</code></td><td>integer</td><td>—</td><td>Jumlah rekomendasi. Default: dari konfigurasi (5)</td></tr>
              </tbody>
            </table>
          </div>
          <p><small>*Minimal salah satu dari <code>judul</code> atau <code>abstrak</code> harus diisi.</small></p>

          <h3>Contoh Request</h3>
          <pre><code><span class="tok-comment">// curl</span>
curl -X POST http://localhost:5000/api/rekomendasi/single \
  -H <span class="tok-str">"Content-Type: application/json"</span> \
  -d '{
    <span class="tok-key">"judul"</span>: <span class="tok-str">"Penerapan Deep Learning untuk Deteksi Penyakit Tanaman"</span>,
    <span class="tok-key">"abstrak"</span>: <span class="tok-str">"Penelitian ini bertujuan mengklasifikasi penyakit daun menggunakan CNN..."</span>,
    <span class="tok-key">"k_rank"</span>: <span class="tok-num">5</span>
  }'</code></pre>

          <h3>Contoh Response</h3>
          <pre><code>{
  <span class="tok-key">"status"</span>: <span class="tok-str">"success"</span>,
  <span class="tok-key">"data"</span>: {
    <span class="tok-key">"metadata"</span>: {
      <span class="tok-key">"alpha"</span>: <span class="tok-num">0.35</span>,          <span class="tok-comment">// bobot BM25</span>
      <span class="tok-key">"beta"</span>: <span class="tok-num">0.65</span>,           <span class="tok-comment">// bobot SBERT</span>
      <span class="tok-key">"num_query_tokens"</span>: <span class="tok-num">18</span>,  <span class="tok-comment">// panjang query → mode abstrak</span>
      <span class="tok-key">"k_rank"</span>: <span class="tok-num">5</span>
    },
    <span class="tok-key">"pipeline"</span>: {
      <span class="tok-key">"preprocessing"</span>: { <span class="tok-comment">/* token hasil preprocessing */</span> },
      <span class="tok-key">"ekspansi"</span>: { <span class="tok-comment">/* sinonim yang ditemukan */</span> },
      <span class="tok-key">"bm25"</span>: { <span class="tok-comment">/* kandidat & skor BM25 */</span> },
      <span class="tok-key">"sbert"</span>: { <span class="tok-comment">/* kandidat & cosine similarity */</span> },
      <span class="tok-key">"hybrid"</span>: { <span class="tok-comment">/* bobot & mode aktif */</span> }
    },
    <span class="tok-key">"recommendations"</span>: [
      {
        <span class="tok-key">"dosen"</span>: {
          <span class="tok-key">"nidn"</span>: <span class="tok-str">"0012345678"</span>,
          <span class="tok-key">"nama"</span>: <span class="tok-str">"Dr. Ahmad Farid, M.Kom"</span>,
          <span class="tok-key">"program_studi"</span>: <span class="tok-str">"Teknik Informatika"</span>,
          <span class="tok-key">"bidang_keahlian"</span>: <span class="tok-str">"Machine Learning, Computer Vision"</span>,
          <span class="tok-key">"jurnal"</span>: <span class="tok-str">"CNN for Plant Disease, ..."</span>,
          <span class="tok-key">"judul_bimbing"</span>: <span class="tok-str">"Deteksi Objek YOLO, ..."</span>
        },
        <span class="tok-key">"scores"</span>: {
          <span class="tok-key">"hybrid"</span>: <span class="tok-num">0.7821</span>,  <span class="tok-comment">// skor akhir</span>
          <span class="tok-key">"bm25"</span>: <span class="tok-num">0.6543</span>,    <span class="tok-comment">// skor leksikal (0–1)</span>
          <span class="tok-key">"sbert"</span>: <span class="tok-num">0.8712</span>   <span class="tok-comment">// cosine similarity (0–1)</span>
        },
        <span class="tok-key">"xai"</span>: {
          <span class="tok-key">"irisan_kata"</span>: [<span class="tok-str">"deep_learning"</span>, <span class="tok-str">"cnn"</span>, <span class="tok-str">"penyakit"</span>],
          <span class="tok-key">"topik_dosen"</span>: [<span class="tok-str">"image classification"</span>, <span class="tok-str">"neural network"</span>]
        }
      }
    ]
  }
}</code></pre>
        </section>

        <!-- Batch JSON -->
        <section id="batch">
          <h2>POST /rekomendasi/batch</h2>
          <p>
            Menjalankan pipeline rekomendasi untuk banyak data sekaligus melalui JSON payload.
            Cocok untuk integrasi programatik dengan sistem akademik.
          </p>

          <h3>Request Body</h3>
          <p>Array of objects. Setiap objek mewakili satu dokumen penelitian.</p>
          <div class="param-table">
            <table>
              <thead><tr><th>Field</th><th>Tipe</th><th>Wajib</th><th>Keterangan</th></tr></thead>
              <tbody>
                <tr><td><code>id</code></td><td>string</td><td>✓</td><td>Identifier unik dokumen (digunakan untuk mapping output)</td></tr>
                <tr><td><code>judul</code></td><td>string</td><td>✓*</td><td>Judul penelitian</td></tr>
                <tr><td><code>abstrak</code></td><td>string</td><td>—</td><td>Abstrak penelitian</td></tr>
              </tbody>
            </table>
          </div>

          <h3>Contoh Request</h3>
          <pre><code>curl -X POST http://localhost:5000/api/rekomendasi/batch \
  -H <span class="tok-str">"Content-Type: application/json"</span> \
  -d '[
    {
      <span class="tok-key">"id"</span>: <span class="tok-str">"MHS-001"</span>,
      <span class="tok-key">"judul"</span>: <span class="tok-str">"Sistem Deteksi Fraud Menggunakan Random Forest"</span>,
      <span class="tok-key">"abstrak"</span>: <span class="tok-str">"Penelitian ini mengimplementasikan algoritma..."</span>
    },
    {
      <span class="tok-key">"id"</span>: <span class="tok-str">"MHS-002"</span>,
      <span class="tok-key">"judul"</span>: <span class="tok-str">"Analisis Sentimen Ulasan Produk dengan BERT"</span>
    }
  ]'</code></pre>

          <h3>Contoh Response</h3>
          <pre><code>{
  <span class="tok-key">"status"</span>: <span class="tok-str">"success"</span>,
  <span class="tok-key">"data"</span>: [
    {
      <span class="tok-key">"id"</span>: <span class="tok-str">"MHS-001"</span>,
      <span class="tok-key">"judul"</span>: <span class="tok-str">"Sistem Deteksi Fraud..."</span>,
      <span class="tok-key">"rekomendasi"</span>: {
        <span class="tok-key">"metadata"</span>: { ... },
        <span class="tok-key">"recommendations"</span>: [ ... ]
      }
    }
  ]
}</code></pre>
        </section>

        <!-- Batch Upload -->
        <section id="batch-upload">
          <h2>POST /rekomendasi/batch/upload</h2>
          <p>
            Upload file Excel (<code>.xlsx</code>) untuk memproses banyak dokumen sekaligus.
            File harus mengandung kolom <code>id</code>, <code>judul</code>, dan opsional <code>abstrak</code>.
          </p>

          <h3>Content-Type</h3>
          <pre><code>Content-Type: <span class="tok-str">multipart/form-data</span></code></pre>

          <h3>Form Fields</h3>
          <div class="param-table">
            <table>
              <thead><tr><th>Field</th><th>Tipe</th><th>Keterangan</th></tr></thead>
              <tbody>
                <tr><td><code>file</code></td><td>File (.xlsx)</td><td>File Excel dengan kolom: id, judul, abstrak</td></tr>
              </tbody>
            </table>
          </div>

          <h3>Template Kolom Excel</h3>
          <div class="excel-preview">
            <table>
              <thead><tr><th>id</th><th>judul</th><th>abstrak</th></tr></thead>
              <tbody>
                <tr><td>MHS-001</td><td>Sistem Deteksi Fraud...</td><td>Penelitian ini...</td></tr>
                <tr><td>MHS-002</td><td>Analisis Sentimen...</td><td>(opsional)</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Config GET -->
        <section id="config-get">
          <h2>GET /config</h2>
          <p>Mengambil konfigurasi aktif mesin rekomendasi.</p>

          <h3>Response</h3>
          <pre><code>{
  <span class="tok-key">"status"</span>: <span class="tok-str">"success"</span>,
  <span class="tok-key">"data"</span>: {
    <span class="tok-key">"k_rank"</span>: <span class="tok-num">5</span>,                        <span class="tok-comment">// jumlah top-K dosen</span>
    <span class="tok-key">"threshold"</span>: <span class="tok-num">0.0</span>,                   <span class="tok-comment">// BM25 hard filter minimum</span>
    <span class="tok-key">"adaptive_alpha_threshold"</span>: <span class="tok-num">15</span>     <span class="tok-comment">// batas token keyword vs abstrak</span>
  }
}</code></pre>
        </section>

        <!-- Config PATCH -->
        <section id="config-patch">
          <h2>PATCH /config</h2>
          <p>Memperbarui konfigurasi mesin rekomendasi. Field yang tidak disertakan tidak akan berubah.</p>

          <h3>Request Body</h3>
          <div class="param-table">
            <table>
              <thead><tr><th>Parameter</th><th>Tipe</th><th>Keterangan</th></tr></thead>
              <tbody>
                <tr><td><code>k_rank</code></td><td>integer (1–20)</td><td>Jumlah rekomendasi top-K</td></tr>
                <tr><td><code>threshold</code></td><td>float (0.0–5.0)</td><td>Minimum skor BM25 mentah untuk hard filter</td></tr>
                <tr><td><code>adaptive_alpha_threshold</code></td><td>integer</td><td>Batas token untuk switch mode keyword/abstrak</td></tr>
              </tbody>
            </table>
          </div>
          <pre><code>curl -X PATCH http://localhost:5000/api/config \
  -H <span class="tok-str">"Content-Type: application/json"</span> \
  -d '{ <span class="tok-key">"k_rank"</span>: <span class="tok-num">10</span> }'</code></pre>
        </section>

        <!-- Status -->
        <section id="status">
          <h2>GET /status</h2>
          <p>Memeriksa status server dan apakah model AI (BM25 + SBERT) sudah selesai di-load ke memori.</p>

          <h3>Response</h3>
          <pre><code>{
  <span class="tok-key">"status"</span>: <span class="tok-str">"success"</span>,
  <span class="tok-key">"data"</span>: {
    <span class="tok-key">"cache_ready"</span>: <span class="tok-bool">true</span>,   <span class="tok-comment">// false = model masih loading</span>
    <span class="tok-key">"message"</span>: <span class="tok-str">"SiReDo v3 is running"</span>
  }
}</code></pre>
          <p>
            Gunakan endpoint ini sebagai <strong>health check</strong>. Tunggu hingga
            <code>cache_ready: true</code> sebelum mengirimkan request rekomendasi.
          </p>
        </section>

        <!-- Errors -->
        <section id="errors">
          <h2>Error Handling</h2>
          <p>SiReDo menggunakan HTTP status code standar. Semua error dikembalikan dalam format JSON.</p>

          <div class="info-table">
            <table>
              <thead><tr><th>Status Code</th><th>Arti</th><th>Penyebab Umum</th></tr></thead>
              <tbody>
                <tr><td><code>200</code></td><td>OK</td><td>Request berhasil</td></tr>
                <tr><td><code>400</code></td><td>Bad Request</td><td>Field wajib kosong, format JSON salah</td></tr>
                <tr><td><code>422</code></td><td>Unprocessable</td><td>Tipe data tidak valid (mis. k_rank bukan integer)</td></tr>
                <tr><td><code>500</code></td><td>Server Error</td><td>Model belum ready, error internal</td></tr>
              </tbody>
            </table>
          </div>

          <pre><code><span class="tok-comment">// Contoh error 400</span>
{
  <span class="tok-key">"status"</span>: <span class="tok-str">"error"</span>,
  <span class="tok-key">"message"</span>: <span class="tok-str">"Judul atau abstrak harus diisi"</span>
}</code></pre>
        </section>

      </div>
    </main>
  </div>
</template>

<style scoped>
/* Two-column layout: page TOC + main content */
.docs-layout {
  display: flex;
  min-height: 100svh;
  position: relative;
}

/* Page TOC */
.toc-sidebar {
  width: 200px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100svh;
  overflow-y: auto;
  border-right: 1px solid var(--border);
  padding: 2rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}
.toc-title {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  padding: 0 0.5rem;
  margin-bottom: 0.5rem;
}
.toc-nav { display: flex; flex-direction: column; gap: 1px; }
.toc-link {
  font-size: 0.825rem;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0.35rem 0.6rem;
  border-radius: var(--radius-sm);
  transition: background 0.12s, color 0.12s;
  line-height: 1.4;
}
.toc-link:hover { background: var(--bg-muted); color: var(--text-primary); }
.toc-link.active { background: var(--brand-light); color: var(--brand); font-weight: 600; }

/* Main content */
.docs-main {
  flex: 1;
  min-width: 0;
  padding: 3rem 2.5rem 5rem;
}
.docs-prose {
  max-width: var(--content-max);
}

/* Page header */
.page-header {
  margin-bottom: 0;
}
.page-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  font-family: var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--brand);
  background: var(--brand-light);
  border: 1px solid #c4b5fd;
  padding: 3px 10px;
  border-radius: 99px;
  margin-bottom: 1rem;
}
.page-lead {
  font-size: 1.05rem;
  color: var(--text-secondary);
  line-height: 1.75;
  margin-bottom: 1.5rem !important;
}
.base-url-box {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: #0f0f14;
  border-radius: var(--radius-lg);
  padding: 0.65rem 1.25rem;
  margin-bottom: 0.5rem;
}
.bu-label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #6b7280;
  font-family: var(--font-mono);
}
.bu-val {
  font-family: var(--font-mono);
  font-size: 0.88rem;
  color: #a6e3a1;
  background: none;
  border: none;
  padding: 0;
}

/* Tables */
.info-table, .param-table {
  margin: 1rem 0 1.5rem;
  overflow-x: auto;
}
.info-table table, .param-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}
.info-table th, .param-table th {
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  padding: 0.6rem 0.9rem;
  text-align: left;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-secondary);
}
.info-table td, .param-table td {
  border: 1px solid var(--border);
  padding: 0.6rem 0.9rem;
  color: var(--text-secondary);
  vertical-align: top;
  line-height: 1.5;
}
.info-table code, .param-table code {
  font-size: 0.8rem;
}

/* Excel preview */
.excel-preview {
  margin: 1rem 0 1.5rem;
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius);
}
.excel-preview table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.excel-preview th {
  background: #f0fdf4;
  color: var(--green);
  font-weight: 700;
  font-size: 0.75rem;
  border-bottom: 1px solid var(--green-border);
  padding: 0.5rem 0.85rem;
  text-align: left;
  font-family: var(--font-mono);
}
.excel-preview td {
  padding: 0.5rem 0.85rem;
  border-bottom: 1px solid var(--border);
  color: var(--text-secondary);
  font-size: 0.82rem;
}

/* HTTP Method badges */
.badge-post  { font-family: var(--font-mono); font-size: 0.7rem; font-weight: 700; padding: 2px 7px; border-radius: var(--radius-sm); background: var(--green-bg); color: var(--green); border: 1px solid var(--green-border); }
.badge-get   { font-family: var(--font-mono); font-size: 0.7rem; font-weight: 700; padding: 2px 7px; border-radius: var(--radius-sm); background: var(--blue-bg); color: var(--blue); border: 1px solid var(--blue-border); }
.badge-patch { font-family: var(--font-mono); font-size: 0.7rem; font-weight: 700; padding: 2px 7px; border-radius: var(--radius-sm); background: var(--amber-bg); color: var(--amber); border: 1px solid var(--amber-border); }

@media (max-width: 768px) {
  .toc-sidebar { display: none; }
  .docs-main { padding: 2rem 1.25rem 4rem; }
}
</style>
