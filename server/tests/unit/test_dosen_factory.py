from server.database.factories.dosen_factory import DosenFactory
from server.src.models.dosen.dosen_model import Dosen

def test_dosen_factory_make_dosen():
    dosen = DosenFactory.make_dosen(index=1, prodi="Teknik Informatika")
    assert isinstance(dosen, Dosen)
    assert dosen.nidn == "000001"
    assert dosen.program_studi == "Teknik Informatika"
    assert len(dosen.nama) > 0
    assert len(dosen.bidang_keahlian) > 0

def test_dosen_factory_make_batch():
    batch = DosenFactory.make_batch(count=5)
    assert len(batch) == 5
    assert all(isinstance(d, Dosen) for d in batch)
    assert batch[0].nidn != batch[1].nidn

def test_dosen_factory_make_dict_record():
    record = DosenFactory.make_dict_record(index=2)
    assert isinstance(record, dict)
    assert "nidn" in record
    assert "publikasi" in record
    assert isinstance(record["publikasi"], list)
