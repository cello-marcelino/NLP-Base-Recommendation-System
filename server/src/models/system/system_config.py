from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class SystemConfig:
    adaptive_mode: bool = True
    manual_alpha: float = 0.50
    manual_beta: float = 0.50
    top_k_default: int = 5
    short_query_threshold: int = 15
    alpha_short: float = 0.70
    alpha_long: float = 0.35
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "adaptive_mode": self.adaptive_mode,
            "manual_alpha": self.manual_alpha,
            "manual_beta": self.manual_beta,
            "top_k_default": self.top_k_default,
            "short_query_threshold": self.short_query_threshold,
            "alpha_short": self.alpha_short,
            "alpha_long": self.alpha_long
        }
