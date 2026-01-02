import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('pt_token'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    // For demo, accept any login
    token.value = 'demo-token'
    user.value = { id: 'demo', email }
    localStorage.setItem('pt_token', 'demo-token')
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('pt_token')
  }

  function checkAuth() {
    if (token.value) {
      user.value = { id: 'demo', email: 'admin@insight.com' }
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    checkAuth
  }
})
