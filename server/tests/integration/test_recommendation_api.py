import json

def test_single_recommendation_success(client):
    payload = {
        "judul": "Penerapan Natural Language Processing untuk Ekstraksi Informasi",
        "abstrak": "Penelitian menggunakan model BERT dan Text Mining untuk analisis teks bahasa Indonesia",
        "k_rank": 3
    }
    response = client.post('/api/recommendations', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "data" in data
    assert "recommendations" in data["data"]
    assert "metadata" in data["data"]
    assert "pipeline" in data["data"]

def test_single_recommendation_empty_input(client):
    response = client.post('/api/recommendations', json={"judul": "", "abstrak": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_batch_recommendation_success(client):
    payload = {
        "proposals": [
            {"id": "P01", "judul": "NLP Analisis Sentimen", "abstrak": "Penggunaan BERT"},
            {"id": "P02", "judul": "Deteksi Objek YOLO", "abstrak": "Computer vision untuk citra medis"}
        ]
    }
    response = client.post('/api/recommendations/batch', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 2
    assert data["data"][0]["id"] == "P01"

def test_batch_recommendation_limit_exceeded(client):
    # TestConfig MAX_BATCH_SIZE is 5
    oversized_proposals = [
        {"id": f"P{i}", "judul": f"Judul {i}", "abstrak": f"Abstrak {i}"}
        for i in range(10)
    ]
    response = client.post('/api/recommendations/batch', json={"proposals": oversized_proposals})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "BATCH_LIMIT_EXCEEDED"
