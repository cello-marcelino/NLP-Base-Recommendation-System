import os

class Config:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    STORAGE_DIR = os.path.join(BASE_DIR, "storage")
    DATA_DIR = os.path.join(STORAGE_DIR, "data")
    MODELS_DIR = os.path.join(STORAGE_DIR, "models")
    CACHE_DIR = os.path.join(STORAGE_DIR, "cache")
    
    # We first check if the original exists, otherwise use the rule path
    _OLD_EXCEL = os.path.join(BASE_DIR, "data", "dataset_profiles_terintegrasi.xlsx")
    _NEW_EXCEL = os.path.join(DATA_DIR, "data_dosen.xlsx")
    EXCEL_FILE = _OLD_EXCEL if os.path.exists(_OLD_EXCEL) and not os.path.exists(_NEW_EXCEL) else _NEW_EXCEL
    
    VEKTOR_CACHE = os.path.join(CACHE_DIR, "vektor_dosen.npy")
    FINGERPRINT_CACHE = os.path.join(CACHE_DIR, "vektor_dosen.npy.fingerprint")
    KEYBERT_CACHE = os.path.join(CACHE_DIR, "keybert_dosen.json")
    
    SBERT_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
