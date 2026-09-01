from typing import Optional, Dict, Any
from server.database.connection.database import DatabaseManager
from server.src.models.admin.admin_model import AdminUser
from server.src.config.logging_config import logger

class AdminRepository:
    """Data Access Repository for Admin user entity."""
    
    @staticmethod
    def get_by_username(username: str) -> Optional[AdminUser]:
        conn = DatabaseManager.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            driver = DatabaseManager.get_driver()
            param_char = '%s' if driver == 'mysql' and hasattr(conn, 'cmd_query') else '?'
            
            cursor.execute(f"SELECT id, username, password_hash, name, created_at, updated_at FROM admins WHERE username = {param_char}", (username,))
            row = cursor.fetchone()
            cursor.close()
            
            if not row:
                return None
                
            if isinstance(row, dict):
                return AdminUser(
                    id=row['id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    name=row['name'],
                    created_at=row.get('created_at'),
                    updated_at=row.get('updated_at')
                )
            else:
                return AdminUser(
                    id=row[0],
                    username=row[1],
                    password_hash=row[2],
                    name=row[3],
                    created_at=row[4] if len(row) > 4 else None,
                    updated_at=row[5] if len(row) > 5 else None
                )
        except Exception as e:
            logger.error(f"AdminRepository.get_by_username error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(admin_id: int) -> Optional[AdminUser]:
        conn = DatabaseManager.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            driver = DatabaseManager.get_driver()
            param_char = '%s' if driver == 'mysql' and hasattr(conn, 'cmd_query') else '?'
            
            cursor.execute(f"SELECT id, username, password_hash, name, created_at, updated_at FROM admins WHERE id = {param_char}", (admin_id,))
            row = cursor.fetchone()
            cursor.close()
            
            if not row:
                return None
                
            if isinstance(row, dict):
                return AdminUser(
                    id=row['id'],
                    username=row['username'],
                    password_hash=row['password_hash'],
                    name=row['name'],
                    created_at=row.get('created_at'),
                    updated_at=row.get('updated_at')
                )
            else:
                return AdminUser(
                    id=row[0],
                    username=row[1],
                    password_hash=row[2],
                    name=row[3],
                    created_at=row[4] if len(row) > 4 else None,
                    updated_at=row[5] if len(row) > 5 else None
                )
        except Exception as e:
            logger.error(f"AdminRepository.get_by_id error: {e}")
            return None
        finally:
            conn.close()
