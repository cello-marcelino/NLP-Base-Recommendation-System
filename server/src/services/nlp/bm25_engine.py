from typing import List
import numpy as np
from rank_bm25 import BM25Okapi

class BM25Engine:
    """Lexical scoring engine utilizing BM25Okapi with Z-Score Sigmoid normalization."""
    
    def __init__(self):
        self.bm25: BM25Okapi = None
        self.corpus_tokens: List[List[str]] = []
        self.avg_idf: float = 0.0
        self.max_idf: float = 0.0

    def fit(self, corpus_tokens: List[List[str]]):
        self.corpus_tokens = corpus_tokens
        self.bm25 = BM25Okapi(corpus_tokens)
        if self.bm25.idf:
            self.avg_idf = float(sum(self.bm25.idf.values()) / len(self.bm25.idf))
            self.max_idf = float(max(self.bm25.idf.values()))

    def get_scores(self, query_tokens: List[str]) -> np.ndarray:
        if not self.bm25 or not query_tokens:
            return np.array([])
            
        skor_mentah = np.array(self.bm25.get_scores(query_tokens))
        
        # Guard: all raw scores are zero
        if len(skor_mentah) == 0 or skor_mentah.max() <= 1e-9:
            return np.zeros_like(skor_mentah)
            
        mean = skor_mentah.mean()
        std = skor_mentah.std()
        
        # Guard: standard deviation is near zero
        if std < 1e-9:
            return np.zeros_like(skor_mentah)
            
        # Z-Score Sigmoid Normalization
        z = (skor_mentah - mean) / std
        skor_norm = 1.0 / (1.0 + np.exp(-z / 2.0))
        
        # Hard reset: candidates with 0 raw BM25 score are explicitly reset to 0.0
        skor_norm[skor_mentah <= 1e-9] = 0.0
        
        return skor_norm
