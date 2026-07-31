from rank_bm25 import BM25Okapi
import numpy as np

class BM25Engine:
    def __init__(self):
        self.bm25 = None
        self.corpus_tokens = []
        self.avg_idf = 0
        self.max_idf = 0

    def fit(self, corpus_tokens: list[list[str]]):
        self.corpus_tokens = corpus_tokens
        self.bm25 = BM25Okapi(corpus_tokens)
        if self.bm25.idf:
            self.avg_idf = sum(self.bm25.idf.values()) / len(self.bm25.idf)
            self.max_idf = max(self.bm25.idf.values())

    def get_scores(self, query_tokens: list[str]) -> np.ndarray:
        if not self.bm25:
            return np.array([])
            
        skor_mentah = np.array(self.bm25.get_scores(query_tokens))
        
        # Guard: jika semua skor = 0
        if skor_mentah.max() <= 1e-9:
            return np.zeros_like(skor_mentah)
            
        mean = skor_mentah.mean()
        std = skor_mentah.std()
        
        # Guard: jika deviasi = 0
        if std < 1e-9:
            return np.zeros_like(skor_mentah)
            
        # Z-Score Sigmoid
        z = (skor_mentah - mean) / std
        skor_norm = 1.0 / (1.0 + np.exp(-z / 2.0))
        
        # Hard reset: dosen dengan BM25 mentah = 0 -> dinol-kan
        skor_norm[skor_mentah <= 1e-9] = 0.0
        
        return skor_norm

