from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Memuat Model AI SBERT (Hanya dilakukan sekali saat server menyala)
# Kita gunakan model 'multilingual' agar AI mengerti Bahasa Indonesia dan Inggris
print("Sedang memuat Model Semantik (SBERT)... (Hanya memakan waktu di awal)")
model_sbert = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def hitung_rekomendasi(data_dosen, judul_mhs, abstrak_mhs, k_rank, bobot_lexical, bobot_semantic):
    # Gabungkan teks input dari mahasiswa menjadi satu kalimat utuh
    teks_mahasiswa = judul_mhs + " " + abstrak_mhs
    
    ## 2. Siapkan data teks dosen (Corpus)
    teks_semua_dosen = []
    for dosen in data_dosen:
        # Menggabungkan semua kolom penting dari format baru
        teks_gabungan = str(dosen['RIWAYAT_PENDIDIKAN']) + " " + \
                        str(dosen['BIDANG_KEAHLIAN']) + " " + \
                        str(dosen['JURNAL']) + " " + \
                        str(dosen['judul uji']) + " " + \
                        str(dosen['judul bimbing'])
        teks_semua_dosen.append(teks_gabungan.lower())
        
    # ==========================================
    # PROSES 1: PERHITUNGAN LEKSIKAL (BM25)
    # ==========================================
    # Pecah teks menjadi kata-per-kata (tokenisasi sederhana)
    token_dosen = [teks.split() for teks in teks_semua_dosen]
    token_mahasiswa = teks_mahasiswa.lower().split()
    
    mesin_bm25 = BM25Okapi(token_dosen)
    skor_bm25_mentah = mesin_bm25.get_scores(token_mahasiswa)
    
    # Normalisasi BM25 (Penting!)
    # Skor BM25 bisa mencapai puluhan. Kita harus ubah ke skala 0 - 1 agar setara dengan SBERT
    nilai_tertinggi_bm25 = max(skor_bm25_mentah) if max(skor_bm25_mentah) > 0 else 1
    skor_leksikal = [skor / nilai_tertinggi_bm25 for skor in skor_bm25_mentah]


    # ==========================================
    # PROSES 2: PERHITUNGAN SEMANTIK (SBERT)
    # ==========================================
    # Ubah teks menjadi angka matematika (Vektor)
    vektor_mahasiswa = model_sbert.encode([teks_mahasiswa])
    vektor_dosen = model_sbert.encode(teks_semua_dosen)
    
    # Hitung kemiripan maknanya (Cosine Similarity)
    skor_semantik = cosine_similarity(vektor_mahasiswa, vektor_dosen)[0] #type: ignore


    # ==========================================
    # PROSES 3: MENGGABUNGKAN SKOR (HYBRID)
    # ==========================================
    hasil_akhir = []
    
    for indeks in range(len(data_dosen)):
        # Bobot: 40% Leksikal (Kecocokan Kata) + 60% Semantik (Kecocokan Makna)
        skor_hybrid = (bobot_lexical * skor_leksikal[indeks]) + (bobot_semantic * skor_semantik[indeks])
        
        # Susun data untuk dikirim ke Klien
        data_rekomendasi = {
            "NAMA": data_dosen[indeks]['NAMA'],
            "PROGRAM_STUDI": data_dosen[indeks]['PROGRAM_STUDI'],
            "BIDANG_KEAHLIAN": data_dosen[indeks]['BIDANG_KEAHLIAN'],
            "Lexical Score": round(float(skor_leksikal[indeks]), 3),
            "Semantic Score": round(float(skor_semantik[indeks]), 3),
            "Hybrid Score": round(float(skor_hybrid), 3),
            "JURNAL": data_dosen[indeks]['JURNAL'],
            "judul uji": data_dosen[indeks]['judul uji'],
            "judul bimbing": data_dosen[indeks]['judul bimbing']
        }
        hasil_akhir.append(data_rekomendasi)
        
    # Urutkan berdasarkan Hybrid Score paling tinggi ke rendah
    hasil_akhir.sort(key=lambda x: x["Hybrid Score"], reverse=True)
    
    # Kembalikan hanya sejumlah k_rank (misal 5 terbaik)
    return hasil_akhir[:k_rank]