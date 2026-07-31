from flask import request
from app.services.recommendation_service import RecommendationService
from app.utils.response_formatter import ResponseFormatter

class RecommendationController:
    @staticmethod
    def single_recommendation():
        data = request.json
        if not data:
            return ResponseFormatter.error("Request body is missing")
            
        judul = data.get('judul', '')
        abstrak = data.get('abstrak', '')
        k_rank = data.get('k_rank')
        
        if not judul and not abstrak:
            return ResponseFormatter.error("Judul atau abstrak harus diisi")
            
        try:
            result = RecommendationService.get_recommendations(judul, abstrak, k_rank)
            return ResponseFormatter.success(data=result)
        except Exception as e:
            return ResponseFormatter.error(str(e), status_code=500)
