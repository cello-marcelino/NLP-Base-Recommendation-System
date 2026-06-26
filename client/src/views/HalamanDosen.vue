<template>
  <div class="max-w-7xl mx-auto py-8">
    
    <div class="flex flex-col md:flex-row md:justify-between md:items-end gap-5 mb-8">
      <div>
        <h2 class="text-3xl font-extrabold text-surface-800 tracking-tight">Pangkalan Data Dosen</h2>
        <p class="text-surface-500 mt-1">Daftar seluruh tenaga pendidik beserta rekam jejak akademik.</p>
      </div>
      
      <div class="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
        <div class="relative w-full sm:w-64">
          <div class="absolute inset-y-0 left-0 flex items-center pl-3.5 pointer-events-none">
            <svg class="w-4 h-4 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </div>
          <input v-model="searchQuery" type="text" placeholder="Cari nama, prodi, keahlian..."
            class="w-full pl-10 pr-4 py-2.5 bg-white border border-surface-200 rounded-xl shadow-sm text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all placeholder-surface-400 text-surface-700 font-medium">
          <button v-if="searchQuery" @click="searchQuery = ''" class="absolute inset-y-0 right-0 flex items-center pr-3 text-surface-400 hover:text-red-500 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <div class="flex items-center gap-2 bg-white border border-surface-200 pl-3 pr-1 py-1.5 rounded-xl shadow-sm focus-within:ring-2 focus-within:ring-primary-500 transition-all w-full sm:w-auto">
          <span class="text-surface-500 font-medium text-sm whitespace-nowrap">Tampilkan:</span>
          <div class="relative">
            <select v-model="itemsPerPage" @change="currentPage = 1"
              class="appearance-none bg-surface-50 border border-surface-100 text-primary-700 font-bold text-sm rounded-lg focus:outline-none cursor-pointer py-1 pl-3 pr-8 hover:bg-primary-50 transition-colors">
              <option :value="5">5 baris</option>
              <option :value="10">10 baris</option>
              <option :value="25">25 baris</option>
              <option :value="50">50 baris</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-primary-600">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-sm border border-surface-200 overflow-hidden mb-6">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-surface-50/50 border-b border-surface-200 text-xs uppercase tracking-widest text-surface-400 font-bold">
              <th class="p-5 font-bold w-16 text-center">No</th>
              <th class="p-5 font-bold">Informasi Dosen</th>
              <th class="p-5 font-bold">Bidang Keahlian</th>
              <th class="p-5 font-bold text-center">Rekam Jejak</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-surface-100">
            <tr v-if="paginatedDosen.length === 0">
              <td colspan="4" class="p-10 text-center">
                <div class="flex flex-col items-center justify-center text-surface-400">
                  <svg class="w-12 h-12 mb-3 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  <span class="font-bold text-base text-surface-500">Pencarian tidak menemukan hasil.</span>
                  <span class="text-sm mt-1">Coba gunakan kata kunci lain.</span>
                </div>
              </td>
            </tr>
            
            <tr v-for="(dosen, index) in paginatedDosen" :key="index" class="hover:bg-surface-50/80 transition-colors group">
              <td class="p-5 text-center text-surface-400 font-bold text-sm">
                {{ startIndex + index + 1 }}
              </td>
              <td class="p-5">
                <div class="font-bold text-surface-800 text-base">{{ dosen.NAMA }}</div>
                <div class="text-sm font-medium text-primary-600 mt-0.5">{{ dosen.PROGRAM_STUDI }}</div>
              </td>
              <td class="p-5 max-w-md">
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="(skill, i) in formatArray(dosen.BIDANG_KEAHLIAN).slice(0, 4)" :key="i"
                    class="bg-surface-100 text-surface-600 px-2.5 py-1 rounded-md text-[10px] font-bold border border-surface-200 uppercase tracking-wider">
                    {{ skill }}
                  </span>
                  <span v-if="formatArray(dosen.BIDANG_KEAHLIAN).length > 4"
                    class="bg-primary-50 border border-primary-100 text-primary-600 px-2 py-1 rounded-md text-[10px] font-extrabold">
                    +{{ formatArray(dosen.BIDANG_KEAHLIAN).length - 4 }}
                  </span>
                </div>
              </td>
              <td class="p-5 text-center">
                <button @click="bukaDetail(dosen)"
                  class="text-sm bg-white border border-surface-300 text-surface-600 font-semibold px-4 py-2 rounded-lg transition-all group-hover:border-primary-400 group-hover:bg-primary-50 group-hover:text-primary-700 shadow-sm hover:shadow">
                  Lihat Detail
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="filteredDosen.length > 0" class="flex flex-col sm:flex-row justify-between items-center gap-4 bg-white p-4 rounded-xl border border-surface-200 shadow-sm">
      <div class="text-sm text-surface-500 font-medium">
        Menampilkan <span class="font-bold text-surface-800">{{ startIndex + 1 }}</span> - 
        <span class="font-bold text-surface-800">{{ Math.min(endIndex, filteredDosen.length) }}</span> 
        dari <span class="font-bold text-surface-800">{{ filteredDosen.length }}</span> dosen
      </div>
      
      <div class="flex items-center gap-2">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
          class="flex items-center justify-center w-9 h-9 rounded-lg border border-surface-200 text-surface-600 hover:bg-surface-50 hover:text-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        </button>
        
        <div class="flex gap-1">
          <button v-for="page in visiblePages" :key="page" @click="goToPage(page)"
            :class="['w-9 h-9 rounded-lg text-sm font-bold transition-all', 
              page === currentPage 
              ? 'bg-primary-600 text-white shadow-md shadow-primary-200 border-none' 
              : 'bg-white border border-surface-200 text-surface-600 hover:bg-surface-50 hover:text-primary-600']">
            {{ page }}
          </button>
        </div>

        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages"
          class="flex items-center justify-center w-9 h-9 rounded-lg border border-surface-200 text-surface-600 hover:bg-surface-50 hover:text-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </button>
      </div>
    </div>

    <ModalDetail :isOpen="modalAktif" :dataDosen="dosenTerpilih" :tutupModal="tutupDetail" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import api from '../services/api';
import ModalDetail from '../components/ModalDetail.vue';

const daftarDosen = ref([]);
const modalAktif = ref(false);
const dosenTerpilih = ref({});

// State pencarian
const searchQuery = ref('');

const currentPage = ref(1);
const itemsPerPage = ref(10);

// Filter pencarian
const filteredDosen = computed(() => {
  if (!searchQuery.value) {
    return daftarDosen.value;
  }
  
  const query = searchQuery.value.toLowerCase();
  return daftarDosen.value.filter(dosen => {
    const nama = dosen.NAMA ? dosen.NAMA.toLowerCase() : '';
    const prodi = dosen.PROGRAM_STUDI ? dosen.PROGRAM_STUDI.toLowerCase() : '';
    const keahlian = dosen.BIDANG_KEAHLIAN ? dosen.BIDANG_KEAHLIAN.toLowerCase() : '';
    
    return nama.includes(query) || prodi.includes(query) || keahlian.includes(query);
  });
});

// Reset halaman saat query berubah
watch(searchQuery, () => {
  currentPage.value = 1;
});

// Paginasi
const totalPages = computed(() => {
  return Math.ceil(filteredDosen.value.length / itemsPerPage.value) || 1;
});

const startIndex = computed(() => {
  return (currentPage.value - 1) * itemsPerPage.value;
});

const endIndex = computed(() => {
  return startIndex.value + itemsPerPage.value;
});

const paginatedDosen = computed(() => {
  return filteredDosen.value.slice(startIndex.value, endIndex.value);
});

const visiblePages = computed(() => {
  const pages = [];
  const maxVisibleButtons = 5;
  let startPage = Math.max(1, currentPage.value - Math.floor(maxVisibleButtons / 2));
  let endPage = startPage + maxVisibleButtons - 1;

  if (endPage > totalPages.value) {
    endPage = totalPages.value;
    startPage = Math.max(1, endPage - maxVisibleButtons + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }
  return pages;
});

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

onMounted(async () => {
  try {
    const respons = await api.getSemuaDosen();
    daftarDosen.value = respons.data;
  } catch (error) {
    console.error("Gagal mengambil data.");
  }
});

const formatArray = (text) => {
  if (!text) return [];
  let str = String(text).replace(/^\[|\]$/g, '').trim();
  let arr = str.includes('", "') ? str.split('", "') : str.split(',');
  return arr.map(s => s.replace(/(^")|("$)/g, '').trim()).filter(x => x && x !== '-');
};

const bukaDetail = (dosen) => { dosenTerpilih.value = dosen; modalAktif.value = true; };
const tutupDetail = () => { modalAktif.value = false; };
</script>
