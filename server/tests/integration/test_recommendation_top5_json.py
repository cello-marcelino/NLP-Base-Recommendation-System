import json
import pytest

# Dataset hardcoded data proposal tugas akhir / tesis mahasiswa dari berbagai rumpun keahlian
HARDCODED_THESIS_DATASET = [
    {
        "id": "TESIS-001",
        "kategori": "Natural Language Processing",
        "judul": "Implementasi Model Sentence-BERT dan BM25 untuk Rekomendasi Dosen Pembimbing Skripsi Berbasis Hybrid NLP",
        "abstrak": "Penelitian ini mengembangkan sistem temu balik informasi akademik menggunakan ekstraksi semantik transformer dan pembobotan leksikal term frequency untuk mencocokkan topik proposal mahasiswa dengan publikasi jurnal dan rekam jejak dosen."
    },
    {
        "id": "TESIS-002",
        "kategori": "Computer Vision",
        "judul": "Deteksi dan Klasifikasi Kendaraan Menggunakan Algoritma YOLOv8 pada Citra Udara Drone",
        "abstrak": "Pengolahan citra digital berbasis deep learning convolutional neural network untuk segmentasi objek transportasi secara real-time pada rekaman video resolusi tinggi."
    },
    {
        "id": "TESIS-003",
        "kategori": "Decision Support System",
        "judul": "Sistem Pendukung Keputusan Penentuan Kelayakan Penerima Bantuan Pangan Menggunakan Metode AHP dan TOPSIS",
        "abstrak": "Penerapan multi-criteria decision making untuk pembobotan kriteria ekonomi keluarga serta perangkingan alternatif penerima subsidi secara objektif."
    },
    {
        "id": "TESIS-004",
        "kategori": "Cyber Security",
        "judul": "Analisis Keamanan Jaringan Menggunakan Kombinasi Algoritma Enkripsi AES-256 dan Steganografi LSB",
        "abstrak": "Pengamanan transmisi dokumen rahasia melalui saluran komunikasi publik dengan menyisipkan ciphertext terenkripsi ke dalam media citra digital."
    },
    {
        "id": "TESIS-005",
        "kategori": "Internet of Things",
        "judul": "Rancang Bangun Sistem Monitoring Kualitas Udara Berbasis Internet of Things dan Mikrokontroler ESP32",
        "abstrak": "Integrasi sensor gas MQ-135 dan sensor partikulat PM2.5 dengan platform cloud untuk pemantauan polusi lingkungan secara nirkabel dan otomatis."
    }
]

def test_collect_top5_recommendations_for_all_theses_json(client):
    """
    Menguji dan mengumpulkan hasil rekomendasi Top-5 dosen lengkap
    untuk setiap topik tesis (hardcoded manual input) dalam format JSON terstruktur.
    """
    collected_results = []
    
    for thesis in HARDCODED_THESIS_DATASET:
        payload = {
            "judul": thesis["judul"],
            "abstrak": thesis["abstrak"],
            "k_rank": 5
        }
        
        # 1. Eksekusi request API rekomendasi
        response = client.post('/api/recommendations', json=payload)
        assert response.status_code == 200
        
        body = response.get_json()
        assert body["success"] is True
        data = body["data"]
        
        # 2. Verifikasi metadata hasil
        metadata = data["metadata"]
        assert metadata["k_rank"] == 5
        assert "alpha" in metadata
        assert "beta" in metadata
        assert "mode" in metadata
        
        # 3. Verifikasi tepat 5 dosen teratas terkumpul
        recommendations = data["recommendations"]
        assert len(recommendations) == 5, f"Ekspektasi 5 rekomendasi dosen, didapatkan {len(recommendations)}"
        
        # 4. Verifikasi kelengkapan data tiap dosen pada peringkat 1-5
        for idx, rec in enumerate(recommendations, start=1):
            assert rec["rank"] == idx
            
            # Verifikasi profil dosen
            dosen = rec["dosen"]
            assert dosen["nidn"], "NIDN tidak boleh kosong"
            assert dosen["nama"], "Nama dosen tidak boleh kosong"
            assert dosen["program_studi"], "Program studi tidak boleh kosong"
            assert dosen["bidang_keahlian"], "Bidang keahlian tidak boleh kosong"
            assert dosen["pendidikan"], "Pendidikan dosen tidak boleh kosong"
            
            # Verifikasi skor komputasi
            scores = rec["scores"]
            assert 0.0 <= scores["hybrid"] <= 1.0, "Skor hybrid harus berada pada rentang [0, 1]"
            assert 0.0 <= scores["bm25"] <= 1.0, "Skor BM25 harus berada pada rentang [0, 1]"
            assert 0.0 <= scores["sbert"] <= 1.0, "Skor SBERT harus berada pada rentang [0, 1]"
            
            # Verifikasi Explainable AI (XAI)
            xai = rec["xai"]
            assert isinstance(xai["irisan_kata"], list)
            assert isinstance(xai["topik_dosen"], list)
            
        # 5. Kumpulkan ke dalam struktur JSON terpadu
        collected_results.append({
            "thesis_id": thesis["id"],
            "thesis_kategori": thesis["kategori"],
            "thesis_judul": thesis["judul"],
            "thesis_abstrak": thesis["abstrak"],
            "recommendation_metadata": metadata,
            "pipeline_logs": data["pipeline"],
            "top_5_dosen": recommendations
        })
        
    # 6. Serialisasi ke format JSON string utuh & validasi parsing round-trip
    json_output = json.dumps(collected_results, indent=2, ensure_ascii=False)
    assert len(json_output) > 0
    
    parsed_back = json.loads(json_output)
    assert len(parsed_back) == len(HARDCODED_THESIS_DATASET)
    assert parsed_back[0]["thesis_id"] == "TESIS-001"
    assert len(parsed_back[0]["top_5_dosen"]) == 5

def test_batch_collect_top5_recommendations_json(client):
    """
    Menguji pengumpulan rekomendasi Top-5 sekaligus via batch endpoint
    menggunakan dataset tesis hardcoded.
    """
    batch_payload = {
        "k_rank": 5,
        "proposals": [
            {
                "id": t["id"],
                "judul": t["judul"],
                "abstrak": t["abstrak"]
            }
            for t in HARDCODED_THESIS_DATASET
        ]
    }
    
    response = client.post('/api/recommendations/batch', json=batch_payload)
    assert response.status_code == 200
    
    body = response.get_json()
    assert body["success"] is True
    assert body["meta"]["total_processed"] == len(HARDCODED_THESIS_DATASET)
    
    batch_data = body["data"]
    assert len(batch_data) == len(HARDCODED_THESIS_DATASET)
    
    for item in batch_data:
        assert item["id"].startswith("TESIS-")
        rekomendasi = item["rekomendasi"]
        assert len(rekomendasi["recommendations"]) == 5
        for rank_idx, rec in enumerate(rekomendasi["recommendations"], start=1):
            assert rec["rank"] == rank_idx
            assert rec["dosen"]["nama"]
            assert rec["dosen"]["nidn"]
            assert "scores" in rec
            assert "xai" in rec
