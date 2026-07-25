import json
from typing import Generator

def generate_progress_event(step: int, message: str, is_complete: bool = False, payload: dict = None) -> str:
    """Format SSE payload."""
    data = {
        "step": step,
        "message": message,
        "is_complete": is_complete
    }
    if payload:
        data["payload"] = payload
    return f"data: {json.dumps(data)}\n\n"
