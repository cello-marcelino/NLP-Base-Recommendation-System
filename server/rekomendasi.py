import os
import re
import logging
import hashlib
import threading
import json
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

# Lokasi cache untuk vektor, fingerprint, dan hasil KeyBERT
VEKTOR_CACHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/vektor_dosen.npy"))
FINGERPRINT_CACHE_PATH = VEKTOR_CACHE_PATH + ".fingerprint"
KEYBERT_CACHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/keybert_dosen.json"))

# Model dipakai untuk embedding dan ekstraksi frasa
logger.info("Menginisialisasi model semantik...")
model_sbert = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
kw_model = KeyBERT(model=model_sbert) # type: ignore


class PreprocessingPipeline:
    @staticmethod
    def ekspansi_query_dengan_log(teks: str, kamus: Dict = KAMUS_EKSPANSI) -> Tuple[str, Dict[str, str]]:
        # Ekspansi frasa penting dan simpan log frasa yang ditambahkan
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
        # Ambil token bersih dan bentuk n-gram dari token tersebut
        tokens = re.findall(r"\b[a-z0-9]{2,}\b", teks.lower())
        tokens_bersih = [t for t in tokens if t not in STOPWORDS]
        bigrams = ["_".join(g) for g in ngrams(tokens_bersih, n)]
        return tokens_bersih, bigrams

    @staticmethod
    def tokenize_ngram(teks: str, n: int = 2) -> List[str]:
        # Gabungkan unigram dan n-gram untuk kebutuhan BM25
        uni, bi = PreprocessingPipeline.tokenize_split(teks, n)
        return uni + bi

    @staticmethod
    def _parse_dan_dedup_judul(raw: str, max_items: int = 12) -> str:
        if not raw or raw == "-":
            return ""
        items = re.split(r'",\s*"', raw.strip().strip('"'))
        seen = set()
        unik = []
        for it in items:
            key = it.strip().lower()
            if key and key not in seen:
                seen.add(key)
                unik.append(it.strip())
            if len(unik) >= max_items:
                break
        return " ".join(unik)

    @staticmethod
    def buat_teks_terbobot(dosen: Dict[str, Any]) -> Tuple[str, str]:
        # Susun teks berbobot untuk embedding dan teks normal untuk ekstraksi frasa
        keahlian = str(dosen.get("BIDANG_KEAHLIAN", ""))
        jurnal = str(dosen.get("JURNAL", ""))
        pendidikan = str(dosen.get("RIWAYAT_PENDIDIKAN", ""))
        bimbing = PreprocessingPipeline._parse_dan_dedup_judul(str(dosen.get("judul bimbing", "")), max_items=12)
        uji = PreprocessingPipeline._parse_dan_dedup_judul(str(dosen.get("judul uji", "")), max_items=8)

        inti = f"{keahlian} " * 5 + f"{bimbing} " + f"{uji} " + f"{jurnal} " * 2
        teks_terbobot = f"{inti} {pendidikan}"
        teks_normal = f"{pendidikan} {keahlian} {jurnal} {uji} {bimbing}"
        return teks_terbobot, teks_normal


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
        # Hitung bobot leksikal dari banyaknya kata langka di query
        if not mesin_bm25 or not token_mhs:
            return 0.3, 0.7, []

        kata_langka = [t for t in token_mhs if mesin_bm25.idf.get(t, max_idf) > avg_idf]
        rasio_langka = len(kata_langka) / len(token_mhs)
        bobot_lex = cls.BATAS_MIN + rasio_langka * (cls.BATAS_MAX - cls.BATAS_MIN)
        kata_langka_unik = list(dict.fromkeys(kata_langka))
        return round(bobot_lex, 2), round(1.0 - bobot_lex, 2), kata_langka_unik


class ScoringPipeline:
    @staticmethod
    def hitung_leksikal_normalized(mesin: BM25Okapi, token_mhs: List[str]) -> np.ndarray:
        # Normalisasi skor BM25 dengan z-score lalu sigmoid
        skor_mentah = np.array(mesin.get_scores(token_mhs), dtype=float)

        if skor_mentah.max() <= 1e-9:
            return np.zeros_like(skor_mentah)

        mean = skor_mentah.mean()
        std = skor_mentah.std()
        if std < 1e-9:
            return np.zeros_like(skor_mentah)

        z = (skor_mentah - mean) / std
        skor_norm = 1.0 / (1.0 + np.exp(-z / 2.0))
        skor_norm[skor_mentah <= 1e-9] = 0.0
        return skor_norm

    @staticmethod
    def hitung_semantik(vektor_mhs: np.ndarray, vektor_dosen: np.ndarray) -> np.ndarray:
        # Ukur kemiripan semantik dengan cosine similarity
        skor_mentah = cosine_similarity(vektor_mhs.reshape(1, -1), vektor_dosen)[0]
        return np.clip(skor_mentah, 0.0, None)


@lru_cache(maxsize=256)
def _encode_query_cached(teks_mhs_expand: str) -> tuple:
    # Cache embedding query agar request berulang lebih cepat
    vektor = model_sbert.encode([teks_mhs_expand], convert_to_numpy=True)[0]
    return tuple(vektor.tolist())


def _fingerprint_data(data_dosen: List[Dict]) -> str:
    # Buat fingerprint dari field yang benar-benar dipakai saat membangun teks
    payload_parts = []
    for d in data_dosen:
        bagian = "-".join(
            [
                str(d.get("NAMA", "")),
                str(d.get("BIDANG_KEAHLIAN", "")),
                str(d.get("JURNAL", "")),
                str(d.get("RIWAYAT_PENDIDIKAN", "")),
                str(d.get("judul bimbing", "")),
                str(d.get("judul uji", "")),
            ]
        )
        payload_parts.append(bagian)
    payload = "|".join(payload_parts)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()


class CacheManager:
    def __init__(self):
        # Lock menjaga state cache tetap konsisten saat update dan baca
        self._lock = threading.RLock()
        self.data_dosen: List[Dict] = []
        self.teks_bobot_list: List[str] = []
        self.teks_raw_list: List[str] = []
        self.token_dosen: List[List[str]] = []
        self.vektor_dosen: Optional[np.ndarray] = None
        self.mesin_bm25: Optional[BM25Okapi] = None
        self.keybert_data: List[List[Tuple[str, float]]] = []
        self.avg_idf: float = 0.0
        self.max_idf: float = 0.0
        self.is_ready = False

    def siapkan(self, data_dosen: List[Dict], force_recalculate: bool = False) -> None:
        # Bangun teks, token, vektor, BM25, dan cache lokal
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

            if not force_recalculate and os.path.exists(VEKTOR_CACHE_PATH) and os.path.exists(KEYBERT_CACHE_PATH):
                try:
                    vektor_lokal = np.load(VEKTOR_CACHE_PATH)
                    fingerprint_lama = None
                    if os.path.exists(FINGERPRINT_CACHE_PATH):
                        with open(FINGERPRINT_CACHE_PATH, "r") as f:
                            fingerprint_lama = f.read().strip()

                    if vektor_lokal.shape[0] == len(data_dosen) and fingerprint_lama == fingerprint_baru:
                        self.vektor_dosen = vektor_lokal
                        with open(KEYBERT_CACHE_PATH, "r") as f:
                            self.keybert_data = json.load(f)
                        pakai_cache = True
                        logger.info("Matriks SBERT dan KeyBERT dimuat dari cache lokal.")
                    else:
                        logger.warning("Data dosen berubah, hitung ulang vektor dan frasa.")
                except Exception as e:
                    logger.warning(f"Gagal membaca cache lokal: {e}")

            if not pakai_cache:
                logger.info("Menghitung ulang matriks SBERT...")
                self.vektor_dosen = np.array(model_sbert.encode(self.teks_bobot_list, convert_to_numpy=True))

                logger.info("Mengekstrak frasa KeyBERT...")
                raw_keywords = kw_model.extract_keywords(
                    self.teks_raw_list,
                    keyphrase_ngram_range=(1, 3),
                    stop_words=list(STOPWORDS),
                    use_maxsum=True,
                    nr_candidates=15,
                    top_n=5,
                )

                if len(self.teks_raw_list) == 1 and raw_keywords and isinstance(raw_keywords[0], tuple):
                    self.keybert_data = [raw_keywords] # type: ignore
                else:
                    self.keybert_data = raw_keywords # type: ignore

                try:
                    np.save(VEKTOR_CACHE_PATH, self.vektor_dosen)
                    with open(KEYBERT_CACHE_PATH, "w") as f:
                        json.dump(self.keybert_data, f)
                    with open(FINGERPRINT_CACHE_PATH, "w") as f:
                        f.write(fingerprint_baru)
                except Exception as e:
                    logger.error(f"Gagal menyimpan cache npy/json/fingerprint: {e}")

            self.mesin_bm25 = BM25Okapi(self.token_dosen)
            if self.mesin_bm25.idf:
                self.avg_idf = sum(self.mesin_bm25.idf.values()) / len(self.mesin_bm25.idf)
                self.max_idf = max(self.mesin_bm25.idf.values())
            else:
                self.avg_idf = self.max_idf = 0.0

            self.is_ready = True
            _encode_query_cached.cache_clear()

    def snapshot(self) -> Dict[str, Any]:
        # Ambil state cache secara atomik supaya pembacaan tetap konsisten
        with self._lock:
            if not self.is_ready:
                raise RuntimeError("Cache belum siap. Panggil siapkan_cache() dulu.")
            return {
                "data_dosen": self.data_dosen,
                "token_dosen": self.token_dosen,
                "vektor_dosen": self.vektor_dosen,
                "mesin_bm25": self.mesin_bm25,
                "keybert_data": self.keybert_data,
                "avg_idf": self.avg_idf,
                "max_idf": self.max_idf,
            }


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
        # Ambil snapshot sekali agar semua komponen memakai state yang sama
        snap = self.cache.snapshot()
        mesin_bm25 = snap["mesin_bm25"]
        vektor_dosen = snap["vektor_dosen"]
        data_dosen = snap["data_dosen"]
        token_dosen = snap["token_dosen"]
        keybert_data = snap["keybert_data"]
        avg_idf = snap["avg_idf"]
        max_idf = snap["max_idf"]

        if mesin_bm25 is None or vektor_dosen is None:
            raise RuntimeError("Cache tidak konsisten.")

        teks_mhs_raw = f"{judul_mhs} {abstrak_mhs}"
        teks_mhs_expand, log_ekspansi = PreprocessingPipeline.ekspansi_query_dengan_log(teks_mhs_raw)
        tokens_unigram, tokens_bigram = PreprocessingPipeline.tokenize_split(teks_mhs_expand)
        token_mhs = tokens_unigram + tokens_bigram

        bobot_lex = float(bobot_lex)
        is_adaptif = bobot_lex < 0
        kata_langka: List[str] = []

        if is_adaptif:
            bobot_lex, bobot_sem, kata_langka = AdaptiveWeighting.hitung(token_mhs, mesin_bm25, avg_idf, max_idf)
        else:
            bobot_lex = round(bobot_lex, 2)
            bobot_sem = round(float(bobot_sem), 2)

        skor_lex = ScoringPipeline.hitung_leksikal_normalized(mesin_bm25, token_mhs)
        vektor_mhs = np.array(_encode_query_cached(teks_mhs_expand))
        skor_sem = ScoringPipeline.hitung_semantik(vektor_mhs, vektor_dosen)

        top_k = self._rank(skor_lex, skor_sem, bobot_lex, bobot_sem, k_rank, data_dosen)
        hasil_final = self._enrich(top_k, token_mhs, token_dosen, keybert_data)

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
        self,
        skor_lex: np.ndarray,
        skor_sem: np.ndarray,
        bobot_lex: float,
        bobot_sem: float,
        k_rank: int,
        data_dosen: List[Dict],
    ) -> List[Dict[str, Any]]:
        # Gabungkan skor leksikal dan semantik, lalu ambil kandidat teratas
        skor_hybrid = (bobot_lex * skor_lex) + (bobot_sem * skor_sem)

        n = skor_hybrid.shape[0]
        k = min(k_rank, n)
        if k <= 0:
            return []

        if k < n:
            kandidat_idx = np.argpartition(skor_hybrid, -k)[-k:]
        else:
            kandidat_idx = np.arange(n)

        top_k_indices = kandidat_idx[np.argsort(skor_hybrid[kandidat_idx])[::-1]]

        semua_hasil = []
        for i in top_k_indices:
            idx = int(i)
            semua_hasil.append(
                {
                    "indeks": idx,
                    "NAMA": data_dosen[idx].get("NAMA", "-"),
                    "PROGRAM_STUDI": data_dosen[idx].get("PROGRAM_STUDI", "-"),
                    "BIDANG_KEAHLIAN": data_dosen[idx].get("BIDANG_KEAHLIAN", "-"),
                    "JURNAL": data_dosen[idx].get("JURNAL", "-"),
                    "judul bimbing": data_dosen[idx].get("judul bimbing", "-"),
                    "judul uji": data_dosen[idx].get("judul uji", "-"),
                    "RIWAYAT_PENDIDIKAN": data_dosen[idx].get("RIWAYAT_PENDIDIKAN", "-"),
                    "Hybrid Score": round(float(skor_hybrid[idx]), 3),
                    "Lexical Score": round(float(skor_lex[idx]), 3),
                    "Semantic Score": round(float(skor_sem[idx]), 3),
                }
            )
        return semua_hasil

    def _enrich(
        self,
        top_k: List[Dict[str, Any]],
        token_mhs: List[str],
        token_dosen: List[List[str]],
        keybert_data: List[List[Tuple[str, float]]],
    ) -> List[Dict[str, Any]]:
        # Tambahkan irisan kata dan frasa KeyBERT ke hasil akhir
        mhs_set = set(token_mhs)

        hasil_final = []
        for h in top_k:
            idx = h["indeks"]
            dsn_set = set(token_dosen[idx])
            irisan = list(mhs_set.intersection(dsn_set))
            kata_lex = [str(k).replace("_", " ") for k in irisan]

            kw_result = keybert_data[idx]
            kata_sem = [str(k[0]) for k in kw_result]

            h["Irisan Kata (Lexical)"] = ", ".join(kata_lex) if kata_lex else "-"
            h["Frasa Terkait (KeyBERT)"] = ", ".join(kata_sem) if kata_sem else "-"
            h["Topik Utama Dosen (statis, bukan match ke proposal)"] = ", ".join(kata_sem) if kata_sem else "-"

            del h["indeks"]
            hasil_final.append(h)

        return hasil_final


engine = RecommendationEngine()
