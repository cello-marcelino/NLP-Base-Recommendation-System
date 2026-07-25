import numpy as np
from rank_bm25 import BM25Okapi
from typing import List, Optional, Tuple

class BM25Service:
    def __init__(self):
        self.mesin_bm25: Optional[BM25Okapi] = None
        self.avg_idf: float = 0.0
        self.max_idf: float = 0.0

    def siapkan(self, token_dosen: List[List[str]]):
        self.mesin_bm25 = BM25Okapi(token_dosen)
        if self.mesin_bm25.idf:
            self.avg_idf = sum(self.mesin_bm25.idf.values()) / len(self.mesin_bm25.idf)
            self.max_idf = max(self.mesin_bm25.idf.values())
        else:
            self.avg_idf = self.max_idf = 0.0

    def hitung_leksikal_normalized(self, token_mhs: List[str]) -> np.ndarray:
        if not self.mesin_bm25:
            return np.array([])
        skor_mentah = np.array(self.mesin_bm25.get_scores(token_mhs), dtype=float)
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

    def hitung_bobot_adaptif(self, token_mhs: List[str]) -> Tuple[float, float, List[str]]:
        if not self.mesin_bm25 or not token_mhs:
            return 0.35, 0.65, []
            
        # Skenario B: Adaptive Hybrid Weighting (Alpha Dinamis)
        if len(token_mhs) < 15:
            bobot_lex = 0.70
            bobot_sem = 0.30
        else:
            bobot_lex = 0.35
            bobot_sem = 0.65
            
        kata_langka = [t for t in token_mhs if self.mesin_bm25.idf.get(t, self.max_idf) > self.avg_idf]
        kata_langka_unik = list(dict.fromkeys(kata_langka))
        return bobot_lex, bobot_sem, kata_langka_unik
