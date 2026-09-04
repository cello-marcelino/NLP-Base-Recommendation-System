import os
import sys
import time
import signal
import urllib.request
import urllib.error
import json
import subprocess

from server.src.config.config import Config
from server.src.config.logging_config import logger

PID_FILE = os.path.join(Config.DATA_DIR, 'siredo.pid')

def get_running_pid():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            if is_pid_alive(pid):
                return pid
            else:
                os.remove(PID_FILE)
        except Exception:
            pass
    return None

def is_pid_alive(pid: int) -> bool:
    if os.name == 'nt':
        try:
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

def check_server_healthy(host: str, port: int) -> bool:
    target_host = "127.0.0.1" if host in ("0.0.0.0", "") else host
    url = f"http://{target_host}:{port}/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=1) as res:
            return res.status == 200
    except Exception:
        return False

def _run_server_worker(host: str, port: int, debug: bool, device: str = None):
    """Internal blocking worker that warms cache and runs Flask."""
    # Ensure sys.stdout and sys.stderr are valid file objects under pythonw / DETACHED_PROCESS on Windows
    if sys.stdout is None:
        try:
            sys.stdout = open(Config.LOG_FILE, 'a', encoding='utf-8', buffering=1)
        except Exception:
            sys.stdout = open(os.devnull, 'w')
    if sys.stderr is None:
        try:
            sys.stderr = open(Config.LOG_FILE, 'a', encoding='utf-8', buffering=1)
        except Exception:
            sys.stderr = open(os.devnull, 'w')

    save_pid(os.getpid())
    
    if device:
        os.environ['TORCH_DEVICE'] = device
        Config.TORCH_DEVICE = device
        
    from server.src.app import create_app
    from server.src.services.system.cache_service import CacheService
    
    # 1. Start background warm-up for NLP models & embeddings
    CacheService.get_instance().initialize_cache_async()
    
    # 2. Build Flask App immediately
    app = create_app(Config)
    
    def cleanup_handler(*args):
        remove_pid()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, cleanup_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, cleanup_handler)
        
    try:
        app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)
    finally:
        remove_pid()

def serve(host: str = None, port: int = None, debug: bool = None, foreground: bool = False, is_worker: bool = False, device: str = None):
    """Starts the SiReDo API server in background (default) or foreground with optional compute device."""
    host = host or Config.APP_HOST
    port = port or Config.APP_PORT
    debug = debug if debug is not None else Config.APP_DEBUG
    effective_device = (device or Config.TORCH_DEVICE).lower().strip()
    
    if device:
        os.environ['TORCH_DEVICE'] = device
        Config.TORCH_DEVICE = device
    
    # Check if already running
    current_pid = get_running_pid()
    if current_pid:
        print(f"[ERROR] Server SiReDo sudah berjalan dengan PID {current_pid}.")
        print("Gunakan 'python siredo reload' atau 'python siredo shutdown' terlebih dahulu.")
        sys.exit(1)
        
    # If running directly as worker or in foreground mode
    if is_worker or foreground:
        if foreground:
            print("=" * 60)
            print(f" SiReDo Server v3.0.0 (Foreground Mode)")
            print(f" Host & Port    : http://{host}:{port}")
            print(f" Compute Device : {effective_device.upper()}")
            print(f" Process PID    : {os.getpid()}")
            print(f" Log File       : {Config.LOG_FILE}")
            print("=" * 60)
            print("[INFO] Tekan Ctrl+C untuk menghentikan server.")
        _run_server_worker(host=host, port=port, debug=debug, device=device)
        return

    # Background / Daemon Launcher mode
    print(f"[INFO] Memulai server SiReDo di background (device: {effective_device.upper()}, warming up NLP cache)...")
    
    python_exe = sys.executable
    script_path = os.path.abspath(sys.argv[0])
    
    cmd = [
        python_exe,
        script_path,
        "serve",
        "--host", host,
        "--port", str(port),
        "--worker"
    ]
    if debug:
        cmd.append("--debug")
    if device:
        cmd.extend(["--device", device])
        
    os.makedirs(Config.LOGS_DIR, exist_ok=True)
    
    if os.name == 'nt':
        # DETACHED_PROCESS + CREATE_NO_WINDOW ensures child process survives parent exit and has no console window
        DETACHED_PROCESS = 0x00000008
        CREATE_NO_WINDOW = 0x08000000
        proc = subprocess.Popen(
            cmd,
            creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW,
            close_fds=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
    else:
        # Unix detached process
        proc = subprocess.Popen(
            cmd,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
        
    # Wait until health check responds OK (or timeout 60s)
    started = False
    for _ in range(60):
        time.sleep(0.5)
        pid = get_running_pid()
        if pid and check_server_healthy(host, port):
            started = True
            break
            
    if started:
        pid = get_running_pid()
        print("=" * 60)
        print(f"[OK] Server SiReDo berhasil berjalan di background!")
        print(f"     URL            : http://{host}:{port}")
        print(f"     Compute Device : {effective_device.upper()}")
        print(f"     Process PID    : {pid}")
        print(f"     Log File       : {Config.LOG_FILE}")
        print("=" * 60)
        print("Terminal siap digunakan.")
        print("- Pantau log live : python siredo logs -f")
        print("- Hentikan server : python siredo shutdown")
    else:
        print("[WARN] Server dimulai di background. Sedang menyelesaikan warm-up model.")
        print("       Periksa status dengan: python siredo logs")

def reload(host: str = None, port: int = None):
    """Hot-reloads configuration and caches on running server."""
    host = host or Config.APP_HOST
    if host in ('0.0.0.0', ''):
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
        with urllib.request.urlopen(req, timeout=15) as res:
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
