from functools import wraps
from flask import request, current_app, has_app_context
from server.src.config.config import Config
from server.src.exceptions.app_exceptions import AuthenticationError

def require_admin_key(f):
    """Decorator to require X-API-Key or Authorization header matching ADMIN_API_KEY."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                api_key = auth_header.split(' ', 1)[1]
            else:
                api_key = auth_header
                
        expected_key = current_app.config.get('ADMIN_API_KEY', Config.ADMIN_API_KEY) if has_app_context() else Config.ADMIN_API_KEY
        if not api_key or api_key != expected_key:
            raise AuthenticationError("Akses ditolak: API Key admin tidak valid atau tidak disertakan")
            
        return f(*args, **kwargs)
    return decorated_function
