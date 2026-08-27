import os
import sys
import importlib.util
import glob
from typing import List

from server.src.config.config import Config
from server.database.connection.database import DatabaseManager
from server.src.config.logging_config import logger

def ensure_migrations_table(conn, driver: str):
    cursor = conn.cursor()
    if driver == 'mysql':
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                migration VARCHAR(255) NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration TEXT NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.commit()
    cursor.close()

def get_applied_migrations(conn, driver: str) -> List[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT migration FROM migrations ORDER BY id ASC;")
    rows = cursor.fetchall()
    cursor.close()
    if driver == 'mysql':
        return [r[0] if isinstance(r, (list, tuple)) else r['migration'] for r in rows]
    return [r[0] for r in rows]

def record_migration(conn, driver: str, migration_name: str):
    param_char = '%s' if driver == 'mysql' else '?'
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO migrations (migration) VALUES ({param_char});", (migration_name,))
    conn.commit()
    cursor.close()

def run_migrations():
    """Runs all pending migrations in order with graceful SQLite fallback."""
    driver = DatabaseManager.get_driver()
    
    # 1. If MySQL, ensure the database exists first (or fallback to SQLite)
    if driver == 'mysql':
        try:
            import mysql.connector
            server_conn = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                connect_timeout=3
            )
            s_cursor = server_conn.cursor()
            s_cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            server_conn.commit()
            s_cursor.close()
            server_conn.close()
        except Exception as e:
            logger.warning(f"MySQL server tidak dapat diakses ({e}). Mengalihkan migrasi ke SQLite...")
            driver = 'sqlite'

    conn = DatabaseManager.get_sqlite_connection() if driver == 'sqlite' else DatabaseManager.get_mysql_connection()
    if not conn:
        conn = DatabaseManager.get_sqlite_connection()
        driver = 'sqlite'
        
    if not conn:
        raise RuntimeError(f"Gagal membuka koneksi database ({driver})")
        
    try:
        ensure_migrations_table(conn, driver)
        applied = set(get_applied_migrations(conn, driver))
        
        # Discover migration files
        migrations_dir = os.path.dirname(os.path.abspath(__file__))
        migration_files = sorted(glob.glob(os.path.join(migrations_dir, "[0-9][0-9][0-9]_*.py")))
        
        executed_count = 0
        for filepath in migration_files:
            filename = os.path.basename(filepath)
            module_name = filename[:-3]
            
            if module_name in applied:
                continue
                
            logger.info(f"Menjalankan migrasi ({driver}): {filename}...")
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'up'):
                module.up(conn, driver)
                record_migration(conn, driver, module_name)
                executed_count += 1
                logger.info(f"[OK] Migrasi {filename} berhasil diaplikasikan.")
                
        if executed_count == 0:
            logger.info(f"Database skema ({driver}) sudah up to date. Tidak ada migrasi baru.")
        else:
            logger.info(f"Berhasil mengaplikasikan {executed_count} migrasi baru ke ({driver}).")
            
        return executed_count
    finally:
        conn.close()

if __name__ == '__main__':
    run_migrations()
