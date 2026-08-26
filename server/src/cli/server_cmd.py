import os
import sys
import time
import signal
import urllib.request
import urllib.error
import json
import subprocess

from server.src.core.config import Config
from server.src.core.logging import logger

PID_FILE = os.path.join(Config.DATA_DIR, 'siredo.pid')

def get_running_pid():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            # Check if process is still running
            if is_pid_alive(pid):
                return pid
            else:
                # Stale PID file
                os.remove(PID_FILE)
        except Exception:
            pass
    return None

def is_pid_alive(pid: int) -> bool:
    if os.name == 'nt':
        try:
            # Query tasklist for PID on Windows
            output = subprocess.check_output(f'tasklist /FI "PID eq {pid}" /NH', shell=True).decode()
            return str(pid) in output
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

def save_pid(pid: int):
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    with open(PID_FILE, 'w') as f:
        f.write(str(pid))

def remove_pid():
    if os.path.exists(PID_FILE):
        try:
            os.remove(PID_FILE)
        except Exception:
            pass

def serve(host: str = None, port: int = None, debug: bool = None):
    """Starts the SiReDo API server."""
    host = host or Config.APP_HOST
    port = port or Config.APP_PORT
    debug = debug if debug is not None else Config.APP_DEBUG
    
    current_pid = get_running_pid()
    if current_pid:
        print(f"[ERROR] Server SiReDo sudah berjalan dengan PID {current_pid}.")
        print("Gunakan 'python siredo reload' atau 'python siredo shutdown' terlebih dahulu.")
        sys.exit(1)
        
    # Save PID
    save_pid(os.getpid())
    
    from server.src.app import create_app
    from server.src.modules.system.cache_service import CacheService
    
    print("=" * 60)
    print(f" SiReDo Server v3.0.0")
    print(f" Environment : {Config.APP_ENV}")
    print(f" Database    : {Config.DB_DRIVER}")
    print(f" Host & Port : http://{host}:{port}")
    print(f" Process PID : {os.getpid()}")
    print("=" * 60)
    print("[INFO] Memanaskan NLP cache & embedding model...")
    
    # Initialize cache and models
    CacheService.get_instance().initialize_cache()
    
    app = create_app(Config)
    
    def cleanup_handler(*args):
        print("\n[INFO] Menerima sinyal stop, mematikan server...")
        remove_pid()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, cleanup_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, cleanup_handler)
        
    try:
        print(f"[OK] Server aktif dan siap menerima request di http://{host}:{port}")
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    finally:
        remove_pid()

def reload(host: str = None, port: int = None):
    """Hot-reloads configuration and caches on running server."""
    host = host or Config.APP_HOST
    if host == '0.0.0.0':
        host = '127.0.0.1'
    port = port or Config.APP_PORT
    
    url = f"http://{host}:{port}/api/system/reload"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": Config.ADMIN_API_KEY
    }
    
    print(f"[INFO] Mengirim sinyal reload ke {url}...")
    req = urllib.request.Request(url, data=b"{}", headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            res_body = res.read().decode('utf-8')
            data = json.loads(res_body)
            print("[OK] " + data.get("message", "Reload berhasil diselesaikan."))
            print(f"Status Cache: Ready (Total Dosen: {data.get('data', {}).get('total_dosen', '-')})")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Reload gagal dengan status code {e.code}: {e.read().decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Gagal menghubungi server SiReDo di http://{host}:{port}. Pastikan server menyala.")
        print(f"Detail error: {e}")
        sys.exit(1)

def shutdown():
    """Stops the running SiReDo server process."""
    pid = get_running_pid()
    if not pid:
        print("[INFO] Tidak ada server SiReDo yang sedang berjalan.")
        return
        
    print(f"[INFO] Menghentikan proses server SiReDo (PID: {pid})...")
    try:
        if os.name == 'nt':
            subprocess.run(f"taskkill /PID {pid} /F", shell=True, check=True)
        else:
            os.kill(pid, signal.SIGTERM)
            
        remove_pid()
        print(f"[OK] Server SiReDo (PID: {pid}) berhasil dimatikan.")
    except Exception as e:
        print(f"[ERROR] Gagal mematikan proses PID {pid}: {e}")
        remove_pid()
