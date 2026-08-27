from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class ConfigUpdateDTO:
    data: Dict[str, Any]
