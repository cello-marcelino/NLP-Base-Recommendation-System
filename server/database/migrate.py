import os
import sys
import pandas as pd
from mysql.connector import Error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.config import get_db_connection

EXCEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/dataset_profiles_terintegrasi.xlsx'))

def jalankan_migrasi():
    print("\n==================================================")
    print("🚀 MEMULAI PROSES MIGRASI DATA EXCEL KE MYSQL")
    print("==================================================")
    
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ Error: File Excel tidak ditemukan di: {EXCEL_PATH}")
        return

    try:
        df = pd.read_excel(EXCEL_PATH)
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        data_dosen = df.to_dict(orient='records')
        print(f"✅ Berhasil membaca {len(data_dosen)} baris data dari Excel.")
    except Exception as e:
        print(f"❌ Gagal memproses file Excel: {e}")
        return

    conn = get_db_connection()
    if not conn:
        print("❌ Gagal membuka koneksi ke MySQL. Pastikan XAMPP/MySQL menyala.")
        return

    try:
        cursor = conn.cursor()
        
        print("🧹 Mengosongkan data tabel dosen lama di MySQL...")
        cursor.execute("TRUNCATE TABLE dosen")
        
        query = """
        INSERT INTO dosen (nidn, nama, program_studi, bidang_keahlian, jurnal, judul_bimbing, judul_uji, riwayat_pendidikan)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
        for row in data_dosen:
            nidn_mentah = str(row.get('NIDN', '') or row.get('nidn', '')).strip()

            nidn_final = None if nidn_mentah == "" else nidn_mentah

            cursor.execute(query, (
                nidn_final,
                str(row.get('NAMA', '') or row.get('nama', '')),
                str(row.get('PROGRAM_STUDI', '') or row.get('program_studi', '')),
                str(row.get('BIDANG_KEAHLIAN', '') or row.get('bidang_keahlian', '')),
                str(row.get('JURNAL', '') or row.get('jurnal', '')),
                str(row.get('judul bimbing', '') or row.get('judul_bimbing', '')),
                str(row.get('judul uji', '') or row.get('judul_uji', '')),
                str(row.get('RIWAYAT_PENDIDIKAN', '') or row.get('riwayat_pendidikan', ''))
            ))
            inserted_count += 1
            
        conn.commit()
        print("==================================================")
        print(f"🎉 MIGRASI SUKSES! {inserted_count} data dosen disuntikkan ke MySQL.")
        print("==================================================\n")
        
    except Error as e:
        print(f"❌ Terjadi kesalahan query SQL: {e}")
        conn.rollback()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    jalankan_migrasi()
