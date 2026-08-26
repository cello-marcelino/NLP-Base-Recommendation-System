import os
import logging
from logging.handlers import RotatingFileHandler
import time
import uuid
from flask import request, g

from server.src.core.config import Config

def setup_logger(app_name: str = "siredo-server", log_level: str = None) -> logging.Logger:
    level_name = log_level or Config.LOG_LEVEL
    log_level_val = getattr(logging, level_name.upper(), logging.INFO)
    
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level_val)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z"
        )
        
        # 1. Dedicated File Handler (Rotating File Handler: max 10MB, 5 backups)
        try:
            log_file = Config.LOG_FILE
            os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level_val)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # Fallback if file cannot be created
            pass

        # 2. Console Error Handler (Only warnings & errors to stderr for clean terminal)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()

def init_app_logging(app):
    """Attach request tracing and structured logging middleware to Flask app."""
    # Suppress verbose standard werkzeug request logger from polluting terminal stdout
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)
    
    @app.before_request
    def before_request_logging():
        g.request_start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])

    @app.after_request
    def after_request_logging(response):
        duration = round((time.time() - getattr(g, 'request_start_time', time.time())) * 1000, 2)
        request_id = getattr(g, 'request_id', '-')
        
        # Structured log written directly to dedicated file
        logger.info(
            f"request_id={request_id} endpoint={request.method} {request.path} "
            f"status={response.status_code} duration={duration}ms"
        )
        response.headers['X-Request-ID'] = request_id
        return response
