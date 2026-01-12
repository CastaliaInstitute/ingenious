import axios from 'axios'

/**
 * Pre-configured Axios instance for API communication.
 * Includes base URL configuration and JSON content type header.
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('pt_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only clear token and reload for authenticated requests (not login)
      const isLoginRequest = error.config?.url?.includes('/auth/login')
      if (!isLoginRequest && localStorage.getItem('pt_token')) {
        localStorage.removeItem('pt_token')
        window.location.reload()
      }
    }
    return Promise.reject(error)
  }
)

export default api
