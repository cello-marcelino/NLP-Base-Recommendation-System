"""
Migration 001: Create Dosen and Relational Subtables
Tables:
- dosen (Master)
- publikasi (Child)
- riwayat_bimbingan (Child)
- riwayat_pengujian (Child)
"""

def up(conn, driver: str = 'sqlite'):
    cursor = conn.cursor()
    
    if driver == 'mysql':
        # MySQL DDL
        statements = [
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
        for stmt in statements:
            cursor.execute(stmt)
    else:
        # SQLite DDL
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
    cursor.close()

def down(conn, driver: str = 'sqlite'):
    cursor = conn.cursor()
    tables = ['riwayat_pengujian', 'riwayat_bimbingan', 'publikasi', 'dosen']
    for t in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {t};")
    conn.commit()
    cursor.close()
