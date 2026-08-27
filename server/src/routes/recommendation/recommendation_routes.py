from flask import Blueprint
from server.src.controllers.recommendation.recommendation_controller import RecommendationController

recommendation_bp = Blueprint('recommendation', __name__)

# Single recommendation routes
@recommendation_bp.route('/recommendations', methods=['POST'])
@recommendation_bp.route('/recommendations/single', methods=['POST'])
@recommendation_bp.route('/rekomendasi/single', methods=['POST'])
def single_recommendation():
    return RecommendationController.single_recommendation()

# Batch recommendation routes
@recommendation_bp.route('/recommendations/batch', methods=['POST'])
@recommendation_bp.route('/rekomendasi/batch', methods=['POST'])
def batch_recommendation():
    return RecommendationController.batch_recommendation()

# Batch upload Excel routes
@recommendation_bp.route('/recommendations/upload', methods=['POST'])
@recommendation_bp.route('/recommendations/batch/upload', methods=['POST'])
@recommendation_bp.route('/rekomendasi/batch/upload', methods=['POST'])
def batch_upload():
    return RecommendationController.batch_upload()

# SSE Stream recommendation routes
@recommendation_bp.route('/recommendations/stream', methods=['POST'])
@recommendation_bp.route('/rekomendasi/stream', methods=['POST'])
def stream_recommendation():
    return RecommendationController.stream_recommendation()
