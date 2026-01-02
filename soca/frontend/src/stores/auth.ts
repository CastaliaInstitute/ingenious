import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { authService } from '@/services/auth.service'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('soca_token'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    const response = await authService.login(email, password)
    token.value = response.token
    user.value = response.user
    localStorage.setItem('soca_token', response.token)
  }

  async function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('soca_token')
  }

  async function checkAuth() {
    if (token.value) {
      try {
        const response = await authService.me()
        user.value = response.user
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
    checkAuth
  }
})
