import os
from flask import Flask
from flask_cors import CORS

from server.src.config.config import Config
from server.src.config.logging_config import logger
from server.src.config.response import ResponseFormatter
from server.src.exceptions.app_exceptions import AppException
from server.src.middleware.logging_middleware import init_app_logging

def create_app(config_class=Config) -> Flask:
    """Flask application factory conforming to Layered Architecture rules."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 1. Setup CORS with explicit origins whitelist
    CORS(
        app,
        origins=config_class.CORS_ORIGINS,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-API-Key", "X-Request-ID"]
    )
    
    # 2. Setup Structured Logging and Request Tracing Middleware
    init_app_logging(app)
    
    # 3. Ensure required storage directories exist
    os.makedirs(config_class.CACHE_DIR, exist_ok=True)
    os.makedirs(config_class.DATA_DIR, exist_ok=True)
    os.makedirs(config_class.LOGS_DIR, exist_ok=True)
    os.makedirs(config_class.DATASET_DIR, exist_ok=True)
    
    # 4. Register Blueprints from routes layer
    from server.src.routes.system.system_routes import system_bp
    from server.src.routes.dosen.dosen_routes import dosen_bp
    from server.src.routes.recommendation.recommendation_routes import recommendation_bp
    
    app.register_blueprint(system_bp, url_prefix='/api')
    app.register_blueprint(dosen_bp, url_prefix='/api')
    app.register_blueprint(recommendation_bp, url_prefix='/api')
    
    # Root health check endpoint
    @app.route('/health', methods=['GET'])
    def root_health():
        from server.src.controllers.system.system_controller import SystemController
        return SystemController.get_health()

    # 5. Global Error Handlers (conforming to rules/api-design.md & rules/error-handling.md)
    @app.errorhandler(AppException)
    def handle_app_exception(error: AppException):
        logger.warning(f"Application error [{error.error_code}]: {error.message}")
        return ResponseFormatter.error(
            message=error.message,
            code=error.error_code,
            details=error.details if error.details else None,
            status_code=error.status_code
        )

    @app.errorhandler(400)
    def handle_bad_request(error):
        return ResponseFormatter.error(message="Bad request: " + str(error), code="BAD_REQUEST", status_code=400)

    @app.errorhandler(404)
    def handle_not_found(error):
        return ResponseFormatter.error(message="Endpoint atau resource tidak ditemukan", code="NOT_FOUND", status_code=404)

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return ResponseFormatter.error(message="HTTP Method tidak diizinkan untuk endpoint ini", code="METHOD_NOT_ALLOWED", status_code=405)

    @app.errorhandler(413)
    def handle_payload_too_large(error):
        return ResponseFormatter.error(message="Ukuran file atau payload melebihi batas yang diizinkan", code="PAYLOAD_TOO_LARGE", status_code=413)

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        logger.error(f"Unhandled server error: {error}", exc_info=True)
        message = "Terjadi kesalahan internal pada server"
        if app.config.get('APP_DEBUG'):
            message = f"{message}: {str(error)}"
        return ResponseFormatter.error(message=message, code="INTERNAL_SERVER_ERROR", status_code=500)

    return app
