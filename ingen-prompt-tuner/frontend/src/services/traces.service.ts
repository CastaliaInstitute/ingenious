import api from './api'
import type { ConversationTrace } from '@/types'

export const tracesService = {
  async list(revision?: string): Promise<ConversationTrace[]> {
    const params = new URLSearchParams()
    if (revision) {
      params.append('revision', revision)
    }
    params.append('limit', '50')

    const response = await api.get(`/traces?${params.toString()}`)
    return response.data
  },

  async get(traceId: string): Promise<ConversationTrace | null> {
    try {
      const response = await api.get(`/traces/${traceId}`)
      return response.data
    } catch {
      return null
    }
  },
}
