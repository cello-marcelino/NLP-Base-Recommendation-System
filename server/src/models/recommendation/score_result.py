from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class RecommendationItem:
    rank: int
    nidn: str
    nama: str
    program_studi: str
    bidang_keahlian: str
    hybrid_score: float
    bm25_score: float
    sbert_score: float
    xai_highlights: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rank": self.rank,
            "nidn": self.nidn,
            "nama": self.nama,
            "program_studi": self.program_studi,
            "bidang_keahlian": self.bidang_keahlian,
            "hybrid_score": self.hybrid_score,
            "bm25_score": self.bm25_score,
            "sbert_score": self.sbert_score,
            "xai_highlights": self.xai_highlights
        }

@dataclass
class RecommendationResult:
    query: str
    total_candidates: int
    applied_alpha: float
    applied_beta: float
    recommendations: List[RecommendationItem]
    pipeline_logs: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "total_candidates": self.total_candidates,
            "applied_alpha": self.applied_alpha,
            "applied_beta": self.applied_beta,
            "recommendations": [item.to_dict() for item in self.recommendations],
            "pipeline_logs": self.pipeline_logs
        }
