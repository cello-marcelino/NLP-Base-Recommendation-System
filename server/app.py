from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import threading

# Mengimpor mesin pintar yang baru saja kita buat
from rekomendasi import RecommendationEngine

lecturers_dataset = "data/dataset_profiles_terintegrasi.xlsx"

app = Flask(__name__)
CORS(app)

status_server = {
    "ready": False,
    "progress": 0,
    "pesan": "Menginisialisasi peladen..."
}

def get_data_dosen():
    try:
        df = pd.read_excel(lecturers_dataset) 
        # Membersihkan spasi tak kasatmata di semua judul kolom
        df.columns = df.columns.str.strip()
        df = df.fillna("") 
        return df.to_dict(orient='records')
    except Exception as e:
        print("Error membaca data:", e)
        return []

def muat_mesin_ai():
    """Fungsi ini akan dijalankan di latar belakang agar tidak mengunci API"""
    global status_server
    
    try:
        status_server["pesan"] = "Membaca Pangkalan Data Dosen (Excel)..."
        status_server["progress"] = 25
        # 1. Ambil data asli berbentuk list dari Excel terlebih dahulu bray
        data_dosen = get_data_dosen()
        
        status_server["pesan"] = "Memuat Arsitektur SBERT & Ekstraksi Vektor Cache (Ini memakan waktu)..."
        status_server["progress"] = 65
        
        # 2. Masukkan objek data_dosen ke dalam cache, BUKAN teks path file-nya
        RecommendationEngine.siapkan_cache(data_dosen)
        
        status_server["pesan"] = "Mempersiapkan jalur komunikasi API..."
        status_server["progress"] = 90
        
        # STATUS SIAP
        status_server["pesan"] = "Mesin SIREDO Siap Beroperasi!"
        status_server["progress"] = 100
        status_server["ready"] = True
        
    except Exception as e:
        status_server["pesan"] = f"Gagal menghidupkan mesin: {str(e)}"
        status_server["progress"] = 0

# Picu proses pemuatan berat di latar belakang sesaat setelah kodingan dibaca
threading.Thread(target=muat_mesin_ai, daemon=True).start()

# Pintu 1: Cek Status
@app.route('/api/status', methods=['GET'])
def cek_status():
    return jsonify(status_server)

# Pintu 2: Mengambil Semua Dosen
@app.route('/api/dosen', methods=['GET'])
def daftar_dosen():
    data = get_data_dosen()
    return jsonify({"status": "sukses", "total_data": len(data), "data": data})

# Pintu 3: PINTU REKOMENDASI AI (SUDAH DIPERBAIKI)
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
    
    try:
        hasil_rekomendasi = RecommendationEngine.jalankan_pipeline(
            judul_mhs=judul, 
            abstrak_mhs=abstrak, 
            k_rank=int(k), 
            bobot_lex=float(bobot_lexical), 
            bobot_sem=float(bobot_semantic)
        )
        return jsonify({"status": "sukses", "data": hasil_rekomendasi})
    except Exception as e:
        return jsonify({"status": "gagal", "pesan": str(e)}), 500

# PINTU 4: Fitur Refresh Server (SUDAH DIPERBAIKI)
@app.route('/api/refresh', methods=['POST'])
def refresh_server():
    # Saat data Excel di-refresh, kalkulasi ulang matriks vektor barunya ke dalam cache RAM
    data_dosen = get_data_dosen()
    try:
        RecommendationEngine.siapkan_cache(data_dosen)
        return jsonify({
            "status": "sukses", 
            "pesan": f"Server berhasil disegarkan. {len(data_dosen)} data dosen dan cache vektor dimuat ulang."
        })
    except Exception as e:
        return jsonify({"status": "gagal", "pesan": f"Gagal refresh cache: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5050)