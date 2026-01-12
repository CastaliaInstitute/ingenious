import api from './api'
import type { CriteriaSet } from '@/types'

/**
 * Service for managing evaluation criteria sets.
 * Provides CRUD operations and AI-powered criteria generation.
 */
export const criteriaService = {
  /**
   * Retrieves all user-created criteria sets.
   * @returns Array of criteria set objects.
   */
  async list(): Promise<CriteriaSet[]> {
    const response = await api.get<CriteriaSet[]>('/criteria-sets')
    return response.data
  },

  /**
   * Retrieves all predefined criteria templates.
   * @returns Array of template criteria set objects.
   */
  async listTemplates(): Promise<CriteriaSet[]> {
    const response = await api.get<CriteriaSet[]>('/criteria-templates')
    return response.data
  },

  /**
   * Creates a new criteria set.
   * @param data - The criteria set data without id and createdAt.
   * @returns The created criteria set object.
   */
  async create(data: Omit<CriteriaSet, 'id' | 'createdAt'>): Promise<CriteriaSet> {
    const response = await api.post<CriteriaSet>('/criteria-sets', data)
    return response.data
  },

  /**
   * Updates an existing criteria set.
   * @param id - The criteria set identifier.
   * @param data - The updated criteria set data.
   * @returns The updated criteria set object.
   */
  async update(id: string, data: Omit<CriteriaSet, 'id' | 'createdAt'>): Promise<CriteriaSet> {
    const response = await api.patch<CriteriaSet>(`/criteria-sets/${id}`, data)
    return response.data
  },

  /**
   * Deletes a criteria set.
   * @param id - The criteria set identifier to delete.
   */
  async delete(id: string): Promise<void> {
    await api.delete(`/criteria-sets/${id}`)
  },

  /**
   * Generates criteria from an uploaded document using AI.
   * @param file - The document file to analyze.
   * @param name - The name for the generated criteria set.
   * @returns The generated criteria set object.
   */
  async generateFromDocument(file: File, name: string): Promise<CriteriaSet> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('name', name)

    const response = await api.post<CriteriaSet>('/criteria-sets/generate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  /**
   * Generates criteria from text content using AI.
   * @param text - The document text to analyze.
   * @param name - The name for the generated criteria set.
   * @returns The generated criteria set object.
   */
  async generateFromText(text: string, name: string): Promise<CriteriaSet> {
    const formData = new FormData()
    formData.append('document_text', text)
    formData.append('name', name)

    const response = await api.post<CriteriaSet>('/criteria-sets/generate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}
