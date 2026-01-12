import api from './api'
import type { Evaluation } from '@/types'

/**
 * Service for managing document evaluations.
 * Provides CRUD operations, execution, and export functionality.
 */
export const evaluationsService = {
  /**
   * Retrieves all evaluations.
   * @returns Array of evaluation objects.
   */
  async list(): Promise<Evaluation[]> {
    const response = await api.get<Evaluation[]>('/evaluations')
    return response.data
  },

  /**
   * Retrieves a specific evaluation by ID.
   * @param id - The evaluation identifier.
   * @returns The evaluation object.
   */
  async get(id: string): Promise<Evaluation> {
    const response = await api.get<Evaluation>(`/evaluations/${id}`)
    return response.data
  },

  /**
   * Creates a new evaluation.
   * @param data - The evaluation configuration.
   * @param data.name - The name for the evaluation.
   * @param data.submissionIds - Array of submission IDs to evaluate.
   * @param data.criteriaSetId - The criteria set ID to use for evaluation.
   * @returns The created evaluation object.
   */
  async create(data: {
    name: string
    submissionIds: string[]
    criteriaSetId: string
  }): Promise<Evaluation> {
    const response = await api.post<Evaluation>('/evaluations', data)
    return response.data
  },

  /**
   * Executes an evaluation to score submissions against criteria.
   * @param id - The evaluation identifier to run.
   * @returns The updated evaluation object with results.
   */
  async run(id: string): Promise<Evaluation> {
    const response = await api.post<Evaluation>(`/evaluations/${id}/run`)
    return response.data
  },

  /**
   * Exports evaluation results in the specified format.
   * @param id - The evaluation identifier.
   * @param format - The export format (pdf, csv, or json).
   * @returns The exported data as a Blob.
   */
  async exportData(id: string, format: 'pdf' | 'csv' | 'json'): Promise<Blob> {
    const response = await api.get(`/evaluations/${id}/export/${format}`, {
      responseType: 'blob',
    })
    return response.data
  },

  /**
   * Deletes an evaluation.
   * @param id - The evaluation identifier to delete.
   */
  async delete(id: string): Promise<void> {
    await api.delete(`/evaluations/${id}`)
  },
}
