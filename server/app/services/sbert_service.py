import os
import json
import logging
import numpy as np
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Optional

from app.config import Config
from app.utils.stopwords import STOPWORDS

logger = logging.getLogger("siredo.sbert")

class SbertService:
    def __init__(self):
        self.model_sbert = SentenceTransformer(Config.SBERT_MODEL_NAME)
        self.kw_model = KeyBERT(model=self.model_sbert)
        self.vektor_dosen: Optional[np.ndarray] = None
        self.keybert_data: List[List[Tuple[str, float]]] = []

    def load_cache(self) -> bool:
        if os.path.exists(Config.VEKTOR_CACHE) and os.path.exists(Config.KEYBERT_CACHE):
            try:
                self.vektor_dosen = np.load(Config.VEKTOR_CACHE)
                with open(Config.KEYBERT_CACHE, "r") as f:
                    self.keybert_data = json.load(f)
                return True
            except Exception as e:
                logger.warning(f"Gagal membaca cache lokal: {e}")
        return False

    def encode_query(self, teks_mhs_expand: str) -> np.ndarray:
        return self.model_sbert.encode([teks_mhs_expand], convert_to_numpy=True)

    def hitung_semantik(self, vektor_mhs: np.ndarray, vektor_dosen: np.ndarray) -> np.ndarray:
        skor_mentah = cosine_similarity(vektor_mhs.reshape(1, -1), vektor_dosen)[0]
        return np.clip(skor_mentah, 0.0, None)

    def ekstrak_dan_simpan(self, teks_bobot_list: List[str], teks_raw_list: List[str]):
        logger.info("Menghitung ulang matriks SBERT...")
        self.vektor_dosen = np.array(self.model_sbert.encode(teks_bobot_list, convert_to_numpy=True))
        
        logger.info("Mengekstrak frasa KeyBERT...")
        raw_keywords = self.kw_model.extract_keywords(
            teks_raw_list,
            keyphrase_ngram_range=(1, 3),
            stop_words=list(STOPWORDS),
            use_maxsum=True,
            nr_candidates=15,
            top_n=5,
        )
        if len(teks_raw_list) == 1 and raw_keywords and isinstance(raw_keywords[0], tuple):
            self.keybert_data = [raw_keywords]
        else:
            self.keybert_data = raw_keywords
            
        try:
            os.makedirs(os.path.dirname(Config.VEKTOR_CACHE), exist_ok=True)
            np.save(Config.VEKTOR_CACHE, self.vektor_dosen)
            with open(Config.KEYBERT_CACHE, "w") as f:
                json.dump(self.keybert_data, f)
        except Exception as e:
            logger.error(f"Gagal menyimpan cache npy/json: {e}")

    def ekstrak_parsial(self, teks_bobot: str, teks_raw: str) -> Tuple[np.ndarray, List[Tuple[str, float]]]:
        logger.info("Menjalankan SBERT parsial untuk 1 dosen...")
        vektor_baru = self.model_sbert.encode([teks_bobot], convert_to_numpy=True)[0]
        
        raw_keywords = self.kw_model.extract_keywords(
            [teks_raw],
            keyphrase_ngram_range=(1, 3),
            stop_words=list(STOPWORDS),
            use_maxsum=True,
            nr_candidates=15,
            top_n=5,
        )
        if raw_keywords and isinstance(raw_keywords[0], list):
            kw = raw_keywords[0]
        else:
            kw = raw_keywords
        return vektor_baru, kw

    def simpan_cache(self):
        logger.info("Menyimpan ulang cache vektor & keybert secara parsial...")
        try:
            os.makedirs(os.path.dirname(Config.VEKTOR_CACHE), exist_ok=True)
            np.save(Config.VEKTOR_CACHE, self.vektor_dosen)
            with open(Config.KEYBERT_CACHE, "w") as f:
                json.dump(self.keybert_data, f)
        except Exception as e:
            logger.error(f"Gagal menyimpan cache npy/json: {e}")
