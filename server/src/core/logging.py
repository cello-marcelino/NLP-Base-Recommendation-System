import logging
import time
import uuid
from flask import request, g

def setup_logger(app_name: str = "siredo-server", log_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logger()

def init_app_logging(app):
    """Attach request tracing and structured logging middleware to Flask app."""
    
    @app.before_request
    def before_request_logging():
        g.request_start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])

    @app.after_request
    def after_request_logging(response):
        if request.path.startswith('/health'):
            return response
            
        duration = round((time.time() - getattr(g, 'request_start_time', time.time())) * 1000, 2)
        request_id = getattr(g, 'request_id', '-')
        
        logger.info(
            f"request_id={request_id} endpoint={request.method} {request.path} "
            f"status={response.status_code} duration={duration}ms"
        )
        response.headers['X-Request-ID'] = request_id
        return response
