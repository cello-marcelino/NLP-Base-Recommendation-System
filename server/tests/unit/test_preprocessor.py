import pytest
from server.src.services.nlp.preprocessor import Preprocessor
from server.src.models.dosen.dosen_model import Dosen

def test_clean_text():
    raw = "Penerapan Algoritma CNN untuk Deteksi Objek! (Versi 2.0)"
    cleaned = Preprocessor.clean_text(raw)
    assert "penerapan" in cleaned
    assert "algoritma" in cleaned
    assert "cnn" in cleaned
    assert "deteksi" in cleaned
    assert "!" not in cleaned

def test_remove_stopwords():
    words = ["analisis", "sentimen", "dan", "twitter", "menggunakan"]
    filtered = Preprocessor.remove_stopwords(words)
    assert filtered == ["sentimen", "twitter"]

def test_create_ngrams():
    words = ["machine", "learning", "model"]
    ngrams = Preprocessor.create_ngrams(words)
    assert "machine" in ngrams
    assert "machine_learning" in ngrams
    assert "learning_model" in ngrams

def test_ekspansi_query_dengan_log():
    teks = "penelitian natural language processing untuk klasifikasi"
    expanded, log = Preprocessor.ekspansi_query_dengan_log(teks)
    assert "natural language processing" in log
    assert "bert" in expanded
    assert "word2vec" in expanded

def test_build_corpus_text():
    dosen = Dosen(
        nidn="123",
        nama="Prof. Test",
        program_studi="Teknik Informatika",
        bidang_keahlian="Kecerdasan Buatan",
        jurnal="Jurnal AI",
        judul_bimbing="Chatbot, Chatbot, Web AI",
        judul_uji="Sistem Cerdas",
        pendidikan="S3 AI"
    )
    teks_terbobot, teks_normal = Preprocessor.build_corpus_text(dosen)
    assert "Kecerdasan Buatan" in teks_terbobot
    assert "Jurnal AI" in teks_terbobot
    assert "S3 AI" in teks_normal
