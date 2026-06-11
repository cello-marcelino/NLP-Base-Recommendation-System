import re
import threading
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
kw_model = KeyBERT(model=model_sbert) #type:ignore

# ==========================================
# CACHE THREAD-SAFE
# Menggunakan Lock untuk mencegah race condition
# saat Flask berjalan dengan multiple workers.
# ==========================================
_cache_lock = threading.Lock()

CACHE = {
    "data_dosen":       [],
    "teks_bm25_list":   [],   # Teks berbobot (repetisi) — khusus untuk BM25
    "teks_sbert_list":  [],   # Teks natural — khusus untuk SBERT
    "teks_raw_list":    [],   # Teks asli — untuk explainability
    "token_dosen":      [],
    "vektor_dosen":     None,
    "mesin_bm25":       None,
    "kata_kunci_dosen": [],   # KeyBERT di-precompute saat siapkan_cache, bukan saat query
    "is_ready":         False
}


# ==========================================
# PREPROCESSING PIPELINE
# ==========================================
class PreprocessingPipeline:

    @staticmethod
    def validasi_input(judul: str, abstrak: str) -> tuple:
        """Validasi dan normalisasi input sebelum masuk pipeline."""
        if not isinstance(judul, str) or not judul.strip():
            raise ValueError("Judul tidak boleh kosong atau bukan string.")
        if not isinstance(abstrak, str) or not abstrak.strip():
            raise ValueError("Abstrak tidak boleh kosong atau bukan string.")
        return judul.strip(), abstrak.strip()

    @staticmethod
    def ekspansi_query_dengan_log(teks: str, kamus: dict = KAMUS_EKSPANSI) -> tuple:
        """
        Mengekspansi teks berdasarkan kamus domain.

        Perbaikan dari versi sebelumnya:
        - Check selalu terhadap teks_lower yang tidak berubah,
          sehingga tidak ada cascading expansion (sinonim tidak
          ikut diekspansi lagi).
        - Dedup dilakukan di tahap tokenisasi, bukan di sini,
          agar frasa ekspansi tetap bisa terbentuk sebagai bigram.
        """
        teks_lower = teks.lower()      # Tidak pernah diubah — anti-cascading
        teks_ekspansi = teks_lower
        log_ekspansi = {}

        # Urutkan dari frasa terpanjang agar "machine learning" diproses
        # sebelum "machine", mencegah partial match yang salah
        sorted_keys = sorted(kamus.keys(), key=len, reverse=True)

        for frasa in sorted_keys:
            if frasa in teks_lower:
                sinonim_str = " ".join(kamus[frasa])
                teks_ekspansi += " " + sinonim_str
                log_ekspansi[frasa] = sinonim_str

        return teks_ekspansi, log_ekspansi

    @staticmethod
    def tokenize_ngram(teks: str, n: int = 2) -> list:
        """
        Tokenisasi unigram + bigram dengan dedup.

        Perbaikan dari versi sebelumnya:
        - Dedup via ordered-set mencegah token duplikat mempengaruhi
          skor BM25 secara tidak terduga ketika teks berisi repetisi.
        """
        tokens = re.findall(r'\b[a-z0-9]{2,}\b', teks.lower())
        tokens_bersih = [t for t in tokens if t not in STOPWORDS]
        bigrams = ["_".join(g) for g in ngrams(tokens_bersih, n)]

        seen, hasil = set(), []
        for t in tokens_bersih + bigrams:
            if t not in seen:
                seen.add(t)
                hasil.append(t)
        return hasil

    @staticmethod
    def _safe_get(dosen: dict, key: str) -> str:
        """Ambil nilai dosen, handle None dan nilai 'nan' dari pandas."""
        val = dosen.get(key, '')
        if val is None:
            return ''
        val_str = str(val).strip()
        return '' if val_str.lower() in ('nan', 'none', '') else val_str

    @staticmethod
    def buat_teks_dosen(dosen: dict) -> tuple:
        """
        Menghasilkan TIGA representasi teks dari data dosen:

        1. teks_bm25  : Berbobot dengan repetisi untuk memanipulasi
                        TF pada BM25. Repetisi hanya tepat untuk model
                        statistik seperti BM25.

        2. teks_sbert : Kalimat natural tanpa repetisi untuk SBERT.
                        Model transformer tidak dirancang untuk input
                        yang diulang — repetisi justru merusak
                        representasi vektor semantik.

        3. teks_raw   : Teks asli untuk perhitungan irisan kata
                        (explainability) dan seed KeyBERT.

        Perbaikan dari versi sebelumnya:
        - Versi asli menggunakan teks_bobot_list untuk KEDUA BM25 dan SBERT,
          sehingga embedding SBERT rusak akibat menerima teks repetisi.
        - Sekarang dipisah menjadi dua representasi berbeda.
        """
        sg = PreprocessingPipeline._safe_get

        keahlian   = sg(dosen, 'BIDANG_KEAHLIAN')
        bimbing    = sg(dosen, 'judul bimbing')
        uji        = sg(dosen, 'judul uji')
        jurnal     = sg(dosen, 'JURNAL')
        pendidikan = sg(dosen, 'RIWAYAT_PENDIDIKAN')

        # BM25: repetisi untuk weighting (term frequency manipulation)
        teks_bm25 = (
            f"{keahlian} " * 3 +
            f"{bimbing} "  * 3 +
            f"{uji} "      * 2 +
            f"{jurnal} "       +
            f"{pendidikan}"
        ).strip()

        # SBERT: kalimat natural, dipisahkan titik agar model memahami batas frasa
        bagian = [b for b in [keahlian, bimbing, uji, jurnal, pendidikan] if b]
        teks_sbert = ". ".join(bagian)

        # Raw: untuk explainability (irisan token & KeyBERT)
        teks_raw = " ".join(bagian)

        return teks_bm25, teks_sbert, teks_raw


# ==========================================
# SCORING PIPELINE
# ==========================================
class ScoringPipeline:

    @staticmethod
    def normalisasi_robust(skor: np.ndarray) -> np.ndarray:
        """
        Normalisasi berbasis percentile-95 untuk meredam efek outlier.

        Perbaikan dari versi sebelumnya:
        - Versi asli menggunakan max-based normalization. Jika satu
          dosen memiliki skor jauh lebih tinggi, semua skor lain
          tertekan mendekati nol.
        - Sekarang menggunakan soft-clip pada P95 sebelum normalisasi
          sehingga distribusi skor lebih merata dan informatif.
        """
        if not np.any(skor > 0):
            return np.zeros_like(skor, dtype=float)

        skor_positif = skor[skor > 0]
        batas_atas = np.percentile(skor_positif, 95)
        skor_clipped = np.clip(skor, 0, batas_atas)
        denom = skor_clipped.max()

        return skor_clipped / denom if denom > 1e-9 else np.zeros_like(skor, dtype=float)

    @staticmethod
    def hitung_leksikal(token_mhs: list) -> np.ndarray:
        skor_mentah = np.array(CACHE["mesin_bm25"].get_scores(token_mhs))
        return ScoringPipeline.normalisasi_robust(skor_mentah)

    @staticmethod
    def hitung_semantik(teks_mhs_raw: str) -> np.ndarray:
        """
        Encoding query menggunakan teks RAW (natural), bukan teks ekspansi.

        Perbaikan dari versi sebelumnya:
        - Versi asli meneruskan teks_mhs_expand (keyword-stuffed) ke SBERT.
        - Teks yang penuh sinonim dan token tambahan bukan kalimat natural,
          sehingga merusak representasi semantik query.
        - Ekspansi query hanya relevan untuk BM25 (lexical matching),
          bukan untuk SBERT (semantic matching).
        """
        vektor_mhs = model_sbert.encode([teks_mhs_raw])
        return cosine_similarity(vektor_mhs, CACHE["vektor_dosen"])[0] #type:ignore


# ==========================================
# RECOMMENDATION ENGINE
# ==========================================
class RecommendationEngine:

    @staticmethod
    def siapkan_cache(data_dosen: list) -> None:
        """
        Membangun seluruh cache: token BM25, vektor SBERT, dan KeyBERT phrases.

        Perbaikan dari versi sebelumnya:
        1. Thread-safe: menggunakan _cache_lock sehingga tidak terjadi
           race condition saat Flask multiworker membaca CACHE sementara
           rebuild sedang berjalan.
        2. KeyBERT di-precompute di sini (bukan saat query) sehingga
           tidak ada bottleneck latensi saat inference.
        3. is_ready di-set False dulu sebelum rebuild, baru True setelah
           semua field selesai di-assign (atomic update).
        4. Teks SBERT dan BM25 dipisah sejak tahap ini.
        """
        if not data_dosen:
            raise ValueError("data_dosen tidak boleh kosong.")

        with _cache_lock:
            CACHE["is_ready"] = False  # Guard: tolak request selama rebuild

            teks_bm25_list  = []
            teks_sbert_list = []
            teks_raw_list   = []

            for dsn in data_dosen:
                tb, ts, tr = PreprocessingPipeline.buat_teks_dosen(dsn)
                teks_bm25_list.append(tb)
                teks_sbert_list.append(ts)
                teks_raw_list.append(tr)

            # BM25: tokenisasi dari teks berbobot
            token_dosen = [
                PreprocessingPipeline.tokenize_ngram(t)
                for t in teks_bm25_list
            ]

            # SBERT: encode dari teks natural
            print("Encoding vektor SBERT dosen...")
            vektor_dosen = model_sbert.encode(
                teks_sbert_list,
                show_progress_bar=True,
                batch_size=32
            )

            # KeyBERT: precompute dari teks raw (sekali saat build, bukan per-request)
            print("Precomputing KeyBERT phrases dosen...")
            kata_kunci_dosen = []
            for teks in teks_raw_list:
                if teks.strip():
                    kw = kw_model.extract_keywords(
                        teks,
                        keyphrase_ngram_range=(1, 3),
                        stop_words=list(STOPWORDS),
                        use_maxsum=True,
                        nr_candidates=20,
                        top_n=5
                    )
                    kata_kunci_dosen.append([k[0] for k in kw])
                else:
                    kata_kunci_dosen.append([])

            # Atomic assignment: semua field diset sebelum is_ready=True
            # Jika ada exception sebelum baris ini, is_ready tetap False
            CACHE["data_dosen"]        = data_dosen
            CACHE["teks_bm25_list"]    = teks_bm25_list
            CACHE["teks_sbert_list"]   = teks_sbert_list
            CACHE["teks_raw_list"]     = teks_raw_list
            CACHE["token_dosen"]       = token_dosen
            CACHE["vektor_dosen"]      = vektor_dosen
            CACHE["mesin_bm25"]        = BM25Okapi(token_dosen)
            CACHE["kata_kunci_dosen"]  = kata_kunci_dosen
            CACHE["is_ready"]          = True

        print(f"Cache siap: {len(data_dosen)} dosen terindeks.")

    @staticmethod
    def jalankan_pipeline(
        judul_mhs:  str,
        abstrak_mhs: str,
        k_rank:     int   = 5,
        bobot_lex:  float = 0.3,
        bobot_sem:  float = 0.7
    ) -> dict:

        # --- Guard ---
        if not CACHE["is_ready"]:
            raise RuntimeError(
                "Cache belum siap. Panggil siapkan_cache() terlebih dahulu."
            )

        # --- Validasi Input ---
        judul_mhs, abstrak_mhs = PreprocessingPipeline.validasi_input(
            judul_mhs, abstrak_mhs
        )
        if abs(bobot_lex + bobot_sem - 1.0) > 1e-6:
            raise ValueError(
                f"bobot_lex + bobot_sem harus = 1.0 "
                f"(saat ini: {bobot_lex + bobot_sem:.4f})"
            )

        teks_mhs_raw = f"{judul_mhs} {abstrak_mhs}"

        # --- Ekspansi Query (untuk BM25) ---
        teks_mhs_expand, log_ekspansi = PreprocessingPipeline.ekspansi_query_dengan_log(
            teks_mhs_raw
        )

        # --- Tokenisasi Query (dari teks ekspansi, untuk BM25) ---
        tokens_mentah  = re.findall(r'\b[a-z0-9]{2,}\b', teks_mhs_expand.lower())
        tokens_unigram = [t for t in tokens_mentah if t not in STOPWORDS]
        tokens_bigram  = ["_".join(g) for g in ngrams(tokens_unigram, 2)]

        # Dedup token query (ordered set)
        seen, token_mhs = set(), []
        for t in tokens_unigram + tokens_bigram:
            if t not in seen:
                seen.add(t)
                token_mhs.append(t)

        # --- Komputasi Skor ---
        skor_lex    = ScoringPipeline.hitung_leksikal(token_mhs)
        skor_sem    = ScoringPipeline.hitung_semantik(teks_mhs_raw)   # teks RAW
        skor_hybrid = (bobot_lex * skor_lex) + (bobot_sem * skor_sem)

        # --- Ambil Top-K via argsort (lebih efisien dari sort list of dicts) ---
        top_indices = np.argsort(skor_hybrid)[::-1][:k_rank]

        data_dosen = CACHE["data_dosen"]
        mhs_set    = set(token_mhs)

        # --- Susun Hasil + Explainability ---
        hasil_final = []
        for idx in top_indices:
            dsn     = data_dosen[idx]
            dsn_set = set(CACHE["token_dosen"][idx])

            # Irisan token: bukti leksikal
            irisan   = list(mhs_set.intersection(dsn_set))
            kata_lex = sorted([k.replace('_', ' ') for k in irisan])

            # KeyBERT phrases: dari cache (sudah di-precompute)
            kata_sem = CACHE["kata_kunci_dosen"][idx]

            hasil_final.append({
                "NAMA":                    dsn.get('NAMA', '-'),
                "PROGRAM_STUDI":           dsn.get('PROGRAM_STUDI', '-'),
                "BIDANG_KEAHLIAN":         dsn.get('BIDANG_KEAHLIAN', '-'),
                "JURNAL":                  dsn.get('JURNAL', '-'),
                "judul bimbing":           dsn.get('judul bimbing', '-'),
                "judul uji":               dsn.get('judul uji', '-'),
                "RIWAYAT_PENDIDIKAN":      dsn.get('RIWAYAT_PENDIDIKAN', '-'),
                "Hybrid Score":            round(float(skor_hybrid[idx]), 4),
                "Lexical Score":           round(float(skor_lex[idx]),    4),
                "Semantic Score":          round(float(skor_sem[idx]),    4),
                "Irisan Kata (Lexical)":   ", ".join(kata_lex) if kata_lex else "-",
                "Frasa Terkait (KeyBERT)": ", ".join(kata_sem) if kata_sem else "-",
            })

        return {
            "hasil_rekomendasi": hasil_final,
            "metadata_mesin": {
                "teks_asli":       teks_mhs_raw,
                "teks_ekspansi":   teks_mhs_expand,
                "kata_diekspansi": log_ekspansi,
                "token_unigram":   sorted(set(tokens_unigram)),
                "token_bigram":    sorted(set(tokens_bigram)),
            }
        }