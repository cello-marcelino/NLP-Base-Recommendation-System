# SiReDo v3 — Sistem Rekomendasi Dosen

SiReDo v3 adalah platform rekomendasi dosen pembimbing dan penguji berbasis Hybrid Natural Language Processing (NLP) yang menggabungkan pencarian leksikal (BM25Okapi) dan pencocokan semantik (Sentence-BERT), dilengkapi lapisan Explainable AI (XAI) berbasis KeyBERT dan irisan kata kunci.

Dibangun dengan arsitektur Decoupled Fullstack:
- Backend (`server/`): Flask 3.0 REST API dengan Layered Architecture + Domain Grouping, Z-Score Sigmoid Normalization, Hard Constraint Pruning, Adaptive Weighting, skema database relasional (SQLite/MySQL), dan SiReDo CLI Framework.
- Frontend (`web/`): Vue 3 SPA + Vite + Tailwind CSS 4 + Pinia State Management + Axios Interceptors.

---

## Arsitektur Sistem (Layered Architecture with Domain Grouping)

```
siredo/
├── server/                       # Backend Flask REST API
│   ├── siredo                    # Entrypoint SiReDo CLI (python siredo <cmd>)
│   ├── .env                      # File konfigurasi environment backend
│   ├── .env.example              # Template konfigurasi environment
│   ├── src/
│   │   ├── controllers/          # Presentation Layer: Controller HTTP
│   │   ├── routes/               # Routing Layer: Definisi Blueprint & Endpoint
│   │   ├── services/             # Business Logic Layer: Service & Engine
│   │   ├── repositories/         # Data Access Layer: Composite SQL Repository
│   │   ├── models/               # Domain Models & Data Structures
│   │   ├── dtos/                 # Kontrak DTO Antar Layer
│   │   ├── middleware/           # Security & Structured Logging Middleware
│   │   ├── exceptions/           # Custom Application Exceptions
│   │   ├── config/               # App Configuration, Logger, Response Formatter
│   │   ├── cli/                  # SiReDo CLI Modules (serve, reload, shutdown, db, cache)
│   │   └── app.py                # Application Factory (CORS, Error Handlers, Blueprints)
│   ├── database/                 # Database Tooling & Lifecycle Management
│   │   ├── connection/           # Database connection & lifecycle
│   │   ├── migrations/           # Versioned schema migrations & runner
│   │   ├── seeders/              # Initial reference & static data seeders
│   │   ├── factories/            # Dummy & mock data factories for testing
│   │   └── importers/            # Excel dataset import pipeline
│   ├── storage/                  # Runtime storage (data SQLite, dataset, cache, logs)
│   │   ├── cache/                # Disk embeddings (.npy, .json, .pkl)
│   │   ├── data/                 # SQLite DB, Master Dataset Excel (.xlsx), config.json
│   │   └── logs/                 # Dedicated rotating log file (siredo.log)
│   ├── tests/                    # Feature, Integration, and Unit tests (pytest)
│   └── requirements.txt          # Python dependencies (pinned)
│
├── web/                          # Frontend Vue 3 SPA
│   ├── src/
│   │   ├── assets/               # CSS styles, design tokens
│   │   ├── components/           # Stepper, DosenCard, XaiModal, PipelineLog, InputForm
│   │   ├── router/               # Vue Router configuration
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

## SiReDo CLI Framework

SiReDo dilengkapi CLI mandiri di dalam folder `server/` untuk mempermudah operasional dan development:

```powershell
# Dari dalam direktori server/
python siredo serve                 # Menjalankan API server (background by default)
python siredo serve --foreground    # Menjalankan API server (foreground / blocking)
python siredo reload                # Hot reload NLP cache pada server aktif
python siredo shutdown              # Menghentikan server yang sedang aktif
python siredo logs -f               # Memantau aliran file log secara live
python siredo db:migrate            # Migrasi skema database relasional
python siredo db:seed               # Menjalankan seeder data awal / konfigurasi statis
python siredo db:export             # Ekspor database ke file Excel (.xlsx)
python siredo db:import             # Impor dataset Excel ke database relasional
python siredo db:truncate           # Mengosongkan data tabel database
python siredo db:drop               # Menghapus seluruh database
python siredo cache:clear           # Bersihkan file cache embedding disk
```

---

## Quick Start

### 1. Backend Setup (`server/`)
```bash
cd server
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env

# Inisialisasi Database & Jalankan Server via CLI
python siredo db:migrate
python siredo db:import
python siredo serve
```
Server aktif di `http://localhost:5055` dengan proses warm-up in-memory cache secara otomatis.

### 2. Frontend Setup (`web/`)
```bash
cd web
npm install
npm run dev
```
Buka browser di `http://localhost:5173`.

---

## Menjalankan Automated Tests
```bash
& "server/.venv/Scripts/pytest.exe" server/tests/ -v
```

---

## Dokumentasi Lengkap
- [Dokumentasi SiReDo CLI](docs/cli.md)
- [Arsitektur & Desain Sistem](docs/architecture.md)
- [Desain Sistem & Alur Kerja (System Flow)](docs/system-design.md)
- [Pipeline Hybrid NLP & XAI](docs/nlp-pipeline.md)
- [Arsitektur Caching Layer](docs/caching.md)
- [Akselerasi Hardware (GPU & CPU)](docs/hardware-acceleration.md)
- [Spesifikasi Kontrak REST API](docs/api.md)
- [Desain Database & Tooling](docs/database.md)
- [Strategi & Lapisan Pengujian](docs/testing.md)






