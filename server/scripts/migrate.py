import os
import sys
import sqlite3

# Ensure server package root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.src.core.config import Config
from server.src.core.database import DatabaseManager
from server.src.core.logging import logger

def run_sqlite_migration(conn: sqlite3.Connection):
    """Executes DDL schema creation for SQLite."""
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
    logger.info("Migrasi SQLite berhasil dijalankan.")

def run_mysql_migration(conn):
    """Executes DDL schema creation for MySQL."""
    cursor = conn.cursor()
    
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
    conn.commit()
    cursor.close()
    logger.info("Migrasi MySQL berhasil dijalankan.")

def main():
    driver = DatabaseManager.get_driver()
    logger.info(f"Menjalankan migrasi skema database untuk driver: {driver}")
    
    conn = DatabaseManager.get_connection()
    if not conn:
        logger.error(f"Gagal membuka koneksi database ({driver})")
        sys.exit(1)
        
    try:
        if driver == 'mysql':
            run_mysql_migration(conn)
        else:
            run_sqlite_migration(conn)
        print("Status: Migrasi database berhasil diselesaikan.")
    except Exception as e:
        logger.error(f"Terjadi kesalahan saat migrasi: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    main()
