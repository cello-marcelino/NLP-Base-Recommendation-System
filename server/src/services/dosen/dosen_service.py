from typing import List, Optional, Dict, Any
from server.src.models.dosen.dosen_model import Dosen
from server.src.repositories.dosen.dosen_repository import DosenRepositoryInterface, CompositeDosenRepository

class DosenService:
    """Service handling lecturer domain business logic."""
    
    def __init__(self, repository: Optional[DosenRepositoryInterface] = None):
        self.repository = repository or CompositeDosenRepository()

    def get_all_dosen(self) -> List[Dosen]:
        return self.repository.get_all()

    def get_dosen_by_nidn(self, nidn: str) -> Optional[Dosen]:
        all_dosen = self.get_all_dosen()
        for d in all_dosen:
            if d.nidn == nidn:
                return d
        return None
