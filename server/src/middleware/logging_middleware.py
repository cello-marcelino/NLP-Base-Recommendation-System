import time
import uuid
import logging
from flask import request, g
from server.src.config.logging_config import logger

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
        
        logger.info(
            f"request_id={request_id} endpoint={request.method} {request.path} "
            f"status={response.status_code} duration={duration}ms"
        )
        response.headers['X-Request-ID'] = request_id
        return response
