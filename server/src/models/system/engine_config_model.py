from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class EngineConfig:
    """Domain model representing NLP Engine Configuration entity."""
    threshold: float = 0.3
    adaptive_alpha_threshold: int = 15
    is_adaptive: bool = True
    manual_alpha: float = 0.7
    id: Optional[int] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "threshold": float(self.threshold),
            "adaptive_alpha_threshold": int(self.adaptive_alpha_threshold),
            "is_adaptive": bool(self.is_adaptive),
            "manual_alpha": float(self.manual_alpha)
        }
