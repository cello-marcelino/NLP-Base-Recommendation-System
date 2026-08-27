from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class SingleRecommendationRequestDTO:
    judul: str
    abstrak: Optional[str] = None
    k: Optional[int] = 5
    program_studi: Optional[str] = None

@dataclass
class BatchProposalDTO:
    id: Optional[str]
    judul: str
    abstrak: Optional[str] = None

@dataclass
class BatchRecommendationRequestDTO:
    proposals: List[Dict[str, Any]]
    k: Optional[int] = 2
    program_studi: Optional[str] = None
