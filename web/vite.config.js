import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const port = parseInt(env.VITE_PORT || '5173', 10)
  const target = env.VITE_DEV_API_TARGET || 'http://localhost:5000'

  return {
    plugins: [vue(), tailwindcss()],
    server: {
      port: port,
      proxy: {
        '/api': {
          target: target,
          changeOrigin: true
        },
        '/health': {
          target: target,
          changeOrigin: true
        }
      }
    }
  }
})
