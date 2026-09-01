from typing import Optional, Dict, Any
from server.database.connection.database import DatabaseManager
from server.src.models.system.engine_config_model import EngineConfig
from server.src.config.logging_config import logger

class EngineConfigRepository:
    """Repository layer for engine_configs table."""
    
    @staticmethod
    def get_latest_config() -> Optional[EngineConfig]:
        conn = DatabaseManager.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, threshold, adaptive_alpha_threshold, is_adaptive, manual_alpha, updated_at FROM engine_configs ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            cursor.close()
            
            if not row:
                return None
                
            if isinstance(row, dict):
                return EngineConfig(
                    id=row['id'],
                    threshold=float(row['threshold']),
                    adaptive_alpha_threshold=int(row['adaptive_alpha_threshold']),
                    is_adaptive=bool(row['is_adaptive']),
                    manual_alpha=float(row['manual_alpha']),
                    updated_at=str(row.get('updated_at'))
                )
            else:
                return EngineConfig(
                    id=row[0],
                    threshold=float(row[1]),
                    adaptive_alpha_threshold=int(row[2]),
                    is_adaptive=bool(row[3]),
                    manual_alpha=float(row[4]),
                    updated_at=str(row[5]) if len(row) > 5 else None
                )
        except Exception as e:
            logger.error(f"EngineConfigRepository.get_latest_config error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def save_config(config_data: Dict[str, Any]) -> EngineConfig:
        conn = DatabaseManager.get_connection()
        if not conn:
            raise RuntimeError("Database connection not available")
            
        try:
            cursor = conn.cursor()
            driver = DatabaseManager.get_driver()
            param_char = '%s' if driver == 'mysql' and hasattr(conn, 'cmd_query') else '?'
            
            existing = EngineConfigRepository.get_latest_config()
            threshold = float(config_data.get('threshold', 0.3))
            adaptive_alpha = int(config_data.get('adaptive_alpha_threshold', 15))
            is_adaptive = 1 if config_data.get('is_adaptive', True) else 0
            manual_alpha = float(config_data.get('manual_alpha', 0.7))
            
            if existing and existing.id:
                sql = f"UPDATE engine_configs SET threshold={param_char}, adaptive_alpha_threshold={param_char}, is_adaptive={param_char}, manual_alpha={param_char} WHERE id={param_char}"
                cursor.execute(sql, (threshold, adaptive_alpha, is_adaptive, manual_alpha, existing.id))
            else:
                sql = f"INSERT INTO engine_configs (threshold, adaptive_alpha_threshold, is_adaptive, manual_alpha) VALUES ({param_char}, {param_char}, {param_char}, {param_char})"
                cursor.execute(sql, (threshold, adaptive_alpha, is_adaptive, manual_alpha))
                
            conn.commit()
            cursor.close()
            
            return EngineConfig(
                threshold=threshold,
                adaptive_alpha_threshold=adaptive_alpha,
                is_adaptive=bool(is_adaptive),
                manual_alpha=manual_alpha
            )
        except Exception as e:
            logger.error(f"EngineConfigRepository.save_config error: {e}")
            raise e
        finally:
            conn.close()
