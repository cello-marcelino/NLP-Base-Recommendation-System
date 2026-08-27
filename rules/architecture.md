---
description: Prinsip desain dan arsitektur, termasuk folder structure baku (Layered + Domain Grouping). Berlaku saat membuat atau mengubah struktur module, class, folder, atau layer.
---

# Architecture & Design Principles

## Gaya Arsitektur: Layered Architecture dengan Domain Grouping (Monolith-First, Microservice-Ready)

Multi-stack, dipakai lintas project. Level atas tetap layer-based (Controllers, Services, Repositories, Models) karena itu mental model yang paling nyaman, tapi di dalam tiap layer, file dikelompokkan per domain dengan penamaan folder yang konsisten. Jadi struktur luarnya layer-based, tapi batas antar domain tetap jelas sehingga gampang dipisah jadi microservice kapan pun perlu, tanpa harus redesign dari nol.

## Folder Structure

```
project-root/
├── app/                        # atau src/, sesuai konvensi stack
│   ├── Http/Controllers/
│   │   ├── Auth/
│   │   └── User/
│   ├── Services/
│   │   ├── Auth/
│   │   └── User/
│   ├── Repositories/
│   │   ├── Auth/
│   │   └── User/
│   ├── Models/
│   ├── Middleware/
│   ├── Exceptions/
│   └── Config/
├── tests/
│   ├── Unit/
│   ├── Integration/
│   └── Feature/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/workflows/
│   ├── test.yml
│   └── deploy.yml
├── docs/
│   ├── architecture-rules.md
│   └── api-spec/
├── .env.example
└── README.md
```

Tanggung jawab tiap folder:

| Folder | Tanggung jawab | Contoh (SIREDO) |
|---|---|---|
| `Http/Controllers/` | Terima request, validasi input dasar, panggil Service, return response. Tidak boleh ada business logic. | `RecommendationController`, endpoint `/recommend?query=...` yang panggil `RecommendationService` |
| `Services/` | Rumah business logic murni, jantung aplikasi. | `RecommendationService` sebagai orkestrator yang manggil `PreprocessingService`, `WeightingService`, `ScoringService` |
| `Repositories/` | Satu-satunya lapisan yang boleh akses database/storage langsung. Service tidak query DB sendiri. | `CacheRepository`, `LecturerRepository` |
| `Models/` | Representasi struktur data/entity, tempat definisi relasi kalau pakai ORM. | `LecturerProfile`, `Query`, `ScoreResult` |
| `Middleware/` | Proses request sebelum sampai controller, untuk cross-cutting concern (auth, rate limit, role). | Validasi API key dan rate limiting |
| `Exceptions/` | Custom exception class biar error handling konsisten. | `EmbeddingTimeoutException`, `InvalidQueryException` |
| `Config/` | Semua yang bisa berubah antar environment, dipisah dari kode. | Bobot hybrid scoring (0.57/0.43), threshold cache |
| `tests/Unit, Integration, Feature` | Dipisah berdasarkan kecepatan dan cakupan biar CI efisien. | Unit test formula scoring, integration test pipeline preprocessing sampai scoring |
| `docker/` | Containerize biar environment konsisten dev sampai production. | Persiapan deploy ke VPS |
| `.github/workflows/` | Automasi test dan deploy tiap push/PR. | Jalankan unit test scoring, build image, deploy VPS |
| `docs/` | Dokumentasi arsitektur dan API spec. | SRS, OpenAPI spec, file rules architecture ini sendiri |
| `.env.example` | Template environment variable tanpa expose secret asli. | API key, path model SBERT, cache TTL |

## Dependency Direction (Ketat)

Ini aturan paling penting untuk dijaga AI saat generate kode.

```
Controller -> Service -> Repository -> Model/Database
```

- Controller tidak boleh langsung akses Model/DB, wajib lewat Service
- Service baru boleh panggil Repository, tidak query DB langsung
- Repository tidak boleh menentukan business rules
- Service tidak boleh bergantung langsung pada HTTP response

## Domain Grouping

Penamaan folder domain (`Auth`, `User`, dst) harus sama persis di semua layer: `Controllers/Auth/`, `Services/Auth/`, `Repositories/Auth/`. Ini yang bikin satu domain gampang ditarik jadi microservice terpisah tanpa perlu redesign folder.

## Kontrak Antar Domain (DTO)

Antar layer dan antar domain wajib pakai DTO atau request/response schema, bukan pass array/object mentah. Ini juga jadi fondasi kalau nanti mau bikin OpenAPI spec.

## Dependency Injection

Konsisten di semua service. Laravel sudah native (constructor injection). Di Flask, pakai manual lewat factory pattern atau library seperti `dependency-injector`. Tujuannya supaya kode testable dan gampang di-mock.

## KISS (Keep It Simple, Stupid)
Gunakan solusi paling sederhana yang menyelesaikan masalah dengan benar.
- Jangan menambahkan abstraction tanpa kebutuhan nyata
- Jangan menggunakan design pattern hanya karena pattern tersebut tersedia
- Jangan memperkenalkan infrastructure kompleks sebelum diperlukan

## YAGNI (You Aren't Gonna Need It)
- Jangan implement feature yang belum dibutuhkan
- Jangan membuat generic abstraction untuk kebutuhan hipotetis
- Jangan melakukan optimization sebelum ada bottleneck yang terukur

## DRY (Don't Repeat Yourself)
- Hindari duplikasi business logic, harus ada Single Source of Truth
- Jangan abstraksi hanya karena dua kode terlihat mirip
- Kalau dua kode punya alasan perubahan yang berbeda, duplikasi bisa diterima

## Architecture Complexity Evolution
Gunakan architecture paling sederhana yang memenuhi kebutuhan saat ini, jangan melompati tahap tanpa alasan teknis:
```
Simple Application -> Modular Application -> Modular Monolith
-> Horizontal Scaling -> Service Extraction -> Microservices
```

## Architecture Decision Record (ADR)
Keputusan arsitektur yang sulit dibalik dan berdampak besar wajib didokumentasikan.
```
ADR-00X
Decision: keputusan apa yang diambil
Reason: kenapa keputusan ini dipilih
Rejected: opsi lain yang dipertimbangkan
Reason ditolak: kenapa opsi itu tidak dipilih
```
Gunakan skill `write-adr` untuk membuat ADR baru.

## Lampiran: Konvensi Penamaan per Stack

- **PHP/Laravel**: PascalCase untuk class dan folder domain (`AuthController`, `Services/Auth/`)
- **Python/Flask**: snake_case untuk file dan function (`weighting.py`, `scoring.py`), folder domain tetap konsisten penamaannya dengan layer lain
