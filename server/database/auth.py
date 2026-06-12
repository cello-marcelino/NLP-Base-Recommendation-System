from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from .config import get_db_connection

class AuthLayer:
    @staticmethod
    def register_user(username, password, role='mahasiswa'):
        conn = get_db_connection()
        if not conn: return False, "Gagal terhubung ke database."
        
        try:
            cursor = conn.cursor()
            hashed_pw = generate_password_hash(password)
            
            query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, hashed_pw, role))
            conn.commit()
            return True, "Registrasi berhasil."
        except Error as e:
            return False, f"Username sudah digunakan atau error: {e}"
        finally:
            if conn and conn.is_connected():
                cursor.close() #type: ignore
                conn.close()

    @staticmethod
    def verify_login(username, password):
        conn = get_db_connection()
        if not conn: return False, None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password_hash'], password): #type: ignore
                return True, {"username": user['username'], "role": user['role']} #type: ignore
            return False, None
        finally:
            if conn and conn.is_connected():
                cursor.close() #type: ignore
                conn.close()