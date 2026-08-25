import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useConfigStore = defineStore('config', () => {
  const config = ref({
    threshold: 0.0,
    adaptive_alpha_threshold: 15,
    is_adaptive: true,
    manual_alpha: 0.7
  })
  
  const isLoading = ref(false)
  const isSaving = ref(false)
  const error = ref(null)
  const successMessage = ref('')

  const fetchConfig = async () => {
    isLoading.value = true
    error.value = null
    try {
      const res = await api.get('/system/config')
      config.value = res.data.data
      return config.value
    } catch (err) {
      error.value = err.userMessage || 'Gagal memuat konfigurasi'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const saveConfig = async (newConfig) => {
    isSaving.value = true
    error.value = null
    successMessage.value = ''
    try {
      const res = await api.patch('/system/config', newConfig)
      config.value = res.data.data
      successMessage.value = 'Konfigurasi berhasil disimpan!'
      return config.value
    } catch (err) {
      error.value = err.userMessage || 'Gagal menyimpan konfigurasi'
      throw err
    } finally {
      isSaving.value = false
    }
  }

  return {
    config,
    isLoading,
    isSaving,
    error,
    successMessage,
    fetchConfig,
    saveConfig
  }
})
