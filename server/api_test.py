import requests
import json

# Data buatan seolah-olah dari mahasiswa
data_dikirim = {
    "judul": "Sistem Informasi Geografis Pemetaan Daerah Rawan Banjir",
    "abstrak": "Membangun aplikasi pemetaan menggunakan titik kordinat satelit untuk mengetahui daerah langganan genangan air.",
    "k": 3
}

print("Sedang mengirim data ke Peladen...")
respons = requests.post("http://127.0.0.1:5050/api/rekomendasi", json=data_dikirim)

# Memeriksa apakah Peladen membalas dengan status "OK" (200)
if respons.status_code == 200:
    print("\n--- BERHASIL! ---")
    print(json.dumps(respons.json(), indent=2))
else:
    print("\n--- TERJADI MASALAH DI PELADEN ---")
    print(f"Kode Status: {respons.status_code}")
    print("Pesan Asli dari Peladen:\n", respons.text)