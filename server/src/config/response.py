from typing import Any, Optional, Dict
from flask import jsonify, Response

class ResponseFormatter:
    """Standardized API Response Formatter conforming to rules/api-design.md."""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Sukses",
        status_code: int = 200,
        meta: Optional[Dict[str, Any]] = None
    ) -> Response:
        payload = {
            "success": True,
            "message": message,
            "data": data if data is not None else {}
        }
        if meta:
            payload["meta"] = meta
            
        return jsonify(payload), status_code

    @staticmethod
    def error(
        message: str = "Terjadi kesalahan",
        code: str = "INTERNAL_SERVER_ERROR",
        details: Optional[Any] = None,
        status_code: int = 500
    ) -> Response:
        error_payload = {
            "code": code,
            "message": message
        }
        if details:
            error_payload["details"] = details
            
        payload = {
            "success": False,
            "error": error_payload
        }
        return jsonify(payload), status_code
