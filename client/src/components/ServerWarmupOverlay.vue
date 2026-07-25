<template>
  <div v-if="isModelWarmingUp" class="fixed inset-0 bg-white/90 backdrop-blur-md z-[100] flex flex-col items-center justify-center transition-opacity duration-500">
    <div class="w-16 h-16 border-4 border-surface-200 border-t-primary-600 rounded-full animate-spin mb-4 shadow-sm"></div>
    <h2 class="text-2xl font-extrabold text-surface-800">Menghidupkan Mesin SIREDO...</h2>
    <div class="w-72 bg-surface-200 rounded-full h-2.5 mt-5 mb-2 overflow-hidden shadow-inner relative">
      <div class="bg-primary-500 h-2.5 rounded-full transition-all duration-700 ease-out absolute top-0 left-0" :style="{ width: serverProgress + '%' }"></div>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-primary-700 font-mono text-sm font-extrabold">{{ serverProgress }}%</span>
      <span class="text-surface-400 font-bold">|</span>
      <p class="text-surface-500 text-sm font-medium animate-pulse">{{ serverMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api.js';

const isModelWarmingUp = ref(true);
const serverProgress = ref(0);
const serverMessage = ref('Menghubungkan ke peladen...');

onMounted(() => {
  pantauStatusServer();
});

const pantauStatusServer = () => {
  // Simulasi progress awal
  serverProgress.value = 10;
  
  const interval = setInterval(async () => {
    try {
      const res = await api.cekStatusServer();
      
      // Karena backend saat ini tidak mereturn angka progress spesifik,
      // kita jalankan simulasi progress naik pelan-pelan hingga 90%
      if (!res.ready && serverProgress.value < 90) {
        serverProgress.value += Math.floor(Math.random() * 10) + 5;
        if (serverProgress.value > 90) serverProgress.value = 90;
      }

      serverMessage.value = res.pesan || 'Menghidupkan model AI...';
      
      if (res.ready) {
        serverProgress.value = 100;
        serverMessage.value = 'Mesin Siap!';
        clearInterval(interval);
        setTimeout(() => { isModelWarmingUp.value = false; }, 800);
      }
    } catch {
      serverMessage.value = 'Peladen Python belum menyala...';
    }
  }, 1000);
};
</script>
