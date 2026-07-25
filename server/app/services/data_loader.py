import json
import pandas as pd
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Tuple

from app.config import Config

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_siredo'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error saat menyambung ke MySQL: {e}")
        return None

class DataLoader:
    @staticmethod
    def get_data_dosen() -> List[Dict[str, Any]]:
        try:
            data = DataLoader.fetch_all_dosen()
            if data and len(data) > 0:
                print("[INFO] Berhasil memuat data utama dari MySQL Database.")
                return data
        except Exception as e:
            print(f"[WARNING] MySQL tidak merespons atau belum siap: {e}")
        
        print("[FALLBACK] MySQL kosong atau tidak ditemukan. Menggunakan dataset Excel sebagai seeder...")
        try:
            df = pd.read_excel(Config.EXCEL_FILE) 
            df.columns = df.columns.str.strip()
            df = df.fillna("") 
            return df.to_dict(orient='records')
        except Exception as e:
            print("[ERROR] Gagal membaca dataset fallback Excel:", e)
            return []

    @staticmethod
    def fetch_all_dosen() -> List[Dict[str, Any]]:
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM dosen")
            rows = cursor.fetchall()
            hasil = []
            for row in rows:
                dosen_dict = {
                    "ID_DOSEN": row.get('id_dosen') or row.get('ID_DOSEN') or row.get('id'),
                    "NAMA": row.get('nama') or row.get('NAMA', ''),
                    "PROGRAM_STUDI": row.get('program_studi') or row.get('PROGRAM_STUDI', ''),
                    "BIDANG_KEAHLIAN": row.get('bidang_keahlian') or row.get('BIDANG_KEAHLIAN', ''),
                    "JURNAL": row.get('jurnal') or row.get('JURNAL', ''),
                    "JUDUL_BIMBING": row.get('judul_bimbing') or row.get('JUDUL_BIMBING', ''),
                    "JUDUL_UJI": row.get('judul_uji') or row.get('JUDUL_UJI', ''),
                    "RIWAYAT_PENDIDIKAN": row.get('riwayat_pendidikan') or row.get('RIWAYAT_PENDIDIKAN', '')
                }
                hasil.append(dosen_dict)
            return hasil
        except Exception as e:
            print(f"[ERROR] Gagal mengambil data dosen: {e}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def insert_dosen(data) -> Tuple[bool, str]:
        conn = get_db_connection()
        if not conn:
            return False, "Koneksi database terputus."
        try:
            cursor = conn.cursor()
            query = "INSERT INTO dosen (nama, program_studi, bidang_keahlian, jurnal, judul_bimbing, judul_uji, riwayat_pendidikan) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            nilai = (
                data.get('nama', ''),
                data.get('program_studi', ''),
                data.get('bidang_keahlian', ''),
                data.get('jurnal', ''),
                data.get('judul_bimbing', ''),
                data.get('judul_uji', ''),
                data.get('riwayat_pendidikan', '')
            )
            cursor.execute(query, nilai)
            conn.commit()
            return True, "Data dosen berhasil ditambahkan."
        except Exception as e:
            conn.rollback()
            return False, f"Gagal menambahkan data: {str(e)}"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def update_dosen(id_dosen, data) -> Tuple[bool, str]:
        conn = get_db_connection()
        if not conn:
            return False, "Koneksi database terputus."
        try:
            cursor = conn.cursor()
            query = "UPDATE dosen SET nama=%s, program_studi=%s, bidang_keahlian=%s, jurnal=%s, judul_bimbing=%s, judul_uji=%s, riwayat_pendidikan=%s WHERE id_dosen=%s"
            nilai = (
                data.get('nama', ''),
                data.get('program_studi', ''),
                data.get('bidang_keahlian', ''),
                data.get('jurnal', ''),
                data.get('judul_bimbing', ''),
                data.get('judul_uji', ''),
                data.get('riwayat_pendidikan', ''),
                id_dosen
            )
            cursor.execute(query, nilai)
            if cursor.rowcount == 0:
                return False, "Data dosen tidak ditemukan atau tidak ada perubahan."
            conn.commit()
            return True, "Data dosen berhasil diperbarui."
        except Exception as e:
            conn.rollback()
            return False, f"Gagal memperbarui data: {str(e)}"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def delete_dosen(id_dosen) -> Tuple[bool, str]:
        conn = get_db_connection()
        if not conn:
            return False, "Koneksi database terputus."
        try:
            cursor = conn.cursor()
            query = "DELETE FROM dosen WHERE id_dosen=%s"
            cursor.execute(query, (id_dosen,))
            if cursor.rowcount == 0:
                return False, "Data dosen tidak ditemukan."
            conn.commit()
            return True, "Data dosen berhasil dihapus."
        except Exception as e:
            conn.rollback()
            return False, f"Gagal menghapus data: {str(e)}"
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def simpan_log_json(input_data, top_k_list) -> bool:
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            query = "INSERT INTO log_rekomendasi (judul_mhs, abstrak_mhs, bobot_lexical, bobot_semantic, is_adaptif, batas_k, hasil_rekomendasi_json) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            hasil_json = json.dumps(top_k_list) 
            nilai = (
                input_data.get('judul', ''),
                input_data.get('abstrak', ''),
                input_data.get('bobot_lexical', 0.5),
                input_data.get('bobot_semantic', 0.5),
                input_data.get('is_adaptif', 0),
                len(top_k_list),
                hasil_json
            )
            cursor.execute(query, nilai)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def fetch_riwayat_admin() -> List[Dict]:
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM log_rekomendasi ORDER BY created_at DESC")
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
