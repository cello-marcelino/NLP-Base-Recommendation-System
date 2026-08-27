from typing import List, Dict, Any, Optional
from flask import current_app, has_app_context
from server.src.config.config import Config
from server.src.exceptions.app_exceptions import BatchLimitExceededError, ValidationError
from server.src.services.recommendation.recommendation_service import RecommendationService

class BatchService:
    """Processes bulk recommendation requests with batch limit constraints."""
    
    DEFAULT_BATCH_K_RANK = 2
    
    @staticmethod
    def process_batch(proposals: List[Dict[str, Any]], global_k_rank: Optional[int] = None) -> List[Dict[str, Any]]:
        if not isinstance(proposals, list):
            raise ValidationError("Payload batch proposals harus berupa JSON array")
            
        total_proposals = len(proposals)
        if total_proposals == 0:
            return []
            
        max_batch_size = current_app.config.get('MAX_BATCH_SIZE', Config.MAX_BATCH_SIZE) if has_app_context() else Config.MAX_BATCH_SIZE
        if total_proposals > max_batch_size:
            raise BatchLimitExceededError(max_limit=max_batch_size, actual_count=total_proposals)
            
        results = []
        for index, p in enumerate(proposals):
            if not isinstance(p, dict):
                continue
                
            id_ = str(p.get('id', index + 1))
            judul = str(p.get('judul', '') or '')
            abstrak = str(p.get('abstrak', '') or '')
            k_rank = p.get('k_rank') or global_k_rank or BatchService.DEFAULT_BATCH_K_RANK
            
            recom = RecommendationService.get_recommendations(judul, abstrak, k_rank)
            
            results.append({
                "id": id_,
                "judul": judul,
                "rekomendasi": recom
            })
            
        return results
