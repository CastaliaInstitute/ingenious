import api from './api'
import type { Prompt } from '@/types'

/**
 * Service for managing prompt templates.
 * Provides CRUD operations for prompts within revisions.
 */
export const promptsService = {
  /**
   * Retrieves all prompts for a specific revision.
   * @param revision - The revision identifier to fetch prompts from.
   * @returns Array of prompt objects for the revision.
   */
  async list(revision: string): Promise<Prompt[]> {
    const response = await api.get(`/prompts/${revision}`)
    return response.data
  },

  /**
   * Retrieves a specific prompt by revision and filename.
   * @param revision - The revision identifier.
   * @param filename - The prompt filename to retrieve.
   * @returns The prompt object if found, null otherwise.
   */
  async get(revision: string, filename: string): Promise<Prompt | null> {
    try {
      const response = await api.get(`/prompts/${revision}/${filename}`)
      return response.data
    } catch {
      return null
    }
  },

  /**
   * Updates the content of a specific prompt.
   * @param revision - The revision identifier.
   * @param filename - The prompt filename to update.
   * @param content - The new content for the prompt.
   */
  async update(revision: string, filename: string, content: string): Promise<void> {
    await api.put(`/prompts/${revision}/${filename}`, { content })
  },
}
