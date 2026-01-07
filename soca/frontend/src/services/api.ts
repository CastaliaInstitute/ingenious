import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('soca_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const hadToken = localStorage.getItem('soca_token')
      localStorage.removeItem('soca_token')
      // Only reload if user was authenticated (not during login)
      if (hadToken) {
        window.location.reload()
      }
    }
    return Promise.reject(error)
  }
)

export default api
