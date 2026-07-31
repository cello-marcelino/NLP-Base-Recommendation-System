from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
import numpy as np
import os
import json
from flask import current_app
from app.utils.stopwords import STOPWORDS

class SBERTEngine:
    def __init__(self):
        self.model = None
        self.kw_model = None
        self.corpus_embeddings = None
        self.keybert_data = []

    def load_model(self):
        if self.model is None:
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            self.kw_model = KeyBERT(model=self.model)
            
    def encode_corpus(self, corpus_texts: list[str], corpus_normal: list[str], cache_path: str = None) -> np.ndarray:
        self.load_model()
        
        # Determine paths
        kb_cache_path = cache_path.replace('sbert_embeddings.npy', 'keybert_dosen.json') if cache_path else None
        
        # Load or Generate SBERT
        if cache_path and os.path.exists(cache_path):
            self.corpus_embeddings = np.load(cache_path)
            if len(self.corpus_embeddings) != len(corpus_texts):
                self.corpus_embeddings = self.model.encode(corpus_texts, convert_to_numpy=True, show_progress_bar=True)
                np.save(cache_path, self.corpus_embeddings)
        else:
            self.corpus_embeddings = self.model.encode(corpus_texts, convert_to_numpy=True, show_progress_bar=True)
            if cache_path:
                np.save(cache_path, self.corpus_embeddings)
                
        # Load or Generate KeyBERT
        if kb_cache_path and os.path.exists(kb_cache_path):
            with open(kb_cache_path, 'r', encoding='utf-8') as f:
                self.keybert_data = json.load(f)
            if len(self.keybert_data) != len(corpus_normal):
                self._generate_keybert(corpus_normal, kb_cache_path)
        else:
            self._generate_keybert(corpus_normal, kb_cache_path)
            
        return self.corpus_embeddings

    def _generate_keybert(self, corpus_normal: list[str], kb_cache_path: str = None):
        print("      [WAIT] Mengekstrak topik KeyBERT (Semantic XAI)...")
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
            # convert np.float to float for json
            clean_kw = [(kw[0], float(kw[1])) for kw in raw_keywords]
            self.keybert_data.append(clean_kw)
            
        if kb_cache_path:
            with open(kb_cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.keybert_data, f)

    def set_corpus_embeddings(self, embeddings: np.ndarray):
        self.corpus_embeddings = embeddings

    def encode_query(self, query: str) -> np.ndarray:
        self.load_model()
        return self.model.encode(query, convert_to_numpy=True)

    def cosine_similarity(self, query_embedding: np.ndarray, valid_indices: np.ndarray) -> np.ndarray:
        if self.corpus_embeddings is None or len(valid_indices) == 0:
            return np.array([])
            
        filtered_embeddings = self.corpus_embeddings[valid_indices]
        # Cosine similarity using sentence_transformers util
        cos_scores = util.cos_sim(query_embedding, filtered_embeddings)[0].numpy()
        return np.clip(cos_scores, 0.0, None)

