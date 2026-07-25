import { createRouter, createWebHistory } from 'vue-router'

import RecommendationView from '../views/RecommendationView.vue'
import DosenProfileView from '../views/DosenProfileView.vue'

import AdminDosenView from '../views/AdminDosenView.vue'
import RiwayatRekomendasiView from '../views/RiwayatRekomendasiView.vue'

const routes = [
  {
    path: '/',
    name: 'Recommendation',
    component: RecommendationView
  },
  {
    path: '/dosen',
    name: 'DosenProfile',
    component: DosenProfileView
  },
  {
    path: '/admin/dosen',
    name: 'AdminDosen',
    component: AdminDosenView
  },
  {
    path: '/admin/riwayat',
    name: 'AdminRiwayat',
    component: RiwayatRekomendasiView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router