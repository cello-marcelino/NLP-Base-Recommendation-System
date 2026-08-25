import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useRecommendationStore = defineStore('recommendation', () => {
  // Single Recommendation State
  const judul = ref('')
  const abstrak = ref('')
  const kRank = ref(5)
  const isProcessing = ref(false)
  const error = ref(null)
  
  const recommendations = ref([])
  const metadata = ref(null)
  const pipeline = ref(null)
  const selectedDosenXai = ref(null)

  const steps = ref([
    { title: 'Preprocessing Teks', desc: 'Case folding, stopword removal, N-Gram', status: 'idle', open: false },
    { title: 'Ekspansi Sinonim', desc: 'Penambahan sinonim via kamus ontologi', status: 'idle', open: false },
    { title: 'Lexical Scoring (BM25)', desc: 'TF-IDF + Z-Score Sigmoid normalization', status: 'idle', open: false },
    { title: 'Semantic Scoring (SBERT)', desc: 'Cosine Similarity pada embedding vektor', status: 'idle', open: false },
    { title: 'Hybrid Ranking & XAI', desc: 'Adaptive α·BM25 + β·SBERT aggregation', status: 'idle', open: false }
  ])

  // Batch State
  const batchProposals = ref([])
  const batchResults = ref([])
  const batchMeta = ref(null)
  const isBatchProcessing = ref(false)
  const batchError = ref(null)

  const resetSingle = () => {
    recommendations.value = []
    metadata.value = null
    pipeline.value = null
    error.value = null
    steps.value.forEach(s => { s.status = 'idle'; s.open = false })
  }

  const executeSingleRecommendation = async () => {
    if (!judul.value.trim() && !abstrak.value.trim()) {
      error.value = 'Isi minimal judul atau abstrak penelitian'
      return
    }
    
    error.value = null
    isProcessing.value = true
    resetSingle()

    // Stepper visual animation
    let currentStep = 0
    steps.value[currentStep].status = 'running'
    steps.value[currentStep].open = true

    const interval = setInterval(() => {
      if (currentStep < steps.value.length - 1) {
        steps.value[currentStep].status = 'done'
        steps.value[currentStep].open = false
        currentStep++
        steps.value[currentStep].status = 'running'
        steps.value[currentStep].open = true
      }
    }, 500)

    try {
      const res = await api.post('/recommendations', {
        judul: judul.value,
        abstrak: abstrak.value,
        k_rank: kRank.value || null
      })
      
      clearInterval(interval)
      steps.value.forEach(s => { s.status = 'done'; s.open = false })
      
      const payload = res.data.data
      recommendations.value = payload.recommendations || []
      metadata.value = payload.metadata || null
      pipeline.value = payload.pipeline || null
    } catch (err) {
      clearInterval(interval)
      steps.value[currentStep].status = 'error'
      error.value = err.userMessage || 'Gagal memproses rekomendasi'
    } finally {
      isProcessing.value = false
    }
  }

  const executeBatch = async (proposalsList, customKRank) => {
    isBatchProcessing.value = true
    batchError.value = null
    batchResults.value = []
    try {
      const res = await api.post('/recommendations/batch', {
        proposals: proposalsList,
        k_rank: customKRank || null
      })
      batchResults.value = res.data.data || []
      batchMeta.value = res.data.meta || null
      return batchResults.value
    } catch (err) {
      batchError.value = err.userMessage || 'Gagal memproses batch rekomendasi'
      throw err
    } finally {
      isBatchProcessing.value = false
    }
  }

  const uploadExcelBatch = async (formData) => {
    isBatchProcessing.value = true
    batchError.value = null
    batchResults.value = []
    try {
      const res = await api.post('/recommendations/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      batchResults.value = res.data.data || []
      batchMeta.value = res.data.meta || null
      return batchResults.value
    } catch (err) {
      batchError.value = err.userMessage || 'Gagal memproses file Excel batch'
      throw err
    } finally {
      isBatchProcessing.value = false
    }
  }

  return {
    judul,
    abstrak,
    kRank,
    isProcessing,
    error,
    steps,
    recommendations,
    metadata,
    pipeline,
    selectedDosenXai,
    batchProposals,
    batchResults,
    batchMeta,
    isBatchProcessing,
    batchError,
    resetSingle,
    executeSingleRecommendation,
    executeBatch,
    uploadExcelBatch
  }
})
