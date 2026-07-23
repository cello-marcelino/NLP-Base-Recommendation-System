import { createRouter, createWebHistory } from 'vue-router'

import HalamanRekomendasiSingle from '../views/HalamanRekomendasi-single.vue'
import HalamanRekomendasiBatch from '../views/HalamanRekomendasi-batch.vue'
import HalamanDosen from '../views/HalamanDosen.vue'
import AdminDosen from '../views/AdminDosen.vue'
import RiwayatRekomendasi from '../views/RiwayatRekomendasi.vue';

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
  },
  {
    path: '/admin/dosen',
    name: 'AdminDosen',
    component: AdminDosen,
    // Nantinya Anda bisa menambahkan meta: { requiresAuth: true } di sini
  },
  {
    path: '/admin/riwayat',
    name: 'RiwayatRekomendasi',
    component: RiwayatRekomendasi,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router