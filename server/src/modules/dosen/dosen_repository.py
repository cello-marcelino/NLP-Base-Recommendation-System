from abc import ABC, abstractmethod
from typing import List
import os
import pandas as pd
from mysql.connector import Error

from server.src.core.config import Config
from server.src.core.database import DatabaseManager
from server.src.core.logging import logger
from server.src.modules.dosen.dosen_model import Dosen

class BaseDosenRepository(ABC):
    """Abstract base repository for Dosen data source."""
    
    @abstractmethod
    def get_all(self) -> List[Dosen]:
        pass

class MySQLDosenRepository(BaseDosenRepository):
    """Retrieves lecturer profile data from MySQL."""
    
    def get_all(self) -> List[Dosen]:
        connection = DatabaseManager.get_connection()
        if not connection or not connection.is_connected():
            return []
            
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM dosen")
            records = cursor.fetchall()
            
            dosen_list = []
            for row in records:
                dosen_list.append(Dosen(
                    nidn=str(row.get('nidn', '') or ''),
                    nama=str(row.get('nama', '') or ''),
                    program_studi=str(row.get('program_studi', '') or ''),
                    bidang_keahlian=str(row.get('bidang_keahlian', '') or ''),
                    jurnal=str(row.get('jurnal', '') or ''),
                    judul_bimbing=str(row.get('judul_bimbing', '') or ''),
                    judul_uji=str(row.get('judul_uji', '') or ''),
                    pendidikan=str(row.get('pendidikan', '') or '')
                ))
            logger.info(f"Berhasil memuat {len(dosen_list)} data dosen dari MySQL.")
            return dosen_list
        except Error as e:
            logger.error(f"Error query MySQL tabel dosen: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

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
                if dosen.nama:  # Only add valid rows with lecturer name
                    dosen_list.append(dosen)
                    
            logger.info(f"Berhasil memuat {len(dosen_list)} data dosen dari Excel fallback ({self.excel_path}).")
            return dosen_list
        except Exception as e:
            logger.error(f"Gagal membaca Excel dataset fallback: {e}")
            return []

class CompositeDosenRepository(BaseDosenRepository):
    """Composite repository that tries MySQL first and gracefully falls back to Excel."""
    
    def __init__(self, mysql_repo: BaseDosenRepository = None, excel_repo: BaseDosenRepository = None):
        self.mysql_repo = mysql_repo or MySQLDosenRepository()
        self.excel_repo = excel_repo or ExcelDosenRepository()

    def get_all(self) -> List[Dosen]:
        # 1. Try MySQL
        dosen_list = self.mysql_repo.get_all()
        if dosen_list:
            return dosen_list
            
        # 2. Fallback to Excel
        logger.info("Mengaktifkan fallback ke Excel dataset...")
        return self.excel_repo.get_all()
