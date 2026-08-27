from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Tuple
import os
import sqlite3
import pandas as pd
from collections import defaultdict

from server.src.config.config import Config
from server.database.connection.database import DatabaseManager
from server.src.config.logging_config import logger
from server.src.models.dosen.dosen_model import Dosen

class DosenRepositoryInterface(ABC):
    """Abstract interface for Lecturer data access."""
    
    @abstractmethod
    def get_all(self) -> List[Dosen]:
        pass

class SQLDosenRepository(DosenRepositoryInterface):
    """
    Retrieves and persists normalized relational lecturer profile data 
    from SQLite or MySQL without N+1 queries.
    """
    
    def get_all(self) -> List[Dosen]:
        conn = DatabaseManager.get_connection()
        if not conn:
            return []
            
        cursor = None
        is_sqlite = isinstance(conn, sqlite3.Connection)
        driver_name = 'sqlite' if is_sqlite else 'mysql'
        
        try:
            cursor = conn.cursor() if is_sqlite else conn.cursor(dictionary=True)
            
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
                
            logger.info(f"Berhasil memuat {len(dosen_list)} data dosen dari database relasional ({driver_name}).")
            return dosen_list
        except Exception as e:
            logger.error(f"Error query database relasional tabel dosen: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def save_batch(self, validated_records: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Saves a list of validated lecturer records with child relations atomically within a transaction.
        """
        conn = DatabaseManager.get_connection()
        if not conn:
            raise RuntimeError("Gagal membuka koneksi database untuk penyimpanan batch")
            
        is_sqlite = isinstance(conn, sqlite3.Connection)
        param_char = '?' if is_sqlite else '%s'
        cursor = conn.cursor()
        
        counts = {"dosen": 0, "publikasi": 0, "bimbingan": 0, "pengujian": 0}
        
        try:
            for item in validated_records:
                # 1. Insert master dosen
                cursor.execute(
                    f"INSERT INTO dosen (nidn, nama, program_studi, bidang_keahlian, pendidikan) "
                    f"VALUES ({param_char}, {param_char}, {param_char}, {param_char}, {param_char})",
                    (
                        item.get('nidn'),
                        item.get('nama'),
                        item.get('program_studi', 'Informatika'),
                        item.get('bidang_keahlian', ''),
                        item.get('pendidikan', '')
                    )
                )
                dosen_id = cursor.lastrowid
                counts["dosen"] += 1
                
                # 2. Insert publications
                for pub in item.get('publikasi', []):
                    if pub:
                        cursor.execute(
                            f"INSERT INTO publikasi (dosen_id, judul) VALUES ({param_char}, {param_char})",
                            (dosen_id, str(pub))
                        )
                        counts["publikasi"] += 1
                        
                # 3. Insert supervision history
                for bimb in item.get('riwayat_bimbingan', []):
                    if bimb:
                        cursor.execute(
                            f"INSERT INTO riwayat_bimbingan (dosen_id, judul_tugas_akhir, peran) "
                            f"VALUES ({param_char}, {param_char}, {param_char})",
                            (dosen_id, str(bimb), 'Pembimbing')
                        )
                        counts["bimbingan"] += 1
                        
                # 4. Insert examination history
                for uji in item.get('riwayat_pengujian', []):
                    if uji:
                        cursor.execute(
                            f"INSERT INTO riwayat_pengujian (dosen_id, judul_sidang, peran) "
                            f"VALUES ({param_char}, {param_char}, {param_char})",
                            (dosen_id, str(uji), 'Penguji')
                        )
                        counts["pengujian"] += 1
                        
            conn.commit()
            return counts
        except Exception as e:
            conn.rollback()
            logger.error(f"Gagal saat menyimpan data batch ke repository: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    def truncate_all(self):
        """Empties all lecturer and child relation tables atomically."""
        conn = DatabaseManager.get_connection()
        if not conn:
            raise RuntimeError("Gagal membuka koneksi database")
            
        is_sqlite = isinstance(conn, sqlite3.Connection)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM riwayat_pengujian;")
            cursor.execute("DELETE FROM riwayat_bimbingan;")
            cursor.execute("DELETE FROM publikasi;")
            cursor.execute("DELETE FROM dosen;")
            
            if is_sqlite:
                try:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('dosen', 'publikasi', 'riwayat_bimbingan', 'riwayat_pengujian');")
                except Exception:
                    pass
                    
            conn.commit()
            logger.info("Seluruh tabel relasional dosen berhasil dikosongkan.")
        except Exception as e:
            conn.rollback()
            logger.error(f"Gagal mengosongkan tabel relasional: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

# Backward compatibility alias
BaseDosenRepository = DosenRepositoryInterface
MySQLDosenRepository = SQLDosenRepository

class ExcelDosenRepository(DosenRepositoryInterface):
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

class CompositeDosenRepository(DosenRepositoryInterface):
    """Composite repository that queries relational SQL database first and gracefully falls back to Excel."""
    
    def __init__(self, sql_repo: DosenRepositoryInterface = None, excel_repo: DosenRepositoryInterface = None):
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
