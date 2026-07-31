from flask import jsonify

class ResponseFormatter:
    @staticmethod
    def success(data=None, message="Success", meta=None, status_code=200):
        response = {
            "status": "success",
            "message": message,
        }
        if data is not None:
            response["data"] = data
        if meta is not None:
            response["meta"] = meta
            
        return jsonify(response), status_code

    @staticmethod
    def error(message="Error", errors=None, status_code=400):
        response = {
            "status": "error",
            "message": message,
        }
        if errors is not None:
            response["errors"] = errors
            
        return jsonify(response), status_code
