"""
Test sederhana untuk server/app.py
Jalankan dengan: pytest test_api.py -v
"""

import sys
import os
import numpy as np
from unittest.mock import MagicMock, patch

SERVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "server"))
sys.path.insert(0, SERVER_DIR)

# --- mock library berat SEBELUM app.py (yang import rekomendasi.py) di-import ---
mock_sbert_instance = MagicMock()
mock_sbert_instance.encode.side_effect = lambda teks, convert_to_numpy=True: (
    np.random.rand(len(teks), 384) if isinstance(teks, list) else np.random.rand(384)
)
mock_kw_instance = MagicMock()
mock_kw_instance.extract_keywords.return_value = [[("kecerdasan buatan", 0.8)]]

sys.modules["sentence_transformers"] = MagicMock(SentenceTransformer=lambda *a, **k: mock_sbert_instance)
sys.modules["keybert"] = MagicMock(KeyBERT=lambda *a, **k: mock_kw_instance)

# --- cegah thread background asli (muat_mesin_ai) jalan saat import app ---
with patch("threading.Thread"):
    import app as app_module  # noqa: E402

app_module.app.config["TESTING"] = True
client = app_module.app.test_client()


# =========================================================
# /api/status
# =========================================================

def test_status_mengembalikan_200():
    resp = client.get("/api/status")
    assert resp.status_code == 200
    body = resp.get_json()
    assert "ready" in body
    assert "progress" in body


# =========================================================
# /api/dosen
# =========================================================

def test_daftar_dosen_mengembalikan_data():
    with patch.object(app_module, "dapatkan_data_dosen_terintegrasi", return_value=[{"NAMA": "Dr. A"}]):
        resp = client.get("/api/dosen")
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "sukses"
        assert body["total_data"] == 1


# =========================================================
# /api/rekomendasi
# =========================================================

def test_rekomendasi_gagal_503_jika_belum_ready():
    app_module.status_server["ready"] = False
    resp = client.post("/api/rekomendasi", json={"judul": "NLP", "abstrak": "chatbot"})
    assert resp.status_code == 503
    assert resp.get_json()["status"] == "gagal"


def test_rekomendasi_gagal_400_jika_judul_abstrak_kosong():
    app_module.status_server["ready"] = True
    resp = client.post("/api/rekomendasi", json={})
    assert resp.status_code == 400


def test_rekomendasi_sukses_200():
    app_module.status_server["ready"] = True
    with patch.object(
        app_module.engine,
        "jalankan_pipeline",
        return_value={"hasil_rekomendasi": [{"NAMA": "Dr. A", "Hybrid Score": 0.9}]},
    ):
        resp = client.post("/api/rekomendasi", json={"judul": "NLP", "abstrak": "chatbot"})
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["status"] == "sukses"
        assert body["data"]["hasil_rekomendasi"][0]["NAMA"] == "Dr. A"


def test_rekomendasi_gagal_500_jika_engine_error():
    app_module.status_server["ready"] = True
    with patch.object(app_module.engine, "jalankan_pipeline", side_effect=Exception("boom")):
        resp = client.post("/api/rekomendasi", json={"judul": "NLP", "abstrak": "chatbot"})
        assert resp.status_code == 500


# =========================================================
# /api/refresh
# =========================================================

def test_refresh_gagal_400_jika_mysql_kosong():
    with patch.object(app_module.DataLayer, "fetch_all_dosen", return_value=[]):
        resp = client.post("/api/refresh")
        assert resp.status_code == 400


def test_refresh_sukses_200():
    with patch.object(app_module.DataLayer, "fetch_all_dosen", return_value=[{"NAMA": "Dr. A"}]), \
         patch.object(app_module.engine, "siapkan_cache", return_value=None):
        resp = client.post("/api/refresh")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "sukses"


# =========================================================
# Tambahan: dapatkan_data_dosen_terintegrasi() - MySQL vs fallback Excel
# =========================================================

def test_dapatkan_data_dosen_pakai_mysql_jika_tersedia():
    data_mysql = [{"NAMA": "Dr. MySQL"}]
    with patch.object(app_module.DataLayer, "fetch_all_dosen", return_value=data_mysql):
        hasil = app_module.dapatkan_data_dosen_terintegrasi()
        assert hasil == data_mysql


def test_dapatkan_data_dosen_fallback_ke_excel_jika_mysql_gagal():
    import pandas as pd

    fake_df = pd.DataFrame([{"NAMA": "Dr. Excel", "BIDANG_KEAHLIAN": "AI"}])

    with patch.object(app_module.DataLayer, "fetch_all_dosen", side_effect=Exception("MySQL down")), \
         patch("app.pd.read_excel", return_value=fake_df) as mock_read_excel:
        hasil = app_module.dapatkan_data_dosen_terintegrasi()

        assert hasil == [{"NAMA": "Dr. Excel", "BIDANG_KEAHLIAN": "AI"}]
        mock_read_excel.assert_called_once()


def test_dapatkan_data_dosen_fallback_ke_excel_jika_mysql_kosong():
    import pandas as pd

    fake_df = pd.DataFrame([{"NAMA": "Dr. Excel2"}])

    # MySQL tidak error, tapi hasilnya kosong -> tetap harus fallback ke Excel
    with patch.object(app_module.DataLayer, "fetch_all_dosen", return_value=[]), \
         patch("app.pd.read_excel", return_value=fake_df):
        hasil = app_module.dapatkan_data_dosen_terintegrasi()
        assert hasil == [{"NAMA": "Dr. Excel2"}]


def test_dapatkan_data_dosen_kembalikan_list_kosong_jika_excel_juga_gagal():
    with patch.object(app_module.DataLayer, "fetch_all_dosen", side_effect=Exception("MySQL down")), \
         patch("app.pd.read_excel", side_effect=Exception("File Excel tidak ditemukan")):
        hasil = app_module.dapatkan_data_dosen_terintegrasi()
        assert hasil == []