# Panduan Setup Linux (Docker, DevTunnel & Vercel)

Dokumen ini berisi log apa saja yang telah ditambahkan pada cabang `dockerize-siredo` serta panduan lengkap untuk melakukan pengujian sistem di server Linux Anda malam ini.

## Log Penambahan File (Dockerization)
1. `server/Dockerfile` & `server/.dockerignore`: Konfigurasi *image* backend berbasis `python:3.9-slim`. Otomatis menginstal library yang dibutuhkan (NLP, Flask, dsb).
2. `web/Dockerfile` & `web/.dockerignore`: Konfigurasi *image* frontend berbasis `node:18-alpine` untuk menjalankan Vite Dev Server.
3. `docker-compose.yml`: Orkestrasi untuk menjalankan seluruh *stack* secara bersamaan. Backend mem-binding port `5000` dan me-mount folder `storage` untuk persistensi cache. Frontend mem-binding port `5173`.

---

## Panduan Setup di Server Linux

### 1. Menjalankan Docker Compose
Pastikan server Linux Anda sudah menginstal Docker dan Docker Compose.

Kloning repositori (atau tarik cabang `dockerize-siredo`), lalu masuk ke folder utama proyek:
```bash
cd siredo-v3
git checkout dockerize-siredo
```

Jalankan sistem menggunakan Docker Compose di latar belakang (*detached mode*):
```bash
docker-compose up -d --build
```

- Backend dapat diakses pada `http://localhost:5000`
- Frontend dapat diakses pada `http://localhost:5173`
*(Jika Anda ingin melihat log untuk proses NLP model loading, jalankan: `docker-compose logs -f backend`)*

### 2. Ekspos Backend via DevTunnel (Linux)

Untuk agar Vercel dapat memanggil API Flask Anda, Anda perlu menyalakan DevTunnel yang mengarah ke port 5000 (Backend).

**A. Instalasi DevTunnel CLI di Linux:**
Jalankan perintah ini di terminal Linux Anda:
```bash
curl -sL https://aka.ms/DevTunnelCliInstall | bash
```

**B. Menjalankan DevTunnel Anonymous:**
```bash
devtunnel host siredo-server -p 5000 --allow-anonymous
```
Atau jika Anda sebelumnya belum mendaftarkan ID tunnel tersebut:
```bash
devtunnel host -p 5000 -a
```
*(Catat URL yang dihasilkan oleh terminal devtunnel, misalnya `https://siredo-server-5000.jpe1.devtunnels.ms`)*

### 3. Setup Vercel (Frontend Hosting)

Jika Anda ingin men-deploy Frontend di Vercel:

1. Instal Vercel CLI secara global di Linux:
   ```bash
   npm i -g vercel
   ```
2. Masuk ke folder web:
   ```bash
   cd web
   ```
3. Lakukan deploy (ikuti instruksi login jika pertama kali):
   ```bash
   vercel --prod
   ```
4. Masuk ke dasbor web Vercel (atau atur via Vercel CLI / file `.env.production`) dan pastikan *Environment Variable* ini terpasang untuk *production*:
   ```
   VITE_API_URL=https://<URL_DEVTUNNEL_ANDA>/api
   ```
   *(Penting: Jangan lupa tambahkan `/api` di akhir URL DevTunnel).*

---
**Tips**: Karena *storage* di-mount, file konfigurasi dan cache model NLP SBERT akan tersimpan dengan aman di folder `server/storage` Linux Anda meskipun container Docker di-*restart*.
