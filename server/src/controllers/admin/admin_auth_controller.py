from flask import request
from server.src.config.response import ResponseFormatter
from server.src.exceptions.app_exceptions import ValidationError
from server.src.services.admin.admin_auth_service import AdminAuthService

class AdminAuthController:
    """Controller for Admin Authentication endpoints."""
    
    @staticmethod
    def login():
        data = request.get_json(silent=True) or {}
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise ValidationError("Username dan password wajib diisi")
            
        result = AdminAuthService.login(username, password)
        return ResponseFormatter.success(data=result, message="Login admin berhasil")

    @staticmethod
    def get_me():
        auth_header = request.headers.get("Authorization", "")
        token = ""
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
        elif request.headers.get("X-API-Key"):
            token = request.headers.get("X-API-Key")
            
        admin_data = AdminAuthService.get_current_admin(token)
        return ResponseFormatter.success(data=admin_data, message="Data admin berhasil diambil")

    @staticmethod
    def logout():
        return ResponseFormatter.success(data={}, message="Logout admin berhasil")
