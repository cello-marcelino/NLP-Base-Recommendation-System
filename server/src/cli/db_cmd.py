import os
import sys
import sqlite3
import pandas as pd
from typing import Optional
import mysql.connector

from server.src.config.config import Config
from server.database.connection.database import DatabaseManager
from server.src.config.logging_config import logger
from server.database.migrations.migration_runner import run_migrations
from server.database.seeders.database_seeder import DatabaseSeeder
from server.database.importers.dosen_importer import DosenImporter
from server.src.repositories.dosen.dosen_repository import SQLDosenRepository

def confirm_action(prompt_text: str, force: bool = False) -> bool:
    if force:
        return True
    try:
        ans = input(f"{prompt_text} (y/N): ").strip().lower()
        return ans in ('y', 'yes')
    except (KeyboardInterrupt, EOFError):
        print()
        return False

def db_migrate():
    """Runs database migration creating tables, constraints, and indexes."""
    driver = DatabaseManager.get_driver()
    print(f"[INFO] Menjalankan migrasi database untuk driver: {driver}")
    try:
        count = run_migrations()
        if count > 0:
            print(f"[OK] Migrasi skema database berhasil diaplikasikan ({count} file migrasi).")
        else:
            print("[OK] Skema database sudah mutakhir (up to date).")
    except Exception as e:
        print(f"[ERROR] Migrasi gagal: {e}")
        sys.exit(1)

def db_seed():
    """Runs database seeders to populate initial reference/static data."""
    print("[INFO] Menjalankan database seeders...")
    try:
        DatabaseSeeder.run()
        print("[OK] Database seeding berhasil.")
    except Exception as e:
        print(f"[ERROR] Seeding gagal: {e}")
        sys.exit(1)

def db_import(file_path: Optional[str] = None):
    """Imports dataset from Excel file into relational database tables using DosenImporter pipeline."""
    file_path = file_path or Config.EXCEL_FALLBACK_PATH
    print(f"[INFO] Mengimpor dataset dari: {file_path}")
    try:
        importer = DosenImporter()
        counts = importer.import_file(file_path)
        print(
            f"[OK] Impor dataset berhasil: {counts['dosen']} Dosen, {counts['publikasi']} Publikasi, "
            f"{counts['bimbingan']} Bimbingan, {counts['pengujian']} Pengujian."
        )
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

def db_drop(force: bool = False):
    """Drops the entire database or database file."""
    driver = DatabaseManager.get_driver()
    if not confirm_action(f"[PERINGATAN] Apakah Anda yakin ingin MENGHAPUS seluruh database ({driver})?", force):
        print("[INFO] Operasi dibatalkan oleh pengguna.")
        return

    if driver == 'mysql':
        try:
            print(f"[INFO] Menghubungkan ke MySQL server untuk menghapus database `{Config.DB_NAME}`...")
            conn = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS `{Config.DB_NAME}`;")
            conn.commit()
            cursor.close()
            conn.close()
            print(f"[OK] Database MySQL `{Config.DB_NAME}` berhasil dihapus (dropped).")
        except Exception as e:
            print(f"[ERROR] Gagal menghapus database MySQL: {e}")
            sys.exit(1)
    else:
        # SQLite
        db_path = Config.DB_SQLITE_PATH
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"[OK] File database SQLite `{db_path}` berhasil dihapus.")
            except Exception as e:
                print(f"[ERROR] Gagal menghapus file database SQLite: {e}")
                sys.exit(1)
        else:
            print(f"[INFO] File database SQLite `{db_path}` tidak ditemukan.")

def db_truncate(force: bool = False):
    """Empties/truncates all records from relational tables without dropping schema."""
    driver = DatabaseManager.get_driver()
    if not confirm_action(f"[PERINGATAN] Apakah Anda yakin ingin MENGOSONGKAN seluruh data tabel database ({driver})?", force):
        print("[INFO] Operasi dibatalkan oleh pengguna.")
        return

    try:
        print("[INFO] Mengosongkan data dari seluruh tabel relasional via SQLDosenRepository...")
        repo = SQLDosenRepository()
        repo.truncate_all()
        print("[OK] Seluruh data pada tabel dosen, publikasi, riwayat_bimbingan, dan riwayat_pengujian berhasil dikosongkan.")
    except Exception as e:
        print(f"[ERROR] Gagal mengosongkan data tabel: {e}")
        sys.exit(1)
