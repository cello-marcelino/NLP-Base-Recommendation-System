@echo off
echo =======================================================
echo Menyalakan Sistem Rekomendasi Dosen Pembimbing
echo =======================================================
echo.

echo 1. Menyalakan Peladen (Back-end)...
start "API server" cmd /k "cd server && call env\Scripts\activate && python app.py"

timeout /t 3 /nobreak >nul

echo 2. Menyalakan Klien (Front-end)...
start "web client" cmd /k "cd client && npm run dev"

timeout /t 4 /nobreak >nul

echo 3. Membuka peramban web secara otomatis...
start http://localhost:5173

echo.
echo =======================================================
echo Semua sistem telah berjalan di latar belakang!
echo Tekan tombol apa saja untuk menutup jendela pengatur ini.
echo =======================================================
pause >nul
