import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useSystemStore = defineStore('system', () => {
  const isOnline = ref(false)
  const isCacheReady = ref(false)
  const totalDosen = ref(0)
  const dosenList = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchStatus = async () => {
    try {
      const res = await api.get('/system/status')
      const data = res.data.data
      isOnline.value = true
      isCacheReady.value = data.cache_ready
      totalDosen.value = data.total_dosen
      error.value = null
      return data
    } catch (err) {
      isOnline.value = false
      isCacheReady.value = false
      error.value = err.userMessage || 'Server offline'
      return null
    }
  }

  const fetchDosenList = async () => {
    isLoading.value = true
    error.value = null
    try {
      const res = await api.get('/dosen')
      dosenList.value = res.data.data || []
      totalDosen.value = dosenList.value.length
      isCacheReady.value = true
      return dosenList.value
    } catch (err) {
      error.value = err.userMessage || 'Gagal memuat data dosen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    isOnline,
    isCacheReady,
    totalDosen,
    dosenList,
    isLoading,
    error,
    fetchStatus,
    fetchDosenList
  }
})
