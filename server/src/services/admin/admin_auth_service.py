import hmac
import hashlib
import time
import base64
from typing import Dict, Any, Optional
from werkzeug.security import check_password_hash
from server.src.config.config import Config
from server.src.exceptions.app_exceptions import AuthenticationError, NotFoundError
from server.src.repositories.admin.admin_repository import AdminRepository
from server.src.config.logging_config import logger

class AdminAuthService:
    """Service handling Admin user authentication, token generation, and authorization checks."""
    
    @classmethod
    def generate_token(cls, admin_id: int, username: str) -> str:
        timestamp = int(time.time())
        raw_payload = f"{admin_id}:{username}:{timestamp}"
        signature = hmac.new(
            Config.SECRET_KEY.encode('utf-8'),
            raw_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        token_str = f"{raw_payload}:{signature}"
        return base64.urlsafe_b64encode(token_str.encode('utf-8')).decode('utf-8')

    @classmethod
    def verify_token(cls, token: str) -> Optional[Dict[str, Any]]:
        if not token or token == Config.ADMIN_API_KEY:
            return None
            
        try:
            decoded = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
            parts = decoded.split(':')
            if len(parts) != 4:
                return None
                
            admin_id_str, username, timestamp_str, signature = parts
            raw_payload = f"{admin_id_str}:{username}:{timestamp_str}"
            
            expected_signature = hmac.new(
                Config.SECRET_KEY.encode('utf-8'),
                raw_payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return None
                
            # Token expiration check (e.g., 24 hours = 86400 seconds)
            timestamp = int(timestamp_str)
            if time.time() - timestamp > 86400:
                return None
                
            return {
                "admin_id": int(admin_id_str),
                "username": username
            }
        except Exception as e:
            logger.warning(f"Failed to verify admin token: {e}")
            return None

    @classmethod
    def login(cls, username: str, password: str) -> Dict[str, Any]:
        if not username or not password:
            raise AuthenticationError("Username dan password wajib diisi")
            
        admin = AdminRepository.get_by_username(username.strip())
        if not admin:
            raise AuthenticationError("Username atau password salah")
            
        if not check_password_hash(admin.password_hash, password):
            raise AuthenticationError("Username atau password salah")
            
        token = cls.generate_token(admin.id, admin.username)
        logger.info(f"Admin '{admin.username}' berhasil login.")
        
        return {
            "token": token,
            "admin": admin.to_dict()
        }

    @classmethod
    def get_current_admin(cls, token: str) -> Dict[str, Any]:
        payload = cls.verify_token(token)
        if not payload:
            raise AuthenticationError("Sesi admin tidak valid atau sudah kadaluarsa")
            
        admin = AdminRepository.get_by_id(payload['admin_id'])
        if not admin:
            raise NotFoundError("Data akun admin tidak ditemukan")
            
        return admin.to_dict()
