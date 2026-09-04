from flask import request
from server.src.config.config import Config
from server.src.config.response import ResponseFormatter
from server.src.exceptions.app_exceptions import ValidationError
from server.src.services.system.cache_service import CacheService
from server.src.services.system.config_service import ConfigService

class SystemController:
    """Handles system status, health checks, and runtime configuration."""
    
    @staticmethod
    def get_status():
        cache = CacheService.get_instance()
        state = "online" if cache.is_ready else cache.warmup_status.get("state", "warming_up")
        return ResponseFormatter.success(
            data={
                "status": state,
                "app_name": Config.APP_NAME,
                "environment": Config.APP_ENV,
                "cache_ready": cache.is_ready,
                "total_dosen": len(cache.dosen_list) if cache.is_ready else 0,
                "device": Config.TORCH_DEVICE.upper(),
                "warmup_status": cache.warmup_status
            },
            message="Status sistem berhasil diambil"
        )

    @staticmethod
    def get_health():
        cache = CacheService.get_instance()
        status_code = 200 if cache.is_ready else 503
        return ResponseFormatter.success(
            data={
                "status": "healthy" if cache.is_ready else "warming_up",
                "cache_ready": cache.is_ready,
                "warmup_status": cache.warmup_status
            },
            status_code=status_code,
            message="Health check"
        )

    @staticmethod
    def get_config():
        config = ConfigService.get_config()
        return ResponseFormatter.success(data=config, message="Konfigurasi sistem berhasil diambil")

    @staticmethod
    def update_config():
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            raise ValidationError("Request body harus berupa JSON object yang valid")
            
        updated = ConfigService.update_config(data)
        return ResponseFormatter.success(data=updated, message="Konfigurasi sistem berhasil diperbarui")

    @staticmethod
    def reload_system():
        cache = CacheService.get_instance()
        cache.initialize_cache_async(force_refresh=True)
        return ResponseFormatter.success(
            data={
                "status": "reloading",
                "cache_ready": False,
                "warmup_status": cache.warmup_status
            },
            message="Proses reload dan re-indexing NLP engine dimulai di background"
        )
