from mysql.connector import Error
from .config import get_db_connection


class DataLayer:
    @staticmethod
    def fetch_all_dosen():
        """Mengambil semua data dosen dari MySQL dan mengonversinya untuk AI & Admin"""
        conn = get_db_connection()
        if not conn:
            print("[WARNING] MySQL tidak terhubung.")
            return []
        
        try:
            # Menggunakan dictionary=True agar hasil query berupa key-value
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM dosen")
            rows = cursor.fetchall()
            
            hasil = []
            for row in rows:
                # Membuat format UPPERCASE yang diwajibkan oleh mesin AI,
                # NAMUN memastikan ID_DOSEN ikut terbawa untuk keperluan CRUD Admin!
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
    def insert_dosen(data):
        """Menambahkan data dosen baru ke database"""
        conn = get_db_connection()
        if not conn:
            return False, "Koneksi database terputus."
            
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO dosen 
                (nama, program_studi, bidang_keahlian, jurnal, judul_bimbing, judul_uji, riwayat_pendidikan) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
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
            conn.commit()  # WAJIB: Menyimpan perubahan & melepas lock MySQL
            return True, "Data dosen berhasil ditambahkan."
            
        except Exception as e:
            conn.rollback() # WAJIB: Batalkan transaksi jika terjadi error
            return False, f"Gagal menambahkan data: {str(e)}"
            
        finally:
            # WAJIB: Selalu tutup cursor dan koneksi untuk mencegah memory leak
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def update_dosen(id_dosen, data):
        """Memperbarui data dosen berdasarkan ID"""
        conn = get_db_connection()
        if not conn:
            return False, "Koneksi database terputus."
            
        try:
            cursor = conn.cursor()
            query = """
                UPDATE dosen 
                SET nama=%s, program_studi=%s, bidang_keahlian=%s, 
                    jurnal=%s, judul_bimbing=%s, judul_uji=%s, riwayat_pendidikan=%s 
                WHERE id_dosen=%s
            """
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
            
            # Cek apakah ada baris yang benar-benar terupdate
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
    def delete_dosen(id_dosen):
        """Menghapus data dosen berdasarkan ID"""
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
