import os
from dotenv import load_dotenv

# Base & Root paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

# Load .env tunggal dari root proyek
ROOT_ENV = os.path.join(ROOT_DIR, '.env')
load_dotenv(ROOT_ENV)

class Config:
    """Centralized configuration class loaded from environment variables."""
    
    # Base paths
    ROOT_DIR = ROOT_DIR
    BASE_DIR = BASE_DIR
    DATABASE_DIR = os.path.join(BASE_DIR, 'database')
    STORAGE_DIR = os.path.join(BASE_DIR, 'storage')
    CACHE_DIR = os.path.join(STORAGE_DIR, 'cache')
    DATA_DIR = os.path.join(STORAGE_DIR, 'data')
    LOGS_DIR = os.path.join(STORAGE_DIR, 'logs')
    DATASET_DIR = DATA_DIR
    
    # Logging Configuration
    LOG_FILE = os.getenv('LOG_FILE', os.path.join(LOGS_DIR, 'siredo.log'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Application settings
    APP_NAME = os.getenv('APP_NAME', 'SiReDo')
    APP_ENV = os.getenv('APP_ENV', 'development')
    APP_DEBUG = os.getenv('APP_DEBUG', 'false').lower() in ('true', '1', 't', 'yes')
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.getenv('APP_PORT', 5000))
    APP_URL = os.getenv('APP_URL', 'http://localhost:5000')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-siredo-insecure-secret-key')
    
    # Security & CORS
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173').split(',')
        if origin.strip()
    ]
    ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'siredo-admin-secret-key')
    
    # Database Configuration (Driver: 'sqlite' | 'mysql')
    DB_DRIVER = os.getenv('DB_DRIVER', 'sqlite').lower().strip()
    
    # SQLite file located in server/database/siredo.db
    _raw_sqlite = os.getenv('DB_SQLITE_PATH', os.path.join(DATABASE_DIR, 'siredo.db'))
    if not os.path.isabs(_raw_sqlite):
        if _raw_sqlite.startswith('server/'):
            DB_SQLITE_PATH = os.path.abspath(os.path.join(ROOT_DIR, _raw_sqlite))
        else:
            DB_SQLITE_PATH = os.path.abspath(os.path.join(BASE_DIR, _raw_sqlite))
    else:
        DB_SQLITE_PATH = _raw_sqlite
    
    # MySQL Configuration (Used if DB_DRIVER=mysql)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USERNAME', os.getenv('DB_USER', 'root'))
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_DATABASE', os.getenv('DB_NAME', 'db_siredo'))
    
    # Hardware Acceleration / NLP Device (Default: cpu | Opsi: cuda, auto)
    TORCH_DEVICE = os.getenv('TORCH_DEVICE', 'cpu').lower().strip()
    
    # AI / LLM (Untuk integrasi masa depan: OpenAI, Gemini, Claude, dll)
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')
    AI_API_KEY = os.getenv('AI_API_KEY', '')
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-4o-mini')
    
    # Cache & Storage
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() in ('true', '1', 't', 'yes')
    
    # Excel fallback data path (stored in server/storage/data)
    EXCEL_FALLBACK_PATH = os.path.join(DATA_DIR, 'dataset_profiles_terintegrasi.xlsx')
    
    # Runtime configuration file
    CONFIG_JSON_PATH = os.path.join(DATA_DIR, 'config.json')
    
    # Operation constraints
    MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 100))
    MAX_K_RANK = int(os.getenv('MAX_K_RANK', 20))
    DEFAULT_K_RANK = 5
