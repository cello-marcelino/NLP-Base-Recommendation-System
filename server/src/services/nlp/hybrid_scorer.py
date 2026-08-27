from typing import List, Dict, Tuple
import numpy as np

class HybridEngine:
    """Combines lexical and semantic scoring with adaptive weighting and XAI enrichment."""
    
    @staticmethod
    def compute_adaptive_alpha(num_query_tokens: int, threshold: int = 15) -> Tuple[float, float]:
        """
        Adaptive scenario: Dynamic weighting based on query length.
        - Short query (< threshold tokens): Keyword mode (BM25 dominant: alpha=0.70, beta=0.30)
        - Long query (>= threshold tokens): Abstract mode (SBERT dominant: alpha=0.35, beta=0.65)
        """
        if num_query_tokens < threshold:
            return 0.70, 0.30
        return 0.35, 0.65

    @staticmethod
    def rank(skor_lex: np.ndarray, skor_sem: np.ndarray, bobot_lex: float, bobot_sem: float, k_rank: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Top-K ranking with O(n + k log k) complexity using numpy argpartition.
        """
        skor_hybrid = (bobot_lex * skor_lex) + (bobot_sem * skor_sem)
        n = skor_hybrid.shape[0]
        
        if n == 0 or k_rank <= 0:
            return np.array([], dtype=int), skor_hybrid
            
        k = min(k_rank, n)
        
        # O(n) partial sort
        kandidat_idx = np.argpartition(skor_hybrid, -k)[-k:]
        
        # Sort only the top-k candidates (O(k log k))
        top_k_indices = kandidat_idx[np.argsort(skor_hybrid[kandidat_idx])[::-1]]
        
        # Filter out candidates with zero hybrid score
        top_k_indices = [idx for idx in top_k_indices if skor_hybrid[idx] > 0]
        return np.array(top_k_indices, dtype=int), skor_hybrid

    @staticmethod
    def enrich_xai(query_tokens: List[str], dosen_tokens: List[str], keybert_topics: List[Tuple[str, float]]) -> Dict[str, List[str]]:
        """
        Generates Explainable AI (XAI) metadata:
        - Lexical intersection (irisan kata kunci BM25)
        - Semantic topic keywords (KeyBERT extracted topics)
        """
        mhs_set = set(query_tokens)
        dsn_set = set(dosen_tokens)
        
        irisan = mhs_set.intersection(dsn_set)
        kata_lex = [str(k).replace("_", " ") for k in irisan]
        
        kata_sem = [str(k[0]) for k in keybert_topics] if keybert_topics else []
        
        return {
            "irisan_kata": sorted(kata_lex),
            "topik_dosen": kata_sem
        }

# Alias
HybridScorer = HybridEngine
