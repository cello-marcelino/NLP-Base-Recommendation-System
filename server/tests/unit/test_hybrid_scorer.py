import numpy as np
from server.src.services.nlp.hybrid_scorer import HybridEngine

def test_compute_adaptive_alpha_short_query():
    alpha, beta = HybridEngine.compute_adaptive_alpha(num_query_tokens=5, threshold=15)
    assert alpha == 0.70
    assert beta == 0.30

def test_compute_adaptive_alpha_long_query():
    alpha, beta = HybridEngine.compute_adaptive_alpha(num_query_tokens=25, threshold=15)
    assert alpha == 0.35
    assert beta == 0.65

def test_hybrid_rank():
    skor_lex = np.array([0.8, 0.2, 0.0])
    skor_sem = np.array([0.9, 0.4, 0.1])
    
    top_k_indices, scores = HybridEngine.rank(
        skor_lex=skor_lex,
        skor_sem=skor_sem,
        bobot_lex=0.5,
        bobot_sem=0.5,
        k_rank=2
    )
    
    assert len(top_k_indices) == 2
    assert top_k_indices[0] == 0
    assert top_k_indices[1] == 1

def test_enrich_xai():
    query_tokens = ["natural", "language", "processing", "analisis"]
    dosen_tokens = ["natural", "language", "bert", "transformer"]
    keybert_topics = [("deep learning", 0.8), ("transformer", 0.7)]
    
    xai = HybridEngine.enrich_xai(query_tokens, dosen_tokens, keybert_topics)
    assert "natural" in xai["irisan_kata"]
    assert "language" in xai["irisan_kata"]
    assert "analisis" not in xai["irisan_kata"]
    assert "deep learning" in xai["topik_dosen"]
