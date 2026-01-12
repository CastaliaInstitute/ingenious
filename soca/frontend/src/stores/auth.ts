import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { authService } from '@/services/auth.service'

/**
 * Pinia store for authentication state management.
 * Handles user login, logout, and authentication status.
 */
export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('soca_token'))

  const isAuthenticated = computed(() => !!token.value)

  /**
   * Authenticates a user with email and password credentials.
   * @param email - The user's email address.
   * @param password - The user's password.
   */
  async function login(email: string, password: string) {
    const response = await authService.login(email, password)
    token.value = response.token
    user.value = response.user
    localStorage.setItem('soca_token', response.token)
  }

  /**
   * Logs out the current user by clearing token and user data.
   */
  async function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('soca_token')
  }

  /**
   * Validates the current authentication token and retrieves user data.
   * Logs out automatically if the token is invalid.
   */
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
    checkAuth,
  }
})
