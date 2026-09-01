import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'
import { parseLecturerExcel } from '../services/excelReader'

export const useSystemStore = defineStore('system', () => {
  const isOnline = ref(false)
  const isCacheReady = ref(false)
  const isExcelMode = ref(false)
  const totalDosen = ref(0)
  const dosenList = ref(JSON.parse(sessionStorage.getItem('siredo_excel_dosen_cache') || '[]'))
  const isLoading = ref(false)
  const error = ref(null)

  if (dosenList.value.length > 0) {
    isExcelMode.value = true
    totalDosen.value = dosenList.value.length
  }

  const fetchStatus = async () => {
    try {
      const res = await api.get('/system/status')
      const data = res.data.data
      isOnline.value = true
      isCacheReady.value = data.cache_ready
      if (!isExcelMode.value) {
        totalDosen.value = data.total_dosen
      }
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
    if (isExcelMode.value && dosenList.value.length > 0) {
      return dosenList.value
    }
    
    isLoading.value = true
    error.value = null
    try {
      const res = await api.get('/dosen')
      dosenList.value = res.data.data || []
      totalDosen.value = dosenList.value.length
      isCacheReady.value = true
      isExcelMode.value = false
      return dosenList.value
    } catch (err) {
      error.value = err.userMessage || 'Gagal memuat data dosen dari server'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const loadExcelDataset = async (file) => {
    isLoading.value = true
    error.value = null
    try {
      const parsedData = await parseLecturerExcel(file)
      dosenList.value = parsedData
      totalDosen.value = parsedData.length
      isExcelMode.value = true
      sessionStorage.setItem('siredo_excel_dosen_cache', JSON.stringify(parsedData))
      return parsedData
    } catch (err) {
      error.value = 'Gagal membaca file Excel dataset'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const clearExcelMode = () => {
    isExcelMode.value = false
    sessionStorage.removeItem('siredo_excel_dosen_cache')
    fetchStatus()
  }

  return {
    isOnline,
    isCacheReady,
    isExcelMode,
    totalDosen,
    dosenList,
    isLoading,
    error,
    fetchStatus,
    fetchDosenList,
    loadExcelDataset,
    clearExcelMode
  }
})
