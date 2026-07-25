import json
import threading
from flask import Blueprint, request, jsonify, Response, stream_with_context

from app.services.hybrid_engine import engine
from app.services.data_loader import DataLoader
from app.services.progress_stream import generate_progress_event
from app.utils.text_preprocessor import PreprocessingPipeline
from app.utils.response_formatter import ResponseFormatter

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route('/api/rekomendasi', methods=['POST'])
def cari_rekomendasi_standard():
    if not engine.is_ready:
        return jsonify(ResponseFormatter.format_error("Mesin AI sedang warming up", 503)[0]), 503

    data_klien = request.json or {}
    judul = data_klien.get('judul', '')
    abstrak = data_klien.get('abstrak', '')
    k = data_klien.get('k', 10)
    bobot_lexical = data_klien.get('bobot_lexical', 0.4)
    bobot_semantic = data_klien.get('bobot_semantic', 0.6)

    if not judul and not abstrak:
        return jsonify(ResponseFormatter.format_error("Judul dan Abstrak tidak boleh kosong!")[0]), 400

    try:
        # Step 1: Preprocessing Text
        teks_mhs_raw = f"{judul} {abstrak}"
        teks_mhs_expand, log_ekspansi = PreprocessingPipeline.ekspansi_query_dengan_log(teks_mhs_raw)
        token_mhs = PreprocessingPipeline.tokenize_ngram(teks_mhs_expand)

        # Step 2: Lexical Scoring
        skor_lex = engine.bm25.hitung_leksikal_normalized(token_mhs)

        # Step 3: Semantic Scoring
        vektor_mhs = engine.sbert.encode_query(teks_mhs_expand)
        skor_sem = engine.sbert.hitung_semantik(vektor_mhs, engine.sbert.vektor_dosen)

        # Skenario A: Hard Constraint (Pruning Leksikal)
        # Jika skor BM25 nol, maka dosen tersebut di-drop (skor SBERT di-nol-kan)
        skor_sem[skor_lex == 0] = 0.0

        # Step 4: Hybrid Aggregation
        bobot_lexical = float(bobot_lexical)
        bobot_semantic = float(bobot_semantic)
        is_adaptif = bobot_lexical < 0
        kata_langka = []
        if is_adaptif:
            bobot_lexical, bobot_semantic, kata_langka = engine.bm25.hitung_bobot_adaptif(token_mhs)

        top_k = engine._rank(skor_lex, skor_sem, bobot_lexical, bobot_semantic, int(k))

        # Step 5: Final K-Ranking (Enrichment)
        hasil_rekomendasi = engine._enrich(top_k, token_mhs)

        def async_logging():
            input_info = {
                "judul": judul, "abstrak": abstrak,
                "bobot_lexical": bobot_lexical, "bobot_semantic": bobot_semantic,
                "is_adaptif": False
            }
            DataLoader.simpan_log_json(input_info, hasil_rekomendasi)

        threading.Thread(target=async_logging, daemon=True).start()

        return jsonify({
            "status": "sukses",
            "data": {
                "hasil_rekomendasi": hasil_rekomendasi,
                "metadata_mesin": {
                    "teks_asli": teks_mhs_raw,
                    "teks_ekspansi": teks_mhs_expand,
                    "kata_diekspansi": log_ekspansi,
                    "is_adaptif": is_adaptif,
                    "bobot_lex_final": bobot_lexical,
                    "bobot_sem_final": bobot_semantic,
                    "kata_langka": kata_langka
                }
            }
        })

    except Exception as e:
        return jsonify(ResponseFormatter.format_error(str(e), 500)[0]), 500

@recommend_bp.route('/api/rekomendasi/stream', methods=['GET'])
def cari_rekomendasi_stream():
    """SSE endpoint for streaming progress"""
    judul = request.args.get('judul', '')
    abstrak = request.args.get('abstrak', '')
    k = request.args.get('k', 10, type=int)
    bobot_lexical = request.args.get('bobot_lexical', 0.4, type=float)
    bobot_semantic = request.args.get('bobot_semantic', 0.6, type=float)

    def generate():
        if not engine.is_ready:
            yield generate_progress_event(0, "Error: AI engine not ready", True)
            return

        if not judul and not abstrak:
            yield generate_progress_event(0, "Error: Judul/Abstrak empty", True)
            return

        try:
            yield generate_progress_event(1, "Preprocessing Text")
            teks_mhs_raw = f"{judul} {abstrak}"
            teks_mhs_expand, log_ekspansi = PreprocessingPipeline.ekspansi_query_dengan_log(teks_mhs_raw)
            token_mhs = PreprocessingPipeline.tokenize_ngram(teks_mhs_expand)

            yield generate_progress_event(2, "Lexical Scoring (BM25)")
            skor_lex = engine.bm25.hitung_leksikal_normalized(token_mhs)

            yield generate_progress_event(3, "Semantic Scoring (SBERT)")
            vektor_mhs = engine.sbert.encode_query(teks_mhs_expand)
            skor_sem = engine.sbert.hitung_semantik(vektor_mhs, engine.sbert.vektor_dosen)

            # Skenario A: Hard Constraint (Pruning Leksikal)
            skor_sem[skor_lex == 0] = 0.0

            yield generate_progress_event(4, "Hybrid Aggregation & XAI Generation")
            is_adaptif = bobot_lexical < 0
            kata_langka = []
            
            final_bobot_lexical = bobot_lexical
            final_bobot_semantic = bobot_semantic
            if is_adaptif:
                final_bobot_lexical, final_bobot_semantic, kata_langka = engine.bm25.hitung_bobot_adaptif(token_mhs)
                
            top_k = engine._rank(skor_lex, skor_sem, final_bobot_lexical, final_bobot_semantic, k)

            yield generate_progress_event(5, "Final K-Ranking")
            hasil_rekomendasi = engine._enrich(top_k, token_mhs)

            def async_logging():
                DataLoader.simpan_log_json({
                    "judul": judul, "abstrak": abstrak,
                    "bobot_lexical": bobot_lexical, "bobot_semantic": bobot_semantic,
                    "is_adaptif": False
                }, hasil_rekomendasi)

            threading.Thread(target=async_logging, daemon=True).start()

            payload = {
                "hasil_rekomendasi": hasil_rekomendasi,
                "metadata_mesin": {
                    "teks_asli": teks_mhs_raw,
                    "teks_ekspansi": teks_mhs_expand,
                    "kata_diekspansi": log_ekspansi,
                    "is_adaptif": is_adaptif,
                    "bobot_lex_final": final_bobot_lexical,
                    "bobot_sem_final": final_bobot_semantic,
                    "kata_langka": kata_langka
                }
            }
            yield generate_progress_event(6, "Complete", True, payload)

        except Exception as e:
            yield generate_progress_event(-1, f"Error: {str(e)}", True)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')
