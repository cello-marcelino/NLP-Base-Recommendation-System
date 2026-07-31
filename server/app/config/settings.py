import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    STORAGE_DIR = os.path.join(BASE_DIR, 'storage')
    CACHE_DIR = os.path.join(STORAGE_DIR, 'cache')
    DATA_DIR = os.path.join(STORAGE_DIR, 'data')
    
    # DB config
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'db_siredo')
    
    # Excel Fallback
    EXCEL_FALLBACK_PATH = os.path.join(BASE_DIR, 'dataset', 'dataset_profiles_terintegrasi.xlsx')
    
    # Dynamic config storage path
    CONFIG_JSON_PATH = os.path.join(DATA_DIR, 'config.json')
