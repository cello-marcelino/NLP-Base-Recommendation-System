# Panduan Instalasi & Deployment — SiReDo v3

## 1. Kebutuhan Sistem
- **Python**: 3.10 atau 3.11
- **Node.js**: 18+ atau 20+
- **MySQL** (Opsional, otomatis fallback ke file Excel jika MySQL tidak aktif)
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
4. Salin file environment:
   ```bash
   copy .env.example .env
   ```
5. Jalankan server:
   ```bash
   python run.py
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
