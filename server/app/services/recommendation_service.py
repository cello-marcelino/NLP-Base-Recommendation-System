from app.services.cache_service import CacheService
from app.services.nlp.preprocessor import Preprocessor
from app.services.nlp.hybrid_scorer import HybridEngine
from app.storage.config_manager import ConfigManager
import numpy as np

class RecommendationService:
    @staticmethod
    def get_recommendations(judul: str, abstrak: str, k_rank: int = None):
        cache = CacheService.get_instance()
        config = ConfigManager.get_config()
        if not k_rank:
            k_rank = 5
        
        # 1. Preprocessing
        # Untuk ekspansi, butuh dict. Since it's imported in preprocessor, we can just call it
        from app.utils.kamus_ekspansi import KAMUS_EKSPANSI
        query = (judul or "") + " " + (abstrak or "")
        
        query_tokens_raw = Preprocessor.clean_text(query).split()
        num_query_tokens = len(query_tokens_raw)
        
        # Helper to construct empty result
        def empty_result():
            is_adaptive = config.get('is_adaptive', True)
            if is_adaptive:
                alpha, beta = HybridEngine.compute_adaptive_alpha(num_query_tokens) if num_query_tokens > 0 else (0.5, 0.5)
            else:
                alpha = config.get('manual_alpha', 0.7)
                beta = 1.0 - alpha
            return {
                "metadata": {
                    "alpha": alpha,
                    "beta": beta,
                    "num_query_tokens": num_query_tokens,
                    "k_rank": k_rank
                },
                "pipeline": {},
                "recommendations": []
            }
            
        if not cache.is_ready:
            return empty_result()

        # --- Pipeline Step 0: Preprocessing ---
        words_after_case_fold = Preprocessor.clean_text(query).split()
        words_after_stopword = Preprocessor.remove_stopwords(words_after_case_fold)
        query_tokens_bm25 = Preprocessor.preprocess_for_bm25(query)
        bigrams_only = [t for t in query_tokens_bm25 if '_' in t]

        # --- Pipeline Step 1: Ekspansi Sinonim ---
        query_text_expand, log_ekspansi = Preprocessor.ekspansi_query_dengan_log(query, KAMUS_EKSPANSI)
        query_text_sbert = Preprocessor.preprocess_for_sbert(query_text_expand)
        
        # --- Pipeline Step 2: BM25 Scoring ---
        bm25_norm = cache.bm25.get_scores(query_tokens_bm25)
        if len(bm25_norm) == 0:
            return empty_result()
            
        valid_indices = np.where(bm25_norm > 0)[0]

        # Top BM25 candidates (before k-filter, for pipeline log)
        bm25_top_idx = np.argsort(bm25_norm)[::-1][:5]
        bm25_top_candidates = [
            {
                "nama": cache.dosen_list[int(i)].nama,
                "skor": round(float(bm25_norm[int(i)]), 4)
            }
            for i in bm25_top_idx if bm25_norm[int(i)] > 0
        ]

        # --- Pipeline Step 3: SBERT Scoring ---
        sbert_scores = np.zeros_like(bm25_norm)
        
        if len(valid_indices) > 0:
            query_emb = cache.sbert.encode_query(query_text_sbert)
            valid_sbert_scores = cache.sbert.cosine_similarity(query_emb, valid_indices)
            sbert_scores[valid_indices] = valid_sbert_scores

        # Top SBERT candidates (for pipeline log)
        if len(valid_indices) > 0:
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
        is_adaptive = config.get('is_adaptive', True)
        if is_adaptive:
            alpha, beta = HybridEngine.compute_adaptive_alpha(num_query_tokens)
        else:
            alpha = config.get('manual_alpha', 0.7)
            beta = 1.0 - alpha
        top_k_indices, skor_hybrid = HybridEngine.rank(bm25_norm, sbert_scores, alpha, beta, k_rank)
        
        # 4. Enrichment XAI & Formatting
        recommendations = []
        for idx in top_k_indices:
            idx = int(idx)
            dosen = cache.dosen_list[idx]
            
            # XAI
            dosen_tokens = cache.bm25.corpus_tokens[idx]
            keybert_topics = cache.sbert.keybert_data[idx] if cache.sbert.keybert_data else []
            xai = HybridEngine.enrich_xai(query_tokens_bm25, dosen_tokens, keybert_topics)
            
            recommendations.append({
                "dosen": dosen.to_dict(),
                "scores": {
                    "hybrid": float(skor_hybrid[idx]),
                    "bm25": float(bm25_norm[idx]),
                    "sbert": float(sbert_scores[idx])
                },
                "xai": xai
            })
            
        return {
            "metadata": {
                "alpha": alpha,
                "beta": beta,
                "num_query_tokens": num_query_tokens,
                "k_rank": k_rank
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
                    "num_computed": int(len(valid_indices)),
                    "query_text": query_text_sbert[:200],
                    "top_candidates": sbert_top_candidates
                },
                "hybrid": {
                    "alpha": alpha,
                    "beta": beta,
                    "mode": ("keyword" if num_query_tokens < 15 else "abstrak") if is_adaptive else "manual",
                    "num_results": len(recommendations)
                }
            },
            "recommendations": recommendations
        }
