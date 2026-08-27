from server.src.config.response import ResponseFormatter
from server.src.exceptions.app_exceptions import ServiceUnavailableError
from server.src.services.system.cache_service import CacheService

class DosenController:
    """Handles HTTP requests for Dosen resources."""
    
    @staticmethod
    def get_all_dosen():
        cache = CacheService.get_instance()
        
        if not cache.is_ready:
            raise ServiceUnavailableError("Sistem sedang melakukan inisialisasi / warm-up model NLP")
            
        dosen_data = [d.to_dict() for d in cache.dosen_list]
        return ResponseFormatter.success(
            data=dosen_data,
            meta={"total": len(dosen_data)},
            message="Data dosen berhasil diambil"
        )
