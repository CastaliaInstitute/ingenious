import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('pt_token'))

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  async function login(email: string, password: string) {
    const response = await api.post<{ token: string; user: User }>('/auth/login', {
      email,
      password,
    })
    token.value = response.data.token
    user.value = response.data.user
    localStorage.setItem('pt_token', response.data.token)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('pt_token')
  }

  async function checkAuth() {
    if (token.value) {
      try {
        const response = await api.get<{ user: User }>('/auth/me')
        user.value = response.data.user
      } catch {
        logout()
      }
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout,
    checkAuth,
  }
})
