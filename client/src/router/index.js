import { createRouter, createWebHistory } from 'vue-router'
import HalamanRekomendasi from '../views/HalamanRekomendasi.vue'
import HalamanDosen from '../views/HalamanDosen.vue'

// Membuat daftar rute (peta jalan)
const routes = [
  {
    path: '/',                 // Jika URL utamanya kosong (halaman awal)
    name: 'Rekomendasi',
    component: HalamanRekomendasi // Tampilkan komponen Halaman Rekomendasi
  },
  {
    path: '/dosen',            // Jika URL-nya ada tambahan "/dosen"
    name: 'DaftarDosen',
    component: HalamanDosen    // Tampilkan komponen Halaman Dosen
  }
]

// Menyalakan mesin pengatur rute
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router