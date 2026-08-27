# Spesifikasi Desain & Kontrak API — SiReDo v3

Dokumentasi ini mendefinisikan standar kontrak RESTful API untuk platform SiReDo v3 sesuai dengan pedoman `rules/api-design.md`. Seluruh endpoint menggunakan format JSON standar tanpa versioning pada path URL (`/api/*`).

---

## 1. Standar Respon (Response Envelope)

Semua endpoint menghasilkan struktur respon seragam dengan properti `success`, `message`, `data`, dan `error`.

### Respon Sukses (2xx)
```json
{
  "success": true,
  "message": "Deskripsi hasil operasi",
  "data": { ... },
  "meta": { ... }
}
```

### Respon Error (4xx / 5xx)
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Pesan deskriptif penyebab kesalahan",
    "details": { ... }
  }
}
```

### Klasifikasi Error Code
| Error Code | HTTP Status | Keterangan |
|---|---|---|
| `VALIDATION_ERROR` | `400` | Input payload tidak valid atau field wajib kosong |
| `BATCH_LIMIT_EXCEEDED` | `400` | Jumlah batch proposal melebihi `MAX_BATCH_SIZE` |
| `UNAUTHENTICATED` | `401` | Header `X-API-Key` atau `Authorization` hilang atau salah |
| `PERMISSION_DENIED` | `403` | Akses ditolak |
| `NOT_FOUND` | `404` | Endpoint atau resource data tidak ditemukan |
| `METHOD_NOT_ALLOWED` | `405` | HTTP Method tidak didukung pada endpoint tersebut |
| `PAYLOAD_TOO_LARGE` | `413` | Ukuran payload atau file unggahan melebihi batas |
| `SERVICE_UNAVAILABLE` | `503` | Model NLP sedang dalam proses warm-up inisialisasi |
| `INTERNAL_SERVER_ERROR` | `500` | Kesalahan tidak terduga pada server |

---

## 2. Header & Autentikasi

- `Content-Type: application/json` untuk seluruh request body JSON.
- `X-Request-ID`: ID penelusuran request unik (otomatis di-generate jika tidak disertakan).
- `X-API-Key` atau `Authorization: Bearer <ADMIN_API_KEY>` untuk endpoint terproteksi sistem.

---

## 3. Daftar Endpoint Lengkap

### A. Layanan Sistem & Monitoring

#### 1. Health Check
- **Endpoint**: `GET /health`
- **Autentikasi**: Publik
- **Respon 200 (Ready)**:
  ```json
  {
    "success": true,
    "message": "Health check",
    "data": {
      "status": "healthy",
      "cache_ready": true
    }
  }
  ```
- **Respon 503 (Warming Up)**:
  ```json
  {
    "success": true,
    "message": "Health check",
    "data": {
      "status": "warming_up",
      "cache_ready": false
    }
  }
  ```

#### 2. Status Server
- **Endpoint**: `GET /api/system/status`
- **Autentikasi**: Publik
- **Respon 200**:
  ```json
  {
    "success": true,
    "message": "Sistem beroperasi normal",
    "data": {
      "status": "online",
      "app_name": "SiReDo",
      "environment": "development",
      "cache_ready": true,
      "total_dosen": 86
    }
  }
  ```

#### 3. Ambil Konfigurasi Runtime
- **Endpoint**: `GET /api/system/config`
- **Autentikasi**: Publik
- **Respon 200**:
  ```json
  {
    "success": true,
    "message": "Konfigurasi sistem berhasil diambil",
    "data": {
      "threshold": 0.0,
      "adaptive_alpha_threshold": 15,
      "is_adaptive": true,
      "manual_alpha": 0.7
    }
  }
  ```

#### 4. Perbarui Konfigurasi Runtime
- **Endpoint**: `PATCH /api/system/config` (atau `PUT /api/system/config`)
- **Autentikasi**: Memerlukan `X-API-Key`
- **Request Body**:
  ```json
  {
    "is_adaptive": false,
    "manual_alpha": 0.65,
    "threshold": 0.10
  }
  ```
- **Respon 200**:
  ```json
  {
    "success": true,
    "message": "Konfigurasi sistem berhasil diperbarui",
    "data": {
      "threshold": 0.10,
      "adaptive_alpha_threshold": 15,
      "is_adaptive": false,
      "manual_alpha": 0.65
    }
  }
  ```

#### 5. Hot Reload Sistem & Cache NLP
- **Endpoint**: `POST /api/system/reload`
- **Autentikasi**: Memerlukan `X-API-Key`
- **Respon 200**:
  ```json
  {
    "success": true,
    "message": "Sistem dan cache berhasil dimuat ulang (reloaded)",
    "data": {
      "cache_ready": true,
      "total_dosen": 86
    }
  }
  ```

---

### B. Layanan Data Dosen

#### 1. Daftar Seluruh Profil Dosen
- **Endpoint**: `GET /api/dosen`
- **Autentikasi**: Publik
- **Respon 200**:
  ```json
  {
    "success": true,
    "message": "Data dosen berhasil diambil",
    "meta": {
      "total": 86
    },
    "data": [
      {
        "nidn": "0001028301",
        "nama": "Dr. Ir. Contoh Dosen, M.Kom.",
        "program_studi": "Teknik Informatika",
        "bidang_keahlian": "Natural Language Processing, Machine Learning",
        "jurnal": "\"Analisis Sentimen Twitter\", \"Text Classification BERT\"",
        "judul_bimbing": "\"Sistem Temu Balik Informasi\", \"Chatbot FAQ\"",
        "judul_uji": "\"Klasifikasi Berita Hoaks\"",
        "pendidikan": "S3 Ilmu Komputer"
      }
    ]
  }
  ```

---

### C. Layanan Rekomendasi NLP

#### 1. Rekomendasi Single Proposal
- **Endpoint**: `POST /api/recommendations` (alias `/api/recommendations/single`)
- **Autentikasi**: Publik
- **Request Body**:
  ```json
  {
    "judul": "Analisis Sentimen Ulasan Pengguna Menggunakan Model BERT Multilingual",
    "abstrak": "Penelitian ini mengimplementasikan ekstraksi fitur teks berbasis Sentence-BERT untuk klasifikasi opini.",
    "k_rank": 5
  }
  ```
- **Respon 200**:
  ```json
  {
    "success": true,
    "message": "Rekomendasi berhasil dibuat",
    "data": {
      "metadata": {
        "alpha": 0.35,
        "beta": 0.65,
        "num_query_tokens": 18,
        "k_rank": 5,
        "threshold": 0.0,
        "mode": "abstrak"
      },
      "pipeline": {
        "preprocessing": {
          "raw_query": "Analisis Sentimen Ulasan Pengguna Menggunakan Model BERT Multilingual ...",
          "total_tokens": 18
        },
        "ekspansi": {
          "log": {
            "bert": "transformer embedding"
          },
          "num_frasa_ditemukan": 1
        },
        "bm25": {
          "num_candidates": 12,
          "num_total_dosen": 86
        },
        "sbert": {
          "num_computed": 12
        }
      },
      "recommendations": [
        {
          "rank": 1,
          "dosen": {
            "nidn": "0001028301",
            "nama": "Dr. Ir. Contoh Dosen, M.Kom.",
            "program_studi": "Teknik Informatika",
            "bidang_keahlian": "Natural Language Processing, Machine Learning",
            "pendidikan": "S3 Ilmu Komputer"
          },
          "scores": {
            "hybrid": 0.8421,
            "bm25": 0.7915,
            "sbert": 0.8693
          },
          "xai": {
            "irisan_kata": ["analisis", "bert", "model", "sentimen"],
            "topik_dosen": ["natural language processing", "bert", "text mining"]
          }
        }
      ]
    }
  }
  ```

#### 2. Rekomendasi Batch Proposal
- **Endpoint**: `POST /api/recommendations/batch`
- **Autentikasi**: Publik
- **Request Body**:
  ```json
  {
    "k_rank": 2,
    "proposals": [
      {
        "id": "P01",
        "judul": "Deteksi Objek YOLO pada Citra Drone",
        "abstrak": "Pengolahan citra digital untuk identifikasi kendaraan."
      },
      {
        "id": "P02",
        "judul": "Sistem Pendukung Keputusan Pemilihan Vendor Metode AHP",
        "abstrak": "Penerapan metode AHP dan TOPSIS dalam multi-criteria decision making."
      }
    ]
  }
  ```
- **Respon 200**:
  ```json
  {
    "success": true,
    "message": "Batch rekomendasi berhasil diproses",
    "meta": {
      "total_processed": 2
    },
    "data": [
      {
        "id": "P01",
        "judul": "Deteksi Objek YOLO pada Citra Drone",
        "rekomendasi": { ... }
      },
      {
        "id": "P02",
        "judul": "Sistem Pendukung Keputusan Pemilihan Vendor Metode AHP",
        "rekomendasi": { ... }
      }
    ]
  }
  ```

#### 3. Upload File Excel Batch Rekomendasi
- **Endpoint**: `POST /api/recommendations/upload`
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: File spreadsheet `.xlsx` atau `.xls` (kolom: `id`, `judul`, `abstrak`).
  - `k_rank` (opsional): Jumlah rekomendasi per proposal.
- **Respon 200**: Struktur data identik dengan endpoint batch.

#### 4. Streaming Real-Time Rekomendasi (Server-Sent Events)
- **Endpoint**: `POST /api/recommendations/stream`
- **Header Respon**: `Content-Type: text/event-stream`
- **Aliran Event SSE**:
  ```
  data: {"step": 1, "message": "Memulai Text Preprocessing & Cleaning"}

  data: {"step": 2, "message": "Melakukan Ekspansi Sinonim Ontologi"}

  data: {"step": 3, "message": "Kalkulasi Skor Leksikal BM25"}

  data: {"step": 4, "message": "Kalkulasi Skor Semantik Sentence-BERT"}

  data: {"step": 5, "message": "Hybrid Ranking & XAI Selesai", "result": { ... }}
  ```
