import api from './api'
import type { User } from '@/types'

interface LoginResponse {
  token: string
  user: User
}

interface MeResponse {
  user: User
}

/**
 * Service for authentication operations.
 * Handles login and current user retrieval.
 */
export const authService = {
  /**
   * Authenticates a user with email and password.
   * @param email - The user's email address.
   * @param password - The user's password.
   * @returns The login response containing token and user data.
   */
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login', { email, password })
    return response.data
  },

  /**
   * Retrieves the current authenticated user's information.
   * @returns The current user data.
   */
  async me(): Promise<MeResponse> {
    const response = await api.get<MeResponse>('/auth/me')
    return response.data
  },
}
