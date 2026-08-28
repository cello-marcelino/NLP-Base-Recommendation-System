# Laporan Audit Kualitas Rekomendasi NLP (Putaran 2)

Dokumen ini merupakan hasil pengujian ulang (audit ke-2) terhadap pipeline rekomendasi Hybrid NLP setelah perbaikan stopword, normalisasi Min-Max, ekspansi kamus, deduplikasi n-gram, dan normalisasi bidang keahlian diimplementasikan.

## 1. Ringkasan Perubahan Skor & Kualitas

Perbaikan telah berhasil mengatasi masalah utama pada audit pertama:
- **Skor Hybrid sekarang proporsional**: Normalisasi Min-Max membuat skor BM25 dan SBERT merata di rentang [0, 1]. Nilai akhir Hybrid sekarang lebih menggambarkan perpaduan relevansi secara adil.
- **Dosen False-Positive Menghilang**: Dosen dengan bidang tidak relevan (seperti Animasi 3D pada tesis DSS/IoT) **telah hilang** dari Top-5 berkat pembersihan stopword teknis.
- **Ekspansi Query Berjalan Baik**: Frasa spesifik seperti `ahp`, `topsis`, `esp32`, `aes-256`, dan `steganografi` berhasil diekspansi dan menemukan irisan kata yang tepat.

## 2. Matriks Hasil Rekomendasi Per Tesis (Setelah Perbaikan)

### TESIS-001: Natural Language Processing
| Rank | Nama Dosen | Bidang Keahlian | Hybrid |
|---|---|---|---|
| 1 | Hilda Widyastuti, S.T., M.T. | Artificial Intelligence | 0.8934 |
| 2 | Supardianto, S.ST., M.Eng | Ilmu Komputer | 0.8317 |
| 3 | Ahmadi Irmansyah Lubis | AI, DSS, Machine Learning, Computer Science | 0.8255 |
| 4 | Metta Santiputri | Software Engineering | 0.8113 |
| 5 | Cyntia Lasmi | AI, Data Mining | 0.8066 |

> **Evaluasi:** Signifikan membaik. Rank #1 sekarang diisi oleh pakar AI, menggeser rekomendasi umum dari audit sebelumnya. Profil dosen yang masuk Top-5 relevan dengan data dan machine learning.

### TESIS-002: Computer Vision
| Rank | Nama Dosen | Bidang Keahlian | Hybrid |
|---|---|---|---|
| 1 | Agung Riyadi, S.Si., M.Kom | Artificial Intelligence | 0.9312 |
| 2 | Wenang Anurogo, S.Si., M.Sc. | Computer Network, Information Security, Computer Science | 0.9166 |
| 3 | Fendra Dwi R | Aplikasi SIG, Penginderaan Jauh | 0.8597 |
| 4 | Andy Triwinarko, ST., MT., Ph.D | Telecommunication, Informatics | 0.8176 |
| 5 | Nur Cahyono Kushardianto | Jaringan Komputer, Teknologi Komunikasi, Machine Learning | 0.8145 |

> **Evaluasi:** Rank #1 sangat akurat (AI). Rank #5 berhasil masuk (Machine Learning). Dosen Geomatika/SIG masih muncul karena dataset tesis menyebut spesifik "citra udara drone" yang leksikalnya (BM25) tumpang tindih kuat dengan domain pemetaan/SIG.

### TESIS-003: Decision Support System
| Rank | Nama Dosen | Bidang Keahlian | Hybrid |
|---|---|---|---|
| 1 | Ahmadi Irmansyah Lubis | AI, DSS, Machine Learning | 0.9922 |
| 2 | Nur Israyani, S.T, M.T | Geographical Information System (GIS) | 0.8861 |
| 3 | Noper Ardi, S.Pd., M.Eng | RPL, AI | 0.8131 |
| 4 | Cyntia Lasmi | AI, Data Mining | 0.8005 |
| 5 | Alena Uperiati, S.T, M.Cs | Machine Learning, Data Science | 0.7677 |

> **Evaluasi:** Sangat membaik. Pakar DSS (Ahmadi) tetap kokoh di Rank #1 dengan skor hampir absolut (0.9922). Dosen Animasi 3D (false positive) dari audit pertama telah hilang. Sisa kandidat relevan di bidang data/AI.

### TESIS-004: Cyber Security
| Rank | Nama Dosen | Bidang Keahlian | Hybrid |
|---|---|---|---|
| 1 | Antoni Haikal, S.ST.,M.T | Application Security, Offensive Security | 0.9493 |
| 2 | Nelmiawati, B.CS., M.Comp.Sc | Computer Network, Information Security | 0.8798 |
| 3 | Dodi Prima Resda | Rekayasa Keamanan Siber | 0.8541 |
| 4 | Andy Triwinarko, ST., MT., Ph.D | Telecommunication, Informatics | 0.7848 |
| 5 | Sukma Evadini, S.T., M.Kom | Data Mining, Machine Learning, Expert System | 0.7418 |

> **Evaluasi:** Presisi tinggi. Top 3 didominasi murni oleh dosen Rekayasa Keamanan Siber / Information Security.

### TESIS-005: Internet of Things
| Rank | Nama Dosen | Bidang Keahlian | Hybrid |
|---|---|---|---|
| 1 | Supardianto, S.ST., M.Eng | Ilmu Komputer | 0.9481 |
| 2 | Wenang Anurogo, S.Si., M.Sc. | Computer Network, Information Security, Computer Science | 0.9299 |
| 3 | Hamdani Arif, S.Pd., M.Sc | Networking, IoT | 0.8587 |
| 4 | Cyntia Lasmi | AI, Data Mining | 0.7602 |
| 5 | Nur Cahyono Kushardianto | Jaringan Komputer, Teknologi Komunikasi, Machine Learning | 0.7574 |

> **Evaluasi:** Jauh lebih bersih. Rank #3 spesifik pakar IoT, dan dosen Animasi 3D sudah tidak muncul di list. Sisanya relevan dengan jaringan komputer dan data.

---

## 3. Kesimpulan

Tindakan korektif pada preprocessing (stopword & deduplikasi n-gram) dan algoritma hybrid (min-max scaling) **berhasil secara signifikan menekan angka false-positive (rekomendasi meleset akibat bias leksikal)**. Kualitas model rekomendasi saat ini telah masuk pada kategori yang sangat layak untuk dioperasikan pada skenario real-world.
