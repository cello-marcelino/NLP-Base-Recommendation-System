import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // <--- Memanggil peta jalan yang baru dibuat

const app = createApp(App)
app.use(router) // <--- Memasang pengatur rute ke dalam aplikasi
app.mount('#app')