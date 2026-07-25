import re
from typing import Tuple, List, Dict, Any
from nltk import ngrams

from app.utils.stopwords import STOPWORDS
from app.utils.kamus_ekspansi import KAMUS_EKSPANSI

class PreprocessingPipeline:
    @staticmethod
    def ekspansi_query_dengan_log(teks: str, kamus: Dict = KAMUS_EKSPANSI) -> Tuple[str, Dict[str, str]]:
        teks_lower = teks.lower()
        teks_ekspansi = teks_lower
        log_ekspansi = {}
        for frasa in sorted(kamus.keys(), key=len, reverse=True):
            if frasa in teks_lower:
                hasil = " ".join(kamus[frasa])
                teks_ekspansi += " " + hasil
                log_ekspansi[frasa] = hasil
        return teks_ekspansi, log_ekspansi

    @staticmethod
    def tokenize_split(teks: str, n: int = 2) -> Tuple[List[str], List[str]]:
        tokens = re.findall(r"\b[a-z0-9]{2,}\b", teks.lower())
        tokens_bersih = [t for t in tokens if t not in STOPWORDS]
        bigrams = ["_".join(g) for g in ngrams(tokens_bersih, n)]
        return tokens_bersih, bigrams

    @staticmethod
    def tokenize_ngram(teks: str, n: int = 2) -> List[str]:
        uni, bi = PreprocessingPipeline.tokenize_split(teks, n)
        return uni + bi

    @staticmethod
    def _parse_dan_dedup_judul(raw: str, max_items: int = 12) -> str:
        if not raw or raw == "-":
            return ""
        items = re.split(r'",\s*"', raw.strip().strip('"'))
        seen = set()
        unik = []
        for it in items:
            key = it.strip().lower()
            if key and key not in seen:
                seen.add(key)
                unik.append(it.strip())
            if len(unik) >= max_items:
                break
        return " ".join(unik)

    @staticmethod
    def buat_teks_terbobot(dosen: Dict[str, Any]) -> Tuple[str, str]:
        keahlian = str(dosen.get("BIDANG_KEAHLIAN", ""))
        jurnal = str(dosen.get("JURNAL", ""))
        pendidikan = str(dosen.get("RIWAYAT_PENDIDIKAN", ""))
        bimbing = PreprocessingPipeline._parse_dan_dedup_judul(str(dosen.get("judul bimbing", "")), max_items=12)
        uji = PreprocessingPipeline._parse_dan_dedup_judul(str(dosen.get("judul uji", "")), max_items=8)

        inti = f"{keahlian} " * 5 + f"{bimbing} " + f"{uji} " + f"{jurnal} " * 2
        teks_terbobot = f"{inti} {pendidikan}"
        teks_normal = f"{pendidikan} {keahlian} {jurnal} {uji} {bimbing}"
        return teks_terbobot, teks_normal
