from flask import Blueprint
from app.controllers.system_controller import SystemController

system_bp = Blueprint('system', __name__)

@system_bp.route('/status', methods=['GET'])
def get_status():
    return SystemController.get_status()

@system_bp.route('/config', methods=['GET'])
def get_config():
    return SystemController.get_config()

@system_bp.route('/config', methods=['PATCH', 'PUT'])
def update_config():
    return SystemController.update_config()

@system_bp.route('/dosen', methods=['GET'])
def get_dosen():
    return SystemController.get_dosen()
