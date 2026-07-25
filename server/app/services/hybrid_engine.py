import hashlib
import threading
import os
import numpy as np
from typing import List, Dict, Any

from app.config import Config
from app.services.bm25_service import BM25Service
from app.services.sbert_service import SbertService
from app.utils.text_preprocessor import PreprocessingPipeline

def _fingerprint_data(data_dosen: List[Dict]) -> str:
    payload_parts = []
    for d in data_dosen:
        bagian = "-".join(
            [
                str(d.get("NAMA", "")),
                str(d.get("BIDANG_KEAHLIAN", "")),
                str(d.get("JURNAL", "")),
                str(d.get("RIWAYAT_PENDIDIKAN", "")),
                str(d.get("judul bimbing", "")),
                str(d.get("judul uji", "")),
            ]
        )
        payload_parts.append(bagian)
    payload = "|".join(payload_parts)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()

class HybridEngine:
    def __init__(self):
        self._lock = threading.RLock()
        self.bm25 = BM25Service()
        self.sbert = SbertService()
        self.data_dosen = []
        self.token_dosen = []
        self.is_ready = False

    def siapkan_cache(self, data_dosen: List[Dict], force_recalculate: bool = False):
        with self._lock:
            self.data_dosen = data_dosen
            teks_bobot_list = []
            teks_raw_list = []
            for dsn in data_dosen:
                tb, tr = PreprocessingPipeline.buat_teks_terbobot(dsn)
                teks_bobot_list.append(tb)
                teks_raw_list.append(tr)

            self.token_dosen = [PreprocessingPipeline.tokenize_ngram(t) for t in teks_bobot_list]
            self.bm25.siapkan(self.token_dosen)

            fingerprint_baru = _fingerprint_data(data_dosen)
            pakai_cache = False

            if not force_recalculate:
                fingerprint_lama = None
                if os.path.exists(Config.FINGERPRINT_CACHE):
                    with open(Config.FINGERPRINT_CACHE, "r") as f:
                        fingerprint_lama = f.read().strip()
                if fingerprint_lama == fingerprint_baru:
                    if self.sbert.load_cache() and self.sbert.vektor_dosen is not None and self.sbert.vektor_dosen.shape[0] == len(data_dosen):
                        pakai_cache = True

            if not pakai_cache:
                self.sbert.ekstrak_dan_simpan(teks_bobot_list, teks_raw_list)
                try:
                    with open(Config.FINGERPRINT_CACHE, "w") as f:
                        f.write(fingerprint_baru)
                except Exception:
                    pass

            self.is_ready = True

    def sinkronisasi_incremental(self, data_terbaru: List[Dict]):
        with self._lock:
            peta_lama = {str(d.get("ID_DOSEN")): idx for idx, d in enumerate(self.data_dosen)}
            peta_baru = {str(d.get("ID_DOSEN")): d for d in data_terbaru}

            new_data_dosen = []
            new_token_dosen = []
            new_keybert = []
            new_vektors = []

            is_changed = False

            for id_b, dsn_baru in peta_baru.items():
                if id_b in peta_lama:
                    idx_lama = peta_lama[id_b]
                    dsn_lama = self.data_dosen[idx_lama]
                    
                    fp_lama = _fingerprint_data([dsn_lama])
                    fp_baru = _fingerprint_data([dsn_baru])
                    
                    if fp_lama == fp_baru:
                        new_data_dosen.append(dsn_lama)
                        new_token_dosen.append(self.token_dosen[idx_lama])
                        new_keybert.append(self.sbert.keybert_data[idx_lama])
                        new_vektors.append(self.sbert.vektor_dosen[idx_lama])
                    else:
                        is_changed = True
                        tb, tr = PreprocessingPipeline.buat_teks_terbobot(dsn_baru)
                        vek, kw = self.sbert.ekstrak_parsial(tb, tr)
                        new_data_dosen.append(dsn_baru)
                        new_token_dosen.append(PreprocessingPipeline.tokenize_ngram(tb))
                        new_keybert.append(kw)
                        new_vektors.append(vek)
                else:
                    is_changed = True
                    tb, tr = PreprocessingPipeline.buat_teks_terbobot(dsn_baru)
                    vek, kw = self.sbert.ekstrak_parsial(tb, tr)
                    new_data_dosen.append(dsn_baru)
                    new_token_dosen.append(PreprocessingPipeline.tokenize_ngram(tb))
                    new_keybert.append(kw)
                    new_vektors.append(vek)

            if len(peta_lama) != sum(1 for id_b in peta_baru.items() if id_b[0] in peta_lama):
                is_changed = True

            if is_changed:
                self.data_dosen = new_data_dosen
                self.token_dosen = new_token_dosen
                self.sbert.keybert_data = new_keybert
                self.sbert.vektor_dosen = np.array(new_vektors)

                self.bm25.siapkan(self.token_dosen)
                self.sbert.simpan_cache()

                fingerprint_baru = _fingerprint_data(self.data_dosen)
                try:
                    with open(Config.FINGERPRINT_CACHE, "w") as f:
                        f.write(fingerprint_baru)
                except Exception:
                    pass
                print("[INFO] Sinkronisasi Incremental selesai!")
            else:
                print("[INFO] Tidak ada perubahan data, skip sinkronisasi.")

    def _rank(self, skor_lex: np.ndarray, skor_sem: np.ndarray, bobot_lex: float, bobot_sem: float, k_rank: int) -> List[Dict]:
        skor_hybrid = (bobot_lex * skor_lex) + (bobot_sem * skor_sem)
        n = skor_hybrid.shape[0]
        k = min(k_rank, n)
        if k <= 0:
            return []

        if k < n:
            kandidat_idx = np.argpartition(skor_hybrid, -k)[-k:]
        else:
            kandidat_idx = np.arange(n)

        top_k_indices = kandidat_idx[np.argsort(skor_hybrid[kandidat_idx])[::-1]]
        
        semua_hasil = []
        for i in top_k_indices:
            idx = int(i)
            semua_hasil.append({
                "indeks": idx,
                "NAMA": self.data_dosen[idx].get("NAMA", "-"),
                "PROGRAM_STUDI": self.data_dosen[idx].get("PROGRAM_STUDI", "-"),
                "BIDANG_KEAHLIAN": self.data_dosen[idx].get("BIDANG_KEAHLIAN", "-"),
                "JURNAL": self.data_dosen[idx].get("JURNAL", "-"),
                "judul bimbing": self.data_dosen[idx].get("judul bimbing") or self.data_dosen[idx].get("JUDUL_BIMBING", "-"),
                "judul uji": self.data_dosen[idx].get("judul uji") or self.data_dosen[idx].get("JUDUL_UJI", "-"),
                "RIWAYAT_PENDIDIKAN": self.data_dosen[idx].get("RIWAYAT_PENDIDIKAN", "-"),
                "Hybrid Score": round(float(skor_hybrid[idx]), 3),
                "Lexical Score": round(float(skor_lex[idx]), 3),
                "Semantic Score": round(float(skor_sem[idx]), 3),
                "Alpha": float(bobot_lex),
                "Beta": float(bobot_sem)
            })
        return semua_hasil

    def _enrich(self, top_k: List[Dict], token_mhs: List[str]) -> List[Dict]:
        mhs_set = set(token_mhs)
        hasil_final = []
        for h in top_k:
            idx = h["indeks"]
            dsn_set = set(self.token_dosen[idx])
            irisan = list(mhs_set.intersection(dsn_set))
            kata_lex = [str(k).replace("_", " ") for k in irisan]

            kw_result = self.sbert.keybert_data[idx]
            kata_sem = [str(k[0]) for k in kw_result]

            h["Irisan Kata (Lexical)"] = ", ".join(kata_lex) if kata_lex else "-"
            h["Frasa Terkait (KeyBERT)"] = ", ".join(kata_sem) if kata_sem else "-"
            h["Topik Utama Dosen (statis, bukan match ke proposal)"] = ", ".join(kata_sem) if kata_sem else "-"

            del h["indeks"]
            hasil_final.append(h)
        return hasil_final

engine = HybridEngine()
