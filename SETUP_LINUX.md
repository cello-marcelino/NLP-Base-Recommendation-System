# 🚀 Panduan Setup Skenario B: Hybrid Deployment
*(Backend AI di Docker Linux + Microsoft DevTunnel + Frontend di Vercel)*

Dokumen ini adalah panduan lengkap untuk melakukan pengujian dan deployment sistem Siredo v3 menggunakan **Skenario B**.

---

## 🏛️ Arsitektur Skenario B

```
[ Pengguna Publik ]
        │
        ▼
┌────────────────────────────────────────┐
│      1. FRONTEND (Vercel Cloud)        │
│   https://siredo.vercel.app            │
│   (Menyajikan UI Vue 3 yang Cepat)     │
└──────────────────┬─────────────────────┘
                   │
                   │ Request API (VITE_API_URL)
                   ▼
┌────────────────────────────────────────┐
│      2. JALUR AKSES (DevTunnel)        │
│   https://siredo-server-5000...ms/api  │
│   (Jembatan Internet ke Server Linux)  │
└──────────────────┬─────────────────────┘
                   │
                   │ Forward ke Port 5000
                   ▼
┌────────────────────────────────────────┐
│      3. BACKEND (Docker di Linux)      │
│   Container: siredo_backend            │
│   - Python Flask + SBERT & KeyBERT     │
│   - Volume: server/storage (Cache)     │
└────────────────────────────────────────┘
```

---

## 📋 Langkah-Langkah Eksekusi di Linux Debian (No-GUI)

### Langkah 0: Prasyarat Sistem Debian (CLI Murni)
Jika Anda menggunakan server Debian yang masih baru/fresh, pasang paket-paket penting berikut melalui terminal SSH:
```bash
sudo apt update && sudo apt install -y docker.io docker-compose-v2 git curl tmux
sudo systemctl enable --now docker
```

---

### Langkah 1: Clone / Tarik Cabang Git di Linux
Buka terminal Linux Anda dan masuk ke repositori proyek:
```bash
git fetch origin
git checkout dockerize-siredo
git pull origin dockerize-siredo
```

---

### Langkah 2: Jalankan Backend dengan Docker
Jalankan kontainer Backend Flask (lengkap dengan engine AI):
```bash
# Menjalankan backend di background
docker compose up -d --build backend
```
*(Catatan: Jika server Anda menggunakan Docker Compose versi lama, gunakan perintah `docker-compose up -d --build backend`)*

**Memeriksa Status & Log Model AI:**
```bash
docker compose logs -f backend
```
*Tunggu hingga inisialisasi cache model Sentence-BERT dan KeyBERT selesai dan server menampilkan `Running on http://0.0.0.0:5000`.*

---

### Langkah 3: Install & Jalankan DevTunnel di Linux

Agar port 5000 di dalam Docker Linux dapat diakses oleh Vercel dari internet publik:

**1. Instalasi DevTunnel CLI (Hanya jika belum terpasang):**
```bash
curl -sL https://aka.ms/DevTunnelCliInstall | bash
```
*(Jika perintah `devtunnel` belum terbaca, muat ulang shell dengan `source ~/.bashrc` atau buka sesi terminal baru)*

**2. Jalankan DevTunnel dengan ID Persisten `siredo-server`:**
```bash
devtunnel host siredo-server -p 5000 --allow-anonymous
```
Terminal akan menampilkan URL publik tetap, misalnya:  
`https://siredo-server-5000.jpe1.devtunnels.ms`

> 💡 **TIPS AGAR TUNNEL TIDAK MATI SAAT TERMINAL SSH DITUTUP:**  
> Jalankan DevTunnel di dalam sesi **`tmux`** atau **`screen`**:
> ```bash
> # Buat sesi tmux baru
> tmux new -s tunnel
> 
> # Jalankan perintah devtunnel di dalamnya
> devtunnel host siredo-server -p 5000 --allow-anonymous
> 
> # Keluar dari tampilan (detach) tanpa mematikan proses:
> # Tekan Ctrl + B, lalu tekan tombol D
> ```
> *(Untuk masuk kembali ke sesi tunnel: `tmux attach -t tunnel`)*

---

### Langkah 4: Verifikasi Koneksi Backend
Uji apakah backend Anda sudah bisa diakses dari internet publik:
```bash
curl https://siredo-server-5000.jpe1.devtunnels.ms/api/dosen
```
Jika mengembalikan data JSON dosen, berarti backend di Docker Linux dan DevTunnel Anda sudah 100% siap!

---

### Langkah 5: Hubungkan Frontend di Vercel

1. Buka dashboard proyek Anda di **[Vercel Dashboard](https://vercel.com)**.
2. Masuk ke menu **Settings** > **Environment Variables**.
3. Pastikan variabel berikut sudah terdaftar:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://siredo-server-5000.jpe1.devtunnels.ms/api`  
     *(⚠️ Wajib menyertakan `/api` di akhir URL)*
4. Lakukan **Redeploy** pada deployment terbaru di Vercel agar perubahan variabel berlaku.

---

## 🛠️ Perintah Berguna (Maintenance)

| Kebutuhan | Perintah |
|---|---|
| Cek log backend realtime | `docker compose logs -f backend` |
| Restart backend container | `docker compose restart backend` |
| Stop backend | `docker compose down` |
| Cek container yang berjalan | `docker ps` |

---
*Setup Skenario B selesai! Frontend Anda berjalan ultra-cepat di Vercel CDN, sementara proses NLP berat ditangani oleh server Linux Anda.*
