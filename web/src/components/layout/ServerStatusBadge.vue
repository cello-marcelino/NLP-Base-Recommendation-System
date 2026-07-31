<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const status = ref('checking') // checking, online, offline
const cacheReady = ref(false)

const checkStatus = async () => {
  try {
    const res = await api.get('/status')
    status.value = 'online'
    cacheReady.value = res.data.data.cache_ready
  } catch (error) {
    status.value = 'offline'
    cacheReady.value = false
  }
}

onMounted(() => {
  checkStatus()
  setInterval(checkStatus, 30000)
})
</script>

<template>
  <div class="flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border"
    :class="{
      'bg-emerald-50 text-emerald-700 border-emerald-200': status === 'online' && cacheReady,
      'bg-amber-50 text-amber-700 border-amber-200': status === 'online' && !cacheReady,
      'bg-red-50 text-red-700 border-red-200': status === 'offline'
    }"
  >
    <div class="w-2 h-2 rounded-full animate-pulse"
      :class="{
        'bg-emerald-500': status === 'online' && cacheReady,
        'bg-amber-500': status === 'online' && !cacheReady,
        'bg-red-500': status === 'offline'
      }"
    ></div>
    <span v-if="status === 'online' && cacheReady">Server Online (Ready)</span>
    <span v-else-if="status === 'online' && !cacheReady">Server Online (Warming Up)</span>
    <span v-else>Server Offline</span>
  </div>
</template>
