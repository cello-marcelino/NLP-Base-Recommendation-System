# SiReDo — Sistem Rekomendasi Dosen

SiReDo adalah aplikasi web untuk merekomendasikan dosen pembimbing berdasarkan judul dan abstrak rencana tugas akhir. Sistem membandingkan profil akademik serta rekam jejak penelitian dosen dengan input mahasiswa menggunakan pendekatan NLP hibrida: **BM25** untuk kecocokan kata dan **Sentence-BERT** untuk kemiripan makna.

## Ringkasan teknis

Alur utama aplikasi:

1. Data dosen dibaca dari MySQL. Jika MySQL tidak tersedia atau kosong, backend menggunakan `server/data/dataset_profiles_terintegrasi.xlsx` sebagai fallback.
2. Teks profil dosen diproses dengan stopword bahasa Indonesia, token unigram/bigram, dan kamus ekspansi istilah.
3. Backend membuat skor leksikal menggunakan Okapi BM25 dan skor semantik menggunakan cosine similarity dari embedding model `paraphrase-multilingual-MiniLM-L12-v2`.
4. KeyBERT mengekstrak frasa penting dari profil dosen.
5. Skor akhir dirangking dengan rumus hybrid:

   `skor akhir = (bobot lexical × skor BM25) + (bobot semantic × skor SBERT)`

6. Embedding dan hasil KeyBERT disimpan sebagai cache lokal di `server/data/`. Fingerprint MD5 digunakan untuk mendeteksi perubahan data dan memicu perhitungan ulang.

Model AI dimuat ketika Flask mulai berjalan. Pada proses pertama, model dapat mengunduh file dari Hugging Face dan melakukan komputasi cache sehingga startup lebih lama.

## Fitur

- Rekomendasi single berdasarkan judul dan abstrak.
- Rekomendasi batch melalui file `.xlsx`, `.xls`, atau `.csv`.
- Daftar dosen dengan pencarian, pagination, dan detail profil.
- Pengaturan bobot lexical dan semantic.
- Mode bobot adaptif jika bobot lexical dikirim sebagai nilai negatif.
- Endpoint status, refresh cache, daftar dosen, dan rekomendasi.

## Arsitektur dan struktur folder

```text
.
├── client/                 # Frontend Vue + Vite
│   ├── src/views/          # Halaman single, batch, dan daftar dosen
│   ├── src/services/api.js # Komunikasi ke backend
│   └── package.json
├── server/                 # Backend Flask dan mesin rekomendasi
│   ├── app.py              # REST API pada port 5050
│   ├── rekomendasi.py      # Pipeline NLP, ranking, dan cache AI
│   ├── database/           # Koneksi, query data, auth helper, migrasi
│   ├── utils/              # Stopword dan kamus ekspansi
│   ├── data/               # Dataset Excel dan cache AI
│   └── requirements.txt
└── testing/
    └── locustfile.py       # Skenario load test opsional
```

## Tools dan library

### Runtime dan tooling

- Python 3.10+ (disarankan 3.12), `venv`, dan `pip`
- Node.js 20+ dan npm
- Flask development server
- MySQL atau MariaDB; XAMPP dapat digunakan untuk menjalankan MySQL
- Git
- Locust untuk load testing opsional

### Backend

- Flask dan Flask-CORS — REST API dan akses lintas origin
- `mysql-connector-python` — koneksi MySQL
- pandas dan openpyxl — pembacaan dataset Excel
- NumPy dan SciPy — operasi matriks dan numerik
- `rank-bm25` — pencarian/ranking leksikal Okapi BM25
- `sentence-transformers`, Transformers, dan PyTorch — embedding Sentence-BERT
- KeyBERT — ekstraksi frasa kunci
- scikit-learn — cosine similarity
- NLTK — pembentukan n-gram
- Werkzeug — hashing password pada helper autentikasi
- Flask-JWT-Extended tersedia di requirements, tetapi route login/JWT belum diimplementasikan pada API saat ini

### Frontend

- Vue 3 — framework UI
- Vue Router — navigasi `/`, `/batch`, dan `/dosen`
- Vite — development server dan build
- Tailwind CSS 4 dengan `@tailwindcss/vite` — styling
- SheetJS (`xlsx`) — membaca dan mengekspor file spreadsheet batch
- Fetch API — komunikasi frontend ke backend

## Prasyarat database

Repo belum menyediakan file schema SQL. Buat database dan tabel berikut sebelum menjalankan migrasi. Perintah di bawah ditujukan untuk PowerShell dengan MySQL CLI tersedia di `PATH`. Jika password root kosong, hilangkan opsi `-p`.

```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS db_siredo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

mysql -u root -p db_siredo -e "CREATE TABLE IF NOT EXISTS dosen (id INT AUTO_INCREMENT PRIMARY KEY, nidn VARCHAR(30) NULL, nama TEXT NOT NULL, program_studi TEXT NOT NULL, bidang_keahlian LONGTEXT, jurnal LONGTEXT, judul_bimbing LONGTEXT, judul_uji LONGTEXT, riwayat_pendidikan LONGTEXT);"

# Tabel ini hanya diperlukan jika helper AuthLayer akan dikembangkan menjadi fitur login.
mysql -u root -p db_siredo -e "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL, role VARCHAR(30) NOT NULL DEFAULT 'mahasiswa');"
```

Konfigurasi koneksi saat ini berada langsung di `server/database/config.py`:

```python
host = localhost
user = root
password = ''
database = db_siredo
```

Sesuaikan file tersebut jika konfigurasi MySQL lokal berbeda. Untuk deployment, pindahkan kredensial ke environment variable.

## Menjalankan backend

Buka PowerShell pertama:

```powershell
cd "C:\Users\USER\Desktop\Semester 4\PBL\NLP-Base-Recommendation-System\server"

py -3 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Jalankan setelah database dan tabel dosen tersedia.
python .\database\migrate.py

# Menyalakan API pada http://127.0.0.1:5050
python .\app.py
```

`migrate.py` membaca dataset Excel, mengosongkan tabel `dosen`, lalu mengisinya kembali. Jalankan ulang migrasi hanya jika memang ingin mengganti isi tabel dari Excel.

Saat backend aktif, cek status mesin AI dari PowerShell kedua:

```powershell
Invoke-RestMethod http://127.0.0.1:5050/api/status
Invoke-RestMethod http://127.0.0.1:5050/api/dosen
```

Tunggu sampai field `ready` bernilai `True` sebelum mengirim rekomendasi. Pengujian rekomendasi yang tersedia:

```powershell
cd "C:\Users\USER\Desktop\Semester 4\PBL\NLP-Base-Recommendation-System\server"
\.venv\Scripts\Activate.ps1
python .\api_test.py
```

## Menjalankan frontend

Buka PowerShell baru dan biarkan backend tetap berjalan:

```powershell
cd "C:\Users\USER\Desktop\Semester 4\PBL\NLP-Base-Recommendation-System\client"

npm ci
npm run dev -- --host 127.0.0.1
```

Buka URL yang ditampilkan Vite, biasanya `http://127.0.0.1:5173`. Frontend saat ini mengarah langsung ke `http://127.0.0.1:5050/api` melalui `client/src/services/api.js`.

Untuk verifikasi build production:

```powershell
npm run build
npm run preview
```

## API utama

| Method | Endpoint | Fungsi |
|---|---|---|
| `GET` | `/api/status` | Status warming-up dan kesiapan mesin AI |
| `GET` | `/api/dosen` | Mengambil seluruh data dosen |
| `POST` | `/api/rekomendasi` | Menghasilkan ranking rekomendasi |
| `POST` | `/api/refresh` | Menghitung ulang cache dari data MySQL |

Contoh request rekomendasi:

```powershell
$body = @{ judul = 'Sistem informasi geografis pemetaan banjir'; abstrak = 'Pemetaan daerah rawan banjir menggunakan data spasial'; k = 3; bobot_lexical = 0.4; bobot_semantic = 0.6 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5050/api/rekomendasi -ContentType 'application/json' -Body $body
```

## Load test opsional

`locustfile.py` tidak termasuk dalam `server/requirements.txt`, sehingga instalasikan secara terpisah:

```powershell
cd "C:\Users\USER\Desktop\Semester 4\PBL\NLP-Base-Recommendation-System"
server\.venv\Scripts\Activate.ps1
python -m pip install locust
locust -f .\testing\locustfile.py --host http://127.0.0.1:5050
```

Buka `http://localhost:8089` untuk mengatur jumlah user dan durasi pengujian.

## Catatan pengembangan

- `server/data/vektor_dosen.npy`, file fingerprint, dan `keybert_dosen.json` adalah cache yang dibuat otomatis dan diabaikan Git.
- Endpoint `/api/refresh` hanya mengambil data dari MySQL; jika MySQL tidak aktif, gunakan migrasi atau restart backend agar fallback Excel dipakai.
- `server/database/auth.py` hanya berisi helper register/login dan belum dipanggil oleh route Flask maupun frontend.
- Flask dijalankan dengan `debug=True`; gunakan WSGI server dan konfigurasi keamanan tambahan untuk production.
