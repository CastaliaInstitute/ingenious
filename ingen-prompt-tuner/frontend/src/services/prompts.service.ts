import api from './api'
import type { Prompt } from '@/types'

export const promptsService = {
  async list(revision: string): Promise<Prompt[]> {
    const response = await api.get(`/prompts/${revision}`)
    return response.data
  },

  async get(revision: string, filename: string): Promise<Prompt | null> {
    try {
      const response = await api.get(`/prompts/${revision}/${filename}`)
      return response.data
    } catch {
      return null
    }
  },

  async update(revision: string, filename: string, content: string): Promise<void> {
    await api.put(`/prompts/${revision}/${filename}`, { content })
  },
}
