<script setup>
defineProps({
  isOpen: Boolean,
  dosen: Object,
  xai: Object
})

defineEmits(['close'])

const parseStringList = (str) => {
  if (!str || str.trim() === 'nan') return []
  const matches = str.match(/"([^"]+)"/g)
  if (matches) {
    return matches.map(m => m.replace(/(^"|"$)/g, '').trim()).filter(j => j.length > 0)
  }
  return str.split(/\n|;/).map(j => j.trim()).filter(j => j.length > 3)
}
</script>

<template>
  <div v-if="isOpen && dosen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-box">
      <div class="modal-header">
        <div>
          <h3 class="modal-title">{{ dosen.nama }}</h3>
          <p class="modal-subtitle">{{ dosen.program_studi }}</p>
        </div>
        <button @click="$emit('close')" class="modal-close-btn">
          <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="modal-body">
        
        <div class="xai-section">
          <h4 class="xai-label">Bidang Keahlian Utama</h4>
          <p class="xai-text">{{ dosen.bidang_keahlian || '-' }}</p>
        </div>
        
        <div class="xai-section">
          <h4 class="xai-label">Topik Semantic Dosen (KeyBERT)</h4>
          <div class="xai-tags">
            <span v-for="topik in xai?.topik_dosen" :key="topik" class="xai-tag xai-tag--fuchsia">
              {{ topik }}
            </span>
            <span v-if="!xai?.topik_dosen?.length" class="xai-empty">Belum ada data topik semantic.</span>
          </div>
        </div>

        <div class="xai-section">
          <h4 class="xai-label">Kata Yang Sama (BM25 Match)</h4>
          <div class="xai-tags">
            <span v-for="kata in xai?.irisan_kata" :key="kata" class="xai-tag xai-tag--blue">
              <span class="xai-check">✓</span> {{ kata }}
            </span>
            <span v-if="!xai?.irisan_kata?.length" class="xai-empty">Tidak ada kata yang cocok secara leksikal.</span>
          </div>
        </div>

        <div class="xai-section">
          <h4 class="xai-label">Riwayat Jurnal</h4>
          <ul v-if="parseStringList(dosen.jurnal).length" class="xai-bullet-list">
            <li v-for="(jurnal, idx) in parseStringList(dosen.jurnal)" :key="'j'+idx">{{ jurnal }}</li>
          </ul>
          <p v-else class="xai-empty">Belum ada riwayat jurnal.</p>
        </div>
        
        <div class="xai-section">
          <h4 class="xai-label">Riwayat Bimbingan</h4>
          <ul v-if="parseStringList(dosen.judul_bimbing).length" class="xai-bullet-list">
            <li v-for="(bimbing, idx) in parseStringList(dosen.judul_bimbing)" :key="'b'+idx">{{ bimbing }}</li>
          </ul>
          <p v-else class="xai-empty">Belum ada riwayat bimbingan.</p>
        </div>
        
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(17, 17, 24, 0.4);
  backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  padding: 1.5rem; z-index: 50;
}

.modal-box {
  background: var(--bg);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  width: 100%; max-width: 760px; max-height: 85vh;
  display: flex; flex-direction: column; overflow: hidden;
  animation: modal-up 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modal-up {
  from { opacity: 0; transform: translateY(20px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: flex-start;
  background: var(--bg);
}
.modal-title { font-size: 1.35rem; font-weight: 800; color: var(--text-primary); margin: 0 0 0.25rem; }
.modal-subtitle { font-size: 0.875rem; font-weight: 600; color: var(--brand); margin: 0; }

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
  background: var(--bg-subtle);
  display: flex; flex-direction: column; gap: 2rem;
}

.xai-section { display: flex; flex-direction: column; gap: 0.5rem; }
.xai-label {
  font-size: 0.68rem; font-weight: 700; font-family: var(--font-mono);
  text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted);
  margin: 0;
}
.xai-text { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6; margin: 0; }
.xai-empty { font-size: 0.8rem; color: var(--text-muted); font-style: italic; }

.xai-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.xai-tag {
  font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
  padding: 3px 8px; border-radius: var(--radius-sm); border: 1px solid;
}
.xai-tag--fuchsia { background: var(--fuchsia-bg); border-color: var(--fuchsia-border); color: var(--fuchsia); }
.xai-tag--blue {
  background: var(--blue); border-color: #1d4ed8; color: white;
  transform: scale(1.02); display: flex; align-items: center; gap: 4px;
}
.xai-check { font-size: 0.6rem; }

.xai-bullet-list {
  margin: 0; padding-left: 1.2rem;
  display: flex; flex-direction: column; gap: 0.5rem;
}
.xai-bullet-list li {
  font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;
}
</style>
