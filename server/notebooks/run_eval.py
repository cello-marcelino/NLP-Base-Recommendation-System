import pandas as pd
import numpy as np
import re
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import ngrams
import warnings
warnings.filterwarnings('ignore')

df = pd.read_excel('storage/data/dataset_profiles_terintegrasi.xlsx')

SAMPLE_CASES = [
    {
        "label": "Deep Learning",
        "judul": "Implementasi Convolutional Neural Network untuk Klasifikasi Penyakit Tanaman",
        "abstrak": "Penelitian ini membangun model CNN berbasis deep learning untuk mendeteksi penyakit pada daun tanaman padi menggunakan dataset citra digital.",
        "expected_keywords": ["deep learning", "ai", "artificial intelligence", "machine learning", "cnn", "image processing", "komputer", "informatika", "kecerdasan buatan"]
    },
    {
        "label": "Sistem Informasi",
        "judul": "Perancangan Sistem Informasi Manajemen Inventaris Berbasis Web",
        "abstrak": "Sistem informasi berbasis web untuk pengelolaan data barang masuk dan keluar menggunakan framework Laravel dan database MySQL.",
        "expected_keywords": ["sistem informasi", "web", "software engineering", "rekayasa perangkat lunak", "database", "manajemen", "informasi"]
    },
    {
        "label": "Jaringan Komputer",
        "judul": "Analisis Performa Protokol Routing OSPF pada Jaringan SDN",
        "abstrak": "Penelitian ini menganalisis performa algoritma routing OSPF yang diimplementasikan pada Software Defined Network menggunakan simulasi GNS3.",
        "expected_keywords": ["jaringan", "network", "routing", "komunikasi", "sdn", "iot", "komputer", "internet"]
    }
]

STOPWORDS = {
    "adalah", "dan", "yang", "untuk", "dengan", "dalam", "pada", "dari", "ini", "itu", "atau", "ke", "di",
    "oleh", "akan", "juga", "sudah", "telah", "masih", "bisa", "dapat", "harus", "belum", "saya", "kami",
    "mereka", "ada", "tidak", "bukan", "jika", "maka", "karena", "sebagai", "secara", "melalui", "antara",
    "setiap", "semua", "tersebut", "bahwa", "namun", "tetapi", "serta", "maupun", "hingga", "agar", "supaya",
    "tanpa", "tentang", "mengenai", "terhadap", "berbasis", "sistem", "menggunakan"
}

KAMUS_EKSPANSI = {
    "artificial intelligence": ["ai", "kecerdasan buatan", "machine intelligence"],
    "machine learning": ["ml", "deep learning", "supervised learning", "unsupervised learning"],
    "deep learning": ["dl", "neural network", "cnn", "rnn", "lstm"],
    "natural language processing": ["nlp", "pemrosesan bahasa alami", "text mining"],
    "information system": ["sistem informasi", "si", "manajemen informasi", "it"]
}

def preprocess_raw(teks):
    return re.findall(r"\b[a-z0-9]{2,}\b", teks.lower())

def preprocess_stopword(teks):
    tokens = preprocess_raw(teks)
    return [t for t in tokens if t not in STOPWORDS]

def preprocess_ngram(teks, n=2):
    tokens_bersih = preprocess_stopword(teks)
    bigrams = ["_".join(g) for g in ngrams(tokens_bersih, n)]
    return tokens_bersih + bigrams

def preprocess_full(teks):
    teks_lower = teks.lower()
    teks_ekspansi = teks_lower
    for frasa in sorted(KAMUS_EKSPANSI.keys(), key=len, reverse=True):
        if frasa in teks_lower:
            teks_ekspansi += " " + " ".join(KAMUS_EKSPANSI[frasa])
    return preprocess_ngram(teks_ekspansi, n=2)

def _parse_dan_dedup_judul(raw, max_items=12):
    if pd.isna(raw) or not raw or str(raw) == "-":
        return ""
    items = re.split(r'",\s*"', str(raw).strip().strip('"'))
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

def corpus_weighted(dosen):
    keahlian = str(dosen.get("BIDANG_KEAHLIAN", ""))
    jurnal = str(dosen.get("JURNAL", ""))
    pendidikan = str(dosen.get("RIWAYAT_PENDIDIKAN", ""))
    bimbing = _parse_dan_dedup_judul(dosen.get("judul bimbing") or dosen.get("JUDUL_BIMBING", ""), 12)
    uji = _parse_dan_dedup_judul(dosen.get("judul uji") or dosen.get("JUDUL_UJI", ""), 8)
    return f"{keahlian} " * 5 + f"{bimbing} " + f"{uji} " + f"{jurnal} " * 2 + f"{pendidikan}"

def norm_zscore_sigmoid(scores):
    if np.max(scores) <= 1e-9:
        return np.zeros_like(scores)
    mean, std = np.mean(scores), np.std(scores)
    if std < 1e-9:
        return np.zeros_like(scores)
    z = (scores - mean) / std
    skor_norm = 1.0 / (1.0 + np.exp(-z / 2.0))
    skor_norm[scores <= 1e-9] = 0.0
    return skor_norm

# Ekstraksi Corpus
docs_weighted = [preprocess_full(corpus_weighted(row)) for _, row in df.iterrows()]
corpus_texts_raw = [corpus_weighted(row) for _, row in df.iterrows()]

bm25_weighted = BM25Okapi(docs_weighted)
sbert_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
corpus_embs = sbert_model.encode(corpus_texts_raw, convert_to_numpy=True)

alpha = 0.4
beta = 0.6

results = []
for case in SAMPLE_CASES:
    query_str = case['judul'] + " " + case['abstrak']
    query_tokens = preprocess_full(query_str)
    query_emb = sbert_model.encode([query_str], convert_to_numpy=True)
    
    s_bm25 = norm_zscore_sigmoid(bm25_weighted.get_scores(query_tokens))
    s_sbert = cosine_similarity(query_emb, corpus_embs)[0]
    hybrid_score = (alpha * s_bm25) + (beta * s_sbert)
    
    top_idx = np.argsort(hybrid_score)[::-1][:5]
    top_dosens = []
    valid_count = 0
    for i in top_idx:
        dosen = df.iloc[i]
        keahlian = str(dosen.get("BIDANG_KEAHLIAN", "")).lower()
        
        is_valid = any(kw in keahlian for kw in case['expected_keywords'])
        if is_valid:
            valid_count += 1
            
        top_dosens.append({
            "NAMA": dosen['NAMA'],
            "BIDANG_KEAHLIAN": keahlian,
            "is_valid": is_valid
        })
        
    precision_at_5 = valid_count / 5.0
    results.append({
        "Kasus": case['label'],
        "Precision@5": precision_at_5,
        "Top Dosens": top_dosens
    })

for res in results:
    print(f"Kasus: {res['Kasus']}")
    print(f"Precision@5: {res['Precision@5']}")
    for d in res['Top Dosens']:
        print(f"  - {d['NAMA']} (Keahlian: {d['BIDANG_KEAHLIAN']}) -> Valid: {d['is_valid']}")
    print()
