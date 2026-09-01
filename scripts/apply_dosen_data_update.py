import os
import sys
import json
import re
import unicodedata
from difflib import SequenceMatcher

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.src.repositories.dosen.dosen_repository import SQLDosenRepository
from server.src.services.system.cache_service import CacheService
from server.database.connection.database import DatabaseManager

def normalize_name(name: str) -> str:
    if not name:
        return ""
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8').lower()
    titles = [
        r'\bdr\b', r'\bprof\b', r'\bir\b', r'\bs\.st\b', r'\bm\.t\b', r'\bm\.kom\b',
        r'\bs\.kom\b', r'\bm\.sc\b', r'\bph\.d\b', r'\bphd\b', r'\bs\.tr\b', r'\bkom\b',
        r'\bm\.sn\b', r'\bs\.sn\b', r'\bm\.ds\b', r'\bs\.ds\b', r'\bm\.cs\b', r'\bs\.t\b',
        r'\bm\.eng\b', r'\bs\.pd\b', r'\bm\.pd\b', r'\bs\.si\b', r'\bm\.si\b', r'\bssc\b',
        r'\bm\.ides\b', r'\bs\.ag\b', r'\bm\.h\b', r'\blc\b', r'\bma\b', r'\bm\.il\b',
        r'\bm\.hum\b', r'\bs\.s\b', r'\bm\.comp\.sc\b', r'\bb\.cs\b'
    ]
    for t in titles:
        name = re.sub(t, '', name)
    name = re.sub(r'[^a-z\s]', ' ', name)
    return ' '.join(name.split())

def similarity_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_name(a), normalize_name(b)).ratio()

def generate_unique_nidn(used_nidns: set, custom_counter: int) -> tuple[str, int]:
    while True:
        candidate = f"99{custom_counter:04d}" # e.g. 990001, 990002...
        custom_counter += 1
        if candidate not in used_nidns:
            used_nidns.add(candidate)
            return candidate, custom_counter

def main():
    json_path = os.path.abspath("dosen.json")
    if not os.path.exists(json_path):
        print(f"[ERROR] File {json_path} tidak ditemukan!")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        scraped_data = json.load(f)
        
    repo = SQLDosenRepository()
    db_dosen_objects = repo.get_all()
    db_dosen = [d.to_dict() for d in db_dosen_objects]
    
    conn = DatabaseManager.get_connection()
    cursor = conn.cursor()
    
    # Track used NIDNs across the system
    used_nidns = set()
    for s in scraped_data:
        nidn = str(s.get('nidn', '')).strip()
        if nidn:
            used_nidns.add(nidn)
    for d in db_dosen:
        nidn = str(d.get('nidn', '')).strip()
        if nidn:
            used_nidns.add(nidn)
            
    custom_counter = 1
    updated_count = 0
    inserted_count = 0
    matched_db_ids = set()
    
    try:
        # 1. Process scraped records (Update matched or Insert new)
        for s in scraped_data:
            s_nama = s.get('nama', '')
            s_nidn = str(s.get('nidn', '')).strip()
            s_prodi = s.get('program_studi', '')
            
            keahlian_list = s.get('bidang_spesialis', [])
            s_keahlian = ', '.join(keahlian_list) if isinstance(keahlian_list, list) else str(keahlian_list)
            
            pend_list = s.get('riwayat_pendidikan', [])
            s_pendidikan = ', '.join(pend_list) if isinstance(pend_list, list) else str(s.get('pendidikan_terakhir', ''))
            
            best_match = None
            best_score = 0.0
            
            # Match by NIDN
            if s_nidn:
                for d in db_dosen:
                    if str(d.get('nidn', '')).strip() == s_nidn:
                        best_match = d
                        best_score = 1.0
                        break
                        
            # Match by Name
            if not best_match:
                for d in db_dosen:
                    score = similarity_ratio(s_nama, d.get('nama', ''))
                    if score > best_score and score >= 0.70:
                        best_score = score
                        best_match = d
                        
            # Assign unique NIDN if missing
            final_nidn = s_nidn
            if not final_nidn:
                if best_match and best_match.get('nidn'):
                    final_nidn = str(best_match.get('nidn')).strip()
                else:
                    final_nidn, custom_counter = generate_unique_nidn(used_nidns, custom_counter)
                    
            if best_match:
                d_id = best_match.get('id')
                matched_db_ids.add(d_id)
                cursor.execute(
                    "UPDATE dosen SET nidn = ?, nama = ?, program_studi = ?, bidang_keahlian = ?, pendidikan = ? WHERE id = ?",
                    (final_nidn, s_nama, s_prodi if s_prodi else best_match.get('program_studi', ''), s_keahlian if s_keahlian else best_match.get('bidang_keahlian', ''), s_pendidikan if s_pendidikan else best_match.get('pendidikan', ''), d_id)
                )
                updated_count += 1
            else:
                cursor.execute(
                    "INSERT INTO dosen (nidn, nama, program_studi, bidang_keahlian, pendidikan) VALUES (?, ?, ?, ?, ?)",
                    (final_nidn, s_nama, s_prodi, s_keahlian, s_pendidikan)
                )
                inserted_count += 1
                
        # 2. Check remaining DB records without NIDN and assign unique custom NIDN
        unmatched_db = [d for d in db_dosen if (d.get('id')) not in matched_db_ids]
        custom_nidn_assigned_count = 0
        for d in unmatched_db:
            d_nidn = str(d.get('nidn', '')).strip()
            if not d_nidn:
                new_nidn, custom_counter = generate_unique_nidn(used_nidns, custom_counter)
                cursor.execute("UPDATE dosen SET nidn = ? WHERE id = ?", (new_nidn, d.get('id')))
                custom_nidn_assigned_count += 1
                
        conn.commit()
        print(f"[OK] Sukses memperbarui {updated_count} record dosen di database.")
        print(f"[OK] Sukses menambahkan {inserted_count} record dosen baru dari scrap ke database.")
        print(f"[OK] Sukses membuat {custom_nidn_assigned_count} NIDN custom unik untuk dosen tanpa NIDN.")
        
        # Warm-up cache
        print("[INFO] Melakukan warm-up dan refresh cache rekomendasi NLP...")
        CacheService.get_instance().initialize_cache(force_refresh=True)
        print("[OK] Cache NLP engine dan database berhasil disinkronisasi.")
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Gagal melakukan update database: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    main()
