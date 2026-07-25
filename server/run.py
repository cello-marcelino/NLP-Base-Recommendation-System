import threading
import os
import sys

# Tambahkan direktori root agar app module terbaca
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.services.hybrid_engine import engine
from app.services.data_loader import DataLoader

app = create_app()

def muat_mesin_ai():
    try:
        print("[INFO] Memeriksa Pangkalan Data...")
        data_dosen = DataLoader.get_data_dosen()
        
        if not data_dosen:
            raise ValueError("Tidak ada data dosen yang ditemukan di MySQL maupun Excel!")
        
        print("[INFO] Memuat Arsitektur SBERT & Ekstraksi Vektor Cache (Ini memakan waktu)...")
        engine.siapkan_cache(data_dosen)
        
        print("[INFO] Mesin SIREDO Siap Beroperasi!")
    except Exception as e:
        print(f"[ERROR] Gagal menghidupkan mesin: {str(e)}")

# Startup background load
threading.Thread(target=muat_mesin_ai, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True, port=5050)