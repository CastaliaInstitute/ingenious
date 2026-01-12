import api from './api'
import type { ConversationTrace } from '@/types'

/**
 * Service for managing conversation traces.
 * Provides methods to list and retrieve trace data from AI conversations.
 */
export const tracesService = {
  /**
   * Retrieves a list of conversation traces, optionally filtered by revision.
   * @param revision - Optional revision identifier to filter traces.
   * @returns Array of conversation trace objects, limited to 100 entries.
   */
  async list(revision?: string): Promise<ConversationTrace[]> {
    const params = new URLSearchParams()
    if (revision) {
      params.append('revision', revision)
    }
    params.append('limit', '100')

    const response = await api.get(`/traces?${params.toString()}`)
    return response.data
  },

  /**
   * Retrieves a specific conversation trace by its ID.
   * @param traceId - The unique identifier of the trace.
   * @returns The conversation trace object if found, null otherwise.
   */
  async get(traceId: string): Promise<ConversationTrace | null> {
    try {
      const response = await api.get(`/traces/${traceId}`)
      return response.data
    } catch {
      return null
    }
  },
}
