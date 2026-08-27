import os
import time
import pickle
import threading
from typing import List, Optional

from server.src.config.config import Config
from server.src.config.logging_config import logger
from server.src.models.dosen.dosen_model import Dosen
from server.src.repositories.dosen.dosen_repository import CompositeDosenRepository
from server.src.services.nlp.preprocessor import Preprocessor
from server.src.services.nlp.bm25_engine import BM25Engine
from server.src.services.nlp.sbert_engine import SBERTEngine

class CacheService:
    """Thread-safe Singleton managing in-memory lecturer data, BM25, and SBERT model state."""
    
    _instance: Optional['CacheService'] = None
    _lock = threading.RLock()

    def __init__(self):
        self.is_ready: bool = False
        self.dosen_list: List[Dosen] = []
        self.bm25: BM25Engine = BM25Engine()
        self.sbert: SBERTEngine = SBERTEngine()
        self.repository = CompositeDosenRepository()
        
    @classmethod
    def get_instance(cls) -> 'CacheService':
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def initialize_cache(self, force_refresh: bool = False, force_reload: bool = False):
        with self._lock:
            if self.is_ready and not force_refresh and not force_reload:
                return
            self._warm_up()

    def _warm_up(self):
        logger.info("==================================================")
        logger.info("MEMULAI PROSES WARM-UP SERVER (SIREDO V3)")
        logger.info("==================================================")
        start_total = time.time()
        
        cache_dir = Config.CACHE_DIR
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        
        sbert_cache = os.path.join(cache_dir, 'sbert_embeddings.npy')
        dosen_cache = os.path.join(cache_dir, 'dosen_data.pkl')
        
        # Step 1: Load Data Dosen
        logger.info("[1/5] Mengambil data dosen dari Storage (Database MySQL / Excel)...")
        start_step = time.time()
        self.dosen_list = self.repository.get_all()
        if not self.dosen_list:
            logger.error("Gagal memuat data dosen dari sumber data manapun!")
            self.is_ready = True
            return
        logger.info(f"      [OK] Berhasil memuat {len(self.dosen_list)} data dosen ({time.time() - start_step:.2f}s)")

        # Step 2: Corpus Construction & Preprocessing
        logger.info("[2/5] Membangun Korpus & Preprocessing Teks...")
        start_step = time.time()
        corpus_terbobot = []
        corpus_normal = []
        for d in self.dosen_list:
            tb, tn = Preprocessor.build_corpus_text(d)
            corpus_terbobot.append(tb)
            corpus_normal.append(tn)
        logger.info(f"      [OK] Preprocessing korpus selesai ({time.time() - start_step:.2f}s)")
        
        # Step 3: BM25 Fitting
        logger.info("[3/5] Tokenisasi & Fitting BM25 Engine...")
        start_step = time.time()
        corpus_tokens = [Preprocessor.preprocess_for_bm25(text) for text in corpus_terbobot]
        self.bm25.fit(corpus_tokens)
        logger.info(f"      [OK] Lexical BM25 Engine siap ({time.time() - start_step:.2f}s)")
        
        # Step 4: SBERT & KeyBERT Encoding
        logger.info("[4/5] Menyiapkan Semantic SBERT Engine (Model & Embeddings)...")
        start_step = time.time()
        sbert_texts = [Preprocessor.preprocess_for_sbert(text) for text in corpus_terbobot]
        self.sbert.encode_corpus(sbert_texts, corpus_normal, cache_path=sbert_cache)
        logger.info(f"      [OK] Semantic SBERT Engine siap ({time.time() - start_step:.2f}s)")
        
        # Step 5: Save Dosen cache to disk
        logger.info("[5/5] Menyimpan Cache Dosen ke disk...")
        start_step = time.time()
        try:
            with open(dosen_cache, 'wb') as f:
                pickle.dump(self.dosen_list, f)
            logger.info(f"      [OK] Cache state tersimpan ({time.time() - start_step:.2f}s)")
        except Exception as e:
            logger.warning(f"      [WARN] Gagal menyimpan cache pkl: {e}")
            
        self.is_ready = True
        logger.info("==================================================")
        logger.info(f"SERVER WARM-UP SELESAI DALAM {time.time() - start_total:.2f} DETIK")
        logger.info("==================================================")
