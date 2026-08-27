from flask import Blueprint
from server.src.middleware.security_middleware import require_admin_key
from server.src.controllers.system.system_controller import SystemController

system_bp = Blueprint('system', __name__)

# Health check endpoint
@system_bp.route('/health', methods=['GET'])
def health_check():
    return SystemController.get_health()

# Status endpoints
@system_bp.route('/system/status', methods=['GET'])
@system_bp.route('/status', methods=['GET'])
def get_status():
    return SystemController.get_status()

# Runtime configuration endpoints
@system_bp.route('/system/config', methods=['GET'])
@system_bp.route('/config', methods=['GET'])
def get_config():
    return SystemController.get_config()

@system_bp.route('/system/config', methods=['PATCH', 'PUT'])
@system_bp.route('/config', methods=['PATCH', 'PUT'])
@require_admin_key
def update_config():
    return SystemController.update_config()

# System reload endpoint
@system_bp.route('/system/reload', methods=['POST'])
@require_admin_key
def reload_system():
    return SystemController.reload_system()
