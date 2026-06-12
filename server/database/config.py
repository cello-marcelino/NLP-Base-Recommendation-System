import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Kosongkan jika menggunakan XAMPP standar Windows
    'database': 'db_siredo'
}

def get_db_connection():
    """Membuka gerbang koneksi ke MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error saat menyambung ke MySQL: {e}")
        return None