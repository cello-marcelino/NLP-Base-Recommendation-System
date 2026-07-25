from flask import Blueprint, jsonify, request
import threading

from app.services.data_loader import DataLoader
from app.services.hybrid_engine import engine
from app.utils.response_formatter import ResponseFormatter

dosen_bp = Blueprint('dosen', __name__)

def trigger_sinkronisasi_ai_async():
    print("[INFO] Memulai sinkronisasi ulang matriks AI di latar belakang...")
    try:
        data_terbaru = DataLoader.fetch_all_dosen()
        if data_terbaru:
            engine.sinkronisasi_incremental(data_terbaru)
            print("[INFO] Sinkronisasi AI selesai dan berhasil diperbarui!")
    except Exception as e:
        print(f"[ERROR] Sinkronisasi AI latar belakang gagal: {e}")

@dosen_bp.route('/api/dosen', methods=['GET'])
def daftar_dosen():
    data = DataLoader.get_data_dosen()
    return jsonify(ResponseFormatter.format_success(data, len(data)))

@dosen_bp.route('/api/admin/dosen', methods=['POST'])
def admin_tambah_dosen():
    data = request.json
    sukses, pesan = DataLoader.insert_dosen(data)
    if sukses:
        threading.Thread(target=trigger_sinkronisasi_ai_async, daemon=True).start()
        return jsonify({"status": "sukses", "pesan": pesan}), 201
    return jsonify({"status": "gagal", "pesan": pesan}), 400

@dosen_bp.route('/api/admin/dosen/<int:id_dosen>', methods=['PUT'])
def admin_edit_dosen(id_dosen):
    data = request.json
    sukses, pesan = DataLoader.update_dosen(id_dosen, data)
    if sukses:
        threading.Thread(target=trigger_sinkronisasi_ai_async, daemon=True).start()
        return jsonify({"status": "sukses", "pesan": pesan}), 200
    return jsonify({"status": "gagal", "pesan": pesan}), 400

@dosen_bp.route('/api/admin/dosen/<int:id_dosen>', methods=['DELETE'])
def admin_hapus_dosen(id_dosen):
    sukses, pesan = DataLoader.delete_dosen(id_dosen)
    if sukses:
        threading.Thread(target=trigger_sinkronisasi_ai_async, daemon=True).start()
        return jsonify({"status": "sukses", "pesan": pesan}), 200
    return jsonify({"status": "gagal", "pesan": pesan}), 400

@dosen_bp.route('/api/admin/riwayat', methods=['GET'])
def admin_ambil_riwayat():
    try:
        data = DataLoader.fetch_riwayat_admin()
        return jsonify({"status": "sukses", "data": data}), 200
    except Exception:
        return jsonify({"status": "gagal", "pesan": "Gagal mengambil riwayat"}), 500
