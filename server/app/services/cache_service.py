import threading
import os
import pickle
import numpy as np
from flask import current_app
from app.storage.database import Database
from app.services.nlp.preprocessor import Preprocessor
from app.services.nlp.bm25_engine import BM25Engine
from app.services.nlp.sbert_engine import SBERTEngine

class CacheService:
    _instance = None
    _lock = threading.RLock()

    def __init__(self):
        self.is_ready = False
        self.dosen_list = []
        self.bm25 = BM25Engine()
        self.sbert = SBERTEngine()
        
    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def initialize_cache(self, app_context=None):
        with self._lock:
            if self.is_ready:
                return

            # Note: app_context should be provided if calling outside request context
            if app_context:
                with app_context:
                    self._warm_up()
            else:
                self._warm_up()

    def _warm_up(self):
        import time
        print("\n" + "="*50)
        print("MEMULAI PROSES WARM-UP SERVER (SIREDO V3)")
        print("="*50)
        start_total = time.time()
        
        cache_dir = current_app.config['CACHE_DIR']
        sbert_cache = os.path.join(cache_dir, 'sbert_embeddings.npy')
        dosen_cache = os.path.join(cache_dir, 'dosen_data.pkl')
        
        # Load Data
        print("[1/5] Sedang mengambil data dosen dari Storage (Database / Excel)...")
        start_step = time.time()
        self.dosen_list = Database.get_all_dosen()
        if not self.dosen_list:
            print("[ERROR] Gagal memuat data dosen!")
            self.is_ready = True
            return
        print(f"      [OK] Berhasil memuat {len(self.dosen_list)} data dosen. ({(time.time() - start_step):.2f} detik)")

        print("[2/5] Sedang melakukan Build Corpus & Preprocessing...")
        start_step = time.time()
        corpus_terbobot = []
        corpus_normal = []
        for d in self.dosen_list:
            tb, tn = Preprocessor.build_corpus_text(d)
            corpus_terbobot.append(tb)
            corpus_normal.append(tn)
        print(f"      [OK] Preprocessing selesai. ({(time.time() - start_step):.2f} detik)")
        
        # BM25 setup
        print("[3/5] Sedang melakukan Tokenisasi & Fitting BM25 Engine...")
        start_step = time.time()
        corpus_tokens = [Preprocessor.preprocess_for_bm25(text) for text in corpus_terbobot]
        self.bm25.fit(corpus_tokens)
        print(f"      [OK] Lexical BM25 Engine siap! ({(time.time() - start_step):.2f} detik)")
        
        # SBERT setup
        print("[4/5] Sedang menyiapkan SBERT Engine (Load Model & Embeddings)...")
        print("      (Jika model belum ada, sistem akan mendownload secara otomatis dari HuggingFace, ini memakan waktu)")
        start_step = time.time()
        sbert_texts = [Preprocessor.preprocess_for_sbert(text) for text in corpus_terbobot]
        self.sbert.encode_corpus(sbert_texts, corpus_normal, cache_path=sbert_cache)
        print(f"      [OK] Semantic SBERT Engine siap! ({(time.time() - start_step):.2f} detik)")
        
        # Save dosen data cache for quick restart mapping if needed (optional)
        print("[5/5] Sedang menyimpan Cache Sistem ke disk...")
        start_step = time.time()
        with open(dosen_cache, 'wb') as f:
            pickle.dump(self.dosen_list, f)
        print(f"      [OK] Caching state tersimpan. ({(time.time() - start_step):.2f} detik)")
            
        self.is_ready = True
        print("\n" + "="*50)
        print(f"SERVER WARM-UP SELESAI DALAM {(time.time() - start_total):.2f} DETIK")
        print("="*50 + "\n")
