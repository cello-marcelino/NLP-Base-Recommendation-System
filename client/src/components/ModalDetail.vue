<template>
  <div v-if="isOpen" class="fixed inset-0 bg-surface-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50 opacity-100 transition-opacity">
    <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[85vh] flex flex-col overflow-hidden border border-surface-100">

      <!-- Header dengan avatar inisial -->
      <div class="px-7 py-5 border-b border-surface-100 flex justify-between items-center bg-white gap-4">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
            <span class="text-lg font-semibold text-primary-700">
              {{ dataDosen.NAMA?.split(' ').slice(0,2).map(w => w[0]).join('') }}
            </span>
          </div>
          <div>
            <h3 class="text-lg font-bold text-surface-800 leading-snug">{{ dataDosen.NAMA }}</h3>
            <p class="text-sm font-medium text-primary-600 mt-0.5">{{ dataDosen.PROGRAM_STUDI }}</p>
          </div>
        </div>
        <button @click="tutupModal" class="w-8 h-8 rounded-full bg-surface-50 hover:bg-red-50 border border-surface-200 text-surface-400 hover:text-red-500 transition-colors flex items-center justify-center flex-shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Strip skor (opsional, tampilkan jika props skor tersedia) -->
      <div v-if="dataDosen.HYBRID_SCORE" class="grid grid-cols-3 border-b border-surface-100 bg-surface-50/70 divide-x divide-surface-100">
        <div class="py-3 text-center">
          <p class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-1">BM25 Score</p>
          <p class="text-xl font-bold text-primary-600">{{ dataDosen.BM25_SCORE }}</p>
        </div>
        <div class="py-3 text-center">
          <p class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-1">SBERT Score</p>
          <p class="text-xl font-bold text-surface-700">{{ dataDosen.SBERT_SCORE }}</p>
        </div>
        <div class="py-3 text-center">
          <p class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-1">Hybrid Score</p>
          <p class="text-xl font-bold text-emerald-600">{{ dataDosen.HYBRID_SCORE }}</p>
        </div>
      </div>

      <!-- Body -->
      <div class="p-7 overflow-y-auto space-y-6 bg-surface-50/50">

        <!-- Bidang keahlian -->
        <div>
          <h4 class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-3">Bidang keahlian utama</h4>
          <div class="flex flex-wrap gap-2">
            <span v-for="(skill, i) in formatArray(dataDosen.BIDANG_KEAHLIAN)" :key="i"
                  class="bg-primary-100 text-primary-700 border border-primary-200 px-3 py-1.5 rounded-lg text-xs font-semibold">
              {{ skill }}
            </span>
          </div>
        </div>

        <!-- Publikasi -->
        <div>
          <h4 class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-3">Publikasi jurnal</h4>
          <div class="bg-white border border-surface-200 rounded-xl overflow-hidden">
            <div v-for="(item, i) in formatArray(dataDosen.JURNAL)" :key="i"
                 class="flex gap-3 px-5 py-3.5 text-sm text-surface-600 border-b border-surface-100 last:border-b-0">
              <span class="w-1.5 h-1.5 rounded-full bg-surface-300 flex-shrink-0 mt-2"></span>
              <span class="leading-relaxed">{{ item }}</span>
            </div>
            <div v-if="formatArray(dataDosen.JURNAL).length === 0" class="px-5 py-3.5 text-sm text-surface-400 italic">
              Belum ada data tercatat.
            </div>
          </div>
        </div>

        <!-- Historis 2 kolom -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-3">Historis uji</h4>
            <div class="bg-white border border-surface-200 rounded-xl overflow-hidden h-full">
              <div v-for="(item, i) in formatArray(dataDosen['judul uji'])" :key="i"
                   class="flex gap-3 px-4 py-3 text-sm text-surface-600 border-b border-surface-100 last:border-b-0">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-300 flex-shrink-0 mt-1.5"></span>
                <span class="leading-relaxed text-xs">{{ item }}</span>
              </div>
              <div v-if="formatArray(dataDosen['judul uji']).length === 0" class="px-4 py-3 text-xs text-surface-400 italic">Belum ada data.</div>
            </div>
          </div>
          <div>
            <h4 class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-3">Historis bimbingan</h4>
            <div class="bg-white border border-surface-200 rounded-xl overflow-hidden h-full">
              <div v-for="(item, i) in formatArray(dataDosen['judul bimbing'])" :key="i"
                   class="flex gap-3 px-4 py-3 text-sm text-surface-600 border-b border-surface-100 last:border-b-0">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 flex-shrink-0 mt-1.5"></span>
                <span class="leading-relaxed text-xs">{{ item }}</span>
              </div>
              <div v-if="formatArray(dataDosen['judul bimbing']).length === 0" class="px-4 py-3 text-xs text-surface-400 italic">Belum ada data.</div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ isOpen: Boolean, dataDosen: Object, tutupModal: Function });

const formatArray = (text) => {
  if (!text) return [];
  let str = String(text).replace(/^\[|\]$/g, '').trim();
  let arr = str.includes('", "') ? str.split('", "') : str.split(',');
  return arr.map(s => s.replace(/(^")|("$)/g, '').trim()).filter(x => x && x !== '-' && x !== 'None');
};
</script>