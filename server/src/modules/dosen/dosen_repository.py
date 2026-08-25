from abc import ABC, abstractmethod
from typing import List, Dict
import os
import pandas as pd
from collections import defaultdict

from server.src.core.config import Config
from server.src.core.database import DatabaseManager
from server.src.core.logging import logger
from server.src.modules.dosen.dosen_model import Dosen

class BaseDosenRepository(ABC):
    """Abstract base repository for Dosen data source."""
    
    @abstractmethod
    def get_all(self) -> List[Dosen]:
        pass

class SQLDosenRepository(BaseDosenRepository):
    """Retrieves normalized relational lecturer profile data from SQLite or MySQL without N+1 queries."""
    
    def get_all(self) -> List[Dosen]:
        conn = DatabaseManager.get_connection()
        if not conn:
            return []
            
        cursor = None
        try:
            driver = DatabaseManager.get_driver()
            cursor = conn.cursor(dictionary=True) if driver == 'mysql' else conn.cursor()
            
            # 1. Fetch all lecturers
            cursor.execute("SELECT id, nidn, nama, program_studi, bidang_keahlian, pendidikan FROM dosen ORDER BY id ASC")
            dosen_rows = cursor.fetchall()
            
            if not dosen_rows:
                return []
                
            # 2. Batch fetch child relational tables (zero N+1 queries)
            cursor.execute("SELECT dosen_id, judul FROM publikasi ORDER BY id ASC")
            pub_rows = cursor.fetchall()
            publikasi_map: Dict[int, List[str]] = defaultdict(list)
            for r in pub_rows:
                d_id = r['dosen_id'] if isinstance(r, dict) or hasattr(r, 'keys') else r[0]
                j_title = r['judul'] if isinstance(r, dict) or hasattr(r, 'keys') else r[1]
                if j_title:
                    publikasi_map[d_id].append(str(j_title))
                    
            cursor.execute("SELECT dosen_id, judul_tugas_akhir FROM riwayat_bimbingan ORDER BY id ASC")
            bimb_rows = cursor.fetchall()
            bimbingan_map: Dict[int, List[str]] = defaultdict(list)
            for r in bimb_rows:
                d_id = r['dosen_id'] if isinstance(r, dict) or hasattr(r, 'keys') else r[0]
                b_title = r['judul_tugas_akhir'] if isinstance(r, dict) or hasattr(r, 'keys') else r[1]
                if b_title:
                    bimbingan_map[d_id].append(str(b_title))
                    
            cursor.execute("SELECT dosen_id, judul_sidang FROM riwayat_pengujian ORDER BY id ASC")
            uji_rows = cursor.fetchall()
            pengujian_map: Dict[int, List[str]] = defaultdict(list)
            for r in uji_rows:
                d_id = r['dosen_id'] if isinstance(r, dict) or hasattr(r, 'keys') else r[0]
                u_title = r['judul_sidang'] if isinstance(r, dict) or hasattr(r, 'keys') else r[1]
                if u_title:
                    pengujian_map[d_id].append(str(u_title))

            # 3. Assemble Dosen domain models
            def format_list_to_quoted_str(items: List[str]) -> str:
                if not items:
                    return ""
                return ', '.join([f'"{item}"' for item in items])

            dosen_list = []
            for row in dosen_rows:
                d_id = row['id'] if isinstance(row, dict) or hasattr(row, 'keys') else row[0]
                nidn = row['nidn'] if isinstance(row, dict) or hasattr(row, 'keys') else row[1]
                nama = row['nama'] if isinstance(row, dict) or hasattr(row, 'keys') else row[2]
                prodi = row['program_studi'] if isinstance(row, dict) or hasattr(row, 'keys') else row[3]
                keahlian = row['bidang_keahlian'] if isinstance(row, dict) or hasattr(row, 'keys') else row[4]
                pendidikan = row['pendidikan'] if isinstance(row, dict) or hasattr(row, 'keys') else row[5]
                
                jurnal_str = format_list_to_quoted_str(publikasi_map.get(d_id, []))
                bimb_str = format_list_to_quoted_str(bimbingan_map.get(d_id, []))
                uji_str = format_list_to_quoted_str(pengujian_map.get(d_id, []))
                
                dosen_list.append(Dosen(
                    nidn=str(nidn or ''),
                    nama=str(nama or ''),
                    program_studi=str(prodi or ''),
                    bidang_keahlian=str(keahlian or ''),
                    jurnal=jurnal_str,
                    judul_bimbing=bimb_str,
                    judul_uji=uji_str,
                    pendidikan=str(pendidikan or '')
                ))
                
            logger.info(f"Berhasil memuat {len(dosen_list)} data dosen dari database relasional ({driver}).")
            return dosen_list
        except Exception as e:
            logger.error(f"Error query database relasional tabel dosen: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Backward compatibility alias
MySQLDosenRepository = SQLDosenRepository

class ExcelDosenRepository(BaseDosenRepository):
    """Retrieves lecturer profile data from fallback Excel file."""
    
    def __init__(self, excel_path: str = None):
        self.excel_path = excel_path or Config.EXCEL_FALLBACK_PATH

    def get_all(self) -> List[Dosen]:
        if not os.path.exists(self.excel_path):
            logger.error(f"File Excel dataset tidak ditemukan di: {self.excel_path}")
            return []
            
        try:
            df = pd.read_excel(self.excel_path)
            cols = {str(c).lower().strip(): c for c in df.columns}
            
            def get_val(row, possible_names):
                for name in possible_names:
                    if name in cols:
                        val = row[cols[name]]
                        return str(val).strip() if pd.notna(val) else ""
                return ""

            dosen_list = []
            for _, row in df.iterrows():
                dosen = Dosen(
                    nidn=get_val(row, ['nidn', 'id']),
                    nama=get_val(row, ['nama', 'nama dosen', 'nama lengkap']),
                    program_studi=get_val(row, ['program studi', 'prodi', 'program_studi']),
                    bidang_keahlian=get_val(row, ['bidang keahlian', 'keahlian', 'bidang_keahlian']),
                    jurnal=get_val(row, ['jurnal', 'publikasi']),
                    judul_bimbing=get_val(row, ['judul bimbing', 'riwayat bimbing', 'judul bimbingan', 'judul_bimbing']),
                    judul_uji=get_val(row, ['judul uji', 'riwayat uji', 'judul ujian', 'judul_uji']),
                    pendidikan=get_val(row, ['pendidikan', 'riwayat pendidikan', 'riwayat_pendidikan'])
                )
                if dosen.nama:
                    dosen_list.append(dosen)
                    
            logger.info(f"Berhasil memuat {len(dosen_list)} data dosen dari Excel fallback ({self.excel_path}).")
            return dosen_list
        except Exception as e:
            logger.error(f"Gagal membaca Excel dataset fallback: {e}")
            return []

class CompositeDosenRepository(BaseDosenRepository):
    """Composite repository that queries relational SQL database first and gracefully falls back to Excel."""
    
    def __init__(self, sql_repo: BaseDosenRepository = None, excel_repo: BaseDosenRepository = None):
        self.sql_repo = sql_repo or SQLDosenRepository()
        self.excel_repo = excel_repo or ExcelDosenRepository()

    def get_all(self) -> List[Dosen]:
        # 1. Try SQL database (SQLite/MySQL)
        dosen_list = self.sql_repo.get_all()
        if dosen_list:
            return dosen_list
            
        # 2. Fallback to Excel
        logger.info("Mengaktifkan fallback ke Excel dataset...")
        return self.excel_repo.get_all()
