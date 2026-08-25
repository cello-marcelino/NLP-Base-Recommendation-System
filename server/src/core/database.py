from typing import Optional
import mysql.connector
from mysql.connector import Error
from server.src.core.config import Config
from server.src.core.logging import logger

class DatabaseManager:
    """Manages MySQL database connections with structured logging and error handling."""
    
    @staticmethod
    def get_connection() -> Optional[mysql.connector.MySQLConnection]:
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
        except Error as e:
            logger.warning(
                f"Koneksi MySQL gagal ke database '{Config.DB_NAME}' di {Config.DB_HOST}:{Config.DB_PORT}. "
                f"Detail: {e}. Sistem akan beralih ke Excel fallback."
            )
            return None
