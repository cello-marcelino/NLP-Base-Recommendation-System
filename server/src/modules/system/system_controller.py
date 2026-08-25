from flask import request
from server.src.core.config import Config
from server.src.core.response import ResponseFormatter
from server.src.core.exceptions import ValidationError
from server.src.modules.system.cache_service import CacheService
from server.src.modules.system.config_service import ConfigService

class SystemController:
    """Handles system status, health checks, and runtime configuration."""
    
    @staticmethod
    def get_status():
        cache = CacheService.get_instance()
        return ResponseFormatter.success(
            data={
                "status": "online",
                "app_name": Config.APP_NAME,
                "environment": Config.APP_ENV,
                "cache_ready": cache.is_ready,
                "total_dosen": len(cache.dosen_list) if cache.is_ready else 0
            },
            message="Sistem beroperasi normal"
        )

    @staticmethod
    def get_health():
        cache = CacheService.get_instance()
        status_code = 200 if cache.is_ready else 503
        return ResponseFormatter.success(
            data={
                "status": "healthy" if cache.is_ready else "warming_up",
                "cache_ready": cache.is_ready
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
