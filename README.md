# SiReDo v3 — Sistem Rekomendasi Dosen

**SiReDo v3** adalah platform rekomendasi dosen pembimbing dan penguji berbasis **Hybrid Natural Language Processing (NLP)** yang menggabungkan pencarian leksikal (**BM25Okapi**) dan pencocokan semantik (**Sentence-BERT**), dilengkapi lapisan **Explainable AI (XAI)** berbasis **KeyBERT** dan irisan kata kunci.

Dibangun dengan arsitektur **Decoupled Fullstack**:
- **Backend (`server/`)**: Flask 3.0 REST API dengan **Feature-Module Architecture**, Z-Score Sigmoid Normalization, Hard Constraint Pruning, Adaptive Weighting, skema database relasional (SQLite/MySQL), dan **SiReDo CLI Framework**.
- **Frontend (`web/`)**: Vue 3 SPA + Vite + Tailwind CSS 4 + **Pinia State Management** + Axios Interceptors.

---

## 🏛️ Arsitektur Sistem (Feature-Module Architecture)

```
siredo/
├── siredo                        # Entrypoint SiReDo CLI (python siredo <cmd>)
├── .env                          # File konfigurasi environment utama
├── .env.example                  # Template konfigurasi environment
├── server/                       # Backend Flask REST API
│   ├── src/
│   │   ├── core/                 # Config, Database, Logging, Security, Response, Exceptions
│   │   ├── cli/                  # SiReDo CLI Modules (serve, reload, shutdown, db, cache)
│   │   ├── modules/
│   │   │   ├── dosen/            # Entity Model, Composite SQL Repository, Controller, Routes
│   │   │   ├── nlp/              # Preprocessor, BM25, SBERT, Hybrid Scorer, Stopwords, Kamus
│   │   │   ├── recommendation/   # Single & Batch Service, Controller, Routes
│   │   │   └── system/           # Cache Singleton, Config Service, Status & Health Check
│   │   └── app.py                # Application Factory (CORS, Error Handlers, Blueprints)
│   ├── dataset/                  # Dataset profiles dosen (.xlsx)
│   ├── storage/                  # Runtime cache & data SQLite
│   ├── tests/                    # Unit & Integration tests (pytest)
│   ├── requirements.txt          # Python dependencies (pinned)
│   └── run.py                    # Legacy entry point server
│
├── web/                          # Frontend Vue 3 SPA
│   ├── src/
│   │   ├── assets/               # CSS styles, design tokens
│   │   ├── components/           # Stepper, DosenCard, XaiModal, PipelineLog, InputForm
│   │   ├── router/               # Vue Router 5 configuration
│   │   ├── services/             # Axios API client with interceptors
│   │   ├── stores/               # Pinia stores (system, recommendation, config)
│   │   └── views/                # Single, Batch, Dosen, Config, Preprocessing, Docs, Setup
│   ├── package.json              # Web dependencies
│   └── vite.config.js            # Vite configuration with API proxy
│
├── docs/                         # Dokumentasi Arsitektur, CLI, API, Setup
├── rules/                        # Aturan rekayasa software AI workflow
└── README.md
```

---

## 🛠️ SiReDo CLI Framework

SiReDo dilengkapi CLI mandiri untuk mempermudah operasional dan development:

```powershell
python siredo serve                 # Menjalankan API server
python siredo reload                # Hot reload NLP cache pada server aktif
python siredo shutdown              # Menghentikan server yang sedang aktif
python siredo db:migrate            # Migrasi skema database relasional
python siredo db:export             # Ekspor database ke file Excel (.xlsx)
python siredo db:import             # Impor dataset Excel ke database relasional
python siredo db:truncate           # Mengosongkan data tabel database
python siredo db:drop               # Menghapus seluruh database
python siredo cache:clear           # Bersihkan file cache embedding disk
```

---

## 🚀 Quick Start

### 1. Backend Setup (`server/`)
```bash
cd server
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
cd ..
copy .env.example .env

# Inisialisasi Database & Jalankan Server via CLI
python siredo db:migrate
python siredo db:import
python siredo serve
```
Server aktif di `http://localhost:5000` dengan proses warm-up in-memory cache secara otomatis.

### 2. Frontend Setup (`web/`)
```bash
cd web
npm install
npm run dev
```
Buka browser di `http://localhost:5173`.

---

## 🧪 Menjalankan Automated Tests
```bash
& "server/.venv/Scripts/pytest.exe" server/tests/ -v
```

---

## 📖 Dokumentasi Lengkap
- [Dokumentasi SiReDo CLI](docs/cli.md)
- [Arsitektur & Desain Sistem](docs/architecture.md)
- [Spesifikasi Kontrak REST API](docs/api.md)
- [Panduan Instalasi & Deployment](docs/setup.md)
