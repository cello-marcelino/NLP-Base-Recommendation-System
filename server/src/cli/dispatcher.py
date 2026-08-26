import argparse
import sys

from server.src.cli.server_cmd import serve, reload, shutdown
from server.src.cli.db_cmd import db_migrate, db_export, db_import
from server.src.cli.cache_cmd import cache_clear

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python siredo",
        description="SiReDo CLI Framework - Manajemen server, database, dan utilitas sistem.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh Penggunaan:
  python siredo serve                 Menjalankan API server SiReDo
  python siredo serve --port 8000     Menjalankan API server pada port 8000
  python siredo reload                Hot reload NLP cache pada server aktif
  python siredo shutdown              Mematikan proses server yang sedang aktif
  python siredo db:migrate            Menjalankan migrasi skema database
  python siredo db:export             Mengekspor seluruh tabel database ke Excel
  python siredo db:export --format json Mengekspor tabel database ke JSON
  python siredo db:import             Mengimpor dataset Excel ke database
  python siredo cache:clear           Membersihkan cache embedding di disk
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Perintah yang tersedia:")
    
    # 1. serve
    p_serve = subparsers.add_parser("serve", help="Menjalankan server backend SiReDo")
    p_serve.add_argument("--host", type=str, default=None, help="Host address (default dari .env/0.0.0.0)")
    p_serve.add_argument("--port", type=int, default=None, help="Port server (default dari .env/5000)")
    p_serve.add_argument("--debug", action="store_true", default=None, help="Aktifkan debug mode")
    
    # 2. reload
    p_reload = subparsers.add_parser("reload", help="Memuat ulang konfigurasi & NLP cache pada server aktif")
    p_reload.add_argument("--host", type=str, default=None, help="Host server target (default 127.0.0.1)")
    p_reload.add_argument("--port", type=int, default=None, help="Port server target (default 5000)")
    
    # 3. shutdown
    subparsers.add_parser("shutdown", help="Menghentikan proses server SiReDo yang sedang berjalan")
    
    # 4. db:migrate
    subparsers.add_parser("db:migrate", help="Menjalankan migrasi DDL skema database (SQLite/MySQL)")
    
    # 5. db:export
    p_export = subparsers.add_parser("db:export", help="Mengekspor seluruh data database ke Excel/JSON")
    p_export.add_argument("-o", "--output", type=str, default=None, help="Path file output tujuan")
    p_export.add_argument("-f", "--format", type=str, choices=["xlsx", "json"], default="xlsx", help="Format ekspor (default: xlsx)")
    
    # 6. db:import
    p_import = subparsers.add_parser("db:import", help="Mengimpor dataset Excel master ke database relasional")
    p_import.add_argument("-f", "--file", type=str, default=None, help="Path file Excel dataset sumber")
    
    # 7. cache:clear
    subparsers.add_parser("cache:clear", help="Membersihkan file cache embedding SBERT/KeyBERT di disk")
    
    return parser

def main():
    parser = build_parser()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    
    if args.command == "serve":
        serve(host=args.host, port=args.port, debug=args.debug)
    elif args.command == "reload":
        reload(host=args.host, port=args.port)
    elif args.command == "shutdown":
        shutdown()
    elif args.command == "db:migrate":
        db_migrate()
    elif args.command == "db:export":
        db_export(output_path=args.output, export_format=args.format)
    elif args.command == "db:import":
        db_import(file_path=args.file)
    elif args.command == "cache:clear":
        cache_clear()
    else:
        parser.print_help()
