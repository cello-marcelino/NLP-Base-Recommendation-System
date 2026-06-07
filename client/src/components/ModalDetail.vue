<template>
  <div v-if="isOpen" class="fixed inset-0 bg-surface-900/40 backdrop-blur-sm flex items-center justify-center p-4 z-50 opacity-100 transition-opacity">
    <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[85vh] flex flex-col overflow-hidden border border-surface-100">
      
      <div class="px-8 py-6 border-b border-surface-100 flex justify-between items-start bg-white">
        <div>
          <h3 class="text-2xl font-extrabold text-surface-800 mb-1">{{ dataDosen.NAMA }}</h3>
          <p class="text-sm font-medium text-primary-600">{{ dataDosen.PROGRAM_STUDI }}</p>
        </div>
        <button @click="tutupModal" class="p-2 rounded-full bg-surface-50 hover:bg-red-50 text-surface-400 hover:text-red-500 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <div class="p-8 overflow-y-auto space-y-8 bg-surface-50/50">
        
        <div>
          <h4 class="text-xs font-bold uppercase tracking-widest text-surface-400 mb-3">Bidang Keahlian Utama</h4>
          <div class="flex flex-wrap gap-2">
            <span v-for="(skill, i) in formatArray(dataDosen.BIDANG_KEAHLIAN)" :key="i" 
                  class="bg-primary-100 text-primary-700 border border-primary-200 px-3 py-1.5 rounded-lg text-sm font-medium">
              {{ skill }}
            </span>
          </div>
        </div>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-widest text-surface-400 mb-3 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-primary-400"></span> Publikasi Jurnal
          </h4>
          <div class="bg-white border border-surface-200 rounded-xl p-5 shadow-sm">
            <ul class="space-y-3">
              <li v-for="(item, i) in formatArray(dataDosen.JURNAL)" :key="i" class="text-sm text-surface-600 pl-4 relative before:content-[''] before:w-1.5 before:h-1.5 before:bg-surface-300 before:rounded-full before:absolute before:left-0 before:top-2">
                {{ item }}
              </li>
              <li v-if="formatArray(dataDosen.JURNAL).length === 0" class="text-sm text-surface-400 italic">Belum ada data tercatat.</li>
            </ul>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="text-xs font-bold uppercase tracking-widest text-surface-400 mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-amber-400"></span> Historis Uji
            </h4>
            <div class="bg-white border border-surface-200 rounded-xl p-5 shadow-sm h-full">
              <ul class="space-y-3">
                <li v-for="(item, i) in formatArray(dataDosen['judul uji'])" :key="i" class="text-sm text-surface-600 pl-4 relative before:content-[''] before:w-1.5 before:h-1.5 before:bg-surface-300 before:rounded-full before:absolute before:left-0 before:top-2">
                  {{ item }}
                </li>
                <li v-if="formatArray(dataDosen['judul uji']).length === 0" class="text-sm text-surface-400 italic">Belum ada data.</li>
              </ul>
            </div>
          </div>

          <div>
            <h4 class="text-xs font-bold uppercase tracking-widest text-surface-400 mb-3 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-400"></span> Historis Bimbingan
            </h4>
            <div class="bg-white border border-surface-200 rounded-xl p-5 shadow-sm h-full">
              <ul class="space-y-3">
                <li v-for="(item, i) in formatArray(dataDosen['judul bimbing'])" :key="i" class="text-sm text-surface-600 pl-4 relative before:content-[''] before:w-1.5 before:h-1.5 before:bg-surface-300 before:rounded-full before:absolute before:left-0 before:top-2">
                  {{ item }}
                </li>
                <li v-if="formatArray(dataDosen['judul bimbing']).length === 0" class="text-sm text-surface-400 italic">Belum ada data.</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ isOpen: Boolean, dataDosen: Object, tutupModal: Function });

// Fungsi cerdas untuk mengubah teks CSV yang berantakan menjadi Array bersih
const formatArray = (text) => {
  if (!text) return [];
  let str = String(text).replace(/^\[|\]$/g, '').trim();
  // Pisahkan berdasarkan koma yang memiliki tanda kutip (", ") atau koma biasa
  let arr = str.includes('", "') ? str.split('", "') : str.split(',');
  return arr.map(s => s.replace(/(^")|("$)/g, '').trim()).filter(x => x && x !== '-' && x !== 'None');
};
</script>