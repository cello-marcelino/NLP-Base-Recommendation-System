import mysql.connector
from mysql.connector import Error
from flask import current_app
from app.models.dosen import Dosen
import pandas as pd

class Database:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_NAME']
            )
            return connection
        except Error as e:
            return None

    @staticmethod
    def get_all_dosen():
        connection = Database.get_connection()
        if connection and connection.is_connected():
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM dosen")
                records = cursor.fetchall()
                dosen_list = []
                for row in records:
                    dosen_list.append(Dosen(
                        nidn=str(row.get('nidn', '')),
                        nama=str(row.get('nama', '')),
                        program_studi=str(row.get('program_studi', '')),
                        bidang_keahlian=str(row.get('bidang_keahlian', '')),
                        jurnal=str(row.get('jurnal', '')),
                        judul_bimbing=str(row.get('judul_bimbing', '')),
                        judul_uji=str(row.get('judul_uji', '')),
                        pendidikan=str(row.get('pendidikan', ''))
                    ))
                return dosen_list
            except Error as e:
                pass
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        
        # Fallback to Excel
        return ExcelReader.get_all_dosen()

class ExcelReader:
    @staticmethod
    def get_all_dosen():
        try:
            excel_path = current_app.config['EXCEL_FALLBACK_PATH']
            df = pd.read_excel(excel_path)
            
            # Normalize column names for easier mapping
            cols = {str(c).lower().strip(): c for c in df.columns}
            
            def get_val(row, possible_names):
                for name in possible_names:
                    if name in cols:
                        val = row[cols[name]]
                        return str(val) if pd.notna(val) else ""
                return ""

            dosen_list = []
            for _, row in df.iterrows():
                dosen = Dosen(
                    nidn=get_val(row, ['nidn', 'id']),
                    nama=get_val(row, ['nama', 'nama dosen', 'nama lengkap']),
                    program_studi=get_val(row, ['program studi', 'prodi', 'program_studi']),
                    bidang_keahlian=get_val(row, ['bidang keahlian', 'keahlian', 'bidang_keahlian']),
                    jurnal=get_val(row, ['jurnal', 'publikasi']),
                    judul_bimbing=get_val(row, ['judul bimbing', 'riwayat bimbing', 'judul bimbingan', 'judul_bimbing']),
                    judul_uji=get_val(row, ['judul uji', 'riwayat uji', 'judul ujian', 'judul_uji']),
                    pendidikan=get_val(row, ['pendidikan', 'riwayat pendidikan', 'riwayat_pendidikan'])
                )
                dosen_list.append(dosen)
            return dosen_list
        except Exception as e:
            print(f"Excel Fallback Error: {e}")
            return []
