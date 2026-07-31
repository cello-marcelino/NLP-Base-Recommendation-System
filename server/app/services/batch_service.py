from typing import List, Dict, Any
from app.services.recommendation_service import RecommendationService

class BatchService:
    @staticmethod
    def process_batch(proposals: List[Dict[str, Any]], global_k_rank: int = None) -> List[Dict[str, Any]]:
        results = []
        for p in proposals:
            id_ = p.get('id', '')
            judul = p.get('judul', '')
            abstrak = p.get('abstrak', '')
            k_rank = p.get('k_rank') or global_k_rank
            
            recom = RecommendationService.get_recommendations(judul, abstrak, k_rank)
            
            results.append({
                "id": id_,
                "judul": judul,
                "rekomendasi": recom
            })
        return results
