# Siredo v3 - Frontend Web

Ini adalah antarmuka web (Frontend) dari aplikasi Siredo v3.
Dibangun dengan Vue 3 dan Vite dengan antarmuka dinamis dan responsif.

## Setup & Development

- **Instal dependensi:** `npm install`
- **Jalankan server lokal:** `npm run dev`
- **Build aplikasi:** `npm run build`

## Environment Variables

Saat melakukan deployment atau menghubungkan frontend dengan backend publik (misal melalui Vercel dan DevTunnel), Anda perlu mengatur *environment variable* berikut:

- `VITE_API_URL`: Mengarah ke URL backend Flask. **Wajib diakhiri dengan `/api`** (misalnya `https://siredo-server-5000.jpe1.devtunnels.ms/api`). Hal ini dikarenakan semua endpoint backend terdaftar di bawah *prefix* `/api`.

Jika dijalankan murni di lokal (tanpa `.env`), Vite sudah diatur untuk otomatis meneruskan rute `/api` ke `http://localhost:5000` melalui proxy internal.
