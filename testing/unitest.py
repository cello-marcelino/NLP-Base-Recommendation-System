"""
Test sederhana untuk server/rekomendasi.py
Jalankan dengan: pytest test_rekomendasi.py -v

Trik: sentence_transformers & keybert di-mock SEBELUM rekomendasi.py di-import,
jadi tidak perlu download model asli / load berat tiap test.
"""

import sys
import os
import numpy as np
from unittest.mock import MagicMock, patch

# --- arahkan ke folder server ---
SERVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "server"))
sys.path.insert(0, SERVER_DIR)

# --- mock library berat SEBELUM import rekomendasi ---
mock_sbert_instance = MagicMock()
mock_sbert_instance.encode.side_effect = lambda teks, convert_to_numpy=True: (
    np.random.rand(len(teks), 384) if isinstance(teks, list) else np.random.rand(384)
)

mock_kw_instance = MagicMock()


def _fake_extract_keywords(teks_list, **kwargs):
    # KeyBERT asli mengembalikan 1 sub-list keyword per teks input.
    # Mock ini harus ikut jumlah input, bukan hardcode 1, supaya index tidak meleset
    # saat data dosen lebih dari satu.
    jumlah = len(teks_list) if isinstance(teks_list, list) else 1
    return [[("kecerdasan buatan", 0.8)] for _ in range(jumlah)]


mock_kw_instance.extract_keywords.side_effect = _fake_extract_keywords

sys.modules["sentence_transformers"] = MagicMock(SentenceTransformer=lambda *a, **k: mock_sbert_instance)
sys.modules["keybert"] = MagicMock(KeyBERT=lambda *a, **k: mock_kw_instance)

import rekomendasi  # noqa: E402  (import setelah mocking, sengaja)

# pastikan modul rekomendasi benar-benar pakai instance mock kita
rekomendasi.model_sbert = mock_sbert_instance
rekomendasi.kw_model = mock_kw_instance

# arahkan cache ke folder sementara supaya tidak menimpa data/ asli
TMP_CACHE_DIR = os.path.join(os.path.dirname(__file__), "_tmp_cache")
os.makedirs(TMP_CACHE_DIR, exist_ok=True)
rekomendasi.VEKTOR_CACHE_PATH = os.path.join(TMP_CACHE_DIR, "vektor_test.npy")
rekomendasi.FINGERPRINT_CACHE_PATH = rekomendasi.VEKTOR_CACHE_PATH + ".fingerprint"
rekomendasi.KEYBERT_CACHE_PATH = os.path.join(TMP_CACHE_DIR, "keybert_test.json")

# --- data dummy dosen ---
DATA_DOSEN = [
    {
        "NAMA": "Dr. A",
        "BIDANG_KEAHLIAN": "Machine Learning",
        "JURNAL": "AI Journal",
        "RIWAYAT_PENDIDIKAN": "S3 Ilmu Komputer",
        "judul bimbing": '"NLP untuk chatbot"',
        "judul uji": '"Deep learning image"',
    },
    {
        "NAMA": "Dr. B",
        "BIDANG_KEAHLIAN": "Jaringan Komputer",
        "JURNAL": "Network Journal",
        "RIWAYAT_PENDIDIKAN": "S3 Teknik Elektro",
        "judul bimbing": "-",
        "judul uji": "-",
    },
]


# =========================================================
# Test pure logic (tidak butuh model AI sama sekali)
# =========================================================

def test_tokenize_split_hasil_tidak_kosong():
    tokens, bigrams = rekomendasi.PreprocessingPipeline.tokenize_split("saya suka machine learning")
    assert "machine" in tokens
    assert "learning" in tokens


def test_parse_dan_dedup_judul_hapus_duplikat():
    raw = '"Judul A", "Judul A", "Judul B"'
    hasil = rekomendasi.PreprocessingPipeline._parse_dan_dedup_judul(raw)
    assert hasil.count("Judul A") == 1
    assert "Judul B" in hasil


def test_parse_dan_dedup_judul_kosong_jika_strip():
    assert rekomendasi.PreprocessingPipeline._parse_dan_dedup_judul("-") == ""
    assert rekomendasi.PreprocessingPipeline._parse_dan_dedup_judul("") == ""


def test_adaptive_weighting_default_tanpa_bm25():
    lex, sem, langka = rekomendasi.AdaptiveWeighting.hitung([], None, 0, 0)
    assert lex == 0.3
    assert sem == 0.7
    assert langka == []


def test_fingerprint_data_konsisten():
    fp1 = rekomendasi._fingerprint_data(DATA_DOSEN)
    fp2 = rekomendasi._fingerprint_data(DATA_DOSEN)
    assert fp1 == fp2  # data sama harus hasilkan fingerprint sama

    data_beda = DATA_DOSEN + [{"NAMA": "Dr. C"}]
    fp3 = rekomendasi._fingerprint_data(data_beda)
    assert fp1 != fp3  # data beda harus hasilkan fingerprint beda


# =========================================================
# Test yang butuh "model AI" (sudah di-mock di atas)
# =========================================================

def test_cache_manager_siapkan_berhasil():
    engine = rekomendasi.RecommendationEngine()
    engine.siapkan_cache(DATA_DOSEN, force_recalculate=True)

    assert engine.cache.is_ready is True
    assert engine.cache.vektor_dosen.shape[0] == len(DATA_DOSEN)
    assert engine.cache.mesin_bm25 is not None


def test_jalankan_pipeline_mengembalikan_hasil():
    engine = rekomendasi.RecommendationEngine()
    engine.siapkan_cache(DATA_DOSEN, force_recalculate=True)

    hasil = engine.jalankan_pipeline(
        judul_mhs="chatbot NLP",
        abstrak_mhs="penelitian tentang chatbot berbasis NLP",
        k_rank=1,
    )

    assert "hasil_rekomendasi" in hasil
    assert len(hasil["hasil_rekomendasi"]) == 1
    top1 = hasil["hasil_rekomendasi"][0]
    assert "Hybrid Score" in top1
    assert "NAMA" in top1


def test_jalankan_pipeline_gagal_jika_cache_belum_siap():
    engine = rekomendasi.RecommendationEngine()
    try:
        engine.jalankan_pipeline("judul", "abstrak")
        assert False, "harusnya raise RuntimeError karena cache belum disiapkan"
    except RuntimeError:
        pass


# =========================================================
# Tambahan: AdaptiveWeighting dengan BM25 asli (bukan None)
# =========================================================

def test_adaptive_weighting_dengan_bm25_asli():
    from rank_bm25 import BM25Okapi

    token_dosen = [
        ["mesin", "belajar", "jaringan", "saraf"],
        ["basis", "data", "relasional", "sql"],
    ]
    bm25 = BM25Okapi(token_dosen)
    avg_idf = sum(bm25.idf.values()) / len(bm25.idf)
    max_idf = max(bm25.idf.values())

    token_mhs = ["mesin", "belajar"]  # kata yang cukup langka di korpus kecil ini
    lex, sem, kata_langka = rekomendasi.AdaptiveWeighting.hitung(token_mhs, bm25, avg_idf, max_idf)

    # bobot harus tetap berada dalam batas yang didefinisikan class-nya
    assert rekomendasi.AdaptiveWeighting.BATAS_MIN <= lex <= rekomendasi.AdaptiveWeighting.BATAS_MAX
    assert round(lex + sem, 2) == 1.0
    assert isinstance(kata_langka, list)


def test_adaptive_weighting_token_kosong_pakai_default():
    from rank_bm25 import BM25Okapi

    token_dosen = [["mesin", "belajar"], ["basis", "data"]]
    bm25 = BM25Okapi(token_dosen)
    lex, sem, kata_langka = rekomendasi.AdaptiveWeighting.hitung([], bm25, 1.0, 2.0)
    # token_mhs kosong -> masuk jalur default (bukan hitung rasio)
    assert lex == 0.3
    assert sem == 0.7
    assert kata_langka == []


# =========================================================
# Tambahan: ScoringPipeline edge case (skor nol & std nol)
# =========================================================

def test_scoring_leksikal_semua_nol_jika_tidak_ada_skor():
    mesin_mock = MagicMock()
    mesin_mock.get_scores.return_value = np.array([0.0, 0.0, 0.0])
    hasil = rekomendasi.ScoringPipeline.hitung_leksikal_normalized(mesin_mock, ["kata"])
    assert np.all(hasil == 0.0)


def test_scoring_leksikal_std_nol_menghasilkan_nol():
    mesin_mock = MagicMock()
    # semua dokumen mendapat skor identik -> std = 0 -> harus dianggap tidak informatif
    mesin_mock.get_scores.return_value = np.array([1.5, 1.5, 1.5])
    hasil = rekomendasi.ScoringPipeline.hitung_leksikal_normalized(mesin_mock, ["kata"])
    assert np.all(hasil == 0.0)


def test_scoring_leksikal_normal_menghasilkan_nilai_antara_0_dan_1():
    mesin_mock = MagicMock()
    mesin_mock.get_scores.return_value = np.array([0.1, 5.0, 2.3])
    hasil = rekomendasi.ScoringPipeline.hitung_leksikal_normalized(mesin_mock, ["kata"])
    assert hasil.min() >= 0.0
    assert hasil.max() <= 1.0


# =========================================================
# Tambahan: CacheManager - pakai cache lama vs hitung ulang
# =========================================================

def test_cache_manager_pakai_cache_jika_data_sama():
    mock_sbert_instance.encode.reset_mock()
    engine = rekomendasi.RecommendationEngine()

    engine.siapkan_cache(DATA_DOSEN, force_recalculate=True)
    panggilan_pertama = mock_sbert_instance.encode.call_count

    # data persis sama, tanpa force_recalculate -> seharusnya pakai cache lokal, tidak encode ulang
    engine.siapkan_cache(DATA_DOSEN, force_recalculate=False)
    panggilan_kedua = mock_sbert_instance.encode.call_count

    assert panggilan_kedua == panggilan_pertama


def test_cache_manager_hitung_ulang_jika_data_berubah():
    mock_sbert_instance.encode.reset_mock()
    engine = rekomendasi.RecommendationEngine()

    engine.siapkan_cache(DATA_DOSEN, force_recalculate=True)
    panggilan_pertama = mock_sbert_instance.encode.call_count

    data_baru = DATA_DOSEN + [
        {
            "NAMA": "Dr. C",
            "BIDANG_KEAHLIAN": "Basis Data",
            "JURNAL": "DB Journal",
            "RIWAYAT_PENDIDIKAN": "S3 Informatika",
            "judul bimbing": "-",
            "judul uji": "-",
        }
    ]
    # data berubah (nambah 1 dosen), tanpa force_recalculate -> fingerprint beda -> harus hitung ulang
    engine.siapkan_cache(data_baru, force_recalculate=False)
    panggilan_kedua = mock_sbert_instance.encode.call_count

    assert panggilan_kedua > panggilan_pertama