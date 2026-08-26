import os
import sys
import sqlite3
import mysql.connector

# Ensure server package root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.src.core.config import Config
from server.src.core.database import DatabaseManager
from server.src.core.logging import logger

def run_sqlite_migration():
    """Executes DDL schema creation for SQLite."""
    conn = DatabaseManager.get_sqlite_connection()
    if not conn:
        raise RuntimeError(f"Gagal membuka koneksi SQLite di: {Config.DB_SQLITE_PATH}")
        
    try:
        cursor = conn.cursor()
        cursor.executescript("""
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS dosen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nidn TEXT UNIQUE,
                nama TEXT NOT NULL,
                program_studi TEXT NOT NULL,
                bidang_keahlian TEXT,
                pendidikan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS publikasi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dosen_id INTEGER NOT NULL,
                judul TEXT NOT NULL,
                tahun INTEGER,
                penerbit TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dosen_id) REFERENCES dosen(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_publikasi_dosen ON publikasi(dosen_id);

            CREATE TABLE IF NOT EXISTS riwayat_bimbingan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dosen_id INTEGER NOT NULL,
                judul_tugas_akhir TEXT NOT NULL,
                tahun INTEGER,
                peran TEXT DEFAULT 'Pembimbing',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dosen_id) REFERENCES dosen(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_bimbingan_dosen ON riwayat_bimbingan(dosen_id);

            CREATE TABLE IF NOT EXISTS riwayat_pengujian (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dosen_id INTEGER NOT NULL,
                judul_sidang TEXT NOT NULL,
                tahun INTEGER,
                peran TEXT DEFAULT 'Penguji',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dosen_id) REFERENCES dosen(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_pengujian_dosen ON riwayat_pengujian(dosen_id);
        """)
        conn.commit()
        logger.info(f"Migrasi SQLite berhasil dijalankan di: {Config.DB_SQLITE_PATH}")
    finally:
        conn.close()

def run_mysql_migration():
    """Executes database creation (CREATE DATABASE IF NOT EXISTS) and DDL table creation for MySQL."""
    logger.info(f"Menghubungkan ke MySQL server di {Config.DB_HOST}:{Config.DB_PORT}...")
    
    server_conn = mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        connect_timeout=5
    )
    cursor = server_conn.cursor()
    
    try:
        # 1. CREATE DATABASE IF NOT EXISTS
        db_name = Config.DB_NAME
        logger.info(f"Memeriksa / membuat database MySQL: `{db_name}`...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE `{db_name}`;")
        
        # 2. CREATE TABLES
        tables = [
            """
            CREATE TABLE IF NOT EXISTS dosen (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nidn VARCHAR(50) UNIQUE,
                nama VARCHAR(255) NOT NULL,
                program_studi VARCHAR(150) NOT NULL,
                bidang_keahlian TEXT,
                pendidikan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS publikasi (
                id INT AUTO_INCREMENT PRIMARY KEY,
                dosen_id INT NOT NULL,
                judul TEXT NOT NULL,
                tahun INT NULL,
                penerbit VARCHAR(255) NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dosen_id) REFERENCES dosen(id) ON DELETE CASCADE,
                INDEX idx_publikasi_dosen (dosen_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS riwayat_bimbingan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                dosen_id INT NOT NULL,
                judul_tugas_akhir TEXT NOT NULL,
                tahun INT NULL,
                peran VARCHAR(100) DEFAULT 'Pembimbing',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dosen_id) REFERENCES dosen(id) ON DELETE CASCADE,
                INDEX idx_bimbingan_dosen (dosen_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS riwayat_pengujian (
                id INT AUTO_INCREMENT PRIMARY KEY,
                dosen_id INT NOT NULL,
                judul_sidang TEXT NOT NULL,
                tahun INT NULL,
                peran VARCHAR(100) DEFAULT 'Penguji',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dosen_id) REFERENCES dosen(id) ON DELETE CASCADE,
                INDEX idx_pengujian_dosen (dosen_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        ]
        
        for sql in tables:
            cursor.execute(sql)
            
        server_conn.commit()
        logger.info(f"Migrasi MySQL ke database `{db_name}` berhasil dijalankan.")
    finally:
        cursor.close()
        server_conn.close()

def main():
    driver = DatabaseManager.get_driver()
    logger.info(f"Menjalankan migrasi skema database untuk driver: {driver}")
    
    try:
        if driver == 'mysql':
            run_mysql_migration()
        else:
            run_sqlite_migration()
        print("Status: Migrasi database berhasil diselesaikan.")
    except Exception as e:
        logger.error(f"Terjadi kesalahan saat migrasi: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
