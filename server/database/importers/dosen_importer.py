import os
import re
from typing import List, Dict, Any, Optional
import pandas as pd

from server.src.config.config import Config
from server.src.config.logging_config import logger
from server.src.repositories.dosen.dosen_repository import SQLDosenRepository

class DosenImporter:
    """
    Pipeline importing real data from external Excel datasets into relational tables.
    Flow: Excel -> DosenImporter -> Validation -> DosenRepository -> Database
    Follows rules/database.md.
    """
    
    def __init__(self, repository: Optional[SQLDosenRepository] = None):
        self.repository = repository or SQLDosenRepository()

    @staticmethod
    def parse_quoted_items(raw_val: Any) -> List[str]:
        """Parses titles enclosed in quotes or separated by semicolons."""
        if pd.isna(raw_val) or not str(raw_val).strip():
            return []
        s = str(raw_val).strip()
        if s == '-' or s.lower() in ('nan', 'null', 'none'):
            return []
            
        matches = re.findall(r'"([^"]+)"', s)
        if matches:
            return [m.strip() for m in matches if m.strip() and m.strip() != '-']
            
        parts = re.split(r'[,;]', s)
        return [p.strip() for p in parts if p.strip() and p.strip() != '-']

    def validate_and_transform_row(self, row: pd.Series, cols: Dict[str, str], index: int) -> Optional[Dict[str, Any]]:
        """Validates and standardizes a single row into a structured record."""
        def get_val(possible_names):
            for name in possible_names:
                if name in cols:
                    val = row[cols[name]]
                    return str(val).strip() if pd.notna(val) else ""
            return ""

        nama = get_val(['nama', 'nama dosen', 'nama lengkap'])
        if not nama:
            return None
            
        nidn = get_val(['nidn', 'id']) or None
        prodi = get_val(['program studi', 'prodi', 'program_studi']) or 'Informatika'
        keahlian = get_val(['bidang keahlian', 'keahlian', 'bidang_keahlian']) or ''
        pendidikan = get_val(['pendidikan', 'riwayat pendidikan', 'riwayat_pendidikan']) or ''
        
        publikasi = self.parse_quoted_items(get_val(['jurnal', 'publikasi']))
        bimbingan = self.parse_quoted_items(get_val(['judul bimbing', 'riwayat bimbing', 'judul bimbingan', 'judul_bimbing']))
        pengujian = self.parse_quoted_items(get_val(['judul uji', 'riwayat uji', 'judul ujian', 'judul_uji']))
        
        return {
            "nidn": nidn,
            "nama": nama,
            "program_studi": prodi,
            "bidang_keahlian": keahlian,
            "pendidikan": pendidikan,
            "publikasi": publikasi,
            "riwayat_bimbingan": bimbingan,
            "riwayat_pengujian": pengujian
        }

    def import_file(self, excel_path: str = None, truncate_first: bool = True) -> Dict[str, int]:
        """
        Executes complete import pipeline from Excel file.
        """
        excel_path = excel_path or Config.EXCEL_FALLBACK_PATH
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"File Excel dataset tidak ditemukan di: {excel_path}")
            
        logger.info(f"DosenImporter: Membaca file Excel dari {excel_path}...")
        df = pd.read_excel(excel_path)
        cols = {str(c).lower().strip(): c for c in df.columns}
        
        validated_records: List[Dict[str, Any]] = []
        for index, row in df.iterrows():
            record = self.validate_and_transform_row(row, cols, index)
            if record:
                validated_records.append(record)
                
        if not validated_records:
            logger.warning("DosenImporter: Tidak ada record valid yang berhasil diekstraksi dari Excel.")
            return {"dosen": 0, "publikasi": 0, "bimbingan": 0, "pengujian": 0}
            
        # Optionally truncate existing records
        if truncate_first:
            self.repository.truncate_all()
            
        # Delegate persistence to Repository (atomic batch transaction)
        counts = self.repository.save_batch(validated_records)
        logger.info(
            f"DosenImporter: Sukses mengimpor {counts['dosen']} Dosen, {counts['publikasi']} Publikasi, "
            f"{counts['bimbingan']} Bimbingan, {counts['pengujian']} Pengujian."
        )
        return counts

def import_dosen_dataset(excel_path: str = None) -> Dict[str, int]:
    """Convenience helper function to run DosenImporter."""
    importer = DosenImporter()
    return importer.import_file(excel_path)
