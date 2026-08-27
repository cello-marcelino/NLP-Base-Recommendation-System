import numpy as np
from server.src.services.nlp.bm25_engine import BM25Engine

def test_bm25_fit_and_get_scores():
    engine = BM25Engine()
    corpus = [
        ["nlp", "bert", "text", "mining"],
        ["computer", "vision", "yolo", "image"],
        ["data", "mining", "ahp", "spk"]
    ]
    engine.fit(corpus)
    
    # Query for nlp
    scores = engine.get_scores(["nlp", "bert"])
    assert len(scores) == 3
    assert scores[0] > scores[1]
    assert scores[1] == 0.0  # Zero raw score becomes 0.0

def test_bm25_empty_query():
    engine = BM25Engine()
    corpus = [["nlp", "bert"], ["vision", "yolo"]]
    engine.fit(corpus)
    scores = engine.get_scores([])
    assert len(scores) == 0
