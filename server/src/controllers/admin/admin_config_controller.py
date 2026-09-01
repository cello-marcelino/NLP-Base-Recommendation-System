from flask import request
from server.src.config.response import ResponseFormatter
from server.src.exceptions.app_exceptions import ValidationError
from server.src.services.system.config_service import ConfigService

class AdminConfigController:
    """Controller for Admin NLP Engine Configuration."""
    
    @staticmethod
    def get_config():
        config = ConfigService.get_config()
        return ResponseFormatter.success(data=config, message="Konfigurasi NLP engine berhasil diambil")

    @staticmethod
    def update_config():
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            raise ValidationError("Request body harus berupa JSON object yang valid")
            
        updated = ConfigService.update_config(data)
        return ResponseFormatter.success(data=updated, message="Konfigurasi NLP engine berhasil diperbarui")
