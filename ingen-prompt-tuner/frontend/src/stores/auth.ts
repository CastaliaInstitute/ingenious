import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import api from '@/services/api'

/**
 * Pinia store for authentication state management.
 * Handles user login, logout, and authentication status.
 */
export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('pt_token'))

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  /**
   * Authenticates a user with email and password credentials.
   * @param email - The user's email address.
   * @param password - The user's password.
   */
  async function login(email: string, password: string) {
    const response = await api.post<{ token: string; user: User }>('/auth/login', {
      email,
      password,
    })
    token.value = response.data.token
    user.value = response.data.user
    localStorage.setItem('pt_token', response.data.token)
  }

  /**
   * Logs out the current user by clearing token and user data.
   */
  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('pt_token')
  }

  /**
   * Validates the current authentication token and retrieves user data.
   * Logs out automatically if the token is invalid.
   */
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
