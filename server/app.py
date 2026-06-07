from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

# Mengimpor mesin pintar yang baru saja kita buat
from rekomendasi import hitung_rekomendasi

lecturers_dataset = "data/dataset_profiles_terintegrasi.xlsx"

app = Flask(__name__)
CORS(app)

def get_data_dosen():
    try:
        df = pd.read_excel(lecturers_dataset) 
        # BARIS BARU: Membersihkan spasi tak kasatmata di semua judul kolom
        df.columns = df.columns.str.strip()
        df = df.fillna("") 
        return df.to_dict(orient='records')
    except Exception as e:
        print("Error membaca data:", e)
        return []

# Pintu 1: Cek Status
@app.route('/api/status', methods=['GET'])
def cek_status():
    return jsonify({"pesan": "Server Flask berjalan dengan baik!"})

# Pintu 2: Mengambil Semua Dosen
@app.route('/api/dosen', methods=['GET'])
def daftar_dosen():
    data = get_data_dosen()
    return jsonify({"status": "sukses", "total_data": len(data), "data": data})

# Pintu 3: PINTU BARU UNTUK REKOMENDASI AI
# Tambahkan ini di dalam Pintu 3 (cari_rekomendasi) sebelum memanggil hitung_rekomendasi:
@app.route('/api/rekomendasi', methods=['POST'])
def cari_rekomendasi():
    data_klien = request.json
    judul = data_klien.get('judul', '')
    abstrak = data_klien.get('abstrak', '')
    k = data_klien.get('k', 10)
    
    # Menangkap bobot dari Klien (nilai default 0.4 dan 0.6)
    bobot_lexical = data_klien.get('bobot_lexical', 0.4)
    bobot_semantic = data_klien.get('bobot_semantic', 0.6)
    
    if not judul and not abstrak:
        return jsonify({"status": "gagal", "pesan": "Judul dan Abstrak tidak boleh kosong!"}), 400
        
    data_dosen = get_data_dosen()
    if len(data_dosen) == 0:
        return jsonify({"status": "gagal", "pesan": "Dataset kosong atau gagal dibaca!"}), 500
    
    # Berikan bobot ke Mesin AI
    hasil_rekomendasi = hitung_rekomendasi(data_dosen, judul, abstrak, k, bobot_lexical, bobot_semantic)
    
    return jsonify({"status": "sukses", "data": hasil_rekomendasi})

# PINTU 4: Fitur Refresh Server
@app.route('/api/refresh', methods=['POST'])
def refresh_server():
    # Mensimulasikan pemuatan ulang data
    data_dosen = get_data_dosen()
    return jsonify({
        "status": "sukses", 
        "pesan": f"Server berhasil disegarkan. {len(data_dosen)} data dosen dimuat ulang."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5050)