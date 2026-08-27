import os
import sys
import time

from server.src.config.config import Config

def show_logs(lines: int = 30, follow: bool = False, clear: bool = False):
    """Displays or monitors the dedicated SiReDo server log file."""
    log_file = Config.LOG_FILE
    
    if clear:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.truncate(0)
                print(f"[OK] File log '{log_file}' berhasil dibersihkan.")
            except Exception as e:
                print(f"[ERROR] Gagal membersihkan log: {e}")
        else:
            print(f"[INFO] File log '{log_file}' belum dibuat.")
        return

    if not os.path.exists(log_file):
        print(f"[INFO] File log belum ditemukan di: {log_file}")
        print("Jalankan server terlebih dahulu dengan 'python siredo serve'.")
        return

    # Read last N lines
    try:
        with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
            all_lines = f.readlines()
            tail_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            for l in tail_lines:
                print(l, end='')
    except Exception as e:
        print(f"[ERROR] Gagal membaca log file: {e}")
        return

    # Live follow mode (tail -f)
    if follow:
        print(f"\n--- [LIVE MONITORING] Memantau log secara real-time (Ctrl+C untuk berhenti) ---")
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                f.seek(0, os.SEEK_END)
                while True:
                    line = f.readline()
                    if line:
                        print(line, end='')
                        sys.stdout.flush()
                    else:
                        time.sleep(0.3)
        except KeyboardInterrupt:
            print("\n[INFO] Monitoring log dihentikan.")
