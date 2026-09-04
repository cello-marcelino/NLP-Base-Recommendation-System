"""
Migration 002: Create Admin and Engine Configuration Tables
Tables:
- admins (Admin users)
- engine_configs (NLP engine dynamic runtime parameters)
"""

from werkzeug.security import generate_password_hash

def up(conn, driver: str = 'sqlite'):
    cursor = conn.cursor()
    
    if driver == 'mysql':
        statements = [
            """
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS engine_configs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                threshold FLOAT NOT NULL DEFAULT 0.3,
                adaptive_alpha_threshold INT NOT NULL DEFAULT 15,
                is_adaptive TINYINT(1) NOT NULL DEFAULT 1,
                manual_alpha FLOAT NOT NULL DEFAULT 0.7,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        ]
        for stmt in statements:
            cursor.execute(stmt)
    else:
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS engine_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                threshold REAL NOT NULL DEFAULT 0.3,
                adaptive_alpha_threshold INTEGER NOT NULL DEFAULT 15,
                is_adaptive INTEGER NOT NULL DEFAULT 1,
                manual_alpha REAL NOT NULL DEFAULT 0.7,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
    # Auto-seed default admin user & default engine config on table creation
    param_char = '%s' if driver == 'mysql' else '?'
    cursor.execute(f"SELECT id FROM admins WHERE username = {param_char}", ('admin',))
    if not cursor.fetchone():
        pwd_hash = generate_password_hash("admin123")
        cursor.execute(
            f"INSERT INTO admins (username, password_hash, name) VALUES ({param_char}, {param_char}, {param_char})",
            ('admin', pwd_hash, 'Administrator SiReDo')
        )
        
    cursor.execute("SELECT id FROM engine_configs LIMIT 1")
    if not cursor.fetchone():
        cursor.execute(
            f"INSERT INTO engine_configs (threshold, adaptive_alpha_threshold, is_adaptive, manual_alpha) VALUES ({param_char}, {param_char}, {param_char}, {param_char})",
            (0.3, 15, 1, 0.7)
        )
        
    conn.commit()
    cursor.close()

def down(conn, driver: str = 'sqlite'):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS engine_configs;")
    cursor.execute("DROP TABLE IF EXISTS admins;")
    conn.commit()
    cursor.close()
