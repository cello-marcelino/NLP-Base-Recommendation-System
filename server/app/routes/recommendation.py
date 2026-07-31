from flask import Blueprint, Response, stream_with_context, request
from app.controllers.recommendation_controller import RecommendationController
import json
import time

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/single', methods=['POST'])
def single_recommendation():
    return RecommendationController.single_recommendation()

@recommendation_bp.route('/stream', methods=['POST'])
def stream_recommendation():
    data = request.json or {}
    
    def generate():
        # SSE format
        yield f"data: {json.dumps({'step': 1, 'message': 'Preprocessing started'})}\n\n"
        time.sleep(0.5)
        
        yield f"data: {json.dumps({'step': 2, 'message': 'BM25 scoring completed'})}\n\n"
        time.sleep(0.5)
        
        yield f"data: {json.dumps({'step': 3, 'message': 'SBERT semantic completed'})}\n\n"
        time.sleep(0.5)
        
        # We process the actual logic here (or pass data to service)
        # Simplified for now, just to show SSE capability
        # Normally you would yield progress from within the service
        
        try:
            # We call the normal single recommendation to get result
            # Assuming we can get request data here if it wasn't consumed
            result_tuple = RecommendationController.single_recommendation()
            result_data = result_tuple[0].json
            yield f"data: {json.dumps({'step': 4, 'message': 'Ranking selesai', 'result': result_data})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'step': 4, 'error': str(e)})}\n\n"
            
    return Response(stream_with_context(generate()), mimetype="text/event-stream")
