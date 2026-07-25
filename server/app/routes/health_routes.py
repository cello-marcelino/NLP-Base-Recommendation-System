from flask import Blueprint, jsonify
from app.services.hybrid_engine import engine
from app.services.data_loader import DataLoader
from app.utils.response_formatter import ResponseFormatter

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/status', methods=['GET'])
def cek_status():
    from app.services.data_loader import get_db_connection
    conn = get_db_connection()
    sumber_data = "MySQL" if conn else "Excel (Fallback)"
    if conn:
        conn.close()

    status_server = {
        "ready": engine.is_ready,
        "pesan": "Mesin SIREDO Siap Beroperasi!" if engine.is_ready else "Menginisialisasi peladen...",
        "sumber_data": sumber_data
    }
    return jsonify(status_server)

@health_bp.route('/api/refresh', methods=['POST'])
def refresh_server():
    data_dosen = DataLoader.fetch_all_dosen()
    if not data_dosen:
        return jsonify(ResponseFormatter.format_error("Gagal refresh: Pangkalan data MySQL kosong atau tidak terhubung.", 400)[0]), 400
        
    try:
        engine.siapkan_cache(data_dosen, force_recalculate=True)
        return jsonify({
            "status": "sukses", 
            "pesan": f"Server berhasil disegarkan! {len(data_dosen)} data dosen dari MySQL diperbarui ke file matriks vektor."
        })
    except Exception as e:
        return jsonify(ResponseFormatter.format_error(f"Gagal refresh cache: {str(e)}", 500)[0]), 500
