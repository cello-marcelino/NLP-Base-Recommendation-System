from flask import Blueprint
from app.controllers.batch_controller import BatchController

batch_bp = Blueprint('batch', __name__)

@batch_bp.route('/batch', methods=['POST'])
def batch_recommendation():
    return BatchController.batch_recommendation()

@batch_bp.route('/batch/upload', methods=['POST'])
def batch_recommendation_upload():
    return BatchController.batch_upload()
