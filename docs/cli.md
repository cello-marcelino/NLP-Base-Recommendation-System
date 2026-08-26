# Dokumentasi SiReDo CLI Framework

**SiReDo CLI** adalah antarmuka baris perintah (*Command Line Interface*) untuk mengelola siklus hidup server, operasi database relasional, ekspor/impor data, pembersihan cache NLP, dan pemantauan log real-time pada sistem SiReDo.

---

## 1. Format Eksekusi

CLI dieksekusi langsung dari root direktori proyek menggunakan interpreter Python:

```powershell
python siredo <command> [options]
```

Untuk melihat bantuan dan daftar seluruh perintah yang tersedia:
```powershell
python siredo --help
```

---

## 2. Referensi Perintah Lengkap

### A. Manajemen Siklus Hidup Server

#### `serve`
Menjalankan API server backend SiReDo. Perintah ini otomatis melakukan *warm-up* cache memori & model Sentence-BERT/KeyBERT sebelum menerima *traffic*, serta mencatat Process ID (PID) ke `server/storage/data/siredo.pid`. Output terminal dijaga tetap bersih, sedangkan seluruh log request dicatat secara *real-time* ke `server/storage/logs/siredo.log`.

```powershell
# Menjalankan server default (host: 0.0.0.0, port: 5000 dari .env)
python siredo serve

# Menjalankan pada host dan port kustom
python siredo serve --host 127.0.0.1 --port 8000

# Menjalankan dengan mode debug aktif
python siredo serve --debug
```

#### `reload`
Melakukan *hot reload* pada server yang sedang aktif tanpa perlu mematikan proses server. Perintah ini memicu pembaruan konfigurasi runtime dan meregenerasi cache NLP di memori via authenticated endpoint `/api/system/reload`.

```powershell
python siredo reload

# Menargetkan host/port kustom
python siredo reload --host 127.0.0.1 --port 8000
```

#### `shutdown`
Menghentikan proses server SiReDo yang sedang berjalan secara aman (*graceful termination*) berdasarkan PID yang tersimpan di `siredo.pid`.

```powershell
python siredo shutdown
```

---

### B. Pemantauan Log Real-Time

#### `logs`
Menampilkan isi file log terdedikasi (`server/storage/logs/siredo.log`) atau memantau aliran log secara langsung (*live tailing*).

```powershell
# Melihat 30 baris log terakhir (default)
python siredo logs

# Melihat 100 baris log terakhir
python siredo logs -n 100

# Memantau aliran log secara real-time (live stream / tail -f)
python siredo logs -f

# Membersihkan isi file log
python siredo logs --clear
```

---

### C. Operasi Database

#### `db:migrate`
Menjalankan skrip migrasi DDL (*Data Definition Language*) untuk membuat database (jika belum ada) beserta seluruh tabel relasional (`dosen`, `publikasi`, `riwayat_bimbingan`, `riwayat_pengujian`), indeks, dan konstrain foreign key.

```powershell
python siredo db:migrate
```
*Driver yang digunakan disesuaikan dengan konfigurasi `DB_DRIVER` di file `.env` (`sqlite` atau `mysql`).*

#### `db:export`
Mengekspor seluruh data profil dosen beserta publikasi, riwayat bimbingan, dan riwayat pengujian dari database relasional ke dalam file dataset Excel (`.xlsx`) atau JSON.

```powershell
# Ekspor default ke server/storage/data/dataset_profiles_exported.xlsx
python siredo db:export

# Ekspor dalam format JSON
python siredo db:export --format json

# Menentukan lokasi file output kustom
python siredo db:export --output backup_dataset.xlsx
```

#### `db:import`
Mengimpor data master profil dosen dari file Excel (`dataset_profiles_terintegrasi.xlsx`) ke dalam 4 tabel database relasional.

```powershell
# Impor file dataset master default
python siredo db:import

# Impor dari file Excel kustom
python siredo db:import --file path/to/dataset.xlsx
```

#### `db:truncate` (alias `db:empty`)
Mengosongkan seluruh data pada tabel relasional (`riwayat_pengujian`, `riwayat_bimbingan`, `publikasi`, `dosen`) tanpa menghapus struktur skema tabel.

```powershell
# Mengosongkan data dengan konfirmasi keamanan interaktif
python siredo db:truncate

# Mengosongkan data langsung tanpa prompt
python siredo db:truncate --force
```

#### `db:drop`
Menghapus seluruh database MySQL atau menghapus file database SQLite di disk.

```powershell
# Menghapus database dengan konfirmasi keamanan interaktif
python siredo db:drop

# Menghapus database langsung tanpa prompt
python siredo db:drop --force
```

---

### D. Pembersihan Cache

#### `cache:clear`
Membersihkan file cache hasil pra-proses embedding Sentence-BERT (`.npy`) dan ekstraksi topik KeyBERT (`.json`) di direktori `server/storage/cache/`.

```powershell
python siredo cache:clear
```

---

## 3. Alur Kerja Pengembangan (Workflow Scenario)

### Skenario Inisialisasi Proyek Baru
```powershell
# 1. Migrasi database
python siredo db:migrate

# 2. Impor dataset master awal
python siredo db:import

# 3. Jalankan server
python siredo serve
```

### Skenario Pemantauan Log & Reset Data
```powershell
# Buka terminal kedua untuk live monitoring
python siredo logs -f

# Di terminal pertama jika ingin melakukan reset data
python siredo cache:clear
python siredo db:truncate --force
python siredo db:import
python siredo reload
```
