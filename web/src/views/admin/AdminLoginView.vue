<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminAuthStore } from '../../stores/adminAuth'

const router = useRouter()
const adminAuth = useAdminAuthStore()

const username = ref('admin')
const password = ref('')
const showPassword = ref(false)
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
          <div class="password-input-wrapper">
            <input 
              id="password"
              :type="showPassword ? 'text' : 'password'" 
              v-model="password" 
              placeholder="Masukkan password..." 
              required
              autocomplete="current-password"
            />
            <button 
              type="button" 
              class="password-toggle-btn"
              @click="showPassword = !showPassword"
              :title="showPassword ? 'Sembunyikan password' : 'Lihat password'"
              :aria-label="showPassword ? 'Sembunyikan password' : 'Lihat password'"
            >
              <!-- Eye Off (Slash) Icon -->
              <svg v-if="showPassword" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
              <!-- Eye Open Icon -->
              <svg v-else width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
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

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.password-input-wrapper input {
  width: 100%;
  padding-right: 2.5rem;
}
.password-toggle-btn {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.35rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}
.password-toggle-btn:hover {
  color: #0f766e;
  background: #f1f5f9;
}
.password-toggle-btn:focus {
  outline: none;
  color: #0d9488;
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
