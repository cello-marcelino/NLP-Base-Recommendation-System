from flask import Blueprint
from server.src.controllers.dosen.dosen_controller import DosenController

dosen_bp = Blueprint('dosen', __name__)

@dosen_bp.route('/dosen', methods=['GET'])
def get_dosen_list():
    return DosenController.get_all_dosen()
