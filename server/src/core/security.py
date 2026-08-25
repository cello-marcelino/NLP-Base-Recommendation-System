from functools import wraps
from flask import request, current_app, has_app_context
from server.src.core.config import Config
from server.src.core.exceptions import AuthenticationError

def require_admin_key(f):
    """
    Decorator to protect sensitive admin operations (e.g. PATCH config).
    Checks Authorization header (Bearer <key>) or X-API-Key header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        expected_key = current_app.config.get('ADMIN_API_KEY', Config.ADMIN_API_KEY) if has_app_context() else Config.ADMIN_API_KEY
        if not expected_key:
            return f(*args, **kwargs)
            
        auth_header = request.headers.get('Authorization', '')
        api_key_header = request.headers.get('X-API-Key', '')
        
        token = ""
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()
        elif api_key_header:
            token = api_key_header.strip()
            
        if not token or token != expected_key:
            raise AuthenticationError("Akses ditolak: API Key admin tidak valid atau tidak disertakan")
            
        return f(*args, **kwargs)
    return decorated_function
