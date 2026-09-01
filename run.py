import os
import sys

# Ensure repository root is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from server.src.app import create_app
from server.src.config.config import Config
from server.src.services.system.cache_service import CacheService

app = create_app(Config)

if __name__ == '__main__':
    # Initialize in-memory cache and warm up NLP engines before accepting incoming traffic
    CacheService.get_instance().initialize_cache()
    
    # Run server safely with parameters from Config/.env
    app.run(
        host=Config.APP_HOST,
        port=Config.APP_PORT,
        debug=Config.APP_DEBUG
    )
