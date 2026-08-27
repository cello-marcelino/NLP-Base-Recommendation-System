# Panduan SiReDo CLI Framework

**SiReDo CLI** adalah antarmuka baris perintah (*Command Line Interface*) untuk mengelola siklus hidup server, operasi database relasional, migrasi skema, ekspor/impor dataset, pembersihan cache NLP, dan pemantauan log real-time pada sistem SiReDo.

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
Menjalankan API server backend SiReDo. Secara default, server berjalan sebagai background daemon (pada Windows menggunakan `pythonw.exe` tanpa jendela konsol tambahan) sehingga terminal langsung bebas digunakan. Server melakukan warm-up cache in-memory dan model Sentence-BERT/KeyBERT sebelum siap melayani request, serta mencatat Process ID ke `server/storage/data/siredo.pid`.

```powershell
# Menjalankan server di background (default: CPU, host: 0.0.0.0, port: 5000 dari .env)
python siredo serve

# Menjalankan dengan akselerasi GPU (CUDA)
python siredo serve --device cuda

# Menjalankan di foreground (blocking mode, output langsung terlihat)
python siredo serve --foreground

# Menjalankan pada host dan port kustom
python siredo serve --host 127.0.0.1 --port 8000

# Menjalankan dengan mode debug aktif
python siredo serve --debug
```


#### `reload`
Melakukan *hot reload* pada server yang sedang aktif tanpa perlu mematikan proses server. Perintah ini memperbarui konfigurasi runtime dan meregenerasi cache NLP di memori via endpoint terotentikasi `/api/system/reload`.

```powershell
python siredo reload

# Menargetkan host/port kustom
python siredo reload --host 127.0.0.1 --port 8000
```

#### `shutdown`
Menghentikan proses server SiReDo yang sedang berjalan secara aman (*graceful termination*) berdasarkan PID yang tercatat di `server/storage/data/siredo.pid`.

```powershell
python siredo shutdown
```

---

### B. Pemantauan Log Real-Time

#### `logs`
Menampilkan isi file log server (`server/storage/logs/siredo.log`) atau memantau aliran request log secara langsung (*live tailing*).

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
Menjalankan skrip migrasi berversi dari `server/database/migrations/` untuk membuat tabel relasional (`dosen`, `publikasi`, `riwayat_bimbingan`, `riwayat_pengujian`), indeks, dan konstrain foreign key (dengan tracking riwayat pada tabel `migrations`).

```powershell
python siredo db:migrate
```
*Driver database disesuaikan dengan konfigurasi `DB_DRIVER` di file `.env` (`sqlite` atau `mysql`).*

#### `db:seed`
Menjalankan database seeder dari `server/database/seeders/` untuk mengisi data awal dan inisialisasi konfigurasi sistem default (`config.json`).

```powershell
python siredo db:seed
```

#### `db:import`
Mengimpor dataset profil dosen dari file Excel (`dataset_profiles_terintegrasi.xlsx`) ke dalam 4 tabel database relasional via pipeline validasi `DosenImporter`.

```powershell
# Impor dataset default dari server/storage/data/dataset_profiles_terintegrasi.xlsx
python siredo db:import

# Impor dari file Excel kustom
python siredo db:import --file path/to/dataset.xlsx
```

#### `db:export`
Mengekspor seluruh data profil dosen beserta seluruh riwayat relasional dari database ke dalam file spreadsheet Excel (`.xlsx`) atau JSON.

```powershell
# Ekspor default ke server/storage/data/dataset_profiles_exported.xlsx
python siredo db:export

# Ekspor dalam format JSON
python siredo db:export --format json

# Menentukan lokasi output kustom
python siredo db:export --output backup_dataset.xlsx
```

#### `db:truncate` (alias `db:empty`)
Mengosongkan seluruh data pada tabel relasional (`riwayat_pengujian`, `riwayat_bimbingan`, `publikasi`, `dosen`) tanpa menghapus skema tabel.

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
Membersihkan file cache hasil komputasi embedding Sentence-BERT (`.npy`), ekstraksi topik KeyBERT (`.json`), dan serialisasi memori (`.pkl`) di direktori `server/storage/cache/`.

```powershell
python siredo cache:clear
```

---

## 3. Skenario Alur Kerja Umum

### Skenario Setup Awal Proyek
```powershell
# 1. Migrasi skema database
python siredo db:migrate

# 2. Inisialisasi konfigurasi seeder
python siredo db:seed

# 3. Impor dataset profil dosen
python siredo db:import

# 4. Jalankan server background
python siredo serve

# 5. Buka stream log (opsional)
python siredo logs -f
```

### Skenario Pembaruan Dataset & Refresh Cache
```powershell
# 1. Bersihkan cache embedding disk
python siredo cache:clear

# 2. Kosongkan data tabel database lama
python siredo db:truncate --force

# 3. Impor dataset baru
python siredo db:import --file path/to/new_dataset.xlsx

# 4. Hot reload server aktif
python siredo reload
```
