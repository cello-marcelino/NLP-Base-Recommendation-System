import re
import pandas as pd
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

# ==========================================
# PENYIMPANAN CACHE VEKTOR (MEMORY)
# ==========================================
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
    def ekspansi_query(teks, kamus=KAMUS_EKSPANSI):
        teks_lower = teks.lower()
        teks_ekspansi = teks_lower
        sorted_keys = sorted(kamus.keys(), key=len, reverse=True)
        for frasa in sorted_keys:
            if frasa in teks_lower:
                teks_ekspansi += " " + " ".join(kamus[frasa])
        return teks_ekspansi

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
        vektor_mhs = model_sbert.encode([teks_mhs])
        return cosine_similarity(vektor_mhs, CACHE["vektor_dosen"])[0] # type:ignore

class RecommendationEngine:
    @staticmethod
    def siapkan_cache(data_dosen):
        """Memproses Vektor dan Tokenisasi 1x saat Server Menyala"""
        CACHE["data_dosen"] = data_dosen
        CACHE["teks_bobot_list"] = []
        CACHE["teks_raw_list"] = []
        
        for dsn in data_dosen:
            tb, tr = PreprocessingPipeline.buat_teks_terbobot(dsn)
            CACHE["teks_bobot_list"].append(tb)
            CACHE["teks_raw_list"].append(tr)
            
        CACHE["token_dosen"] = [PreprocessingPipeline.tokenize_ngram(t) for t in CACHE["teks_bobot_list"]]
        CACHE["vektor_dosen"] = model_sbert.encode(CACHE["teks_bobot_list"])
        CACHE["mesin_bm25"] = BM25Okapi(CACHE["token_dosen"])
        CACHE["is_ready"] = True

    @staticmethod
    def jalankan_pipeline(judul_mhs, abstrak_mhs, k_rank=5, bobot_lex=0.3, bobot_sem=0.7):
        if not CACHE["is_ready"]:
            raise Exception("Memori Cache Vektor belum siap!")
            
        teks_mhs_raw = judul_mhs + " " + abstrak_mhs
        teks_mhs_expand = PreprocessingPipeline.ekspansi_query(teks_mhs_raw)
        
        token_mhs = PreprocessingPipeline.tokenize_ngram(teks_mhs_expand)

        # Proses komputasi instan karena data dosen diambil dari RAM (Cache)
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
            kata_lex = [k.replace('_', ' ') for k in irisan]
            
            kw = kw_model.extract_keywords(
                teks_dsn, keyphrase_ngram_range=(1, 3), stop_words=list(STOPWORDS), 
                use_maxsum=True, nr_candidates=15, top_n=3, seed_keywords=[teks_mhs_raw]
            )
            kata_sem = [k[0] for k in kw]
            
            h["Irisan Kata (Lexical)"] = ", ".join(kata_lex) if kata_lex else "-"
            h["Frasa Terkait (KeyBERT)"] = ", ".join(kata_sem) if kata_sem else "-" # type:ignore
            del h["indeks"]
            hasil_final.append(h)

        return hasil_final