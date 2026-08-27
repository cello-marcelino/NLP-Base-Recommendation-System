import sqlite3
import importlib

migration_001 = importlib.import_module('server.database.migrations.001_create_dosen_tables')
from server.database.migrations.migration_runner import ensure_migrations_table, get_applied_migrations, record_migration

def test_migration_001_sqlite_lifecycle():
    conn = sqlite3.connect(":memory:")
    
    # 1. Run migration UP
    migration_001.up(conn, driver='sqlite')
    
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cursor.fetchall()]
    assert "dosen" in tables
    assert "publikasi" in tables
    assert "riwayat_bimbingan" in tables
    assert "riwayat_pengujian" in tables
    
    # 2. Test migration DOWN
    migration_001.down(conn, driver='sqlite')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    remaining_tables = [r[0] for r in cursor.fetchall()]
    assert "dosen" not in remaining_tables
    assert "publikasi" not in remaining_tables
    
    conn.close()

def test_migrations_tracking_table():
    conn = sqlite3.connect(":memory:")
    ensure_migrations_table(conn, driver='sqlite')
    
    applied_before = get_applied_migrations(conn, driver='sqlite')
    assert len(applied_before) == 0
    
    record_migration(conn, driver='sqlite', migration_name="001_create_dosen_tables")
    
    applied_after = get_applied_migrations(conn, driver='sqlite')
    assert len(applied_after) == 1
    assert applied_after[0] == "001_create_dosen_tables"
    
    conn.close()
