from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import threading

# Dependensi utama
from rekomendasi import engine
from database import DataLayer

lecturers_dataset = "data/dataset_profiles_terintegrasi.xlsx"

app = Flask(__name__)
CORS(app)

status_server = {
    "ready": False,
    "progress": 0,
    "pesan": "Menginisialisasi peladen..."
}

def dapatkan_data_dosen_terintegrasi():
    """Ambil data dosen dari MySQL atau Excel."""
    try:
        data_mysql = DataLayer.fetch_all_dosen()
        if data_mysql and len(data_mysql) > 0:
            print("[INFO] Berhasil memuat data utama dari MySQL Database.")
            return data_mysql
    except Exception as e:
        print(f"[WARNING] MySQL tidak merespons atau belum siap: {e}")

    print("[FALLBACK] MySQL kosong atau tidak ditemukan. Menggunakan dataset Excel sebagai seeder...")
    try:
        df = pd.read_excel(lecturers_dataset) 
        df.columns = df.columns.str.strip()
        df = df.fillna("") 
        return df.to_dict(orient='records')
    except Exception as e:
        print("[ERROR] Gagal membaca dataset fallback Excel:", e)
        return []

def muat_mesin_ai():
    """Muat mesin AI di latar belakang."""
    global status_server
    
    try:
        status_server["pesan"] = "Memeriksa Pangkalan Data (MySQL / Fallback Excel)..."
        status_server["progress"] = 25
        
        data_dosen = dapatkan_data_dosen_terintegrasi()
        
        if not data_dosen:
            raise ValueError("Tidak ada data dosen yang ditemukan di MySQL maupun Excel!")
        
        status_server["pesan"] = "Memuat Arsitektur SBERT & Ekstraksi Vektor Cache (Ini memakan waktu)..."
        status_server["progress"] = 65
        
        engine.siapkan_cache(data_dosen)
        
        status_server["pesan"] = "Mempersiapkan jalur komunikasi API..."
        status_server["progress"] = 90
        
        status_server["pesan"] = "Mesin SIREDO Siap Beroperasi!"
        status_server["progress"] = 100
        status_server["ready"] = True
        
    except Exception as e:
        status_server["pesan"] = f"Gagal menghidupkan mesin: {str(e)}"
        status_server["progress"] = 0
        status_server["ready"] = False

# Startup background load
threading.Thread(target=muat_mesin_ai, daemon=True).start()

# Status server
@app.route('/api/status', methods=['GET'])
def cek_status():
    return jsonify(status_server)

# Daftar dosen
@app.route('/api/dosen', methods=['GET'])
def daftar_dosen():
    data = dapatkan_data_dosen_terintegrasi()
    return jsonify({"status": "sukses", "total_data": len(data), "data": data})

# Rekomendasi AI
@app.route('/api/rekomendasi', methods=['POST'])
def cari_rekomendasi():
    if not status_server["ready"]:
        return jsonify({
            "status": "gagal", 
            "pesan": "Mesin AI sedang melakukan pemanasan (warming up/caching). Silakan coba beberapa saat lagi!"
        }), 503

    data_klien = request.json
    judul = data_klien.get('judul', '')
    abstrak = data_klien.get('abstrak', '')
    k = data_klien.get('k', 10)
    
    bobot_lexical = data_klien.get('bobot_lexical', 0.4)
    bobot_semantic = data_klien.get('bobot_semantic', 0.6)
    
    if not judul and not abstrak:
        return jsonify({"status": "gagal", "pesan": "Judul dan Abstrak tidak boleh kosong!"}), 400
    
    try:
        hasil_rekomendasi = engine.jalankan_pipeline(
            judul_mhs=judul, 
            abstrak_mhs=abstrak, 
            k_rank=int(k), 
            bobot_lex=float(bobot_lexical), 
            bobot_sem=float(bobot_semantic)
        )
        return jsonify({"status": "sukses", "data": hasil_rekomendasi})
    except Exception as e:
        return jsonify({"status": "gagal", "pesan": str(e)}), 500

# Refresh cache
@app.route('/api/refresh', methods=['POST'])
def refresh_server():
    data_dosen = DataLayer.fetch_all_dosen()
    if not data_dosen:
        return jsonify({"status": "gagal", "pesan": "Gagal refresh: Pangkalan data MySQL kosong atau tidak terhubung."}), 400
        
    try:
        engine.siapkan_cache(data_dosen, force_recalculate=True)
        return jsonify({
            "status": "sukses", 
            "pesan": f"Server berhasil disegarkan! {len(data_dosen)} data dosen dari MySQL diperbarui ke file matriks vektor."
        })
    except Exception as e:
        return jsonify({"status": "gagal", "pesan": f"Gagal refresh cache: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5050)
