from server.src.core.response import ResponseFormatter
from server.src.core.exceptions import ServiceUnavailableError

class DosenController:
    """Handles HTTP requests for Dosen resources."""
    
    @staticmethod
    def get_all_dosen():
        from server.src.modules.system.cache_service import CacheService
        cache = CacheService.get_instance()
        
        if not cache.is_ready:
            raise ServiceUnavailableError("Sistem sedang melakukan inisialisasi / warm-up model NLP")
            
        dosen_data = [d.to_dict() for d in cache.dosen_list]
        return ResponseFormatter.success(
            data=dosen_data,
            meta={"total": len(dosen_data)},
            message="Data dosen berhasil diambil"
        )
