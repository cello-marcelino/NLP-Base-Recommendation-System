import os
import sys
import pandas as pd
from typing import Optional

from server.src.core.config import Config
from server.src.core.database import DatabaseManager
from server.src.core.logging import logger
from server.scripts.migrate import run_mysql_migration, run_sqlite_migration
from server.scripts.import_excel_to_db import import_data
from server.src.modules.dosen.dosen_repository import SQLDosenRepository

def db_migrate():
    """Runs database migration creating tables, constraints, and indexes."""
    driver = DatabaseManager.get_driver()
    print(f"[INFO] Menjalankan migrasi database untuk driver: {driver}")
    try:
        if driver == 'mysql':
            run_mysql_migration()
        else:
            run_sqlite_migration()
        print("[OK] Migrasi skema database berhasil diselesaikan.")
    except Exception as e:
        print(f"[ERROR] Migrasi gagal: {e}")
        sys.exit(1)

def db_import(file_path: Optional[str] = None):
    """Imports dataset from Excel file into relational database tables."""
    file_path = file_path or Config.EXCEL_FALLBACK_PATH
    print(f"[INFO] Mengimpor dataset dari: {file_path}")
    try:
        import_data(file_path)
        print("[OK] Impor dataset ke database relasional berhasil.")
    except Exception as e:
        print(f"[ERROR] Impor gagal: {e}")
        sys.exit(1)

def db_export(output_path: Optional[str] = None, export_format: str = 'xlsx'):
    """Exports normalized database records into Excel or JSON dataset."""
    default_filename = f"dataset_profiles_exported.{export_format}"
    output_path = output_path or os.path.join(Config.DATA_DIR, default_filename)
    
    print(f"[INFO] Mengambil seluruh data dari database ({DatabaseManager.get_driver()})...")
    repo = SQLDosenRepository()
    dosen_list = repo.get_all()
    
    if not dosen_list:
        print("[WARN] Tidak ada data dosen yang ditemukan di database untuk diekspor.")
        return
        
    records = []
    for d in dosen_list:
        records.append({
            "NAMA": d.nama,
            "PROGRAM_STUDI": d.program_studi,
            "RIWAYAT_PENDIDIKAN": d.pendidikan,
            "BIDANG_KEAHLIAN": d.bidang_keahlian,
            "JURNAL": d.jurnal,
            "judul uji": d.judul_uji or "-",
            "judul bimbing": d.judul_bimbing or "-"
        })
        
    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    if export_format == 'json':
        df.to_json(output_path, orient='records', indent=2, force_ascii=False)
    else:
        df.to_excel(output_path, index=False)
        
    print(f"[OK] Berhasil mengekspor {len(records)} data profil dosen ke:")
    print(f"     -> {os.path.abspath(output_path)}")
