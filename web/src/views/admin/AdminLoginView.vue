<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminAuthStore } from '../../stores/adminAuth'

const router = useRouter()
const adminAuth = useAdminAuthStore()

const username = ref('admin')
const password = ref('')
const isSubmitting = ref(false)

const handleLogin = async () => {
  if (!username.value || !password.value) return
  isSubmitting.value = true
  try {
    await adminAuth.login(username.value, password.value)
    router.push('/admin/dashboard')
  } catch (err) {
    // Error is set in store
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="admin-login-page">
    <div class="login-box">
      <div class="login-header">
        <div class="brand-badge">SiReDo Admin</div>
        <h1>Portal Pengelola Systems</h1>
        <p>Masuk menggunakan kredensial administrator untuk mengelola data dosen & engine NLP.</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="adminAuth.error" class="error-alert">
          <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ adminAuth.error }}</span>
        </div>

        <div class="form-group">
          <label for="username">Username Admin</label>
          <input 
            id="username"
            type="text" 
            v-model="username" 
            placeholder="Masukkan username..." 
            required
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password"
            type="password" 
            v-model="password" 
            placeholder="Masukkan password..." 
            required
            autocomplete="current-password"
          />
        </div>

        <button type="submit" :disabled="isSubmitting" class="btn-submit">
          <span v-if="!isSubmitting">Masuk Ke Dashboard</span>
          <span v-else>Memverifikasi...</span>
        </button>
      </form>

      <div class="login-footer">
        <router-link to="/" class="back-link">← Kembali ke Portal Publik</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  background: #022c22; /* Very deep Teal */
  padding: 1.5rem;
}
.login-box {
  width: 100%; max-width: 420px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
  padding: 2.25rem;
}
.login-header { text-align: center; margin-bottom: 1.75rem; }
.brand-badge {
  display: inline-block; font-size: 0.7rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
  background: #ccfbf1; color: #0f766e;
  padding: 3px 10px; border-radius: 99px; margin-bottom: 0.75rem;
}
.login-header h1 { font-size: 1.5rem; font-weight: 700; color: #0f172a; margin: 0 0 0.4rem; }
.login-header p { font-size: 0.83rem; color: #64748b; line-height: 1.5; margin: 0; }

.login-form { display: flex; flex-direction: column; gap: 1.25rem; }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-group label { font-size: 0.8rem; font-weight: 600; color: #334155; }
.form-group input {
  padding: 0.65rem 0.85rem; font-size: 0.9rem;
  border: 1px solid #cbd5e1; border-radius: 6px;
  background: #f8fafc; color: #0f172a; transition: all 0.15s;
}
.form-group input:focus {
  outline: none; border-color: #0d9488; background: #ffffff;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15);
}

.error-alert {
  display: flex; align-items: center; gap: 0.5rem;
  background: #fef2f2; border: 1px solid #fca5a5; color: #991b1b;
  padding: 0.6rem 0.85rem; border-radius: 6px; font-size: 0.8rem;
}

.btn-submit {
  background: #0d9488; color: white;
  padding: 0.75rem; font-size: 0.9rem; font-weight: 600;
  border: none; border-radius: 6px; cursor: pointer;
  transition: background 0.15s; margin-top: 0.5rem;
}
.btn-submit:hover:not(:disabled) { background: #0f766e; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.login-footer { margin-top: 1.5rem; text-align: center; }
.back-link { font-size: 0.8rem; color: #0d9488; text-decoration: none; font-weight: 500; }
.back-link:hover { text-decoration: underline; }
</style>
