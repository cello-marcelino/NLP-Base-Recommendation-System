import os
import json
from typing import Dict, Any
from server.src.config.config import Config
from server.src.exceptions.app_exceptions import ValidationError
from server.src.config.logging_config import logger
from server.src.repositories.system.engine_config_repository import EngineConfigRepository

class ConfigService:
    """Manages dynamic runtime configuration stored in Database engine_configs table with JSON backup fallback."""
    
    # Default values hardcoded based on NLP optimization changelog
    DEFAULT_CONFIG: Dict[str, Any] = {
        "threshold": 0.3,
        "adaptive_alpha_threshold": 15,
        "is_adaptive": True,
        "manual_alpha": 0.7
    }
    
    ALLOWED_KEYS = {"threshold", "adaptive_alpha_threshold", "is_adaptive", "manual_alpha"}

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        # 1. Try reading from Database table engine_configs
        try:
            db_cfg = EngineConfigRepository.get_latest_config()
            if db_cfg:
                return db_cfg.to_dict()
        except Exception as e:
            logger.warning(f"Gagal membaca konfigurasi dari database: {e}. Mengalihkan ke file/default.")

        # 2. Fallback to JSON file or DEFAULT_CONFIG
        config_path = Config.CONFIG_JSON_PATH
        if not os.path.exists(config_path):
            return dict(cls.DEFAULT_CONFIG)
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                valid_saved = {k: v for k, v in saved_config.items() if k in cls.ALLOWED_KEYS}
                return {**cls.DEFAULT_CONFIG, **valid_saved}
        except (json.JSONDecodeError, OSError, IOError) as e:
            logger.warning(f"Gagal membaca file konfigurasi {config_path}: {e}. Menggunakan konfigurasi default.")
            return dict(cls.DEFAULT_CONFIG)

    @classmethod
    def validate_and_sanitize(cls, new_config: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(new_config, dict):
            raise ValidationError("Payload konfigurasi harus berupa JSON object")
            
        sanitized = {}
        for key, val in new_config.items():
            if key not in cls.ALLOWED_KEYS:
                continue
                
            if key == "threshold":
                try:
                    num_val = float(val)
                    if num_val < 0.0 or num_val > 1.0:
                        raise ValueError()
                    sanitized[key] = num_val
                except (ValueError, TypeError):
                    raise ValidationError("Field 'threshold' harus berupa angka desimal antara 0.0 dan 1.0")
                    
            elif key == "adaptive_alpha_threshold":
                try:
                    int_val = int(val)
                    if int_val < 1:
                        raise ValueError()
                    sanitized[key] = int_val
                except (ValueError, TypeError):
                    raise ValidationError("Field 'adaptive_alpha_threshold' harus berupa bilangan bulat positif (>= 1)")
                    
            elif key == "is_adaptive":
                if not isinstance(val, bool):
                    if str(val).lower() in ('true', '1'):
                        sanitized[key] = True
                    elif str(val).lower() in ('false', '0'):
                        sanitized[key] = False
                    else:
                        raise ValidationError("Field 'is_adaptive' harus berupa boolean (true/false)")
                else:
                    sanitized[key] = val
                    
            elif key == "manual_alpha":
                try:
                    num_val = float(val)
                    if not (0.0 <= num_val <= 1.0):
                        raise ValueError()
                    sanitized[key] = num_val
                except (ValueError, TypeError):
                    raise ValidationError("Field 'manual_alpha' harus berupa angka antara 0.0 sampai 1.0")
                    
        if not sanitized:
            raise ValidationError("Tidak ada parameter konfigurasi valid yang disertakan")
            
        return sanitized

    @classmethod
    def update_config(cls, new_config: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = cls.validate_and_sanitize(new_config)
        current = cls.get_config()
        updated = {**current, **sanitized}
        
        # 1. Save to Database
        try:
            saved_entity = EngineConfigRepository.save_config(updated)
            res_dict = saved_entity.to_dict()
        except Exception as e:
            logger.error(f"Gagal menyimpan konfigurasi ke database: {e}")
            res_dict = updated

        # 2. Save JSON file as backup
        config_path = Config.CONFIG_JSON_PATH
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(res_dict, f, indent=4)
        except (OSError, IOError) as e:
            logger.warning(f"Gagal menyimpan backup file JSON konfigurasi: {e}")
            
        logger.info(f"Konfigurasi runtime berhasil diperbarui: {sanitized}")
        return res_dict
