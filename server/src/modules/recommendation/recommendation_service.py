from typing import Optional, Dict, Any
import numpy as np

from server.src.core.config import Config
from server.src.modules.system.cache_service import CacheService
from server.src.modules.system.config_service import ConfigService
from server.src.modules.nlp.kamus_ekspansi import KAMUS_EKSPANSI
from server.src.modules.nlp.preprocessor import Preprocessor
from server.src.modules.nlp.hybrid_scorer import HybridEngine

class RecommendationService:
    """Core recommendation orchestrator combining NLP lexical, semantic, and hybrid pipeline."""
    
    @staticmethod
    def get_recommendations(judul: str, abstrak: str, k_rank: Optional[int] = None) -> Dict[str, Any]:
        cache = CacheService.get_instance()
        config = ConfigService.get_config()
        
        # Proper k_rank resolution and boundary checking
        if k_rank is None or k_rank <= 0:
            k_rank = Config.DEFAULT_K_RANK
        else:
            k_rank = min(int(k_rank), Config.MAX_K_RANK)
        
        query = f"{judul or ''} {abstrak or ''}".strip()
        query_tokens_raw = Preprocessor.clean_text(query).split()
        num_query_tokens = len(query_tokens_raw)
        
        is_adaptive = config.get('is_adaptive', True)
        adaptive_threshold = config.get('adaptive_alpha_threshold', 15)
        
        if is_adaptive:
            alpha, beta = HybridEngine.compute_adaptive_alpha(num_query_tokens, adaptive_threshold) if num_query_tokens > 0 else (0.5, 0.5)
        else:
            alpha = float(config.get('manual_alpha', 0.7))
            beta = 1.0 - alpha

        def empty_result() -> Dict[str, Any]:
            return {
                "metadata": {
                    "alpha": round(alpha, 2),
                    "beta": round(beta, 2),
                    "num_query_tokens": num_query_tokens,
                    "k_rank": k_rank
                },
                "pipeline": {},
                "recommendations": []
            }
            
        if not cache.is_ready or num_query_tokens == 0 or len(cache.dosen_list) == 0:
            return empty_result()

        # --- Pipeline Step 0: Preprocessing ---
        words_after_case_fold = Preprocessor.clean_text(query).split()
        words_after_stopword = Preprocessor.remove_stopwords(words_after_case_fold)
        query_tokens_bm25 = Preprocessor.preprocess_for_bm25(query)
        bigrams_only = [t for t in query_tokens_bm25 if '_' in t]

        # --- Pipeline Step 1: Ekspansi Sinonim ---
        query_text_expand, log_ekspansi = Preprocessor.ekspansi_query_dengan_log(query, KAMUS_EKSPANSI)
        query_text_sbert = Preprocessor.preprocess_for_sbert(query_text_expand)
        
        # --- Pipeline Step 2: BM25 Lexical Scoring ---
        bm25_norm = cache.bm25.get_scores(query_tokens_bm25)
        if len(bm25_norm) == 0:
            return empty_result()
            
        valid_indices = np.where(bm25_norm > 0)[0]

        # Top BM25 candidates for pipeline logging
        bm25_top_idx = np.argsort(bm25_norm)[::-1][:5]
        bm25_top_candidates = [
            {
                "nama": cache.dosen_list[int(i)].nama,
                "skor": round(float(bm25_norm[int(i)]), 4)
            }
            for i in bm25_top_idx if bm25_norm[int(i)] > 0
        ]

        # --- Pipeline Step 3: SBERT Semantic Scoring ---
        sbert_scores = np.zeros_like(bm25_norm)
        
        if len(valid_indices) > 0 and cache.sbert.corpus_embeddings is not None:
            query_emb = cache.sbert.encode_query(query_text_sbert)
            valid_sbert_scores = cache.sbert.cosine_similarity(query_emb, valid_indices)
            if len(valid_sbert_scores) == len(valid_indices):
                sbert_scores[valid_indices] = valid_sbert_scores

        # Top SBERT candidates for pipeline logging
        if len(valid_indices) > 0 and cache.sbert.corpus_embeddings is not None:
            sbert_top_local = np.argsort(sbert_scores[valid_indices])[::-1][:5]
            sbert_top_candidates = [
                {
                    "nama": cache.dosen_list[int(valid_indices[i])].nama,
                    "skor": round(float(sbert_scores[valid_indices[i]]), 4)
                }
                for i in sbert_top_local
            ]
        else:
            sbert_top_candidates = []
            
        # --- Pipeline Step 4: Hybrid Ranking ---
        top_k_indices, skor_hybrid = HybridEngine.rank(bm25_norm, sbert_scores, alpha, beta, k_rank)
        
        # --- Pipeline Step 5: XAI Enrichment & Output Formatting ---
        score_threshold = float(config.get('threshold', 0.0))
        recommendations = []
        
        for rank_pos, idx in enumerate(top_k_indices, start=1):
            idx = int(idx)
            hybrid_val = float(skor_hybrid[idx])
            
            if hybrid_val < score_threshold:
                continue
                
            dosen = cache.dosen_list[idx]
            
            # XAI Details
            dosen_tokens = cache.bm25.corpus_tokens[idx] if idx < len(cache.bm25.corpus_tokens) else []
            keybert_topics = cache.sbert.keybert_data[idx] if idx < len(cache.sbert.keybert_data) else []
            xai = HybridEngine.enrich_xai(query_tokens_bm25, dosen_tokens, keybert_topics)
            
            recommendations.append({
                "rank": rank_pos,
                "dosen": dosen.to_dict(),
                "scores": {
                    "hybrid": round(hybrid_val, 4),
                    "bm25": round(float(bm25_norm[idx]), 4),
                    "sbert": round(float(sbert_scores[idx]), 4)
                },
                "xai": xai
            })
            
        return {
            "metadata": {
                "alpha": round(alpha, 2),
                "beta": round(beta, 2),
                "num_query_tokens": num_query_tokens,
                "k_rank": k_rank,
                "threshold": score_threshold,
                "mode": ("keyword" if num_query_tokens < adaptive_threshold else "abstrak") if is_adaptive else "manual"
            },
            "pipeline": {
                "preprocessing": {
                    "raw_query": query.strip(),
                    "after_case_fold": words_after_case_fold[:20],
                    "after_stopword": words_after_stopword[:20],
                    "bigrams": bigrams_only[:10],
                    "final_tokens": [t for t in query_tokens_bm25 if '_' not in t][:15],
                    "total_tokens": len(query_tokens_bm25)
                },
                "ekspansi": {
                    "log": log_ekspansi,
                    "num_frasa_ditemukan": len(log_ekspansi)
                },
                "bm25": {
                    "num_candidates": int(len(valid_indices)),
                    "num_total_dosen": len(cache.dosen_list),
                    "top_candidates": bm25_top_candidates
                },
                "sbert": {
                    "num_computed": int(len(valid_indices)) if cache.sbert.corpus_embeddings is not None else 0,
                    "query_text": query_text_sbert[:200],
                    "top_candidates": sbert_top_candidates
                },
                "hybrid": {
                    "alpha": round(alpha, 2),
                    "beta": round(beta, 2),
                    "mode": ("keyword" if num_query_tokens < adaptive_threshold else "abstrak") if is_adaptive else "manual",
                    "num_results": len(recommendations)
                }
            },
            "recommendations": recommendations
        }
