import os
import re
import pandas as pd
import numpy as np
from nltk import ngrams
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from sklearn.metrics.pairwise import cosine_similarity
from utils import KAMUS_EKSPANSI, STOPWORDS

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.feature_extraction.text")

print("Menginisialisasi Model Semantik...")
model_sbert = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
kw_model = KeyBERT(model=model_sbert) # type:ignore

# Path absolut untuk mengunci lokasi file cache bray
VEKTOR_CACHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/vektor_dosen.npy'))

CACHE = {
    "data_dosen": [],
    "teks_bobot_list": [],
    "teks_raw_list": [],
    "token_dosen": [],
    "vektor_dosen": None,
    "mesin_bm25": None,
    "is_ready": False
}

class PreprocessingPipeline:
    @staticmethod
    def ekspansi_query_dengan_log(teks, kamus=KAMUS_EKSPANSI):
        teks_lower = teks.lower()
        teks_ekspansi = teks_lower
        log_ekspansi = {}
        sorted_keys = sorted(kamus.keys(), key=len, reverse=True)
        for frasa in sorted_keys:
            if frasa in teks_lower:
                hasil = " ".join(kamus[frasa])
                teks_ekspansi += " " + hasil
                log_ekspansi[frasa] = hasil
        return teks_ekspansi, log_ekspansi

    @staticmethod
    def tokenize_ngram(teks, n=2):
        tokens = re.findall(r'\b[a-z0-9]{2,}\b', teks.lower()) 
        tokens_bersih = [t for t in tokens if t not in STOPWORDS]
        bigrams = ["_".join(g) for g in ngrams(tokens_bersih, n)]
        return tokens_bersih + bigrams

    @staticmethod
    def buat_teks_terbobot(dosen):
        keahlian = str(dosen.get('BIDANG_KEAHLIAN', ''))
        bimbing = str(dosen.get('judul bimbing', ''))
        uji = str(dosen.get('judul uji', ''))
        jurnal = str(dosen.get('JURNAL', ''))
        pendidikan = str(dosen.get('RIWAYAT_PENDIDIKAN', ''))
        
        inti = f"{keahlian} " * 3 + f"{bimbing} " * 3 + f"{uji} " * 2 + f"{jurnal} "
        teks_terbobot = f"{inti} {pendidikan}"
        teks_normal = f"{pendidikan} {keahlian} {jurnal} {uji} {bimbing}"
        return teks_terbobot, teks_normal

class ScoringPipeline:
    @staticmethod
    def hitung_leksikal(token_mhs):
        skor_mentah = CACHE["mesin_bm25"].get_scores(token_mhs)
        nilai_max = max(skor_mentah) if max(skor_mentah) > 0 else 1
        return [skor / nilai_max for skor in skor_mentah]

    @staticmethod
    def hitung_semantik(teks_mhs):
        vektor_mhs = np.array(model_sbert.encode([teks_mhs], convert_to_numpy=True))
        return cosine_similarity(vektor_mhs, CACHE["vektor_dosen"])[0]

class RecommendationEngine:
    @staticmethod
    def siapkan_cache(data_dosen, force_recalculate=False):
        """Memproses Vektor secara cerdas (Membaca file lokal npy jika sudah ada)"""
        CACHE["data_dosen"] = data_dosen
        CACHE["teks_bobot_list"] = []
        CACHE["teks_raw_list"] = []
        
        for dsn in data_dosen:
            tb, tr = PreprocessingPipeline.buat_teks_terbobot(dsn)
            CACHE["teks_bobot_list"].append(tb)
            CACHE["teks_raw_list"].append(tr)
            
        CACHE["token_dosen"] = [PreprocessingPipeline.tokenize_ngram(t) for t in CACHE["teks_bobot_list"]]
        
        # --- LEVEL 1 OPTIMIZATION LAYER ---
        folder_cache = os.path.dirname(VEKTOR_CACHE_PATH)
        if not os.path.exists(folder_cache):
            os.makedirs(folder_cache, exist_ok=True)
            
        pakai_file_cache = False
        
        # Cek apakah file npy ada dan tidak dipaksa hitung ulang bray
        if not force_recalculate and os.path.exists(VEKTOR_CACHE_PATH):
            try:
                vektor_lokal = np.load(VEKTOR_CACHE_PATH)
                # Validasi ukuran: Pastikan total baris matriks sama dengan total dosen di MySQL
                if vektor_lokal.shape[0] == len(data_dosen):
                    CACHE["vektor_dosen"] = vektor_lokal
                    pakai_file_cache = True
                    print("⚡ [INSTANT LOAD] Matriks SBERT berhasil dimuat dari cache lokal (0.1 detik)!")
                else:
                    print("⚠️ Jumlah data dosen berubah! Bersiap menghitung ulang matriks vektor...")
            except Exception as e:
                print(f"⚠️ Gagal membaca file npy: {e}, mengalihkan ke hitung manual...")
        
        # Jika file cache tidak ada atau tidak valid, panggil SBERT untuk hitung ulang bray
        if not pakai_file_cache:
            print("⏳ Menghitung ulang matriks SBERT dari awal (Sabar, proses ini memakan waktu)...")
            CACHE["vektor_dosen"] = np.array(model_sbert.encode(CACHE["teks_bobot_list"], convert_to_numpy=True))
            try:
                np.save(VEKTOR_CACHE_PATH, CACHE["vektor_dosen"])
                print(f"💾 Sukses mengunci cache file npy baru di: {VEKTOR_CACHE_PATH}")
            except Exception as e:
                print(f"❌ Gagal menyimpan file cache npy: {e}")
                
        CACHE["mesin_bm25"] = BM25Okapi(CACHE["token_dosen"])
        CACHE["is_ready"] = True

    @staticmethod
    def jalankan_pipeline(judul_mhs, abstrak_mhs, k_rank=5, bobot_lex=0.3, bobot_sem=0.7):
        if not CACHE["is_ready"]:
            raise Exception("Memori Cache Vektor belum siap!")
            
        teks_mhs_raw = judul_mhs + " " + abstrak_mhs
        teks_mhs_expand, log_ekspansi = PreprocessingPipeline.ekspansi_query_dengan_log(teks_mhs_raw)
        
        tokens_mentah = re.findall(r'\b[a-z0-9]{2,}\b', teks_mhs_expand.lower())
        tokens_unigram = [t for t in tokens_mentah if t not in STOPWORDS]
        tokens_bigram = ["_".join(g) for g in ngrams(tokens_unigram, 2)]
        
        token_mhs = tokens_unigram + tokens_bigram

        skor_lex = ScoringPipeline.hitung_leksikal(token_mhs)
        skor_sem = ScoringPipeline.hitung_semantik(teks_mhs_expand)

        semua_hasil = []
        data_dosen = CACHE["data_dosen"]
        
        for i in range(len(data_dosen)):
            skor_hybrid = (bobot_lex * skor_lex[i]) + (bobot_sem * skor_sem[i])
            semua_hasil.append({
                "indeks": i,
                "NAMA": data_dosen[i].get('NAMA', '-'),
                "PROGRAM_STUDI": data_dosen[i].get('PROGRAM_STUDI', '-'),
                "BIDANG_KEAHLIAN": data_dosen[i].get('BIDANG_KEAHLIAN', '-'),
                "JURNAL": data_dosen[i].get('JURNAL', '-'),
                "judul bimbing": data_dosen[i].get('judul bimbing', '-'),
                "judul uji": data_dosen[i].get('judul uji', '-'),
                "RIWAYAT_PENDIDIKAN": data_dosen[i].get('RIWAYAT_PENDIDIKAN', '-'),
                "Hybrid Score": round(float(skor_hybrid), 3),
                "Lexical Score": round(float(skor_lex[i]), 3),
                "Semantic Score": round(float(skor_sem[i]), 3)
            })
            
        semua_hasil.sort(key=lambda x: x["Hybrid Score"], reverse=True)
        top_k = semua_hasil[:k_rank]

        mhs_set = set(token_mhs)
        hasil_final = []
        
        for h in top_k:
            idx = h["indeks"]
            teks_dsn = CACHE["teks_raw_list"][idx]
            
            dsn_set = set(CACHE["token_dosen"][idx])
            irisan = list(mhs_set.intersection(dsn_set))
            kata_lex = [str(k).replace('_', ' ') for k in irisan]
            
            kw = kw_model.extract_keywords(
                teks_dsn, keyphrase_ngram_range=(1, 3), stop_words=list(STOPWORDS), 
                use_maxsum=True, nr_candidates=15, top_n=3, seed_keywords=[teks_mhs_raw]
            )
            kata_sem = [str(k[0]) for k in kw]
            
            h["Irisan Kata (Lexical)"] = ", ".join(kata_lex) if kata_lex else "-"
            h["Frasa Terkait (KeyBERT)"] = ", ".join(kata_sem) if kata_sem else "-"
            del h["indeks"]
            hasil_final.append(h)

        return {
            "hasil_rekomendasi": hasil_final,
            "metadata_mesin": {
                "teks_asli": teks_mhs_raw,
                "teks_ekspansi": teks_mhs_expand,
                "kata_diekspansi": log_ekspansi,
                "token_unigram": list(set(tokens_unigram)),
                "token_bigram": list(set(tokens_bigram))
            }
        }