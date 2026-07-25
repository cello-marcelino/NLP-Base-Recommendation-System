import json

class ResponseFormatter:
    @staticmethod
    def format_success(data, total_data=None, message="Success"):
        resp = {"status": "sukses"}
        if total_data is not None:
            resp["total_data"] = total_data
        resp["data"] = data
        return resp
        
    @staticmethod
    def format_error(message, code=400):
        return {"status": "gagal", "pesan": message}, code
