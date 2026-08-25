import os
import json
from typing import List, Tuple, Optional
import numpy as np
from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT

from server.src.core.logging import logger
from server.src.modules.nlp.stopwords import STOPWORDS

class SBERTEngine:
    """Semantic scoring engine with Sentence-BERT embeddings and KeyBERT XAI extraction."""
    
    MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
    
    def __init__(self):
        self.model: Optional[SentenceTransformer] = None
        self.kw_model: Optional[KeyBERT] = None
        self.corpus_embeddings: Optional[np.ndarray] = None
        self.keybert_data: List[List[Tuple[str, float]]] = []

    def load_model(self):
        """Lazy load SBERT and KeyBERT models."""
        if self.model is None:
            logger.info(f"Memuat model Sentence-BERT '{self.MODEL_NAME}'...")
            self.model = SentenceTransformer(self.MODEL_NAME)
            self.kw_model = KeyBERT(model=self.model)

    def encode_corpus(self, corpus_texts: List[str], corpus_normal: List[str], cache_path: Optional[str] = None) -> np.ndarray:
        self.load_model()
        
        kb_cache_path = cache_path.replace('sbert_embeddings.npy', 'keybert_dosen.json') if cache_path else None
        
        # 1. Load or Generate SBERT Embeddings
        if cache_path and os.path.exists(cache_path):
            logger.info(f"Memuat SBERT cache embeddings dari disk: {cache_path}")
            self.corpus_embeddings = np.load(cache_path)
            if len(self.corpus_embeddings) != len(corpus_texts):
                logger.info("Jumlah data berubah, meregenerasi SBERT embeddings...")
                self.corpus_embeddings = self.model.encode(corpus_texts, convert_to_numpy=True, show_progress_bar=False)
                np.save(cache_path, self.corpus_embeddings)
        else:
            logger.info("Meng-encode korpus dosen dengan Sentence-BERT...")
            self.corpus_embeddings = self.model.encode(corpus_texts, convert_to_numpy=True, show_progress_bar=False)
            if cache_path:
                np.save(cache_path, self.corpus_embeddings)
                
        # 2. Load or Generate KeyBERT Keywords
        if kb_cache_path and os.path.exists(kb_cache_path):
            try:
                with open(kb_cache_path, 'r', encoding='utf-8') as f:
                    self.keybert_data = json.load(f)
                if len(self.keybert_data) != len(corpus_normal):
                    self._generate_keybert(corpus_normal, kb_cache_path)
            except Exception as e:
                logger.warning(f"Gagal memuat cache KeyBERT: {e}. Meregenerasi...")
                self._generate_keybert(corpus_normal, kb_cache_path)
        else:
            self._generate_keybert(corpus_normal, kb_cache_path)
            
        return self.corpus_embeddings

    def _generate_keybert(self, corpus_normal: List[str], kb_cache_path: Optional[str] = None):
        logger.info("Mengekstrak topik kata kunci KeyBERT (Semantic XAI)...")
        self.keybert_data = []
        for teks in corpus_normal:
            raw_keywords = self.kw_model.extract_keywords(
                teks,
                keyphrase_ngram_range=(1, 3),
                stop_words=list(STOPWORDS),
                use_maxsum=True,
                nr_candidates=15,
                top_n=5
            )
            clean_kw = [(str(kw[0]), float(kw[1])) for kw in raw_keywords]
            self.keybert_data.append(clean_kw)
            
        if kb_cache_path:
            with open(kb_cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.keybert_data, f, ensure_ascii=False, indent=2)

    def set_corpus_embeddings(self, embeddings: np.ndarray):
        self.corpus_embeddings = embeddings

    def encode_query(self, query: str) -> np.ndarray:
        self.load_model()
        return self.model.encode(query, convert_to_numpy=True)

    def cosine_similarity(self, query_embedding: np.ndarray, valid_indices: np.ndarray) -> np.ndarray:
        if self.corpus_embeddings is None or len(valid_indices) == 0:
            return np.array([])
            
        filtered_embeddings = self.corpus_embeddings[valid_indices]
        cos_scores = util.cos_sim(query_embedding, filtered_embeddings)[0].numpy()
        return np.clip(cos_scores, 0.0, None)
