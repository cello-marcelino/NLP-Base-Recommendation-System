from flask import request
from app.services.batch_service import BatchService
from app.utils.response_formatter import ResponseFormatter
import pandas as pd

class BatchController:
    @staticmethod
    def batch_recommendation():
        data = request.json
        k_rank = data.get('k_rank') if isinstance(data, dict) else None
        
        # If data is a dict that wraps proposals, handle it. If it's a list, k_rank is None
        proposals = data.get('proposals', data) if isinstance(data, dict) else data

        if not proposals or not isinstance(proposals, list):
            return ResponseFormatter.error("Request body must be a JSON array of proposals or an object with 'proposals' array")
            
        try:
            results = BatchService.process_batch(proposals, global_k_rank=k_rank)
            return ResponseFormatter.success(data=results)
        except Exception as e:
            return ResponseFormatter.error(str(e), status_code=500)

    @staticmethod
    def batch_upload():
        if 'file' not in request.files:
            return ResponseFormatter.error("No file part")
            
        file = request.files['file']
        if file.filename == '':
            return ResponseFormatter.error("No selected file")
            
        if not file.filename.endswith(('.xlsx', '.xls')):
            return ResponseFormatter.error("File must be Excel format")
            
        try:
            df = pd.read_excel(file)
            
            # Expecting columns: id, judul, abstrak
            proposals = []
            cols = {str(c).lower().strip(): c for c in df.columns}
            
            for index, row in df.iterrows():
                id_col = cols.get('id')
                judul_col = cols.get('judul')
                abstrak_col = cols.get('abstrak')
                
                proposals.append({
                    "id": str(row[id_col]) if id_col and pd.notna(row[id_col]) else str(index),
                    "judul": str(row[judul_col]) if judul_col and pd.notna(row[judul_col]) else "",
                    "abstrak": str(row[abstrak_col]) if abstrak_col and pd.notna(row[abstrak_col]) else ""
                })
                
            k_rank_str = request.form.get('k_rank')
            global_k_rank = int(k_rank_str) if k_rank_str and k_rank_str.isdigit() else None
            
            results = BatchService.process_batch(proposals, global_k_rank=global_k_rank)
            return ResponseFormatter.success(data=results)
        except Exception as e:
            return ResponseFormatter.error(f"Error processing file: {str(e)}", status_code=500)
