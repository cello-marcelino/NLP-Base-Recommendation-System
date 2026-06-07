@echo off
echo =======================================================
echo Menyalakan Sistem Rekomendasi Dosen Pembimbing
echo =======================================================
echo.

:: Menjalankan Peladen (Python/Flask) di jendela terminal baru
echo 1. Menyalakan Peladen (Back-end)...
start "API server" cmd /k "cd server && call env\Scripts\activate && python app.py"

:: Menunggu 3 detik agar peladen menyala lebih dulu
timeout /t 3 /nobreak >nul

:: Menjalankan Klien (Vue/Vite) di jendela terminal baru
echo 2. Menyalakan Klien (Front-end)...
start "web client" cmd /k "cd client && npm run dev"

:: Menunggu 4 detik agar Klien (Vite) selesai merakit antarmuka
timeout /t 4 /nobreak >nul

:: Membuka peramban web (browser) secara otomatis
echo 3. Membuka peramban web secara otomatis...
start http://localhost:5173

echo.
echo =======================================================
echo Semua sistem telah berjalan di latar belakang!
echo Tekan tombol apa saja untuk menutup jendela pengatur ini.
echo =======================================================
pause >nul