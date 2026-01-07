import api from './api'
import type { User } from '@/types'

interface LoginResponse {
  token: string
  user: User
}

interface MeResponse {
  user: User
}

export const authService = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login', { email, password })
    return response.data
  },

  async me(): Promise<MeResponse> {
    const response = await api.get<MeResponse>('/auth/me')
    return response.data
  },
}
