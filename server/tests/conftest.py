import os
import sys
import pytest
import numpy as np

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.src.app import create_app
from server.src.config.config import Config
from server.src.models.dosen.dosen_model import Dosen
from server.src.services.system.cache_service import CacheService

@pytest.fixture(scope='session')
def sample_dosen_list():
    return [
        Dosen(
            nidn="001",
            nama="Dr. Andi Wijaya, M.Kom.",
            program_studi="Teknik Informatika",
            bidang_keahlian="Natural Language Processing, Machine Learning, Text Mining",
            jurnal="Analisis Sentimen Menggunakan BERT, Ekstraksi Topik Bahasa Indonesia",
            judul_bimbing="Sistem Klasifikasi Berita, Chatbot Akademik",
            judul_uji="Pendeteksi Hoaks Twitter, Analisis Opini Publik",
            pendidikan="S3 Ilmu Komputer"
        ),
        Dosen(
            nidn="002",
            nama="Budi Santoso, M.T.",
            program_studi="Teknik Informatika",
            bidang_keahlian="Computer Vision, Deep Learning, Image Processing",
            jurnal="Deteksi Objek dengan YOLO, Segmentasi Citra Medis",
            judul_bimbing="Pengenalan Wajah Presensi, Klasifikasi Rontgen Paru",
            judul_uji="Deteksi Helm Proyek Otomatis, Klasifikasi Plat Nomor",
            pendidikan="S2 Teknik Elektro"
        ),
        Dosen(
            nidn="003",
            nama="Citra Lestari, Ph.D.",
            program_studi="Sistem Informasi",
            bidang_keahlian="Decision Support System, Data Mining, SPK",
            jurnal="Penerapan Metode AHP dan TOPSIS Pemilihan Vendor",
            judul_bimbing="SPK Penerima Beasiswa, Analisis Pola Penjualan Apriori",
            judul_uji="Sistem Rekomendasi Menu Restoran, Evaluasi Kinerja Karyawan",
            pendidikan="S3 Sistem Informasi"
        )
    ]

@pytest.fixture
def app(sample_dosen_list, tmp_path):
    storage_dir = str(tmp_path / "storage")
    cache_dir = str(tmp_path / "storage" / "cache")
    data_dir = str(tmp_path / "storage" / "data")
    logs_dir = str(tmp_path / "storage" / "logs")
    config_json_path = str(tmp_path / "storage" / "data" / "config.json")
    
    class RuntimeTestConfig(Config):
        TESTING = True
        APP_DEBUG = False
        APP_ENV = 'testing'
        ADMIN_API_KEY = 'test-admin-key'
        STORAGE_DIR = storage_dir
        CACHE_DIR = cache_dir
        DATA_DIR = data_dir
        DATASET_DIR = data_dir
        LOGS_DIR = logs_dir
        CONFIG_JSON_PATH = config_json_path
        MAX_BATCH_SIZE = 5

    app = create_app(RuntimeTestConfig)
    
    # Pre-populate in-memory cache for deterministic testing
    cache = CacheService.get_instance()
    cache.dosen_list = sample_dosen_list
    
    # Fit BM25 with sample data
    corpus_tokens = [
        ["natural", "language", "processing", "machine", "learning", "text", "mining", "bert"],
        ["computer", "vision", "deep", "learning", "image", "processing", "yolo"],
        ["decision", "support", "system", "data", "mining", "ahp", "topsis", "spk"]
    ]
    cache.bm25.fit(corpus_tokens)
    
    # MiniLM embedding dimension is 384
    cache.sbert.corpus_embeddings = np.random.rand(len(sample_dosen_list), 384).astype(np.float32)
    cache.sbert.keybert_data = [
        [("nlp bert", 0.9), ("machine learning", 0.85)],
        [("computer vision", 0.9), ("yolo object detection", 0.85)],
        [("decision support system", 0.9), ("ahp topsis", 0.85)]
    ]
    
    cache.is_ready = True
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
