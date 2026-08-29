# Changelog & Task Breakdown: Audit Perbaikan Kualitas Rekomendasi NLP

Dokumen ini mencatat perbaikan yang dilakukan berdasarkan temuan pada `recommendation-quality-audit.md` (kecuali NIDN).

## Breakdown Task & Status

| Kategori | Task | Komponen | Status | Diff / Tindakan |
|---|---|---|---|---|
| **High** | 1. Tambahkan stopword akademik teknis | `stopwords.py` | Selesai | Menambahkan 12 kata generik ("menggunakan", "berbasis", "sistem", dll) ke dalam `STOPWORDS`. |
| **High** | 2. Normalisasi skala skor BM25 dan SBERT | `hybrid_scorer.py` | Selesai | Menambahkan fungsi `minmax()` sebelum perhitungan bobot akhir hibrida untuk memastikan rentang skor [0, 1] seimbang. |
| **High** | 3. Perkaya kamus ekspansi query | `kamus_ekspansi.py` | Selesai | Menambahkan key spesifik: "nlp", "sentence-bert", "bm25", "yolov8", "spk", "ahp", "topsis", "iot", "esp32", "aes-256", "steganografi". |
| **Medium**| 4. Deduplikasi token | `preprocessor.py` | Selesai | Menambahkan filtering `set()` pada output `preprocess_for_bm25` untuk mempertahankan urutan token unik. |
| **Medium**| 5. Aktifkan mode adaptif | `config.json` | Selesai | Mengubah runtime config `is_adaptive = True` via CLI script. |
| **Medium**| 6. Terapkan threshold minimum | `config.json` | Selesai | Mengubah runtime config `threshold = 0.3` via CLI script. |
| **Low** | 7. Normalisasi bidang keahlian | `dosen_importer.py` | Selesai | Menambahkan pemetaan (mapping) regex case-insensitive (misal: "kecerdasan buatan" -> "Artificial Intelligence") saat import data. |
| **Low** | 8. NIDN Data | Dataset | **Skipped** | Sesuai instruksi (exclude). |

## Detail Perubahan (Code Level)

1. **`server/src/services/nlp/stopwords.py`**:
   - Ditambahkan: `"menggunakan", "berbasis", "sistem", "rancang", "bangun", "metode", "informasi", "analisis", "penerapan", "implementasi", "studi", "kasus"`

2. **`server/src/services/nlp/hybrid_scorer.py`**:
   - Implementasi Min-Max scaling pada skor BM25 dan SBERT sebelum dikalikan `alpha` dan `beta` di fungsi `rank()`.

3. **`server/src/services/nlp/kamus_ekspansi.py`**:
   - Ekspansi key yang sebelumnya hanya phrase panjang menjadi term pendek yang lebih sering dicari (e.g., `ahp`, `topsis`, `iot`).

4. **`server/src/services/nlp/preprocessor.py`**:
   - Filter deduplikasi n-grams: `[x for x in ngrams if not (x in seen or seen.add(x))]`

5. **`server/database/importers/dosen_importer.py`**:
   - Kamus normalisasi: `norm_map = {"kecerdasan buatan": "Artificial Intelligence", ...}` di fungsi `validate_and_transform_row`.
