from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class AdminUser:
    """Domain model representing an Admin User entity."""
    id: Optional[int]
    username: str
    password_hash: str
    name: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None
        }
