import { createRouter, createWebHistory } from 'vue-router'
import HalamanRekomendasi from '../views/HalamanRekomendasi.vue'
import HalamanDosen from '../views/HalamanDosen.vue'

// Rute aplikasi
const routes = [
  {
    path: '/',
    name: 'Rekomendasi',
    component: HalamanRekomendasi
  },
  {
    path: '/dosen',
    name: 'DaftarDosen',
    component: HalamanDosen
  }
]

// Router Vue
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
