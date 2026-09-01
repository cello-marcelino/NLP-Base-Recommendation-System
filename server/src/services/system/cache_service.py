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

    @staticmethod
    def _get_default_steps():
        return [
            {
                "id": 1,
                "code": "loading_data",
                "title": "Load Data Dosen",
                "desc": "Mengambil data profil dari Storage / Database",
                "status": "pending",
                "duration_ms": 0,
                "detail": "Menghubungkan ke repository dan membaca dataset"
            },
            {
                "id": 2,
                "code": "preprocessing",
                "title": "Preprocessing Korpus",
                "desc": "Case folding, stopword removal, dan bigram n-gram",
                "status": "pending",
                "duration_ms": 0,
                "detail": "Membangun korpus teks normal dan korpus terbobot"
            },
            {
                "id": 3,
                "code": "vektoring",
                "title": "BM25 Lexical Vektoring",
                "desc": "Tokenisasi korpus terbobot & fitting BM25 Okapi",
                "status": "pending",
                "duration_ms": 0,
                "detail": "Menghitung matriks frekuensi dan inverted index"
            },
            {
                "id": 4,
                "code": "embedding",
                "title": "SBERT & KeyBERT Embedding",
                "desc": "Dense vector 384-dimensi & ekstraksi topik semantik",
                "status": "pending",
                "duration_ms": 0,
                "detail": "Menghitung representasi vektor semantik dense"
            },
            {
                "id": 5,
                "code": "persisting",
                "title": "Sinkronisasi Cache ke Disk",
                "desc": "Menyimpan snapshot embedding .npy & metadata ke disk",
                "status": "pending",
                "duration_ms": 0,
                "detail": "Serialisasi cache state untuk instant warmup berikutnya"
            }
        ]

    def __init__(self):
        self.is_ready: bool = False
        self.dosen_list: List[Dosen] = []
        self.bm25: BM25Engine = BM25Engine()
        self.sbert: SBERTEngine = SBERTEngine()
        self.repository = CompositeDosenRepository()
        self.warmup_status = {
            "state": "idle",
            "current_step": 0,
            "total_steps": 5,
            "step_code": "idle",
            "step_name": "Siap",
            "message": "Server siap beroperasi",
            "detail": "Semua model AI telah dimuat di memori",
            "progress_pct": 0,
            "elapsed_seconds": 0.0,
            "device": Config.TORCH_DEVICE.upper(),
            "total_dosen": 0,
            "completed": False,
            "started_at": None,
            "completed_at": None,
            "steps": self._get_default_steps()
        }
        
    @classmethod
    def get_instance(cls) -> 'CacheService':
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def initialize_cache_async(self, force_refresh: bool = False, force_reload: bool = False):
        """Menjalankan warm-up di background thread agar server langsung siap menerima HTTP requests."""
        thread = threading.Thread(
            target=self.initialize_cache,
            kwargs={"force_refresh": force_refresh, "force_reload": force_reload},
            daemon=True
        )
        thread.start()
        return thread

    def initialize_cache(self, force_refresh: bool = False, force_reload: bool = False):
        with self._lock:
            if self.is_ready and not force_refresh and not force_reload:
                return
            self._warm_up(force_refresh=force_refresh or force_reload)

    def _set_step_running(self, step_id: int, step_code: str, message: str, detail: str):
        self.warmup_status["current_step"] = step_id
        self.warmup_status["step_code"] = step_code
        self.warmup_status["message"] = message
        self.warmup_status["detail"] = detail
        self.warmup_status["progress_pct"] = (step_id - 1) * 20 + 5
        for s in self.warmup_status["steps"]:
            if s["id"] == step_id:
                s["status"] = "running"
                s["detail"] = detail
            elif s["id"] < step_id and s["status"] != "completed":
                s["status"] = "completed"

    def _set_step_completed(self, step_id: int, detail: str, duration_ms: int = 0):
        self.warmup_status["progress_pct"] = step_id * 20
        for s in self.warmup_status["steps"]:
            if s["id"] == step_id:
                s["status"] = "completed"
                s["duration_ms"] = duration_ms
                s["detail"] = detail

    def _set_step_error(self, step_id: int, error_msg: str):
        self.warmup_status["state"] = "error"
        self.warmup_status["message"] = f"Error: {error_msg}"
        self.warmup_status["detail"] = error_msg
        for s in self.warmup_status["steps"]:
            if s["id"] == step_id:
                s["status"] = "error"
                s["detail"] = error_msg

    def _warm_up(self, force_refresh: bool = False):
        logger.info("==================================================")
        logger.info("MEMULAI PROSES WARM-UP SERVER (SIREDO V3)")
        logger.info("==================================================")
        start_total = time.time()
        
        is_reload = force_refresh or (self.warmup_status.get("state") == "ready")
        self.is_ready = False
        self.warmup_status["state"] = "reloading" if is_reload else "warming_up"
        self.warmup_status["completed"] = False
        self.warmup_status["current_step"] = 0
        self.warmup_status["progress_pct"] = 0
        self.warmup_status["started_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.warmup_status["completed_at"] = None
        self.warmup_status["steps"] = self._get_default_steps()
        self.warmup_status["device"] = Config.TORCH_DEVICE.upper()
        self.warmup_status["message"] = "Memulai inisialisasi AI Engine..."
        self.warmup_status["detail"] = "Menyiapkan direktori dan dependensi NLP..."

        cache_dir = Config.CACHE_DIR
        os.makedirs(cache_dir, exist_ok=True)
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        
        sbert_cache = os.path.join(cache_dir, 'sbert_embeddings.npy')
        dosen_cache = os.path.join(cache_dir, 'dosen_data.pkl')
        
        # Step 1: Load Data Dosen
        self._set_step_running(1, "loading_data", "Mengambil data dosen dari Storage...", "Menghubungkan ke database dan membaca profil dosen...")
        logger.info(f"[1/5] {self.warmup_status['message']}")
        start_step = time.time()
        self.dosen_list = self.repository.get_all()
        if not self.dosen_list:
            logger.error("Gagal memuat data dosen dari sumber data manapun!")
            self._set_step_error(1, "Gagal memuat data dosen dari database/file")
            self.is_ready = True
            return
        d_count = len(self.dosen_list)
        self.warmup_status["total_dosen"] = d_count
        step_dur = int((time.time() - start_step) * 1000)
        self._set_step_completed(1, f"Berhasil memuat {d_count} data profil dosen", duration_ms=step_dur)
        logger.info(f"      [OK] Berhasil memuat {d_count} data dosen ({step_dur}ms)")

        # Step 2: Corpus Construction & Preprocessing
        self._set_step_running(2, "preprocessing", "Membangun Korpus & Preprocessing Teks...", f"Case folding, stopword removal & n-gram untuk {d_count} dosen...")
        logger.info(f"[2/5] {self.warmup_status['message']}")
        start_step = time.time()
        corpus_terbobot = []
        corpus_normal = []
        for d in self.dosen_list:
            tb, tn = Preprocessor.build_corpus_text(d)
            corpus_terbobot.append(tb)
            corpus_normal.append(tn)
        step_dur = int((time.time() - start_step) * 1000)
        self._set_step_completed(2, f"Preprocessing {d_count} dokumen korpus selesai", duration_ms=step_dur)
        logger.info(f"      [OK] Preprocessing korpus selesai ({step_dur}ms)")
        
        # Step 3: BM25 Fitting
        self._set_step_running(3, "vektoring", "Tokenisasi & Fitting BM25 Engine...", "Membangun inverted index dan matriks pembobotan BM25Okapi...")
        logger.info(f"[3/5] {self.warmup_status['message']}")
        start_step = time.time()
        corpus_tokens = [Preprocessor.preprocess_for_bm25(text) for text in corpus_terbobot]
        self.bm25.fit(corpus_tokens)
        step_dur = int((time.time() - start_step) * 1000)
        self._set_step_completed(3, f"Lexical BM25 Engine siap ({len(corpus_tokens)} dokumen)", duration_ms=step_dur)
        logger.info(f"      [OK] Lexical BM25 Engine siap ({step_dur}ms)")
        
        # Step 4: SBERT & KeyBERT Encoding
        self._set_step_running(4, "embedding", "Menyiapkan Semantic SBERT Engine & KeyBERT...", f"Meng-encode representasi vektor dense 384-dimensi ({Config.TORCH_DEVICE.upper()})...")
        logger.info(f"[4/5] {self.warmup_status['message']}")
        start_step = time.time()
        sbert_texts = [Preprocessor.preprocess_for_sbert(text) for text in corpus_terbobot]
        self.sbert.encode_corpus(sbert_texts, corpus_normal, cache_path=sbert_cache, force_refresh=force_refresh)
        step_dur = int((time.time() - start_step) * 1000)
        self._set_step_completed(4, f"Semantic SBERT & KeyBERT Embeddings siap ({Config.TORCH_DEVICE.upper()})", duration_ms=step_dur)
        logger.info(f"      [OK] Semantic SBERT Engine siap ({step_dur}ms)")
        
        # Step 5: Save Dosen cache to disk
        self._set_step_running(5, "persisting", "Menyimpan Snapshot Cache ke Disk...", "Serialisasi metadata & embeddings ke file pkl/npy...")
        logger.info(f"[5/5] {self.warmup_status['message']}")
        start_step = time.time()
        try:
            with open(dosen_cache, 'wb') as f:
                pickle.dump(self.dosen_list, f)
            step_dur = int((time.time() - start_step) * 1000)
            self._set_step_completed(5, "Snapshot cache tersimpan di disk", duration_ms=step_dur)
            logger.info(f"      [OK] Cache state tersimpan ({step_dur}ms)")
        except Exception as e:
            logger.warning(f"      [WARN] Gagal menyimpan cache pkl: {e}")
            self._set_step_completed(5, f"Peringatan penyimpanan cache: {e}", duration_ms=0)
            
        total_dur = time.time() - start_total
        self.is_ready = True
        self.warmup_status["state"] = "ready"
        self.warmup_status["step_code"] = "ready"
        self.warmup_status["step_name"] = "Ready & Idle"
        self.warmup_status["completed"] = True
        self.warmup_status["progress_pct"] = 100
        self.warmup_status["elapsed_seconds"] = round(total_dur, 2)
        self.warmup_status["message"] = f"AI Engine Siap & Idle ({total_dur:.2f}s)"
        self.warmup_status["detail"] = f"Total {len(self.dosen_list)} dosen aktif dalam memori ({Config.TORCH_DEVICE.upper()})"
        self.warmup_status["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        
        logger.info("==================================================")
        logger.info(f"SERVER WARM-UP SELESAI DALAM {total_dur:.2f} DETIK")
        logger.info("==================================================")

    def incremental_add(self, new_dosen: Dosen):
        """Tambahkan 1 dosen baru ke index tanpa full rebuild."""
        with self._lock:
            if not self.is_ready:
                self._warm_up()
                return
            
            logger.info(f"Mengeksekusi Incremental Add untuk Dosen {new_dosen.nidn}...")
            # 1. Append to dosen_list
            self.dosen_list.append(new_dosen)
            
            # 2. Build corpus for single dosen
            tb, tn = Preprocessor.build_corpus_text(new_dosen)
            
            # 3. Rebuild BM25 (cepat, ~0.1s)
            self._rebuild_bm25_index()
            
            # 4. Incremental SBERT
            self.sbert.add_single_embedding(
                Preprocessor.preprocess_for_sbert(tb), tn
            )
            
            # 5. Save cache to disk
            self._save_cache()
            logger.info("Incremental Add selesai.")

    def incremental_update(self, dosen_identifier):
        """Update 1 dosen di index tanpa full rebuild."""
        with self._lock:
            if not self.is_ready:
                self._warm_up()
                return
            
            logger.info(f"Mengeksekusi Incremental Update untuk Dosen ID {dosen_identifier}...")
            # 1. Find index in current list
            idx = self._find_dosen_index(dosen_identifier)
            if idx is None:
                logger.warning(f"Dosen dengan identifier {dosen_identifier} tidak ditemukan di cache. Melakukan warm-up fallback.")
                self._warm_up(force_refresh=True)
                return
            
            # 2. Reload from DB
            fresh_list = self.repository.get_all()
            fresh_dosen = None
            for d in fresh_list:
                if str(d.nidn) == str(dosen_identifier) or str(getattr(d, 'id', '')) == str(dosen_identifier):
                    fresh_dosen = d
                    break
            
            if not fresh_dosen:
                logger.warning(f"Dosen dengan identifier {dosen_identifier} tidak ditemukan di database. Melakukan warm-up fallback.")
                self._warm_up(force_refresh=True)
                return
            
            # 3. Replace in list
            self.dosen_list[idx] = fresh_dosen
            
            # 4. Rebuild BM25 with updated corpus
            self._rebuild_bm25_index()
            
            # 5. Incremental SBERT
            tb, tn = Preprocessor.build_corpus_text(fresh_dosen)
            self.sbert.update_single_embedding(
                idx, Preprocessor.preprocess_for_sbert(tb), tn
            )
            
            # 6. Save cache to disk
            self._save_cache()
            logger.info("Incremental Update selesai.")

    def incremental_delete(self, dosen_identifier):
        """Hapus 1 dosen dari index tanpa full rebuild."""
        with self._lock:
            if not self.is_ready:
                return
            
            logger.info(f"Mengeksekusi Incremental Delete untuk Dosen ID {dosen_identifier}...")
            idx = self._find_dosen_index(dosen_identifier)
            if idx is None:
                return
            
            # 1. Remove from list
            self.dosen_list.pop(idx)
            
            # 2. Rebuild BM25 
            self._rebuild_bm25_index()
            
            # 3. Remove from SBERT matrix
            self.sbert.delete_single_embedding(idx)
            
            # 4. Save cache
            self._save_cache()
            logger.info("Incremental Delete selesai.")

    def _find_dosen_index(self, identifier) -> Optional[int]:
        for i, d in enumerate(self.dosen_list):
            if str(d.nidn) == str(identifier) or str(getattr(d, 'id', '')) == str(identifier):
                return i
        return None

    def _rebuild_bm25_index(self):
        """Rebuild BM25 dari current dosen_list."""
        corpus_terbobot = []
        for d in self.dosen_list:
            tb, _ = Preprocessor.build_corpus_text(d)
            corpus_terbobot.append(tb)
        corpus_tokens = [Preprocessor.preprocess_for_bm25(text) for text in corpus_terbobot]
        self.bm25.fit(corpus_tokens)

    def _save_cache(self):
        """Simpan current state ke disk."""
        cache_dir = Config.CACHE_DIR
        sbert_cache = os.path.join(cache_dir, 'sbert_embeddings.npy')
        dosen_cache = os.path.join(cache_dir, 'dosen_data.pkl')
        kb_cache = os.path.join(cache_dir, 'keybert_dosen.json')
        
        if self.sbert.corpus_embeddings is not None:
            import numpy as np
            np.save(sbert_cache, self.sbert.corpus_embeddings)
        
        with open(dosen_cache, 'wb') as f:
            pickle.dump(self.dosen_list, f)
        
        if self.sbert.keybert_data:
            import json
            with open(kb_cache, 'w', encoding='utf-8') as f:
                json.dump(self.sbert.keybert_data, f, ensure_ascii=False, indent=2)
