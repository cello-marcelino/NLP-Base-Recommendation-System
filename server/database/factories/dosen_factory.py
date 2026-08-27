import random
from typing import Dict, Any, List
from server.src.models.dosen.dosen_model import Dosen

class DosenFactory:
    """
    Factory generating mock/dummy lecturer records for unit testing and load testing.
    Follows rules/database.md.
    """
    
    FIRST_NAMES = ["Andi", "Budi", "Citra", "Dewi", "Eko", "Fajar", "Gita", "Hadi", "Indra", "Joko", "Kartika", "Lukman"]
    LAST_NAMES = ["Wijaya", "Santoso", "Lestari", "Pratama", "Kusuma", "Hidayat", "Saputra", "Wibowo", "Nugroho", "Siregar"]
    TITLES = ["M.Kom.", "M.T.", "Ph.D.", "Dr.", "Prof. Dr."]
    
    BIDANG_LIST = [
        "Natural Language Processing, Text Mining, Machine Learning",
        "Computer Vision, Deep Learning, Pengolahan Citra",
        "Decision Support System, SPK, AHP, TOPSIS",
        "Software Engineering, Agile, SDLC, Pengujian Perangkat Lunak",
        "Cyber Security, Kriptografi, Network Security",
        "Internet of Things, Embedded System, Mikrokontroler",
        "Data Mining, Knowledge Discovery, Clustering"
    ]
    
    PUBLIKASI_TEMPLATES = [
        "Analisis Algoritma {topik} Berbasis {metode}",
        "Penerapan Model {metode} untuk {topik}",
        "Studi Komparasi Kinerja {metode} pada Domain {topik}",
        "Optimasi Ekstraksi Fitur pada {topik} Menggunakan {metode}"
    ]
    
    TOPICS = ["Sentimen Analisis", "Klasifikasi Citra", "Deteksi Objek", "Sistem Pendukung Keputusan", "Prediksi Penjualan"]
    METHODS = ["BERT", "YOLOv8", "Deep Learning", "AHP & TOPSIS", "Random Forest", "Transformer"]

    @classmethod
    def make_dosen(cls, index: int = 1, prodi: str = "Teknik Informatika") -> Dosen:
        """Instantiates a Dosen domain model with realistic dummy values."""
        name = f"{random.choice(cls.FIRST_NAMES)} {random.choice(cls.LAST_NAMES)}, {random.choice(cls.TITLES)}"
        nidn = f"00{index:04d}"
        bidang = random.choice(cls.BIDANG_LIST)
        
        topik = random.choice(cls.TOPICS)
        metode = random.choice(cls.METHODS)
        jurnal = f'"{random.choice(cls.PUBLIKASI_TEMPLATES).format(topik=topik, metode=metode)}"'
        bimbing = f'"{random.choice(cls.PUBLIKASI_TEMPLATES).format(topik=random.choice(cls.TOPICS), metode=random.choice(cls.METHODS))}"'
        uji = f'"{random.choice(cls.PUBLIKASI_TEMPLATES).format(topik=random.choice(cls.TOPICS), metode=random.choice(cls.METHODS))}"'
        
        return Dosen(
            nidn=nidn,
            nama=name,
            program_studi=prodi,
            bidang_keahlian=bidang,
            jurnal=jurnal,
            judul_bimbing=bimbing,
            judul_uji=uji,
            pendidikan="S2/S3 Ilmu Komputer"
        )

    @classmethod
    def make_batch(cls, count: int = 5, prodi: str = "Teknik Informatika") -> List[Dosen]:
        """Generates a batch of N dummy Dosen domain models."""
        return [cls.make_dosen(index=i + 1, prodi=prodi) for i in range(count)]

    @classmethod
    def make_dict_record(cls, index: int = 1) -> Dict[str, Any]:
        """Generates raw dictionary representation matching importer format."""
        dosen = cls.make_dosen(index=index)
        return {
            "nidn": dosen.nidn,
            "nama": dosen.nama,
            "program_studi": dosen.program_studi,
            "bidang_keahlian": dosen.bidang_keahlian,
            "pendidikan": dosen.pendidikan,
            "publikasi": [dosen.jurnal.strip('"')],
            "riwayat_bimbingan": [dosen.judul_bimbing.strip('"')],
            "riwayat_pengujian": [dosen.judul_uji.strip('"')]
        }

    @classmethod
    def make_dict_batch(cls, count: int = 5) -> List[Dict[str, Any]]:
        return [cls.make_dict_record(index=i + 1) for i in range(count)]
