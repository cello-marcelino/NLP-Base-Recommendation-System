import os
import glob
from server.src.config.config import Config

def cache_clear():
    """Cleans up generated embedding and NLP keyword cache files."""
    cache_dir = Config.CACHE_DIR
    if not os.path.exists(cache_dir):
        print(f"[INFO] Direktori cache '{cache_dir}' tidak ditemukan.")
        return
        
    pattern_npy = os.path.join(cache_dir, "*.npy")
    pattern_json = os.path.join(cache_dir, "*.json")
    pattern_pkl = os.path.join(cache_dir, "*.pkl")
    
    files = glob.glob(pattern_npy) + glob.glob(pattern_json) + glob.glob(pattern_pkl)
    if not files:
        print("[INFO] Tidak ada file cache (.npy / .json / .pkl) yang perlu dibersihkan.")
        return
        
    deleted_count = 0
    for f in files:
        try:
            os.remove(f)
            deleted_count += 1
            print(f"  [DELETED] {os.path.basename(f)}")
        except Exception as e:
            print(f"  [ERROR] Gagal menghapus {os.path.basename(f)}: {e}")
            
    print(f"[OK] Selesai! Berhasil membersihkan {deleted_count} file cache.")
