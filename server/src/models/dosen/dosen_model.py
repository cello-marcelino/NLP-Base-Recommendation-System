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
    
    def to_dict(self) -> Dict[str, Any]:
        return {
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
    id: Optional[int]
    dosen_id: int
    judul: str
    tahun: Optional[int]
    penerbit: Optional[str]

@dataclass
class RiwayatBimbingan:
    id: Optional[int]
    dosen_id: int
    judul_tugas_akhir: str
    tahun: Optional[int]
    peran: str = "Pembimbing"

@dataclass
class RiwayatPengujian:
    id: Optional[int]
    dosen_id: int
    judul_sidang: str
    tahun: Optional[int]
    peran: str = "Penguji"
