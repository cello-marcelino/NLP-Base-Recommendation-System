<script setup>
import { onMounted } from 'vue'
import { useSystemStore } from '../../stores/system'

const systemStore = useSystemStore()

onMounted(() => {
  systemStore.fetchStatus()
  setInterval(() => {
    systemStore.fetchStatus()
  }, 15000)
})
</script>

<template>
  <div class="flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border transition-colors"
    :class="{
      'bg-emerald-50 text-emerald-700 border-emerald-200': systemStore.isOnline && systemStore.isCacheReady,
      'bg-amber-50 text-amber-700 border-amber-200': systemStore.isOnline && !systemStore.isCacheReady,
      'bg-red-50 text-red-700 border-red-200': !systemStore.isOnline
    }"
  >
    <div class="w-2 h-2 rounded-full animate-pulse"
      :class="{
        'bg-emerald-500': systemStore.isOnline && systemStore.isCacheReady,
        'bg-amber-500': systemStore.isOnline && !systemStore.isCacheReady,
        'bg-red-500': !systemStore.isOnline
      }"
    ></div>
    <span v-if="systemStore.isOnline && systemStore.isCacheReady">Server Online (Ready: {{ systemStore.totalDosen }} Dosen)</span>
    <span v-else-if="systemStore.isOnline && !systemStore.isCacheReady">Server Online (Warming Up...)</span>
    <span v-else>Server Offline</span>
  </div>
</template>
