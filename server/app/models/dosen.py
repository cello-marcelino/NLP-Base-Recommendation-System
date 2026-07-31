from dataclasses import dataclass
from typing import Optional

@dataclass
class Dosen:
    nidn: str
    nama: str
    program_studi: str
    bidang_keahlian: str
    jurnal: str
    judul_bimbing: str
    judul_uji: str
    pendidikan: str
    
    def to_dict(self):
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
