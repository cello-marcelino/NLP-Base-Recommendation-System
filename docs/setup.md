# Panduan Instalasi & Deployment — SiReDo v3

## 1. Kebutuhan Sistem
- **Python**: 3.10 atau 3.11
- **Node.js**: 18+ atau 20+
- **Database**: SQLite (default, zero-setup) atau MySQL (opsional via `.env`)
- **RAM**: Minimal 4GB (direkomendasikan 8GB untuk cache model SBERT & KeyBERT)

---

## 2. Instalasi Backend (`server/`)
1. Masuk ke direktori server:
   ```bash
   cd server
   ```
2. Buat dan aktifkan virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux / macOS:
   source .venv/bin/activate
   ```
3. Pasang dependensi yang terkunci:
   ```bash
   pip install -r requirements.txt
   ```
4. Salin file environment di root proyek:
   ```bash
   cd ..
   copy .env.example .env
   ```
5. Inisialisasi database dan jalankan server via SiReDo CLI:
   ```bash
   # Migrasi skema database
   python siredo db:migrate

   # Impor data master profil dosen
   python siredo db:import

   # Jalankan server
   python siredo serve
   ```

---

## 3. Instalasi Frontend (`web/`)
1. Masuk ke direktori web:
   ```bash
   cd web
   ```
2. Pasang package dependensi:
   ```bash
   npm install
   ```
3. Jalankan server pengembangan Vite:
   ```bash
   npm run dev
   ```
4. Untuk build production:
   ```bash
   npm run build
   ```

---

## 4. Dokumentasi Lanjutan
- [Dokumentasi SiReDo CLI](cli.md)
- [Spesifikasi Kontrak REST API](api.md)
- [Arsitektur & Desain Sistem](architecture.md)
