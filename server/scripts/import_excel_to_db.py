import os
import re
import sys
import pandas as pd
from typing import List

# Ensure server package root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.src.core.config import Config
from server.src.core.database import DatabaseManager
from server.src.core.logging import logger

def parse_items(raw_val: str) -> List[str]:
    """Parses raw text containing publications or thesis titles into a clean list of individual records."""
    if pd.isna(raw_val) or not str(raw_val).strip():
        return []
    s = str(raw_val).strip()
    if s == '-' or s.lower() == 'nan' or s.lower() == 'null':
        return []
        
    # Match double quoted items
    matches = re.findall(r'"([^"]+)"', s)
    if matches:
        return [m.strip() for m in matches if m.strip() and m.strip() != '-']
        
    # Split by semicolon, newline, or bullet points
    parts = re.split(r'[\n;•\r]', s)
    cleaned = []
    for p in parts:
        item = re.sub(r'^[0-9]+[.)]\s*', '', p).strip()
        if item and item != '-' and len(item) > 2:
            cleaned.append(item)
    return cleaned

def import_data(excel_path: str = None):
    excel_path = excel_path or Config.EXCEL_FALLBACK_PATH
    if not os.path.exists(excel_path):
        print(f"Error: File Excel tidak ditemukan di '{excel_path}'")
        sys.exit(1)
        
    logger.info(f"Membaca file Excel master dataset dari: {excel_path}")
    df = pd.read_excel(excel_path)
    
    cols = {str(c).lower().strip(): c for c in df.columns}
    def get_val(row, possible_names):
        for name in possible_names:
            if name in cols:
                val = row[cols[name]]
                return str(val).strip() if pd.notna(val) else ""
        return ""

    driver = DatabaseManager.get_driver()
    conn = DatabaseManager.get_connection()
    if not conn:
        print(f"Error: Gagal membuka koneksi database ({driver})")
        sys.exit(1)

    cursor = conn.cursor()
    
    # Placeholder syntax: '?' for SQLite, '%s' for MySQL
    ph = '%s' if driver == 'mysql' else '?'

    logger.info("Memulai impor data ke tabel relasional...")
    
    total_dosen = 0
    total_publikasi = 0
    total_bimbingan = 0
    total_pengujian = 0

    try:
        # Clear existing data within transaction for clean re-import
        cursor.execute("DELETE FROM riwayat_pengujian")
        cursor.execute("DELETE FROM riwayat_bimbingan")
        cursor.execute("DELETE FROM publikasi")
        cursor.execute("DELETE FROM dosen")

        for _, row in df.iterrows():
            nama = get_val(row, ['nama', 'nama dosen', 'nama lengkap'])
            if not nama:
                continue

            nidn = get_val(row, ['nidn', 'id']) or None
            prodi = get_val(row, ['program studi', 'prodi', 'program_studi']) or 'Teknik Informatika'
            keahlian = get_val(row, ['bidang keahlian', 'keahlian', 'bidang_keahlian'])
            pendidikan = get_val(row, ['pendidikan', 'riwayat pendidikan', 'riwayat_pendidikan'])
            
            raw_jurnal = get_val(row, ['jurnal', 'publikasi'])
            raw_bimbingan = get_val(row, ['judul bimbing', 'riwayat bimbing', 'judul bimbingan', 'judul_bimbing'])
            raw_pengujian = get_val(row, ['judul uji', 'riwayat uji', 'judul ujian', 'judul_uji'])

            # 1. Insert into dosen
            cursor.execute(
                f"INSERT INTO dosen (nidn, nama, program_studi, bidang_keahlian, pendidikan) VALUES ({ph}, {ph}, {ph}, {ph}, {ph})",
                (nidn, nama, prodi, keahlian, pendidikan)
            )
            dosen_id = cursor.lastrowid
            total_dosen += 1

            # 2. Insert into publikasi
            jurnal_list = parse_items(raw_jurnal)
            for j in jurnal_list:
                cursor.execute(
                    f"INSERT INTO publikasi (dosen_id, judul) VALUES ({ph}, {ph})",
                    (dosen_id, j)
                )
                total_publikasi += 1

            # 3. Insert into riwayat_bimbingan
            bimbingan_list = parse_items(raw_bimbingan)
            for b in bimbingan_list:
                cursor.execute(
                    f"INSERT INTO riwayat_bimbingan (dosen_id, judul_tugas_akhir) VALUES ({ph}, {ph})",
                    (dosen_id, b)
                )
                total_bimbingan += 1

            # 4. Insert into riwayat_pengujian
            pengujian_list = parse_items(raw_pengujian)
            for u in pengujian_list:
                cursor.execute(
                    f"INSERT INTO riwayat_pengujian (dosen_id, judul_sidang) VALUES ({ph}, {ph})",
                    (dosen_id, u)
                )
                total_pengujian += 1

        conn.commit()
        logger.info(
            f"Impor selesai! Total: {total_dosen} Dosen, {total_publikasi} Publikasi, "
            f"{total_bimbingan} Riwayat Bimbingan, {total_pengujian} Riwayat Pengujian."
        )
        print(f"Status: Sukses mengimpor {total_dosen} dosen, {total_publikasi} publikasi, {total_bimbingan} bimbingan, {total_pengujian} pengujian.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Gagal saat proses impor: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    import_data()
