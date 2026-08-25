import os
import sqlite3
from typing import Optional, Any
import mysql.connector
from mysql.connector import Error as MySQLError

from server.src.core.config import Config
from server.src.core.logging import logger

class DatabaseManager:
    """Manages database connections supporting both SQLite (default) and MySQL."""
    
    @staticmethod
    def get_driver() -> str:
        return Config.DB_DRIVER
        
    @staticmethod
    def get_sqlite_connection() -> Optional[sqlite3.Connection]:
        try:
            os.makedirs(os.path.dirname(Config.DB_SQLITE_PATH), exist_ok=True)
            conn = sqlite3.connect(Config.DB_SQLITE_PATH)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except Exception as e:
            logger.error(f"Koneksi database SQLite gagal di '{Config.DB_SQLITE_PATH}': {e}")
            return None

    @staticmethod
    def get_mysql_connection() -> Optional[mysql.connector.MySQLConnection]:
        try:
            connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                connect_timeout=3
            )
            return connection
        except MySQLError as e:
            logger.warning(
                f"Koneksi MySQL gagal ke database '{Config.DB_NAME}' di {Config.DB_HOST}:{Config.DB_PORT}. "
                f"Detail: {e}."
            )
            return None

    @staticmethod
    def get_connection() -> Optional[Any]:
        driver = Config.DB_DRIVER
        if driver == 'mysql':
            return DatabaseManager.get_mysql_connection()
        return DatabaseManager.get_sqlite_connection()
