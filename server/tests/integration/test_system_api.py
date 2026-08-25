import json

def test_get_health(client):
    response = client.get('/health')
    assert response.status_code in (200, 503)
    data = response.get_json()
    assert data["success"] is True
    assert "status" in data["data"]

def test_get_system_status(client):
    response = client.get('/api/system/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["status"] == "online"
    assert data["data"]["total_dosen"] == 3

def test_get_dosen_list(client):
    response = client.get('/api/dosen')
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 3
    assert data["data"][0]["nama"] == "Dr. Andi Wijaya, M.Kom."

def test_get_and_patch_config(client):
    # Get config
    get_res = client.get('/api/system/config')
    assert get_res.status_code == 200
    assert get_res.get_json()["success"] is True
    
    # Patch config with valid API key
    patch_res = client.patch(
        '/api/system/config',
        headers={"X-API-Key": "test-admin-key"},
        json={"manual_alpha": 0.65}
    )
    assert patch_res.status_code == 200
    assert patch_res.get_json()["data"]["manual_alpha"] == 0.65

def test_patch_config_unauthorized(client):
    patch_res = client.patch(
        '/api/system/config',
        headers={"X-API-Key": "wrong-key"},
        json={"manual_alpha": 0.65}
    )
    assert patch_res.status_code == 401
    assert patch_res.get_json()["success"] is False
