import { createRouter, createWebHistory } from 'vue-router'

import HalamanRekomendasiSingle from '../views/HalamanRekomendasi-single.vue'
import HalamanRekomendasiBatch from '../views/HalamanRekomendasi-batch.vue'
import HalamanDosen from '../views/HalamanDosen.vue'

const routes = [
  {
    path: '/',
    name: 'RekomendasiSingle',
    component: HalamanRekomendasiSingle
  },
  {
    path: '/batch',
    name: 'RekomendasiBatch',
    component: HalamanRekomendasiBatch
  },
  {
    path: '/dosen',
    name: 'DaftarDosen',
    component: HalamanDosen
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router