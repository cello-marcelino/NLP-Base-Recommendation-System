from typing import Any, Optional, Dict
from flask import jsonify, Response

class ResponseFormatter:
    """
    Standard response formatter conforming to rules/api-design.md.
    """
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", meta: Optional[Dict[str, Any]] = None, status_code: int = 200) -> tuple[Response, int]:
        response: Dict[str, Any] = {
            "success": True,
            "message": message,
        }
        if data is not None:
            response["data"] = data
        if meta is not None:
            response["meta"] = meta
            
        return jsonify(response), status_code

    @staticmethod
    def error(message: str = "Error", code: str = "BAD_REQUEST", details: Optional[Any] = None, status_code: int = 400) -> tuple[Response, int]:
        error_payload: Dict[str, Any] = {
            "code": code,
            "message": message,
        }
        if details is not None:
            error_payload["details"] = details
            
        response: Dict[str, Any] = {
            "success": False,
            "error": error_payload
        }
        return jsonify(response), status_code
