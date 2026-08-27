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
        ),
        Dosen(
            nidn="004",
            nama="Doni Prasetyo, M.Kom.",
            program_studi="Teknik Informatika",
            bidang_keahlian="Cyber Security, Network Security, Kriptografi",
            jurnal="Implementasi Enkripsi AES-256 dan Steganografi Citra Digital",
            judul_bimbing="Pendeteksi Serangan DDoS, Sistem Autentikasi Zero Trust",
            judul_uji="Audit Keamanan Website Akademik, Analisis Malware Android",
            pendidikan="S2 Teknik Informatika"
        ),
        Dosen(
            nidn="005",
            nama="Eka Putri, M.T.",
            program_studi="Teknik Komputer",
            bidang_keahlian="Internet of Things, Embedded System, Sensor Network",
            jurnal="Sistem Monitoring Kualitas Udara Berbasis IoT dan ESP32",
            judul_bimbing="Smart Agriculture Berbasis Sensor Kelembaban, Smart Home",
            judul_uji="Otomasi Irigasi Sawah IoT, Pemantau Suhu Ruang Server",
            pendidikan="S2 Teknik Komputer"
        ),
        Dosen(
            nidn="006",
            nama="Fajar Hidayat, M.Kom.",
            program_studi="Rekayasa Perangkat Lunak",
            bidang_keahlian="Software Engineering, Web Development, Microservices",
            jurnal="Penerapan Arsitektur Microservices pada Sistem E-Commerce",
            judul_bimbing="Rancang Bangun Sistem Informasi Akademik Berbasis Vue dan Flask",
            judul_uji="Pengujian Kualitas Perangkat Lunak ISO 25010, CI/CD Pipeline",
            pendidikan="S2 Ilmu Komputer"
        )
    ]

@pytest.fixture
def app(sample_dosen_list, tmp_path):
    storage_dir = str(tmp_path / "storage")
    cache_dir = str(tmp_path / "storage" / "cache")
    data_dir = str(tmp_path / "storage" / "data")
    logs_dir = str(tmp_path / "storage" / "logs")
    config_json_path = str(tmp_path / "storage" / "data" / "config.json")
    database_dir = str(tmp_path / "database")
    db_sqlite_path = str(tmp_path / "database" / "siredo.db")
    
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
        DATABASE_DIR = database_dir
        DB_SQLITE_PATH = db_sqlite_path
        CONFIG_JSON_PATH = config_json_path
        MAX_BATCH_SIZE = 5

    app = create_app(RuntimeTestConfig)

    
    # Pre-populate in-memory cache for deterministic testing
    cache = CacheService.get_instance()
    cache.dosen_list = sample_dosen_list
    
    # Fit BM25 with realistic sample data
    common_baseline = [
        "analisis", "sistem", "metode", "penelitian", "data", "algoritma", 
        "berbasis", "pengembangan", "penerapan", "klasifikasi", "implementasi", 
        "rancang", "bangun", "pengolahan", "teknologi", "informasi", "evaluasi"
    ]
    corpus_tokens = [
        ["natural", "language", "processing", "machine", "learning", "text", "mining", "bert", "rekomendasi", "dosen", "skripsi"] + common_baseline,
        ["computer", "vision", "deep", "learning", "image", "processing", "yolo", "deteksi", "objek", "citra", "kendaraan"] + common_baseline,
        ["decision", "support", "system", "data", "mining", "ahp", "topsis", "spk", "rekomendasi", "keputusan", "bantuan"] + common_baseline,
        ["cyber", "security", "keamanan", "jaringan", "kriptografi", "aes", "steganografi", "enkripsi", "dokumen"] + common_baseline,
        ["internet", "things", "iot", "sensor", "arduino", "esp32", "monitoring", "nirkabel", "udara", "kualitas"] + common_baseline,
        ["software", "engineering", "rekayasa", "perangkat", "lunak", "agile", "scrum", "web", "sistem", "informasi"] + common_baseline
    ]
    cache.bm25.fit(corpus_tokens)
    
    # MiniLM embedding dimension is 384
    cache.sbert.corpus_embeddings = np.random.rand(len(sample_dosen_list), 384).astype(np.float32)
    cache.sbert.keybert_data = [
        [("nlp bert", 0.95), ("machine learning", 0.88), ("text mining", 0.82)],
        [("computer vision", 0.94), ("yolo object detection", 0.89), ("deep learning", 0.85)],
        [("decision support system", 0.93), ("ahp topsis", 0.87), ("spk", 0.81)],
        [("cyber security", 0.96), ("kriptografi aes", 0.90), ("keamanan jaringan", 0.84)],
        [("internet of things", 0.95), ("sensor esp32", 0.88), ("monitoring", 0.83)],
        [("software engineering", 0.92), ("rekayasa perangkat lunak", 0.86), ("web system", 0.80)]
    ]
    
    cache.is_ready = True
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
