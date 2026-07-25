<template>
  <div
    class="min-h-screen bg-surface-50 font-sans text-surface-800 selection:bg-primary-200 selection:text-primary-900 relative">

    <!-- Toast Notification -->
    <div
      :class="['fixed top-6 left-1/2 transform -translate-x-1/2 z-100 transition-all duration-200 ease-out flex items-center gap-3 px-5 py-3 rounded-2xl shadow-xl border', toastState.show ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0 pointer-events-none', toastState.type === 'error' ? 'bg-red-50 border-red-200 text-red-700' : 'bg-green-50 border-green-200 text-green-700']">
      <svg v-if="toastState.type === 'error'" class="w-5 h-5 shrink-0" fill="none" stroke="currentColor"
        viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <svg v-else class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <span class="text-sm font-bold">{{ toastState.message }}</span>
    </div>

    <!-- Thin Server Status Bar -->
    <div class="bg-surface-900 text-surface-50 text-xs py-1.5 px-4 md:px-8 flex justify-between items-center relative z-50">
      <div class="flex items-center gap-2.5">
        <span class="relative flex h-2.5 w-2.5">
          <span v-if="serverReady" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2.5 w-2.5" :class="serverReady ? 'bg-emerald-500' : 'bg-red-500'"></span>
        </span>
        <span class="font-bold tracking-wide" :class="serverReady ? 'text-surface-100' : 'text-surface-400'">
          {{ serverMessage }}
        </span>
      </div>
      <div class="flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-surface-400">
        <span class="hidden sm:inline">ALOKASI DATA:</span> 
        <strong :class="sumberData === 'MySQL' ? 'text-primary-400' : (sumberData === '-' ? 'text-surface-600' : 'text-amber-400')">
          {{ sumberData }}
        </strong>
      </div>
    </div>

    <nav class="bg-white/80 backdrop-blur-md border-b border-surface-200 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto">
        <div class="flex justify-between items-center h-16 px-4 sm:px-6 lg:px-8">

          <div class="flex items-center gap-3">
            <div class="flex flex-col">
              <span class="font-black text-lg text-surface-800 tracking-tight leading-none">SiReDo</span>
              <span class="text-xs font-bold text-surface-400 tracking-widest capitlize mt-0.5">Sistem Rekomendasi
                Dosen</span>
            </div>
          </div>

          <div class="flex gap-2">
            <router-link v-for="menu in menuNavigasi" :key="menu.path" :to="menu.path" :class="[
              'px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-200 hidden sm:inline-block',
              $route.path === menu.path
                ? 'bg-primary-100 text-primary-600'
                : 'text-surface-500 hover:text-primary-600 hover:bg-primary-50']">
              {{ menu.label }}
            </router-link>
            <!-- Mobile Menu Dropdown Button Fallback (Visual only for now) -->
            <button class="sm:hidden p-2 text-surface-500 hover:text-primary-600 hover:bg-primary-50 rounded-lg">
               <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
          </div>

        </div>
      </div>  
    </nav>

    <main class="flex-1 w-full relative z-0">
      <!-- View Transition Wrapper -->
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { toastState } from './utils/toast';
import api from './services/api.js';

// Server Status State
const serverReady = ref(false);
const serverMessage = ref('Menghubungkan ke peladen...');
const sumberData = ref('-');

let pollInterval = null;

const fetchServerStatus = async () => {
  try {
    const res = await api.cekStatusServer();
    serverReady.value = res.ready;
    serverMessage.value = res.pesan || 'Mesin SIREDO Siap Beroperasi!';
    sumberData.value = res.sumber_data || '-';
  } catch (error) {
    serverReady.value = false;
    serverMessage.value = 'Peladen Python terputus / offline.';
    sumberData.value = '-';
  }
};

onMounted(() => {
  // First initial fetch
  fetchServerStatus();
  // Poll every 3 seconds to keep UI updated dynamically
  pollInterval = setInterval(fetchServerStatus, 3000);
});

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval);
});

// 💡 PUSAT KONTROL MENU NAVIGASI
const menuNavigasi = [
  { label: 'Rekomendasi Proposal', path: '/' },
  { label: 'Daftar Dosen', path: '/dosen' },
  { label: 'Admin Panel', path: '/admin/dosen' },
  { label: 'Riwayat', path: '/admin/riwayat' }
];
</script>