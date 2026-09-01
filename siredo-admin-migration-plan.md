# Implementation Plan: SiReDo Admin Portal & Engine Config Migration

## Goal Description
Tujuan dari rencana ini adalah melakukan restrukturisasi arsitektur SiReDo dengan memisahkan portal publik (**Public Portal**) dan portal administrasi (**SiReDo Admin Portal**). 

1. **Public Portal (`web/`)**: Difokuskan secara murni sebagai pusat dokumentasi API, penjelasan pipeline preprocessing NLP, dan simulasi rekomendasi skripsi tunggal (*Single Recommendation*). Fitur *Batch Recommendation*, *Data Dosen*, dan *Konfigurasi NLP Engine* akan **dihapus** dari menu/halaman publik.
2. **SiReDo Admin Portal (`/admin`)**: Portal khusus pengelola data dan konfigurasi sistem dengan tema visual **Teal Green** yang elegan. Memiliki sistem otentikasi admin terpisah (menggunakan tabel `admins` di database).
3. **Penyimpanan Konfigurasi Engine di Database**: Membuat tabel `engine_configs` di database untuk menyimpan parameter runtime engine (tanpa menggunakan `.env`). Parameter default di-hardcode di service fallback berdasarkan hasil optimasi changelog (`threshold=0.3`, `is_adaptive=true`, `adaptive_alpha_threshold=15`, `manual_alpha=0.7`).
4. **Peringatan Validasi Frontend**: Menambahkan modal/banner peringatan pada UI Admin Konfigurasi untuk mengingatkan admin mengenai dampak perubahan parameter terhadap kualitas normalisasi rekomendasi.

---

## ⚠️ User Review Required

> [!IMPORTANT]
> **Pemisahan Akses & Keamanan:**
> - Seluruh endpoint pengolahan data dan konfigurasi admin akan dipindahkan ke prefix `/api/admin/*` dan dilindungi oleh Token/Header Otorisasi Admin.
> - Data login default admin awal akan di-seed: Username: `admin`, Password: `admin123`.

> [!NOTE]
> **Skema Warna Teal Green:**
> - Admin Portal akan menggunakan palet warna Teal Green (`#0d9488` / `#0f766e` / `#ccfbf1`) untuk membedakan secara visual dengan Portal Publik (Purplish Brand `#5b4bdb`).

---

## Proposed Changes

### 1. Database & Migrations (Backend)

#### [NEW] `server/database/migrations/002_create_admin_and_engine_config_tables.py`
Membuat dua tabel baru untuk SQLite & MySQL:
- `admins`: `id`, `username` (UNIQUE), `password_hash`, `name`, `created_at`, `updated_at`.
- `engine_configs`: `id`, `threshold` (default `0.3`), `adaptive_alpha_threshold` (default `15`), `is_adaptive` (default `1`), `manual_alpha` (default `0.7`), `updated_at`.

#### [NEW] `server/database/seeders/002_admin_seeder.py`
Menanamkan akun admin default (`admin` / `admin123`) dan baris awal `engine_configs` dengan default dari changelog optimasi (`threshold=0.3`).

---

### 2. Models, Repositories & Services (Backend)

#### [NEW] `server/src/models/admin/admin_model.py` & `server/src/models/system/engine_config_model.py`
Representasi data objek Admin dan Engine Config.

#### [NEW] `server/src/repositories/admin/admin_repository.py` & `server/src/repositories/system/engine_config_repository.py`
Repository layer untuk mengolah query SQL ke tabel `admins` dan `engine_configs`.

#### [MODIFY] `server/src/services/system/config_service.py`
- Mengubah `DEFAULT_CONFIG` agar menggunakan `threshold: 0.3` (sesuai changelog optimasi NLP).
- Mengubah alur pembacaan & penyimpanan konfigurasi agar membaca dari DB `engine_configs` alih-alih file JSON/env, dengan fallback ke `DEFAULT_CONFIG` jika DB belum siap.

#### [NEW] `server/src/services/admin/admin_auth_service.py`
Service untuk verifikasi kredensial login admin, generate token sesi admin, dan validasi token.

---

### 3. Routes & Controllers (Backend)

#### [NEW] `server/src/controllers/admin/admin_auth_controller.py`
Controller untuk endpoint `POST /api/admin/auth/login`, `GET /api/admin/auth/me`, dan `POST /api/admin/auth/logout`.

#### [NEW] `server/src/controllers/admin/admin_dosen_controller.py`
Controller CRUD data dosen, publikasi, riwayat bimbingan, dan pengujian khusus admin.

#### [NEW] `server/src/controllers/admin/admin_config_controller.py`
Controller khusus admin untuk membaca dan memperbarui konfigurasi engine NLP.

#### [NEW] `server/src/routes/admin/admin_routes.py`
Blueprint Flask `/api/admin` yang mendaftarkan seluruh endpoint otentikasi, manajemen dosen, batch recommendation, dan konfigurasi admin dengan proteksi middleware.

#### [MODIFY] `server/src/app.py`
Mendaftarkan `admin_bp` ke aplikasi Flask.

---

### 4. Frontend Restructure & Admin Portal (`web/`)

#### [MODIFY] `web/src/router/index.js`
- Menghapus route publik `/batch`, `/dosen`, `/config`.
- Menambahkan route Admin dengan Auth Guard (`meta: { requiresAdmin: true }`):
  - `/admin/login`: Halaman Login Admin
  - `/admin/dashboard`: Dashboard Ringkasan Admin
  - `/admin/dosen`: Pengelolaan Data Dosen, Jurnal, Bimbingan & Pengujian
  - `/admin/batch`: Simulasi Batch Recommendation Admin
  - `/admin/config`: Pengaturan NLP Engine (Teal Green Theme)

#### [MODIFY] `web/src/components/layout/AppSidebar.vue`
Menghapus item menu `Data Dosen`, `Batch Recommendation`, dan `Konfigurasi` dari sidebar publik. Menambahkan tombol / link ke `SiReDo Admin`.

#### [NEW] `web/src/components/layout/AdminSidebar.vue`
Sidebar khusus Admin Portal dengan nuansa **Teal Green**, menampilkan menu Admin (Dashboard, Data Dosen, Batch Simulation, Engine Config, Logout, Kembali ke Portal Publik).

#### [NEW] `web/src/stores/adminAuth.js`
Pinia store untuk menyimpan state autentikasi admin (token, admin profile, login, logout).

#### [NEW] `web/src/views/admin/AdminLoginView.vue`
Halaman login admin yang bersih dan responsif.

#### [NEW] `web/src/views/admin/AdminDashboardView.vue`
Dashboard statistik data dosen, jumlah publikasi, riwayat bimbingan, dan status NLP Engine.

#### [NEW] `web/src/views/admin/AdminDosenView.vue`
Pusat pengelolaan data dosen (CRUD Dosen, Publikasi, Bimbingan, Pengujian).

#### [NEW] `web/src/views/admin/AdminBatchView.vue`
Halaman simulasi rekomendasi batch khusus admin.

#### [NEW] `web/src/views/admin/AdminConfigView.vue`
Halaman pengaturan parameter NLP Engine dengan **Warning Modal** saat admin akan merubah konfigurasi default (`threshold != 0.3` atau `is_adaptive` diubah).

---

## Verification Plan

### Automated Verification
1. Menjalankan pytest (hanya jika diminta user secara eksplisit).

### Manual Verification
1. **Public Portal Verification**:
   - Buka `http://localhost:5173`.
   - Pastikan menu `Data Dosen`, `Batch Recommendation`, dan `Konfigurasi` **sudah tidak ada** di sidebar publik.
   - Pastikan navigasi Beranda, Preprocessing, dan Dokumentasi API tetap berfungsi lancar.
2. **Admin Portal Verification**:
   - Buka `http://localhost:5173/admin/login`.
   - Login dengan username: `admin`, password: `admin123`.
   - Pastikan berhasil masuk ke `Admin Dashboard` dengan tema warna **Teal Green**.
   - Coba halaman **Data Dosen** di admin untuk mengelola dosen dan riwayatnya.
   - Coba halaman **Konfigurasi Engine** di admin: Ubah nilai threshold, pastikan modal peringatan muncul sebelum menyimpan.
   - Coba tombol Logout, pastikan terlempar kembali ke halaman login.
