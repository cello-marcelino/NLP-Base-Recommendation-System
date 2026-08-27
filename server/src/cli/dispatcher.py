import argparse
import sys

from server.src.cli.server_cmd import serve, reload, shutdown
from server.src.cli.db_cmd import db_migrate, db_seed, db_export, db_import, db_drop, db_truncate
from server.src.cli.cache_cmd import cache_clear
from server.src.cli.log_cmd import show_logs

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python siredo",
        description="SiReDo CLI Framework - Manajemen server, database, dan utilitas sistem.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh Penggunaan:
  python siredo serve                 Menjalankan API server di background (default: CPU)
  python siredo serve --device cuda   Menjalankan API server dengan akselerasi GPU (CUDA)
  python siredo serve --foreground    Menjalankan API server di foreground (blocking)
  python siredo serve --port 8000     Menjalankan API server pada port 8000
  python siredo reload                Hot reload NLP cache pada server aktif
  python siredo shutdown              Mematikan proses server yang sedang aktif
  python siredo logs -f               Memantau stream log server secara real-time
  python siredo logs -n 50            Melihat 50 baris log terakhir
  python siredo db:migrate            Menjalankan migrasi skema database
  python siredo db:seed               Menjalankan seeder data awal / konfigurasi statis
  python siredo db:export             Mengekspor seluruh tabel database ke Excel
  python siredo db:import             Mengimpor dataset Excel ke database
  python siredo db:truncate           Mengosongkan seluruh isi data tabel database
  python siredo db:drop               Menghapus seluruh database
  python siredo cache:clear           Membersihkan cache embedding di disk
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Perintah yang tersedia:")
    
    # 1. serve
    p_serve = subparsers.add_parser("serve", help="Menjalankan server backend SiReDo (background by default)")
    p_serve.add_argument("--host", type=str, default=None, help="Host address (default dari .env/0.0.0.0)")
    p_serve.add_argument("--port", type=int, default=None, help="Port server (default dari .env/5000)")
    p_serve.add_argument("--device", type=str, choices=["cpu", "cuda", "auto"], default=None, help="Target perangkat komputasi AI/NLP (default: cpu)")
    p_serve.add_argument("--debug", action="store_true", default=None, help="Aktifkan debug mode")
    p_serve.add_argument("--foreground", "--fg", action="store_true", help="Jalankan di foreground (blocking mode)")
    p_serve.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    
    # 2. reload
    p_reload = subparsers.add_parser("reload", help="Memuat ulang konfigurasi & NLP cache pada server aktif")
    p_reload.add_argument("--host", type=str, default=None, help="Host server target (default 127.0.0.1)")
    p_reload.add_argument("--port", type=int, default=None, help="Port server target (default 5000)")
    
    # 3. shutdown
    subparsers.add_parser("shutdown", help="Menghentikan proses server SiReDo yang sedang berjalan")

    # 4. logs
    p_logs = subparsers.add_parser("logs", help="Menampilkan atau memantau file log real-time server")
    p_logs.add_argument("-f", "--follow", action="store_true", help="Memantau log secara real-time (live tail)")
    p_logs.add_argument("-n", "--lines", type=int, default=30, help="Jumlah baris terakhir yang ditampilkan (default: 30)")
    p_logs.add_argument("--clear", action="store_true", help="Membersihkan isi file log")
    
    # 5. db:migrate
    subparsers.add_parser("db:migrate", help="Menjalankan migrasi DDL skema database (SQLite/MySQL)")
    
    # 6. db:seed
    subparsers.add_parser("db:seed", help="Menjalankan database seeder untuk data awal & konfigurasi")
    
    # 7. db:export
    p_export = subparsers.add_parser("db:export", help="Mengekspor seluruh tabel database ke file Excel (.xlsx) atau JSON")
    p_export.add_argument("-o", "--output", type=str, default=None, help="Lokasi file output ekspor")
    p_export.add_argument("-f", "--format", type=str, choices=["excel", "json"], default="excel", help="Format ekspor (default: excel)")
    
    # 8. db:import
    p_import = subparsers.add_parser("db:import", help="Mengimpor dataset profil dosen dari file Excel ke database")
    p_import.add_argument("--file", type=str, default=None, help="Lokasi file dataset Excel kustom")
    
    # 9. db:truncate (alias: db:empty)
    for alias in ["db:truncate", "db:empty"]:
        p_trunc = subparsers.add_parser(alias, help="Mengosongkan seluruh tabel database tanpa menghapus skema")
        p_trunc.add_argument("-f", "--force", action="store_true", help="Lewati prompt konfirmasi keamanan")
        
    # 10. db:drop
    p_drop = subparsers.add_parser("db:drop", help="Menghapus seluruh database dan tabel")
    p_drop.add_argument("-f", "--force", action="store_true", help="Lewati prompt konfirmasi keamanan")
    
    # 11. cache:clear
    subparsers.add_parser("cache:clear", help="Membersihkan file cache embedding SBERT/KeyBERT di disk")
    
    return parser

def main():
    parser = build_parser()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    
    if args.command == "serve":
        serve(host=args.host, port=args.port, debug=args.debug, foreground=args.foreground, is_worker=args.worker, device=args.device)
    elif args.command == "reload":
        reload(host=args.host, port=args.port)
    elif args.command == "shutdown":
        shutdown()
    elif args.command == "logs":
        show_logs(lines=args.lines, follow=args.follow, clear=args.clear)
    elif args.command == "db:migrate":
        db_migrate()
    elif args.command == "db:seed":
        db_seed()
    elif args.command == "db:export":
        db_export(output_path=args.output, export_format=args.format)
    elif args.command == "db:import":
        db_import(file_path=args.file)
    elif args.command in ("db:truncate", "db:empty"):
        db_truncate(force=args.force)
    elif args.command == "db:drop":
        db_drop(force=args.force)
    elif args.command == "cache:clear":
        cache_clear()
    else:
        parser.print_help()
