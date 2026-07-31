import re
from typing import List, Tuple, Dict
from app.utils.kamus_ekspansi import KAMUS_EKSPANSI
from app.utils.stopwords import STOPWORDS

class Preprocessor:
    @staticmethod
    def _parse_dan_dedup_judul(judul_raw: str, max_limit: int) -> str:
        if not judul_raw or not isinstance(judul_raw, str):
            return ""
        
        # Split by comma or semicolon
        juduls = re.split(r'[,;]', judul_raw)
        
        # Dedup based on lowercase
        seen = set()
        unik = []
        for j in juduls:
            j_clean = j.strip()
            if not j_clean:
                continue
            j_lower = j_clean.lower()
            if j_lower not in seen:
                seen.add(j_lower)
                unik.append(j_clean)
                if len(unik) >= max_limit:
                    break
                    
        return " ".join(unik)

    @staticmethod
    def clean_text(text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        # Lowercase
        text = text.lower()
        # Keep only alphanumeric with length >= 2
        words = re.findall(r'\b[a-z0-9]{2,}\b', text)
        return " ".join(words)

    @staticmethod
    def remove_stopwords(words: List[str]) -> List[str]:
        return [w for w in words if w not in STOPWORDS]

    @staticmethod
    def create_ngrams(words: List[str]) -> List[str]:
        # Unigrams + Bigrams
        bigrams = [f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)]
        return words + bigrams

    @staticmethod
    def ekspansi_query_dengan_log(teks: str, kamus: dict) -> Tuple[str, Dict[str, str]]:
        teks_lower = teks.lower()
        teks_ekspansi = teks_lower
        log_ekspansi = {}
        
        # Sort by length descending for longest-first matching
        for frasa in sorted(kamus.keys(), key=len, reverse=True):
            if frasa in teks_lower:
                sinonim_str = " ".join(kamus[frasa])
                teks_ekspansi += " " + sinonim_str
                log_ekspansi[frasa] = sinonim_str
                
        return teks_ekspansi, log_ekspansi

    @staticmethod
    def preprocess_for_bm25(text: str) -> List[str]:
        clean = Preprocessor.clean_text(text)
        words = clean.split()
        no_stop = Preprocessor.remove_stopwords(words)
        return Preprocessor.create_ngrams(no_stop)

    @staticmethod
    def preprocess_for_sbert(text: str) -> str:
        # For query, expansion is done outside. For corpus, this just cleans.
        return Preprocessor.clean_text(text)

    @staticmethod
    def build_corpus_text(dosen) -> Tuple[str, str]:
        # Parse & Dedup Judul
        judul_bimbing = Preprocessor._parse_dan_dedup_judul(dosen.judul_bimbing, 12)
        judul_uji = Preprocessor._parse_dan_dedup_judul(dosen.judul_uji, 8)
        
        # Handle Nones
        bidang = dosen.bidang_keahlian or ""
        jurnal = dosen.jurnal or ""
        pendidikan = dosen.pendidikan or ""
        
        # Teks untuk BM25 Indexing (memiliki bobot repetisi)
        inti = (bidang + " ") * 5 + \
               (jurnal + " ") * 2 + \
               (judul_bimbing + " ") + \
               (judul_uji + " ")
        teks_terbobot = inti + pendidikan
        
        # Teks untuk SBERT Encoding & KeyBERT (tanpa repetisi)
        teks_normal = f"{pendidikan} {bidang} {jurnal} {judul_uji} {judul_bimbing}"
        
        return teks_terbobot, teks_normal
