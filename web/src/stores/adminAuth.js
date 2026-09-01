import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAdminAuthStore = defineStore('adminAuth', () => {
  const token = ref(localStorage.getItem('siredo_admin_token') || '')
  const admin = ref(JSON.parse(localStorage.getItem('siredo_admin_profile') || 'null'))
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (username, password) => {
    isLoading.value = true
    error.value = null
    try {
      const res = await api.post('/admin/auth/login', { username, password })
      const data = res.data.data
      token.value = data.token
      admin.value = data.admin
      
      localStorage.setItem('siredo_admin_token', data.token)
      localStorage.setItem('siredo_admin_profile', JSON.stringify(data.admin))
      return data
    } catch (err) {
      error.value = err.userMessage || 'Login admin gagal'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchMe = async () => {
    if (!token.value) return null
    try {
      const res = await api.get('/admin/auth/me', {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      admin.value = res.data.data
      localStorage.setItem('siredo_admin_profile', JSON.stringify(res.data.data))
      return res.data.data
    } catch (err) {
      logout()
      return null
    }
  }

  const logout = () => {
    token.value = ''
    admin.value = null
    localStorage.removeItem('siredo_admin_token')
    localStorage.removeItem('siredo_admin_profile')
  }

  return {
    token,
    admin,
    isLoading,
    error,
    isAuthenticated,
    login,
    fetchMe,
    logout
  }
})
