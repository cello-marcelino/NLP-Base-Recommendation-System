from mysql.connector import Error
from .config import get_db_connection


class DataLayer:
    @staticmethod
    def fetch_all_dosen():
        """Ambil semua data dosen."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM dosen")
            data = cursor.fetchall()

            formatted_data = []
            for row in data:
                formatted_data.append({
                    "NAMA": row['nama'],
                    "PROGRAM_STUDI": row['program_studi'],
                    "BIDANG_KEAHLIAN": row['bidang_keahlian'],
                    "JURNAL": row['jurnal'],
                    "judul bimbing": row['judul_bimbing'],
                    "judul uji": row['judul_uji'],
                    "RIWAYAT_PENDIDIKAN": row['riwayat_pendidikan']
                })
            return formatted_data
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
