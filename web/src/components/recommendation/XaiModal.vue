<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  dosen: Object,
  xai: Object
})

defineEmits(['close'])

const showAllRecords = ref(false)

const parseListItems = (str) => {
  if (!str || typeof str !== 'string') return []
  const trimmed = str.trim()
  if (!trimmed || trimmed === '-' || trimmed.toLowerCase() === 'nan' || trimmed.toLowerCase() === 'null') {
    return []
  }
  // Quoted items
  const matches = trimmed.match(/"([^"]+)"/g)
  if (matches && matches.length > 0) {
    return matches
      .map(m => m.replace(/(^"|"$)/g, '').trim())
      .filter(j => j.length > 0 && j !== '-')
  }
  // Array-like
  if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
    try {
      const parsed = JSON.parse(trimmed.replace(/'/g, '"'))
      if (Array.isArray(parsed)) return parsed.map(String).filter(Boolean)
    } catch {}
  }
  // Semicolon / newline separated
  return trimmed
    .split(/\n|;|•|\r/)
    .map(s => s.replace(/^[0-9]+[.)]\s*/, '').trim())
    .filter(s => s.length > 0 && s !== '-')
}

const parseEducationList = (str) => {
  if (!str || typeof str !== 'string') return []
  const trimmed = str.trim()
  if (!trimmed || trimmed === '-' || trimmed.toLowerCase() === 'nan' || trimmed.toLowerCase() === 'null') return []
  
  const regex = /(?=Sarjana|Magister|Doktor|Diploma|S1|S2|S3|D3|D4)/i
  let items = []
  if (trimmed.includes('\n')) {
    items = trimmed.split('\n')
  } else if (trimmed.includes(', ') && regex.test(trimmed)) {
    items = trimmed.split(/,\s*(?=Sarjana|Magister|Doktor|Diploma|S1|S2|S3|D3|D4)/i)
  } else {
    items = trimmed.split(/,|;/)
  }
  return items.map(s => s.trim()).filter(Boolean)
}

const matchTerms = computed(() => {
  const terms = new Set()
  if (Array.isArray(props.xai?.irisan_kata)) {
    props.xai.irisan_kata.forEach(k => {
      if (k && k.trim().length >= 3) terms.add(k.trim().toLowerCase())
    })
  }
  if (Array.isArray(props.xai?.topik_dosen)) {
    props.xai.topik_dosen.forEach(t => {
      if (t && t.trim().length >= 3) {
        t.trim().toLowerCase().split(/\s+/).forEach(word => {
          if (word.length >= 3) terms.add(word)
        })
      }
    })
  }
  return Array.from(terms)
})

const filterRelevant = (items) => {
  if (matchTerms.value.length === 0) return items
  return items.filter(item => {
    const lower = item.toLowerCase()
    return matchTerms.value.some(term => lower.includes(term))
  })
}

const allJurnalList = computed(() => parseListItems(props.dosen?.jurnal))
const allBimbinganList = computed(() => parseListItems(props.dosen?.judul_bimbing))
const allUjiList = computed(() => parseListItems(props.dosen?.judul_uji))
const pendidikanList = computed(() => parseEducationList(props.dosen?.pendidikan))

const displayJurnalList = computed(() => {
  if (showAllRecords.value) return allJurnalList.value
  return filterRelevant(allJurnalList.value)
})

const displayBimbinganList = computed(() => {
  if (showAllRecords.value) return allBimbinganList.value
  return filterRelevant(allBimbinganList.value)
})

const displayUjiList = computed(() => {
  if (showAllRecords.value) return allUjiList.value
  return filterRelevant(allUjiList.value)
})
</script>

<template>
  <div v-if="isOpen && dosen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-box">
      <!-- Modal Header -->
      <div class="modal-header">
        <div class="modal-header-info">
          <div class="modal-badges">
            <span class="prodi-badge">{{ dosen.program_studi }}</span>
            <span v-if="dosen.nidn" class="nidn-badge">NIDN: {{ dosen.nidn }}</span>
          </div>
          <h3 class="modal-title">{{ dosen.nama }}</h3>
        </div>
        <button @click="$emit('close')" class="modal-close-btn" aria-label="Tutup modal">
          <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="modal-body">
        
        <!-- 1. Bidang Keahlian & Pendidikan -->
        <div class="xai-grid-2">
          <div class="xai-card">
            <h4 class="xai-label">Bidang Keahlian</h4>
            <p class="xai-text font-medium">{{ dosen.bidang_keahlian || '-' }}</p>
          </div>
          <div class="xai-card">
            <h4 class="xai-label">Riwayat Pendidikan</h4>
            <div v-if="pendidikanList.length" class="edu-timeline">
              <div v-for="(edu, idx) in pendidikanList" :key="'edu'+idx" class="edu-item">
                <div class="edu-dot"></div>
                <div class="edu-content">
                  <span class="edu-title">{{ edu }}</span>
                </div>
              </div>
            </div>
            <p v-else class="xai-empty">Belum ada data pendidikan.</p>
          </div>
        </div>

        <!-- 2. XAI Explainability (BM25 + KeyBERT) -->
        <div class="xai-card xai-card--brand">
          <div class="xai-header-flex">
            <h4 class="xai-label text-indigo-900">Alasan Rekomendasi (Explainable AI)</h4>
            <button 
              type="button" 
              class="filter-toggle-btn"
              @click="showAllRecords = !showAllRecords"
            >
              {{ showAllRecords ? 'Tampilkan Hanya Yang Relevan' : 'Tampilkan Semua Riwayat' }}
            </button>
          </div>
          
          <div class="xai-reasons-grid">
            <div>
              <div class="xai-sub-label">Irisan Kata Kunci Eksak (BM25 Match):</div>
              <div class="xai-tags">
                <span v-for="kata in xai?.irisan_kata" :key="kata" class="xai-tag xai-tag--blue">
                  <svg class="xai-check" width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                  </svg>
                  {{ kata }}
                </span>
                <span v-if="!xai?.irisan_kata?.length" class="xai-empty">Tidak ada kata kunci yang cocok secara eksak.</span>
              </div>
            </div>

            <div>
              <div class="xai-sub-label">Topik Semantik Dosen (KeyBERT):</div>
              <div class="xai-tags">
                <span v-for="topik in xai?.topik_dosen" :key="topik" class="xai-tag xai-tag--fuchsia">
                  {{ topik }}
                </span>
                <span v-if="!xai?.topik_dosen?.length" class="xai-empty">Belum ada topik semantik terdeteksi.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Riwayat Publikasi Jurnal Relevan -->
        <div class="xai-section">
          <div class="xai-section-header">
            <h4 class="xai-label">
              {{ showAllRecords ? 'Seluruh Riwayat Publikasi Jurnal' : 'Riwayat Publikasi Jurnal Relevan' }}
            </h4>
            <span class="count-badge count-badge--brand">
              {{ displayJurnalList.length }} / {{ allJurnalList.length }}
            </span>
          </div>
          <ul v-if="displayJurnalList.length" class="xai-list-group">
            <li v-for="(jurnal, idx) in displayJurnalList" :key="'j'+idx" class="xai-list-item">
              <span class="item-num">{{ idx + 1 }}</span>
              <span class="item-text">{{ jurnal }}</span>
            </li>
          </ul>
          <p v-else class="xai-empty">Tidak ada riwayat publikasi jurnal yang memuat kata kunci topik input.</p>
        </div>

        <!-- 4. Riwayat Bimbingan Mahasiswa Relevan -->
        <div class="xai-section">
          <div class="xai-section-header">
            <h4 class="xai-label">
              {{ showAllRecords ? 'Seluruh Riwayat Bimbingan' : 'Riwayat Bimbingan Mahasiswa Relevan' }}
            </h4>
            <span class="count-badge count-badge--green">
              {{ displayBimbinganList.length }} / {{ allBimbinganList.length }}
            </span>
          </div>
          <ul v-if="displayBimbinganList.length" class="xai-list-group">
            <li v-for="(bimbing, idx) in displayBimbinganList" :key="'b'+idx" class="xai-list-item">
              <span class="item-num item-num--green">{{ idx + 1 }}</span>
              <span class="item-text">{{ bimbing }}</span>
            </li>
          </ul>
          <p v-else class="xai-empty">Tidak ada riwayat bimbingan mahasiswa yang memuat kata kunci topik input.</p>
        </div>

        <!-- 5. Riwayat Pengujian Mahasiswa Relevan -->
        <div class="xai-section">
          <div class="xai-section-header">
            <h4 class="xai-label">
              {{ showAllRecords ? 'Seluruh Riwayat Pengujian' : 'Riwayat Pengujian Sidang Relevan' }}
            </h4>
            <span class="count-badge count-badge--blue">
              {{ displayUjiList.length }} / {{ allUjiList.length }}
            </span>
          </div>
          <ul v-if="displayUjiList.length" class="xai-list-group">
            <li v-for="(uji, idx) in displayUjiList" :key="'u'+idx" class="xai-list-item">
              <span class="item-num item-num--blue">{{ idx + 1 }}</span>
              <span class="item-text">{{ uji }}</span>
            </li>
          </ul>
          <p v-else class="xai-empty">Tidak ada riwayat pengujian sidang yang memuat kata kunci topik input.</p>
        </div>
        
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(17, 17, 24, 0.45);
  backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  padding: 1.5rem; z-index: 200;
}

.modal-box {
  background: var(--bg);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
  width: 100%; max-width: 820px; max-height: 85vh; height: 85vh;
  display: flex; flex-direction: column; overflow: hidden;
  animation: modal-up 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modal-up {
  from { opacity: 0; transform: translateY(16px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: flex-start;
  background: var(--bg);
  flex-shrink: 0;
}
.modal-header-info { display: flex; flex-direction: column; gap: 0.35rem; }
.modal-badges { display: flex; align-items: center; gap: 0.5rem; }
.prodi-badge {
  font-size: 0.72rem; font-weight: 700; color: var(--brand);
  background: var(--brand-light); padding: 2px 8px; border-radius: var(--radius-sm);
}
.nidn-badge {
  font-family: var(--font-mono); font-size: 0.7rem; font-weight: 600;
  color: var(--text-muted); background: var(--bg-muted); padding: 2px 6px; border-radius: var(--radius-sm);
}
.modal-title { font-size: 1.35rem; font-weight: 800; color: var(--text-primary); margin: 0; }

.modal-close-btn {
  background: var(--bg-muted);
  border: none; border-radius: 50%;
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  color: var(--text-muted);
  cursor: pointer; transition: all 0.15s;
}
.modal-close-btn:hover { background: var(--red-bg); color: var(--red); }

.modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
  min-height: 0;
  background: var(--bg-subtle);
  display: flex; flex-direction: column; gap: 1.5rem;
}

.xai-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.xai-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: flex; flex-direction: column; gap: 0.5rem;
}
.xai-card--brand {
  background: #fcfaff;
  border-color: #ddd6fe;
}

.xai-header-flex {
  display: flex; justify-content: space-between; align-items: center;
}

.filter-toggle-btn {
  font-size: 0.72rem; font-weight: 600;
  color: var(--brand); background: var(--bg);
  border: 1px solid #c4b5fd; border-radius: var(--radius-sm);
  padding: 0.25rem 0.6rem; cursor: pointer; transition: all 0.15s;
}
.filter-toggle-btn:hover {
  background: var(--brand); color: white;
}

.xai-label {
  font-size: 0.72rem; font-weight: 700; font-family: var(--font-mono);
  text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted);
  margin: 0;
}
.xai-sub-label {
  font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.35rem;
}
.xai-text { font-size: 0.85rem; color: var(--text-primary); line-height: 1.5; margin: 0; }
.xai-empty { font-size: 0.78rem; color: var(--text-muted); font-style: italic; margin: 0; }

.edu-timeline { display: flex; flex-direction: column; gap: 0.6rem; margin-top: 0.25rem; }
.edu-item { display: flex; align-items: flex-start; gap: 0.75rem; }
.edu-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--brand); margin-top: 6px; flex-shrink: 0; box-shadow: 0 0 0 3px var(--brand-light); }
.edu-content { flex: 1; background: var(--bg-subtle); border: 1px solid var(--border); border-radius: 6px; padding: 0.4rem 0.6rem; }
.edu-title { font-size: 0.78rem; font-weight: 600; color: var(--text-primary); line-height: 1.35; display: block; }

.xai-reasons-grid {
  display: flex; flex-direction: column; gap: 0.75rem;
}

.xai-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.xai-tag {
  font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
  padding: 3px 8px; border-radius: var(--radius-sm); border: 1px solid;
}
.xai-tag--fuchsia { background: var(--fuchsia-bg); border-color: var(--fuchsia-border); color: var(--fuchsia); }
.xai-tag--blue {
  background: var(--blue-bg); border-color: var(--blue-border); color: var(--blue);
  display: flex; align-items: center; gap: 4px;
}
.xai-check { font-size: 0.65rem; }

.xai-section {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: flex; flex-direction: column; gap: 0.75rem;
}
.xai-section-header {
  display: flex; justify-content: space-between; align-items: center;
}

.count-badge {
  font-family: var(--font-mono); font-size: 0.7rem; font-weight: 700;
  padding: 2px 8px; border-radius: 99px;
}
.count-badge--brand { background: var(--brand-light); color: var(--brand); }
.count-badge--green { background: var(--green-bg); color: var(--green); }
.count-badge--blue { background: var(--blue-bg); color: var(--blue); }

.xai-list-group {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 0.5rem;
}
.xai-list-item {
  display: flex; align-items: flex-start; gap: 0.75rem;
  padding: 0.6rem 0.85rem;
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}
.item-num {
  display: flex; align-items: center; justify-content: center;
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--brand-light); color: var(--brand);
  font-family: var(--font-mono); font-size: 0.68rem; font-weight: 700;
  flex-shrink: 0; margin-top: 1px;
}
.item-num--green { background: var(--green-bg); color: var(--green); }
.item-num--blue { background: var(--blue-bg); color: var(--blue); }

.item-text {
  font-size: 0.825rem; color: var(--text-primary); line-height: 1.5;
}

@media (max-width: 768px) {
  .xai-grid-2 { grid-template-columns: 1fr; }
  .modal-header { padding: 1.25rem 1.5rem; }
  .modal-body { padding: 1.25rem; }
}
</style>
