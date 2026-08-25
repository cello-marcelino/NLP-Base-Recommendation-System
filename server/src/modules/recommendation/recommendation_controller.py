import json
import time
from typing import Dict, Any
from flask import request, Response, stream_with_context
import pandas as pd

from server.src.core.config import Config
from server.src.core.response import ResponseFormatter
from server.src.core.exceptions import ValidationError, ServiceUnavailableError
from server.src.modules.system.cache_service import CacheService
from server.src.modules.recommendation.recommendation_service import RecommendationService
from server.src.modules.recommendation.batch_service import BatchService

class RecommendationController:
    """Controller handling recommendation endpoints."""
    
    @staticmethod
    def single_recommendation():
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            raise ValidationError("Request body harus berupa JSON object")
            
        judul = str(data.get('judul', '') or '').strip()
        abstrak = str(data.get('abstrak', '') or '').strip()
        k_rank = data.get('k_rank')
        
        if not judul and not abstrak:
            raise ValidationError("Judul atau abstrak penelitian harus diisi")
            
        cache = CacheService.get_instance()
        if not cache.is_ready:
            raise ServiceUnavailableError("Model NLP sedang inisialisasi / warm-up")
            
        result = RecommendationService.get_recommendations(judul, abstrak, k_rank)
        return ResponseFormatter.success(data=result, message="Rekomendasi berhasil dibuat")

    @staticmethod
    def batch_recommendation():
        data = request.get_json(silent=True)
        if not data:
            raise ValidationError("Request body kosong atau bukan JSON yang valid")
            
        k_rank = None
        proposals = []
        
        if isinstance(data, dict):
            k_rank = data.get('k_rank')
            proposals = data.get('proposals', [])
        elif isinstance(data, list):
            proposals = data
        else:
            raise ValidationError("Format data tidak didukung. Gunakan JSON array atau object dengan key 'proposals'")
            
        if not proposals:
            raise ValidationError("Daftar proposal tidak boleh kosong")
            
        results = BatchService.process_batch(proposals, global_k_rank=k_rank)
        return ResponseFormatter.success(
            data=results,
            meta={"total_processed": len(results)},
            message="Batch rekomendasi berhasil diproses"
        )

    @staticmethod
    def batch_upload():
        if 'file' not in request.files:
            raise ValidationError("Tidak ada file yang diunggah (key 'file' required)")
            
        file = request.files['file']
        if file.filename == '':
            raise ValidationError("File belum dipilih")
            
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            raise ValidationError("Format file tidak didukung. Harap unggah file Excel (.xlsx atau .xls)")
            
        try:
            df = pd.read_excel(file)
            cols = {str(c).lower().strip(): c for c in df.columns}
            
            proposals = []
            id_col = cols.get('id')
            judul_col = cols.get('judul')
            abstrak_col = cols.get('abstrak')
            
            for index, row in df.iterrows():
                proposals.append({
                    "id": str(row[id_col]) if id_col and pd.notna(row[id_col]) else str(index + 1),
                    "judul": str(row[judul_col]) if judul_col and pd.notna(row[judul_col]) else "",
                    "abstrak": str(row[abstrak_col]) if abstrak_col and pd.notna(row[abstrak_col]) else ""
                })
                
            k_rank_str = request.form.get('k_rank')
            global_k_rank = int(k_rank_str) if k_rank_str and k_rank_str.isdigit() else None
            
            results = BatchService.process_batch(proposals, global_k_rank=global_k_rank)
            return ResponseFormatter.success(
                data=results,
                meta={"total_processed": len(results), "filename": file.filename},
                message="File batch berhasil diproses"
            )
        except Exception as e:
            if "BATCH_LIMIT_EXCEEDED" in str(e):
                raise
            raise ValidationError(f"Gagal memproses file Excel: {str(e)}")

    @staticmethod
    def stream_recommendation():
        data = request.get_json(silent=True) or {}
        judul = str(data.get('judul', '') or '').strip()
        abstrak = str(data.get('abstrak', '') or '').strip()
        k_rank = data.get('k_rank')
        
        if not judul and not abstrak:
            raise ValidationError("Judul atau abstrak harus diisi untuk streaming")
            
        def generate():
            try:
                yield f"data: {json.dumps({'step': 1, 'message': 'Memulai Text Preprocessing & Cleaning'})}\n\n"
                time.sleep(0.1)
                
                yield f"data: {json.dumps({'step': 2, 'message': 'Melakukan Ekspansi Sinonim Ontologi'})}\n\n"
                time.sleep(0.1)
                
                yield f"data: {json.dumps({'step': 3, 'message': 'Kalkulasi Skor Leksikal BM25'})}\n\n"
                time.sleep(0.1)
                
                yield f"data: {json.dumps({'step': 4, 'message': 'Kalkulasi Skor Semantik Sentence-BERT'})}\n\n"
                time.sleep(0.1)
                
                # Compute actual results
                result = RecommendationService.get_recommendations(judul, abstrak, k_rank)
                
                yield f"data: {json.dumps({'step': 5, 'message': 'Hybrid Ranking & XAI Selesai', 'result': result})}\n\n"
            except Exception as err:
                yield f"data: {json.dumps({'step': 5, 'error': str(err)})}\n\n"

        return Response(stream_with_context(generate()), mimetype="text/event-stream")
