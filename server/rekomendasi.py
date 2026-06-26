"""Mesin rekomendasi SIREDO."""

import os
import re
import logging
import hashlib
import threading
from functools import lru_cache
from typing import List, Dict, Tuple, Any, Optional

import numpy as np
from nltk import ngrams
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from sklearn.metrics.pairwise import cosine_similarity

from utils import KAMUS_EKSPANSI, STOPWORDS

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.feature_extraction.text")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("siredo.engine")

VEKTOR_CACHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/vektor_dosen.npy'))
FINGERPRINT_CACHE_PATH = VEKTOR_CACHE_PATH + ".fingerprint"

logger.info("Menginisialisasi model semantik...")
model_sbert = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
kw_model = KeyBERT(model=model_sbert) # type: ignore


# Preprocessing
class PreprocessingPipeline:
    @staticmethod
    def ekspansi_query_dengan_log(teks: str, kamus: Dict = KAMUS_EKSPANSI) -> Tuple[str, Dict[str, str]]:
        teks_lower = teks.lower()
        teks_ekspansi = teks_lower
        log_ekspansi = {}
        for frasa in sorted(kamus.keys(), key=len, reverse=True):
            if frasa in teks_lower:
                hasil = " ".join(kamus[frasa])
                teks_ekspansi += " " + hasil
                log_ekspansi[frasa] = hasil
        return teks_ekspansi, log_ekspansi

    @staticmethod
    def tokenize_split(teks: str, n: int = 2) -> Tuple[List[str], List[str]]:
        """Tokenisasi unigram dan bigram."""
        tokens = re.findall(r'\b[a-z0-9]{2,}\b', teks.lower())
        tokens_bersih = [t for t in tokens if t not in STOPWORDS]
        bigrams = ["_".join(g) for g in ngrams(tokens_bersih, n)]
        return tokens_bersih, bigrams

    @staticmethod
    def tokenize_ngram(teks: str, n: int = 2) -> List[str]:
        """Token BM25."""
        uni, bi = PreprocessingPipeline.tokenize_split(teks, n)
        return uni + bi

    @staticmethod
    def buat_teks_terbobot(dosen: Dict[str, Any]) -> Tuple[str, str]:
        keahlian = str(dosen.get('BIDANG_KEAHLIAN', ''))
        bimbing = str(dosen.get('judul bimbing', ''))
        uji = str(dosen.get('judul uji', ''))
        jurnal = str(dosen.get('JURNAL', ''))
        pendidikan = str(dosen.get('RIWAYAT_PENDIDIKAN', ''))

        inti = f"{keahlian} " * 3 + f"{bimbing} " * 3 + f"{uji} " * 2 + f"{jurnal} "
        teks_terbobot = f"{inti} {pendidikan}"
        teks_normal = f"{pendidikan} {keahlian} {jurnal} {uji} {bimbing}"
        return teks_terbobot, teks_normal


# Adaptive weighting
class AdaptiveWeighting:
    BATAS_MIN = 0.2
    BATAS_MAX = 0.8

    @classmethod
    def hitung(
        cls,
        token_mhs: List[str],
        mesin_bm25: Optional[BM25Okapi],
        avg_idf: float,
        max_idf: float,
    ) -> Tuple[float, float, List[str]]:
        if not mesin_bm25 or not token_mhs:
            return 0.3, 0.7, []

        kata_langka = [t for t in token_mhs if mesin_bm25.idf.get(t, max_idf) > avg_idf]
        rasio_langka = len(kata_langka) / len(token_mhs)
        bobot_lex = cls.BATAS_MIN + rasio_langka * (cls.BATAS_MAX - cls.BATAS_MIN)
        return round(bobot_lex, 2), round(1.0 - bobot_lex, 2), kata_langka


# Scoring
class ScoringPipeline:
    @staticmethod
    def hitung_leksikal_normalized(mesin: BM25Okapi, token_mhs: List[str]) -> np.ndarray:
        """Normalisasi skor leksikal."""
        skor_mentah = np.array(mesin.get_scores(token_mhs), dtype=float)
        skor_min, skor_max = skor_mentah.min(), skor_mentah.max()
        if skor_max - skor_min < 1e-9:
            return np.zeros_like(skor_mentah)
        return (skor_mentah - skor_min) / (skor_max - skor_min)

    @staticmethod
    def hitung_semantik(vektor_mhs: np.ndarray, vektor_dosen: np.ndarray) -> np.ndarray:
        skor_mentah = cosine_similarity(vektor_mhs.reshape(1, -1), vektor_dosen)[0]
        return np.clip(skor_mentah, 0.0, None)


# Cache embedding query
@lru_cache(maxsize=256)
def _encode_query_cached(teks_mhs_expand: str) -> tuple:
    vektor = model_sbert.encode([teks_mhs_expand], convert_to_numpy=True)[0]
    return tuple(vektor.tolist())


def _fingerprint_data(data_dosen: List[Dict]) -> str:
    payload = "|".join(f"{d.get('NAMA', '')}-{d.get('BIDANG_KEAHLIAN', '')}" for d in data_dosen)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()


# Cache state
class CacheManager:
    def __init__(self):
        self._lock = threading.Lock()
        self.data_dosen: List[Dict] = []
        self.teks_bobot_list: List[str] = []
        self.teks_raw_list: List[str] = []
        self.token_dosen: List[List[str]] = []
        self.vektor_dosen: Optional[np.ndarray] = None
        self.mesin_bm25: Optional[BM25Okapi] = None
        self.avg_idf: float = 0.0
        self.max_idf: float = 0.0
        self.is_ready = False

    def siapkan(self, data_dosen: List[Dict], force_recalculate: bool = False) -> None:
        with self._lock:
            self.data_dosen = data_dosen
            self.teks_bobot_list, self.teks_raw_list = [], []
            for dsn in data_dosen:
                tb, tr = PreprocessingPipeline.buat_teks_terbobot(dsn)
                self.teks_bobot_list.append(tb)
                self.teks_raw_list.append(tr)

            self.token_dosen = [PreprocessingPipeline.tokenize_ngram(t) for t in self.teks_bobot_list]

            folder_cache = os.path.dirname(VEKTOR_CACHE_PATH)
            os.makedirs(folder_cache, exist_ok=True)

            fingerprint_baru = _fingerprint_data(data_dosen)
            pakai_cache = False

            if not force_recalculate and os.path.exists(VEKTOR_CACHE_PATH):
                try:
                    vektor_lokal = np.load(VEKTOR_CACHE_PATH)
                    fingerprint_lama = None
                    if os.path.exists(FINGERPRINT_CACHE_PATH):
                        with open(FINGERPRINT_CACHE_PATH, "r") as f:
                            fingerprint_lama = f.read().strip()

                    if vektor_lokal.shape[0] == len(data_dosen) and fingerprint_lama == fingerprint_baru:
                        self.vektor_dosen = vektor_lokal
                        pakai_cache = True
                        logger.info("Matriks SBERT dimuat dari cache lokal (fingerprint cocok).")
                    else:
                        logger.warning("Data dosen berubah (jumlah/isi) -> hitung ulang matriks vektor.")
                except Exception as e:
                    logger.warning(f"Gagal membaca cache npy: {e}")

            if not pakai_cache:
                logger.info("Menghitung ulang matriks SBERT dari awal...")
                self.vektor_dosen = np.array(model_sbert.encode(self.teks_bobot_list, convert_to_numpy=True))
                try:
                    np.save(VEKTOR_CACHE_PATH, self.vektor_dosen)
                    with open(FINGERPRINT_CACHE_PATH, "w") as f:
                        f.write(fingerprint_baru)
                except Exception as e:
                    logger.error(f"Gagal menyimpan cache npy/fingerprint: {e}")

            self.mesin_bm25 = BM25Okapi(self.token_dosen)

            if self.mesin_bm25.idf:
                self.avg_idf = sum(self.mesin_bm25.idf.values()) / len(self.mesin_bm25.idf)
                self.max_idf = max(self.mesin_bm25.idf.values())
            else:
                self.avg_idf = self.max_idf = 0.0

            self.is_ready = True
            _encode_query_cached.cache_clear()


# Facade
class RecommendationEngine:
    def __init__(self):
        self.cache = CacheManager()

    def siapkan_cache(self, data_dosen: List[Dict], force_recalculate: bool = False) -> None:
        self.cache.siapkan(data_dosen, force_recalculate)

    def jalankan_pipeline(
        self,
        judul_mhs: str,
        abstrak_mhs: str,
        k_rank: int = 5,
        bobot_lex: float = 0.3,
        bobot_sem: float = 0.7,
    ) -> Dict[str, Any]:
        if not self.cache.is_ready:
            raise RuntimeError("Cache belum siap. Panggil siapkan_cache() dulu.")

        mesin_bm25 = self.cache.mesin_bm25
        vektor_dosen = self.cache.vektor_dosen
        if mesin_bm25 is None or vektor_dosen is None:
            raise RuntimeError("Cache tidak konsisten: mesin_bm25/vektor_dosen kosong walau is_ready=True.")

        teks_mhs_raw = f"{judul_mhs} {abstrak_mhs}"
        teks_mhs_expand, log_ekspansi = PreprocessingPipeline.ekspansi_query_dengan_log(teks_mhs_raw)

        tokens_unigram, tokens_bigram = PreprocessingPipeline.tokenize_split(teks_mhs_expand)
        token_mhs = tokens_unigram + tokens_bigram

        bobot_lex = float(bobot_lex)
        is_adaptif = bobot_lex < 0
        kata_langka: List[str] = []

        if is_adaptif:
            bobot_lex, bobot_sem, kata_langka = AdaptiveWeighting.hitung(
                token_mhs, mesin_bm25, self.cache.avg_idf, self.cache.max_idf
            )
        else:
            bobot_lex = round(bobot_lex, 2)
            bobot_sem = round(float(bobot_sem), 2)

        skor_lex = ScoringPipeline.hitung_leksikal_normalized(mesin_bm25, token_mhs)

        vektor_mhs = np.array(_encode_query_cached(teks_mhs_expand))
        skor_sem = ScoringPipeline.hitung_semantik(vektor_mhs, vektor_dosen)

        top_k = self._rank(skor_lex, skor_sem, bobot_lex, bobot_sem, k_rank)
        hasil_final = self._enrich(top_k, token_mhs, teks_mhs_raw)

        return {
            "hasil_rekomendasi": hasil_final,
            "metadata_mesin": {
                "teks_asli": teks_mhs_raw,
                "teks_ekspansi": teks_mhs_expand,
                "kata_diekspansi": log_ekspansi,
                "token_unigram": list(set(tokens_unigram)),
                "token_bigram": list(set(tokens_bigram)),
                "is_adaptif": is_adaptif,
                "bobot_lex_final": bobot_lex,
                "bobot_sem_final": bobot_sem,
                "kata_langka": kata_langka,
            },
        }

    def _rank(
        self, skor_lex: np.ndarray, skor_sem: np.ndarray, bobot_lex: float, bobot_sem: float, k_rank: int
    ) -> List[Dict[str, Any]]:
        data_dosen = self.cache.data_dosen
        semua_hasil = []
        for i in range(len(data_dosen)):
            skor_hybrid = bobot_lex * skor_lex[i] + bobot_sem * skor_sem[i]
            semua_hasil.append({
                "indeks": i,
                "NAMA": data_dosen[i].get('NAMA', '-'),
                "PROGRAM_STUDI": data_dosen[i].get('PROGRAM_STUDI', '-'),
                "BIDANG_KEAHLIAN": data_dosen[i].get('BIDANG_KEAHLIAN', '-'),
                "JURNAL": data_dosen[i].get('JURNAL', '-'),
                "judul bimbing": data_dosen[i].get('judul bimbing', '-'),
                "judul uji": data_dosen[i].get('judul uji', '-'),
                "RIWAYAT_PENDIDIKAN": data_dosen[i].get('RIWAYAT_PENDIDIKAN', '-'),
                "Hybrid Score": round(float(skor_hybrid), 3),
                "Lexical Score": round(float(skor_lex[i]), 3),
                "Semantic Score": round(float(skor_sem[i]), 3),
            })
        semua_hasil.sort(key=lambda x: x["Hybrid Score"], reverse=True)
        return semua_hasil[:k_rank]

    def _enrich(
        self, top_k: List[Dict[str, Any]], token_mhs: List[str], teks_mhs_raw: str
    ) -> List[Dict[str, Any]]:
        mhs_set = set(token_mhs)
        teks_list = [self.cache.teks_raw_list[h["indeks"]] for h in top_k]

        keywords_batch: List[List[Tuple[str, float]]] = []
        if teks_list:
            raw = kw_model.extract_keywords(
                teks_list,
                keyphrase_ngram_range=(1, 3),
                stop_words=list(STOPWORDS),
                use_maxsum=True,
                nr_candidates=15,
                top_n=3,
                seed_keywords=[teks_mhs_raw],
            )
            if len(teks_list) == 1 and raw and isinstance(raw[0], tuple):
                keywords_batch = [raw] # type: ignore
            else:
                keywords_batch = raw # type: ignore

        hasil_final = []
        for h, kw_result in zip(top_k, keywords_batch):
            idx = h["indeks"]
            dsn_set = set(self.cache.token_dosen[idx])
            irisan = list(mhs_set.intersection(dsn_set))
            kata_lex = [str(k).replace('_', ' ') for k in irisan]
            kata_sem = [str(k[0]) for k in kw_result]

            h["Irisan Kata (Lexical)"] = ", ".join(kata_lex) if kata_lex else "-"
            h["Frasa Terkait (KeyBERT)"] = ", ".join(kata_sem) if kata_sem else "-"
            del h["indeks"]
            hasil_final.append(h)

        return hasil_final


# Singleton
engine = RecommendationEngine()
