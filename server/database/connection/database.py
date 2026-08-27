import os
import sqlite3
from typing import Optional, Any
from server.src.config.config import Config
from server.src.config.logging_config import logger

class DatabaseManager:
    """
    Manages database connection and lifecycle for SQLite and MySQL.
    Follows rules/database.md: Connection & lifecycle only, zero business queries.
    """
    
    @staticmethod
    def get_driver() -> str:
        return Config.DB_DRIVER
        
    @staticmethod
    def get_sqlite_connection() -> Optional[sqlite3.Connection]:
        try:
            db_path = Config.DB_SQLITE_PATH
            os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            # Enable foreign key enforcement in SQLite
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn
        except Exception as e:
            logger.error(f"Gagal membuka koneksi SQLite di {Config.DB_SQLITE_PATH}: {e}")
            return None

    @staticmethod
    def get_mysql_connection():
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                connect_timeout=3
            )
            return conn
        except Exception as e:
            logger.warning(
                f"Koneksi MySQL gagal ke database '{Config.DB_NAME}' di {Config.DB_HOST}:{Config.DB_PORT}. "
                f"Detail: {e}"
            )
            return None

    @classmethod
    def get_connection(cls) -> Optional[Any]:
        if cls.get_driver() == 'mysql':
            conn = cls.get_mysql_connection()
            if conn:
                return conn
            logger.info("Mengaktifkan fallback ke SQLite...")
            return cls.get_sqlite_connection()
        return cls.get_sqlite_connection()

def get_connection() -> Optional[Any]:
    """Convenience functional accessor for database connection."""
    return DatabaseManager.get_connection()
