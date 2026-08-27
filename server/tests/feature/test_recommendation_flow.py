def test_full_recommendation_feature_flow(client):
    """Feature test simulating end-to-end user recommendation flow."""
    # 1. Health check
    health_res = client.get('/health')
    assert health_res.status_code == 200
    
    # 2. Get Lecturer Catalog
    dosen_res = client.get('/api/dosen')
    assert dosen_res.status_code == 200
    assert len(dosen_res.get_json()["data"]) > 0
    
    # 3. Submit Thesis Proposal Query
    rec_res = client.post('/api/recommendations', json={
        "judul": "Analisis Sentimen Menggunakan Deep Learning Transformer BERT",
        "abstrak": "Penelitian teks mining klasifikasi opini publik pada media sosial",
        "k_rank": 2
    })
    assert rec_res.status_code == 200
    data = rec_res.get_json()["data"]
    assert len(data["recommendations"]) <= 2
    top_candidate = data["recommendations"][0]
    assert top_candidate["rank"] == 1
    assert "scores" in top_candidate
    assert "xai" in top_candidate
