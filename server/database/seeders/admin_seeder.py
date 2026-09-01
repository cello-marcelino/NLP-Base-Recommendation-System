from werkzeug.security import generate_password_hash
from server.database.connection.database import DatabaseManager
from server.src.config.logging_config import logger

def seed_admin_and_config(conn=None):
    """Seeds default admin user and default NLP engine config into the database."""
    should_close = False
    if conn is None:
        conn = DatabaseManager.get_connection()
        should_close = True
        
    if not conn:
        logger.error("AdminSeeder: Gagal membuka koneksi database.")
        return
        
    cursor = conn.cursor()
    driver = DatabaseManager.get_driver()
    param_char = '%s' if driver == 'mysql' and hasattr(conn, 'cmd_query') else '?'
    
    # 1. Seed Admin User if not exists
    cursor.execute(f"SELECT id FROM admins WHERE username = {param_char}", ('admin',))
    row = cursor.fetchone()
    if not row:
        pwd_hash = generate_password_hash("admin123")
        cursor.execute(
            f"INSERT INTO admins (username, password_hash, name) VALUES ({param_char}, {param_char}, {param_char})",
            ('admin', pwd_hash, 'Administrator SiReDo')
        )
        logger.info("AdminSeeder: Default admin user 'admin' berhasil dibuat.")
    else:
        logger.info("AdminSeeder: Admin user 'admin' sudah ada.")
        
    # 2. Seed Default Engine Config if empty
    cursor.execute("SELECT id FROM engine_configs LIMIT 1")
    cfg_row = cursor.fetchone()
    if not cfg_row:
        cursor.execute(
            f"INSERT INTO engine_configs (threshold, adaptive_alpha_threshold, is_adaptive, manual_alpha) VALUES ({param_char}, {param_char}, {param_char}, {param_char})",
            (0.3, 15, 1, 0.7)
        )
        logger.info("AdminSeeder: Default engine_configs berhasil ditanamkan (threshold=0.3).")
    else:
        logger.info("AdminSeeder: engine_configs sudah ada.")
        
    conn.commit()
    cursor.close()
    if should_close:
        conn.close()

if __name__ == '__main__':
    seed_admin_and_config()
