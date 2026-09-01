from flask import request
from server.src.config.response import ResponseFormatter
from server.src.exceptions.app_exceptions import ValidationError, NotFoundError, ServiceUnavailableError
from server.src.services.system.cache_service import CacheService
from server.src.repositories.dosen.dosen_repository import SQLDosenRepository

class AdminDosenController:
    """Controller for Admin Lecturer Data Management (CRUD)."""
    
    @staticmethod
    def get_all():
        cache = CacheService.get_instance()
        if not cache.is_ready:
            repo = SQLDosenRepository()
            dosen_list = [d.to_dict() for d in repo.get_all()]
        else:
            dosen_list = [d.to_dict() for d in cache.dosen_list]
            
        return ResponseFormatter.success(
            data=dosen_list,
            meta={"total": len(dosen_list)},
            message="Data dosen berhasil diambil"
        )

    @staticmethod
    def get_detail(dosen_id):
        cache = CacheService.get_instance()
        dosen_list = cache.dosen_list if cache.is_ready else SQLDosenRepository().get_all()
        
        target = None
        for d in dosen_list:
            if str(d.nidn) == str(dosen_id) or str(getattr(d, 'id', '')) == str(dosen_id):
                target = d
                break
                
        if not target:
            raise NotFoundError(f"Dosen dengan ID/NIDN {dosen_id} tidak ditemukan")
            
        return ResponseFormatter.success(data=target.to_dict(), message="Detail dosen berhasil diambil")

    @staticmethod
    def create():
        data = request.get_json(silent=True) or {}
        nama = data.get("nama")
        prodi = data.get("program_studi", "Teknik Informatika")
        
        if not nama:
            raise ValidationError("Nama dosen wajib diisi")
            
        record = {
            "nidn": data.get("nidn", ""),
            "nama": nama,
            "program_studi": prodi,
            "bidang_keahlian": data.get("bidang_keahlian", ""),
            "pendidikan": data.get("pendidikan", ""),
            "publikasi": data.get("publikasi", []),
            "riwayat_bimbingan": data.get("riwayat_bimbingan", []),
            "riwayat_pengujian": data.get("riwayat_pengujian", [])
        }
        
        repo = SQLDosenRepository()
        counts = repo.save_batch([record])
        
        # Refresh in-memory cache
        CacheService.get_instance().initialize_cache(force_refresh=True)
        
        return ResponseFormatter.success(data=counts, message="Data dosen baru berhasil disimpan")

    @staticmethod
    def update(dosen_id):
        data = request.get_json(silent=True) or {}
        nama = data.get("nama")
        if not nama:
            raise ValidationError("Nama dosen wajib diisi")
            
        record = {
            "nidn": data.get("nidn", ""),
            "nama": nama,
            "program_studi": data.get("program_studi", "Teknik Informatika"),
            "bidang_keahlian": data.get("bidang_keahlian", ""),
            "pendidikan": data.get("pendidikan", ""),
            "publikasi": data.get("publikasi", []),
            "riwayat_bimbingan": data.get("riwayat_bimbingan", []),
            "riwayat_pengujian": data.get("riwayat_pengujian", [])
        }
        
        repo = SQLDosenRepository()
        updated_id = repo.update_single(dosen_id, record)
        
        # Refresh in-memory cache
        CacheService.get_instance().initialize_cache(force_refresh=True)
        
        return ResponseFormatter.success(data={"id": updated_id}, message="Data dosen berhasil diperbarui")

    @staticmethod
    def delete(dosen_id):
        # Delete lecturer from database
        from server.database.connection.database import DatabaseManager
        conn = DatabaseManager.get_connection()
        if not conn:
            raise RuntimeError("Database connection error")
            
        try:
            cursor = conn.cursor()
            driver = DatabaseManager.get_driver()
            param_char = '%s' if driver == 'mysql' and hasattr(conn, 'cmd_query') else '?'
            
            cursor.execute(f"DELETE FROM dosen WHERE id = {param_char} OR nidn = {param_char}", (dosen_id, str(dosen_id)))
            conn.commit()
            cursor.close()
        finally:
            conn.close()
            
        # Refresh cache
        CacheService.get_instance().initialize_cache(force_refresh=True)
        return ResponseFormatter.success(data={"id": dosen_id}, message="Data dosen berhasil dihapus")
