import api from './api'
import type { CriteriaSet } from '@/types'

export const criteriaService = {
  async list(): Promise<CriteriaSet[]> {
    const response = await api.get<CriteriaSet[]>('/criteria-sets')
    return response.data
  },

  async listTemplates(): Promise<CriteriaSet[]> {
    const response = await api.get<CriteriaSet[]>('/criteria-templates')
    return response.data
  },

  async create(data: Omit<CriteriaSet, 'id' | 'createdAt'>): Promise<CriteriaSet> {
    const response = await api.post<CriteriaSet>('/criteria-sets', data)
    return response.data
  }
}
