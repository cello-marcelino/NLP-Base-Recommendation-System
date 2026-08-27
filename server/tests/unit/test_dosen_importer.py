import pandas as pd
from server.database.importers.dosen_importer import DosenImporter

def test_parse_quoted_items():
    raw_str = '"Sistem Temu Balik Informasi", "Analisis Sentimen"'
    parsed = DosenImporter.parse_quoted_items(raw_str)
    assert len(parsed) == 2
    assert "Sistem Temu Balik Informasi" in parsed
    assert "Analisis Sentimen" in parsed

def test_parse_quoted_items_empty_and_nan():
    assert DosenImporter.parse_quoted_items(None) == []
    assert DosenImporter.parse_quoted_items("-") == []
    assert DosenImporter.parse_quoted_items("nan") == []

def test_validate_and_transform_row():
    importer = DosenImporter()
    row = pd.Series({
        "nama": "Dr. Test Lecturer",
        "nidn": "001234",
        "prodi": "Informatika",
        "bidang_keahlian": "AI, NLP",
        "pendidikan": "S3",
        "jurnal": '"Publikasi 1", "Publikasi 2"',
        "judul_bimbing": '"Bimbingan 1"',
        "judul_uji": '"Pengujian 1"'
    })
    cols = {c: c for c in row.index}
    record = importer.validate_and_transform_row(row, cols, 0)
    
    assert record is not None
    assert record["nama"] == "Dr. Test Lecturer"
    assert record["nidn"] == "001234"
    assert len(record["publikasi"]) == 2
    assert len(record["riwayat_bimbingan"]) == 1
    assert len(record["riwayat_pengujian"]) == 1
