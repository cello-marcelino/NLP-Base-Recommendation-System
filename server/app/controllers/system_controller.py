from flask import request
from app.services.cache_service import CacheService
from app.storage.config_manager import ConfigManager
from app.utils.response_formatter import ResponseFormatter

class SystemController:
    @staticmethod
    def get_status():
        cache = CacheService.get_instance()
        return ResponseFormatter.success(data={
            "status": "online",
            "cache_ready": cache.is_ready,
            "total_dosen": len(cache.dosen_list) if cache.is_ready else 0
        })

    @staticmethod
    def get_config():
        config = ConfigManager.get_config()
        return ResponseFormatter.success(data=config)

    @staticmethod
    def update_config():
        data = request.json
        if not data:
            return ResponseFormatter.error("Request body missing")
            
        updated = ConfigManager.update_config(data)
        return ResponseFormatter.success(data=updated, message="Config updated")
        
    @staticmethod
    def get_dosen():
        cache = CacheService.get_instance()
        if not cache.is_ready:
            return ResponseFormatter.error("System is warming up", status_code=503)
            
        dosen_data = [d.to_dict() for d in cache.dosen_list]
        return ResponseFormatter.success(data=dosen_data)
