import numpy as np
from typing import List, Dict

class HybridEngine:
    @staticmethod
    def compute_adaptive_alpha(num_query_tokens: int) -> tuple[float, float]:
        """Skenario B: Bobot dinamis berdasarkan panjang query."""
        if num_query_tokens < 15:
            return 0.70, 0.30  # Keyword mode — BM25 dominan
        return 0.35, 0.65      # Abstrak mode — SBERT dominan

    @staticmethod
    def rank(skor_lex: np.ndarray, skor_sem: np.ndarray, bobot_lex: float, bobot_sem: float, k_rank: int) -> np.ndarray:
        """Top-K Ranking efisien dengan argpartition."""
        skor_hybrid = (bobot_lex * skor_lex) + (bobot_sem * skor_sem)
        n = skor_hybrid.shape[0]
        k = min(k_rank, n)
        if k == 0:
            return np.array([])

        # O(n) partial sort
        kandidat_idx = np.argpartition(skor_hybrid, -k)[-k:]
        
        # Sort hanya k kandidat (O(k log k))
        top_k_indices = kandidat_idx[np.argsort(skor_hybrid[kandidat_idx])[::-1]]
        
        # Filter out zero hybrid scores if any
        top_k_indices = [idx for idx in top_k_indices if skor_hybrid[idx] > 0]
        return np.array(top_k_indices), skor_hybrid

    @staticmethod
    def enrich_xai(query_tokens: List[str], dosen_tokens: List[str], keybert_topics: List[tuple]) -> Dict:
        """Menambahkan Explainability Layer (Irisan Kata & KeyBERT Topics)"""
        mhs_set = set(query_tokens)
        dsn_set = set(dosen_tokens)
        
        irisan = mhs_set.intersection(dsn_set)
        kata_lex = [str(k).replace("_", " ") for k in irisan]
        
        kata_sem = [str(k[0]) for k in keybert_topics] if keybert_topics else []
        
        return {
            "irisan_kata": kata_lex,
            "topik_dosen": kata_sem
        }
