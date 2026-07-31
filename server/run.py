from app import create_app
from app.services.cache_service import CacheService

app = create_app()

if __name__ == '__main__':
    # Eksekusi Warm-up sebelum server menerima request
    with app.app_context():
        CacheService.get_instance().initialize_cache(app_context=app.app_context())
        
    app.run(host='0.0.0.0', port=5000, debug=True)
