# Changelog — SiReDo

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
