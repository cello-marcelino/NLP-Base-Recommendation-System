import json
import pytest
from server.src.config.config import Config

def test_admin_dosen_crud_full_lifecycle(client):
    headers = {"X-API-Key": Config.ADMIN_API_KEY}
    
    # 1. CREATE
    create_payload = {
        "nidn": "TESTCRUD01",
        "nama": "Dr. Test CRUD, M.Kom",
        "program_studi": "Teknik Informatika",
        "bidang_keahlian": "Software Engineering, Cloud Computing",
        "pendidikan": "S1 Teknik Informatika, S2 Ilmu Komputer, S3 Rekayasa Perangkat Lunak",
        "publikasi": ["Paper Testing Alpha", "Paper Testing Beta"],
        "riwayat_bimbingan": ["Bimbingan Skripsi TA 1", "Bimbingan Skripsi TA 2"],
        "riwayat_pengujian": ["Sidang Mahasiswa Uji 1"]
    }
    create_res = client.post('/api/admin/dosen', json=create_payload, headers=headers)
    assert create_res.status_code == 200
    assert create_res.get_json()["success"] is True
    
    # 2. READ (Detail)
    read_res = client.get('/api/admin/dosen/TESTCRUD01', headers=headers)
    assert read_res.status_code == 200
    read_data = read_res.get_json()["data"]
    assert read_data["nidn"] == "TESTCRUD01"
    assert "Dr. Test CRUD" in read_data["nama"]
    assert "Paper Testing Alpha" in read_data["jurnal"]
    assert "Bimbingan Skripsi TA 1" in read_data["judul_bimbing"]
    assert "Sidang Mahasiswa Uji 1" in read_data["judul_uji"]
    
    # 3. UPDATE
    update_payload = {
        "nidn": "TESTCRUD01",
        "nama": "Prof. Dr. Test CRUD (Updated), M.Kom",
        "program_studi": "Sistem Informasi",
        "bidang_keahlian": "Distributed Systems",
        "pendidikan": "S1 TI, S2 IK, S3 RPL",
        "publikasi": ["Paper Testing Gamma"],
        "riwayat_bimbingan": ["Bimbingan Skripsi Updated"],
        "riwayat_pengujian": []
    }
    update_res = client.put('/api/admin/dosen/TESTCRUD01', json=update_payload, headers=headers)
    assert update_res.status_code == 200
    assert update_res.get_json()["success"] is True
    
    # Verify UPDATE
    read_updated_res = client.get('/api/admin/dosen/TESTCRUD01', headers=headers)
    assert read_updated_res.status_code == 200
    updated_data = read_updated_res.get_json()["data"]
    assert "Prof. Dr. Test CRUD (Updated)" in updated_data["nama"]
    assert updated_data["program_studi"] == "Sistem Informasi"
    assert "Paper Testing Gamma" in updated_data["jurnal"]
    assert "Paper Testing Alpha" not in updated_data["jurnal"]
    
    # 4. DELETE
    del_res = client.delete('/api/admin/dosen/TESTCRUD01', headers=headers)
    assert del_res.status_code == 200
    assert del_res.get_json()["success"] is True
    
    # Verify DELETED
    read_del_res = client.get('/api/admin/dosen/TESTCRUD01', headers=headers)
    assert read_del_res.status_code == 404
