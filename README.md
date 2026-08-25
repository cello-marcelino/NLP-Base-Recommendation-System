# SiReDo v3 — Sistem Rekomendasi Dosen

**SiReDo v3** adalah platform rekomendasi dosen pembimbing dan penguji berbasis **Hybrid Natural Language Processing (NLP)** yang menggabungkan pencarian leksikal (**BM25Okapi**) dan pencocokan semantik (**Sentence-BERT**), dilengkapi lapisan **Explainable AI (XAI)** berbasis **KeyBERT** dan irisan kata kunci.

Dibangun dengan arsitektur **Decoupled Fullstack**:
- **Backend (`server/`)**: Flask 3.0 REST API dengan **Feature-Module Architecture**, Z-Score Sigmoid Normalization, Hard Constraint Pruning, Adaptive Weighting, dan Dual Data Source (MySQL primary + Excel fallback).
- **Frontend (`web/`)**: Vue 3 SPA + Vite + Tailwind CSS 4 + **Pinia State Management** + Axios Interceptors.

---

## 🏛️ Arsitektur Sistem (Feature-Module Architecture)

```
siredo/
├── server/                       # Backend Flask REST API
│   ├── src/
│   │   ├── core/                 # Config, Database, Logging, Security, Response, Exceptions
│   │   ├── modules/
│   │   │   ├── dosen/            # Entity Model, MySQL & Excel Repository, Controller, Routes
│   │   │   ├── nlp/              # Preprocessor, BM25, SBERT, Hybrid Scorer, Stopwords, Kamus
│   │   │   ├── recommendation/   # Single & Batch Service, Controller, Routes, SSE Stream
│   │   │   └── system/           # Cache Singleton, Config Service, Status & Health Check
│   │   └── app.py                # Application Factory (CORS, Error Handlers, Blueprints)
│   ├── dataset/                  # Dataset profiles dosen (.xlsx)
│   ├── storage/                  # Runtime cache (.npy, .pkl, .json)
│   ├── tests/                    # Unit & Integration tests (pytest)
│   ├── requirements.txt          # Python dependencies (pinned)
│   ├── .env.example              # Environment variables template
│   └── run.py                    # Entry point server
│
├── web/                          # Frontend Vue 3 SPA
│   ├── src/
│   │   ├── assets/               # CSS styles, images, hero assets
│   │   ├── components/
│   │   │   ├── layout/           # Sidebar, ServerStatusBadge
│   │   │   └── recommendation/   # Stepper, DosenCard, XaiModal, PipelineLog, InputForm
│   │   ├── router/               # Vue Router 5 configuration
│   │   ├── services/             # Axios API client with interceptors
│   │   ├── stores/               # Pinia stores (system, recommendation, config)
│   │   └── views/                # Single, Batch, Dosen, Config, Preprocessing, Docs, Setup
│   ├── package.json              # Web dependencies (named siredo-web)
│   └── vite.config.js            # Vite configuration with API proxy
│
├── docs/                         # Dokumentasi Arsitektur, API, Setup
├── rules/                        # Aturan rekayasa software AI workflow
├── CHANGELOG.md                  # Catatan riwayat versi
└── README.md
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
cp .env.example .env

# Jalankan server
python run.py
```
Server akan aktif di `http://localhost:5000` dengan proses warm-up in-memory cache secara otomatis.

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
cd server
pytest tests/ -v
```

---

## 📖 Dokumentasi Lengkap
- [Arsitektur & Desain Sistem](docs/architecture.md)
- [Spesifikasi Kontrak REST API](docs/api.md)
- [Panduan Instalasi & Deployment](docs/setup.md)
