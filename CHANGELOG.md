# Changelog — SiReDo

## [3.2.0] - 2026-09-02
### Added
- **Asynchronous Non-blocking Server Warmup**: Proses warm-up model AI (BM25 + SBERT + KeyBERT) kini dijalankan secara asinkron di *background thread* saat server *booting*, memungkinkan port HTTP `5000` segera melayani request status tanpa latency startup.
- **Granular 5-Stage Lifecycle Tracking**: Pelacakan status inisialisasi AI yang transparan dengan metrik durasi per-tahap (`loading_data`, `preprocessing`, `vektoring`, `embedding`, `persisting`).
- **Dynamic Clean Status Bar on Admin Dashboard**: Status server real-time yang ramping (*compact*) dan elegan dengan *pulsing indicator*, *progress bar* dinamis saat *warm-up/reloading*, serta tombol *sync engine*.
- **Integrated Live Demo on Landing Page**: Form simulasi rekomendasi langsung disematkan pada halaman utama (`HomeView.vue`) dengan *smooth scrolling* dan navigasi yang disederhanakan.
- **Vertical Timeline for Education History**: Parsing data riwayat pendidikan bertingkat (S1/S2/S3/Diploma) menjadi format *vertical timeline* yang rapi di modal penjelasan XAI (`XaiModal.vue`).

### Changed
- **CLI Encapsulation**: Memindahkan skrip CLI `siredo` ke dalam `server/siredo` dan memastikan seluruh resolusi path (`LOG_FILE`, `DB_SQLITE_PATH`, dll.) menggunakan *absolute path* berbasis `server/` direktori.
- **Monorepo Git Flow Cleanliness**: Menghapus file skrip dan dokumen temporer di root serta mengonsolidasi `.gitignore` utama.

## [3.1.0] - 2026-09-01
### Added
- **Hybrid Incremental Indexing**: Arsitektur pembaruan indeks NLP baru (BM25 + SBERT + KeyBERT) yang mempercepat operasi manipulasi data dosen dari ~315 detik menjadi ~1-3 detik. SBERT dan KeyBERT kini di-update per-record tanpa *full rebuild*. (Lihat: [siredo-hybrid-incremental-indexing.md](docs/changelog/siredo-hybrid-incremental-indexing.md)).
- **CRUD Lifecycle Integration Tests**: Penambahan test `test_admin_dosen_crud_full_lifecycle` dengan execution time 15 detik.

### Fixed
- **Stale SBERT Embedding Bug**: Perbaikan logika `encode_corpus` dimana sebelumnya pengeditan profil dosen tidak merubah embedding-nya di *cache*. 

## [3.0.0] - 2026-08-26
### Added
- **Feature-Module Architecture**: Restrukturisasi penuh backend menjadi modular domain (`modules/recommendation`, `modules/system`, `modules/dosen`, `modules/nlp`, `core`).
- **Pinia State Management**: Sentralisasi state reaktif pada frontend web (`useSystemStore`, `useRecommendationStore`, `useConfigStore`).
- **Automated Test Suite**: Unit & integration tests komprehensif menggunakan `pytest`.
- **CORS Whitelist & Security**: Pembatasan origin CORS dan otentikasi API Key admin pada endpoint sensitif.
- **Batch Size Limit**: Batasan maksimum 100 proposal per batch untuk mencegah risiko DoS.
- **Axios Interceptors**: Penanganan terpadu error server dan dynamic base URL pada frontend.
- **Decomposed Frontend Components**: Dekomposisi komponen besar `SingleRecommendationView` menjadi sub-komponen terfokus (`RecommendationInputForm`, `ProgressStepper`, `PipelineLogAccordion`, `DosenCard`, `XaiModal`).

### Fixed
- Perbaikan potensi RCE Werkzeug dengan memisahkan `APP_DEBUG` ke `.env` (default: false).
- Perbaikan bug SSE streaming generator yang sebelumnya tidak menerima request data.
- Perbaikan bug falsy override pada parameter `k_rank`.
- Perbaikan error logging MySQL yang sebelumnya tertelan tanpa notifikasi (`pass`).
- Perbaikan bare `except:` pada pembacaan konfigurasi JSON.
- Pinning seluruh versi dependensi pada `requirements.txt`.
- Standarisasi format REST API response tanpa versioning path sesuai `rules/api-design.md`.
