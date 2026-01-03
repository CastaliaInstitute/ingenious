import api from './api'
import type { Evaluation } from '@/types'

export const evaluationsService = {
  async list(): Promise<Evaluation[]> {
    const response = await api.get<Evaluation[]>('/evaluations')
    return response.data
  },

  async get(id: string): Promise<Evaluation> {
    const response = await api.get<Evaluation>(`/evaluations/${id}`)
    return response.data
  },

  async create(data: {
    name: string
    submissionIds: string[]
    criteriaSetId: string
  }): Promise<Evaluation> {
    const response = await api.post<Evaluation>('/evaluations', data)
    return response.data
  },

  async run(id: string): Promise<Evaluation> {
    const response = await api.post<Evaluation>(`/evaluations/${id}/run`)
    return response.data
  },

  async exportData(id: string, format: 'pdf' | 'csv' | 'json'): Promise<Blob> {
    const response = await api.get(`/evaluations/${id}/export/${format}`, {
      responseType: 'blob',
    })
    return response.data
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/evaluations/${id}`)
  },
}
