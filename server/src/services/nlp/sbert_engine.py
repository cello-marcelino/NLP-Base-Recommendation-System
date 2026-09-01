import os
import json
from typing import List, Tuple, Optional
import numpy as np
from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT

from server.src.config.config import Config
from server.src.config.logging_config import logger
from server.src.services.nlp.stopwords import STOPWORDS

class SBERTEngine:
    """Semantic scoring engine with Sentence-BERT embeddings and KeyBERT XAI extraction."""
    
    MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
    
    def __init__(self):
        self.model: Optional[SentenceTransformer] = None
        self.kw_model: Optional[KeyBERT] = None
        self.corpus_embeddings: Optional[np.ndarray] = None
        self.keybert_data: List[List[Tuple[str, float]]] = []

    @staticmethod
    def get_compute_device() -> str:
        """Resolves target compute device based on Config.TORCH_DEVICE."""
        target = getattr(Config, 'TORCH_DEVICE', 'cpu').lower().strip()
        if target == 'cuda':
            try:
                import torch
                if torch.cuda.is_available():
                    return 'cuda'
                logger.warning("CUDA diminta namun GPU tidak terdeteksi. Melakukan fallback ke CPU.")
            except ImportError:
                logger.warning("PyTorch CUDA tidak terpasang. Melakukan fallback ke CPU.")
            return 'cpu'
        elif target == 'auto':
            try:
                import torch
                return 'cuda' if torch.cuda.is_available() else 'cpu'
            except ImportError:
                return 'cpu'
        return 'cpu'

    def load_model(self):
        """Lazy load SBERT and KeyBERT models on resolved compute device."""
        if self.model is None:
            device = self.get_compute_device()
            logger.info(f"Memuat model Sentence-BERT '{self.MODEL_NAME}' pada device: {device.upper()}...")
            self.model = SentenceTransformer(self.MODEL_NAME, device=device)
            self.kw_model = KeyBERT(model=self.model)

    def encode_corpus(self, corpus_texts: List[str], corpus_normal: List[str], cache_path: Optional[str] = None, force_refresh: bool = False) -> np.ndarray:
        self.load_model()
        device = self.get_compute_device()
        
        kb_cache_path = cache_path.replace('sbert_embeddings.npy', 'keybert_dosen.json') if cache_path else None
        
        # 1. Load or Generate SBERT Embeddings
        if cache_path and os.path.exists(cache_path) and not force_refresh:
            logger.info(f"Memuat SBERT cache embeddings dari disk: {cache_path}")
            self.corpus_embeddings = np.load(cache_path)
            if len(self.corpus_embeddings) != len(corpus_texts):
                logger.info("Jumlah data berubah, meregenerasi SBERT embeddings...")
                self.corpus_embeddings = self.model.encode(corpus_texts, convert_to_numpy=True, show_progress_bar=False, device=device)
                np.save(cache_path, self.corpus_embeddings)
        else:
            logger.info(f"Meng-encode korpus dosen dengan Sentence-BERT ({device.upper()})...")
            self.corpus_embeddings = self.model.encode(corpus_texts, convert_to_numpy=True, show_progress_bar=False, device=device)
            if cache_path:
                np.save(cache_path, self.corpus_embeddings)
                
        # 2. Load or Generate KeyBERT Keywords
        if kb_cache_path and os.path.exists(kb_cache_path) and not force_refresh:
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
        device = self.get_compute_device()
        logger.info(f"Mengekstrak topik kata kunci KeyBERT (Semantic XAI - {device.upper()})...")
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
        device = self.get_compute_device()
        return self.model.encode(query, convert_to_numpy=True, device=device)

    def cosine_similarity(self, query_embedding: np.ndarray, valid_indices: np.ndarray) -> np.ndarray:
        if self.corpus_embeddings is None or len(valid_indices) == 0:
            return np.array([])
            
        filtered_embeddings = self.corpus_embeddings[valid_indices]
        cos_scores = util.cos_sim(query_embedding, filtered_embeddings)[0].numpy()
        return np.clip(cos_scores, 0.0, None)

    def add_single_embedding(self, sbert_text: str, normal_text: str):
        """Encode 1 teks dan append ke corpus_embeddings matrix."""
        self.load_model()
        device = self.get_compute_device()
        
        logger.info(f"Incremental Add SBERT & KeyBERT...")
        new_emb = self.model.encode(sbert_text, convert_to_numpy=True, show_progress_bar=False, device=device)
        new_emb = new_emb.reshape(1, -1)
        
        if self.corpus_embeddings is not None:
            self.corpus_embeddings = np.vstack([self.corpus_embeddings, new_emb])
        else:
            self.corpus_embeddings = new_emb
        
        # KeyBERT for new entry
        new_kw = self.kw_model.extract_keywords(
            normal_text, keyphrase_ngram_range=(1, 3),
            stop_words=list(STOPWORDS), use_maxsum=True,
            nr_candidates=15, top_n=5
        )
        self.keybert_data.append([(str(k[0]), float(k[1])) for k in new_kw])

    def update_single_embedding(self, idx: int, sbert_text: str, normal_text: str):
        """Re-encode 1 teks dan replace baris idx di corpus_embeddings."""
        self.load_model()
        device = self.get_compute_device()
        
        logger.info(f"Incremental Update SBERT & KeyBERT index {idx}...")
        new_emb = self.model.encode(sbert_text, convert_to_numpy=True, show_progress_bar=False, device=device)
        
        if self.corpus_embeddings is not None and idx < len(self.corpus_embeddings):
            self.corpus_embeddings[idx] = new_emb
        
        # Re-extract KeyBERT for updated entry
        new_kw = self.kw_model.extract_keywords(
            normal_text, keyphrase_ngram_range=(1, 3),
            stop_words=list(STOPWORDS), use_maxsum=True,
            nr_candidates=15, top_n=5
        )
        if idx < len(self.keybert_data):
            self.keybert_data[idx] = [(str(k[0]), float(k[1])) for k in new_kw]

    def delete_single_embedding(self, idx: int):
        """Hapus baris idx dari corpus_embeddings dan keybert_data."""
        logger.info(f"Incremental Delete SBERT & KeyBERT index {idx}...")
        if self.corpus_embeddings is not None and idx < len(self.corpus_embeddings):
            self.corpus_embeddings = np.delete(self.corpus_embeddings, idx, axis=0)
        
        if idx < len(self.keybert_data):
            self.keybert_data.pop(idx)

