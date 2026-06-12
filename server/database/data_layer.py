from mysql.connector import Error
from .config import get_db_connection

class DataLayer:
    @staticmethod
    def fetch_all_dosen():
        """Menarik seluruh data dari tabel dosen MySQL"""
        conn = get_db_connection()
        if not conn: return []
        
        try:
            cursor = conn.cursor(dictionary=True) 
            cursor.execute("SELECT * FROM dosen")
            data = cursor.fetchall()
            
            # Normalisasi keys agar sinkron dengan kebutuhan rekomendasi.py lama
            formatted_data = []
            for row in data:
                formatted_data.append({
                    "NAMA": row['nama'],                                      # type:ignore
                    "PROGRAM_STUDI": row['program_studi'],                    # type:ignore
                    "BIDANG_KEAHLIAN": row['bidang_keahlian'],                # type:ignore
                    "JURNAL": row['jurnal'],                                  # type:ignore
                    "judul bimbing": row['judul_bimbing'],                    # type:ignore
                    "judul uji": row['judul_uji'],                            # type:ignore
                    "RIWAYAT_PENDIDIKAN": row['riwayat_pendidikan']           # type:ignore
                })
            return formatted_data
        finally:
            if conn and conn.is_connected():
                cursor.close() # type:ignore
                conn.close()