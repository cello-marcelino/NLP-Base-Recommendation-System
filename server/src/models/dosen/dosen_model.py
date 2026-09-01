from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class Dosen:
    """Domain model representing a Lecturer (Dosen) entity."""
    nidn: str
    nama: str
    program_studi: str
    bidang_keahlian: str
    jurnal: str
    judul_bimbing: str
    judul_uji: str
    pendidikan: str
    id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nidn": self.nidn,
            "nama": self.nama,
            "program_studi": self.program_studi,
            "bidang_keahlian": self.bidang_keahlian,
            "jurnal": self.jurnal,
            "judul_bimbing": self.judul_bimbing,
            "judul_uji": self.judul_uji,
            "pendidikan": self.pendidikan
        }

@dataclass
class Publikasi:
    id: Optional[int] = None
    dosen_id: int = 0
    judul: str = ""
    tahun: Optional[int] = None
    penerbit: Optional[str] = None

@dataclass
class RiwayatBimbingan:
    id: Optional[int] = None
    dosen_id: int = 0
    judul_tugas_akhir: str = ""
    tahun: Optional[int] = None
    peran: str = "Pembimbing"

@dataclass
class RiwayatPengujian:
    id: Optional[int] = None
    dosen_id: int = 0
    judul_sidang: str = ""
    tahun: Optional[int] = None
    peran: str = "Penguji"
