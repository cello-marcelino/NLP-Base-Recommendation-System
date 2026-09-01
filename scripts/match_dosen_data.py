import os
import sys
import json
import re
import unicodedata
from difflib import SequenceMatcher

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.src.repositories.dosen.dosen_repository import SQLDosenRepository

def normalize_name(name: str) -> str:
    if not name:
        return ""
    # Strip accents & unicode
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    name = name.lower()
    
    # Common academic titles to strip
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
        
    # Strip non-alphanumeric except space
    name = re.sub(r'[^a-z\s]', ' ', name)
    name = ' '.join(name.split())
    return name

def similarity_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_name(a), normalize_name(b)).ratio()

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
    
    print(f"Total Data Scrap: {len(scraped_data)}")
    print(f"Total Data DB   : {len(db_dosen)}")
    
    matches = []
    unmatched_scrap = []
    matched_db_ids = set()
    
    for s in scraped_data:
        s_nama = s.get('nama', '')
        s_nidn = str(s.get('nidn', '')).strip()
        s_prodi = s.get('program_studi', '')
        s_keahlian = ', '.join(s.get('bidang_spesialis', [])) if isinstance(s.get('bidang_spesialis'), list) else str(s.get('bidang_spesialis', ''))
        s_pendidikan = ', '.join(s.get('riwayat_pendidikan', [])) if isinstance(s.get('riwayat_pendidikan'), list) else str(s.get('pendidikan_terakhir', ''))
        
        best_match = None
        best_score = 0.0
        match_type = ""
        
        # 1. NIDN exact match
        if s_nidn:
            for d in db_dosen:
                d_nidn = str(d.get('nidn', '')).strip()
                if d_nidn and d_nidn == s_nidn:
                    best_match = d
                    best_score = 1.0
                    match_type = "NIDN Exact Match"
                    break
                    
        # 2. Name fuzzy / normalized match
        if not best_match:
            for d in db_dosen:
                d_nama = d.get('nama', '')
                score = similarity_ratio(s_nama, d_nama)
                if score > best_score and score >= 0.70:
                    best_score = score
                    best_match = d
                    match_type = f"Name Similarity ({int(score*100)}%)"
                    
        if best_match:
            d_id = best_match.get('id') or best_match.get('nidn')
            matched_db_ids.add(d_id)
            matches.append({
                "scrap_data": s,
                "db_data": best_match,
                "score": best_score,
                "match_type": match_type,
                "changes": {
                    "nidn": {"old": best_match.get('nidn'), "new": s_nidn if s_nidn else best_match.get('nidn')},
                    "nama": {"old": best_match.get('nama'), "new": s_nama},
                    "program_studi": {"old": best_match.get('program_studi'), "new": s_prodi if s_prodi else best_match.get('program_studi')},
                    "bidang_keahlian": {"old": best_match.get('bidang_keahlian'), "new": s_keahlian if s_keahlian else best_match.get('bidang_keahlian')},
                    "pendidikan": {"old": best_match.get('pendidikan'), "new": s_pendidikan if s_pendidikan else best_match.get('pendidikan')}
                }
            })
        else:
            unmatched_scrap.append(s)
            
    unmatched_db = [d for d in db_dosen if (d.get('id') or d.get('nidn')) not in matched_db_ids]
    
    # Write to docs/dosen-data-update.md
    docs_dir = os.path.abspath("docs")
    os.makedirs(docs_dir, exist_ok=True)
    report_file = os.path.join(docs_dir, "dosen-data-update.md")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Laporan Hasil Pencocokan Data Dosen (dosen.json vs Database)\n\n")
        f.write("Dokumen ini berisi hasil analisis perbandingan antara data hasil scraping (`dosen.json`) dan data master dosen yang ada di database (`siredo.db`).\n\n")
        f.write("## 1. Ringkasan Statistik\n\n")
        f.write(f"- **Total Record di Scrap (`dosen.json`)**: {len(scraped_data)}\n")
        f.write(f"- **Total Record Dosen di DB**: {len(db_dosen)}\n")
        f.write(f"- **Record Berhasil Dicocokkan (Matched)**: {len(matches)}\n")
        f.write(f"- **Record Scrap Baru (Unmatched Scrap)**: {len(unmatched_scrap)}\n")
        f.write(f"- **Record DB Tanpa Pasangan Scrap (Unmatched DB)**: {len(unmatched_db)}\n\n")
        
        f.write("## 2. Rincian Data Cocok (Matched Records) & Usulan Penyesuaian\n\n")
        f.write("Tabel di bawah ini menampilkan perbandingan data dosen DB dengan data scrap yang cocok beserta perubahan data yang diusulkan:\n\n")
        f.write("| No | Nama DB | Nama Scrap | Metode Match | NIDN Lama -> Baru | Keahlian Baru | Status |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        
        for idx, m in enumerate(matches, start=1):
            old_name = m['db_data'].get('nama', '')
            new_name = m['scrap_data'].get('nama', '')
            match_type = m['match_type']
            old_nidn = m['changes']['nidn']['old'] or '-'
            new_nidn = m['changes']['nidn']['new'] or '-'
            keahlian = m['changes']['bidang_keahlian']['new'] or '-'
            f.write(f"| {idx} | {old_name} | {new_name} | {match_type} | `{old_nidn}` -> `{new_nidn}` | {keahlian} | READY TO UPDATE |\n")
            
        f.write("\n\n## 3. Rincian Perubahan Field Per Dosen (Detail Inspection)\n\n")
        for idx, m in enumerate(matches, start=1):
            f.write(f"### {idx}. {m['db_data'].get('nama')}\n")
            f.write(f"- **Metode Match**: {m['match_type']}\n")
            f.write(f"- **NIDN**: `{m['changes']['nidn']['old']}` -> `{m['changes']['nidn']['new']}`\n")
            f.write(f"- **Program Studi**: `{m['changes']['program_studi']['old']}` -> `{m['changes']['program_studi']['new']}`\n")
            f.write(f"- **Bidang Keahlian**: `{m['changes']['bidang_keahlian']['old']}` -> `{m['changes']['bidang_keahlian']['new']}`\n")
            f.write(f"- **Pendidikan**: `{m['changes']['pendidikan']['old']}` -> `{m['changes']['pendidikan']['new']}`\n\n")
            
        if unmatched_scrap:
            f.write("## 4. Data Scrap Baru (Belum ada di DB)\n\n")
            f.write("Berikut data dosen baru dari hasil scrap yang dapat di-insert ke DB:\n\n")
            f.write("| No | Nama | NIDN | Program Studi | Bidang Spesialis |\n")
            f.write("|---|---|---|---|---|\n")
            for idx, s in enumerate(unmatched_scrap, start=1):
                f.write(f"| {idx} | {s.get('nama')} | {s.get('nidn', '-')} | {s.get('program_studi', '-')} | {', '.join(s.get('bidang_spesialis', []))} |\n")
                
    print(f"\n[OK] Laporan pencocokan berhasil dibuat di: {report_file}")

if __name__ == '__main__':
    main()
