import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

class Config:
    """Centralized configuration class loaded from environment variables."""
    
    # Base paths
    # Base dir: server root directory (2 levels up from server/src/core)
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    STORAGE_DIR = os.path.join(BASE_DIR, 'storage')
    CACHE_DIR = os.path.join(STORAGE_DIR, 'cache')
    DATA_DIR = os.path.join(STORAGE_DIR, 'data')
    DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
    
    # Application settings
    APP_NAME = os.getenv('APP_NAME', 'SiReDo')
    APP_ENV = os.getenv('APP_ENV', 'development')
    APP_DEBUG = os.getenv('APP_DEBUG', 'false').lower() in ('true', '1', 't', 'yes')
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.getenv('APP_PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-siredo-insecure-secret-key')
    
    # Security & CORS
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173').split(',')
        if origin.strip()
    ]
    ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'siredo-admin-secret-key')
    
    # Database (MySQL)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'db_siredo')
    
    # Excel fallback data path
    EXCEL_FALLBACK_PATH = os.path.join(DATASET_DIR, 'dataset_profiles_terintegrasi.xlsx')
    
    # Runtime configuration file
    CONFIG_JSON_PATH = os.path.join(DATA_DIR, 'config.json')
    
    # Operation constraints
    MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 100))
    MAX_K_RANK = int(os.getenv('MAX_K_RANK', 20))
    DEFAULT_K_RANK = 5
