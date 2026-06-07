<template>
  <div class="min-h-screen bg-slate-50 font-sans text-slate-800 selection:bg-violet-200 selection:text-violet-900 relative">
    
    <div :class="['fixed top-6 left-1/2 transform -translate-x-1/2 z-100 transition-all duration-300 ease-out flex items-center gap-3 px-5 py-3 rounded-2xl shadow-xl border', toastState.show ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0 pointer-events-none', toastState.type === 'error' ? 'bg-red-50 border-red-200 text-red-700' : 'bg-emerald-50 border-emerald-200 text-emerald-700']">
      <svg v-if="toastState.type === 'error'" class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      <svg v-else class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      <span class="text-sm font-bold">{{ toastState.message }}</span>
    </div>

    <nav class="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex justify-between items-center h-16">
          
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-linear-to-br from-violet-600 to-fuchsia-600 flex items-center justify-center text-white font-black text-lg shadow-md shadow-violet-200">
              SR
            </div>
            <div class="flex flex-col">
              <span class="font-black text-lg text-slate-800 tracking-tight leading-none">SIREDO</span>
              <span class="text-[10px] font-bold text-slate-400 tracking-widest uppercase mt-0.5">Sistem Rekomendasi Dosen</span>
            </div>
          </div>
          
          <div class="flex gap-2">
            <router-link to="/" class="px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-200 text-slate-500 hover:text-violet-600 hover:bg-violet-50" active-class="bg-violet-100 text-violet-700">
              Mesin Rekomendasi
            </router-link>
            
            <router-link to="/dosen" class="px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-200 text-slate-500 hover:text-violet-600 hover:bg-violet-50" active-class="bg-violet-100 text-violet-700">
              Daftar Dosen
            </router-link>
          </div>

        </div>
      </div>
    </nav>

    <main class="p-6">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { toastState } from './utils/toast';
</script>