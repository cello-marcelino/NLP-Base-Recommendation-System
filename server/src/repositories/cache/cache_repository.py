import os
import json
import numpy as np
from typing import Optional, List, Dict, Any

from server.src.config.config import Config
from server.src.config.logging_config import logger

class CacheRepository:
    """Handles disk-based caching for preprocessed NLP artifacts and embeddings."""
    
    @staticmethod
    def get_embeddings_path() -> str:
        return os.path.join(Config.CACHE_DIR, 'sbert_embeddings.npy')

    @staticmethod
    def get_keybert_cache_path() -> str:
        return os.path.join(Config.CACHE_DIR, 'keybert_dosen.json')

    @classmethod
    def load_embeddings(cls) -> Optional[np.ndarray]:
        path = cls.get_embeddings_path()
        if os.path.exists(path):
            try:
                embeddings = np.load(path)
                logger.info(f"Memuat SBERT cache embeddings dari disk: {path}")
                return embeddings
            except Exception as e:
                logger.warning(f"Gagal memuat cache embeddings: {e}")
        return None

    @classmethod
    def save_embeddings(cls, embeddings: np.ndarray):
        path = cls.get_embeddings_path()
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            np.save(path, embeddings)
            logger.info(f"SBERT embeddings disimpan ke disk: {path}")
        except Exception as e:
            logger.error(f"Gagal menyimpan cache embeddings: {e}")

    @classmethod
    def load_keybert_cache(cls) -> Optional[Dict[str, Any]]:
        path = cls.get_keybert_cache_path()
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Gagal memuat cache KeyBERT: {e}")
        return None

    @classmethod
    def save_keybert_cache(cls, data: Dict[str, Any]):
        path = cls.get_keybert_cache_path()
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Gagal menyimpan cache KeyBERT: {e}")
