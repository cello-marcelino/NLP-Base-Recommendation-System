from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Setup configuration
    from app.config.settings import Config
    app.config.from_object(Config)
    
    # Initialize cache and data directories
    os.makedirs(app.config['CACHE_DIR'], exist_ok=True)
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    
    # Register blueprints
    from app.routes.system import system_bp
    from app.routes.recommendation import recommendation_bp
    from app.routes.batch import batch_bp
    
    app.register_blueprint(system_bp, url_prefix='/api')
    app.register_blueprint(recommendation_bp, url_prefix='/api/rekomendasi')
    app.register_blueprint(batch_bp, url_prefix='/api/rekomendasi')
    
    return app
