import axios from 'axios'

const api = axios.create({
  baseURL: '/api', // Using Vite proxy
  headers: {
    'Content-Type': 'application/json'
  }
})

export default api
