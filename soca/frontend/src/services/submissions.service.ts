import api from './api'
import type { Submission } from '@/types'

/**
 * Service for managing document submissions.
 * Provides upload, listing, update, and deletion operations.
 */
export const submissionsService = {
  /**
   * Retrieves all submissions.
   * @returns Array of submission objects.
   */
  async list(): Promise<Submission[]> {
    const response = await api.get<Submission[]>('/submissions')
    return response.data
  },

  /**
   * Uploads a new document submission.
   * @param file - The document file to upload.
   * @param name - Optional name for the submission.
   * @param description - Optional description for the submission.
   * @param onProgress - Optional callback for upload progress updates.
   * @returns The created submission object.
   */
  async upload(
    file: File,
    name?: string,
    description?: string,
    onProgress?: (progress: number) => void
  ): Promise<Submission> {
    const formData = new FormData()
    formData.append('file', file)
    if (name) formData.append('name', name)
    if (description) formData.append('description', description)

    const response = await api.post<Submission>('/submissions', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (event) => {
        if (event.total && onProgress) {
          onProgress(Math.round((event.loaded * 100) / event.total))
        }
      },
    })
    return response.data
  },

  /**
   * Deletes a submission.
   * @param id - The submission identifier to delete.
   */
  async delete(id: string): Promise<void> {
    await api.delete(`/submissions/${id}`)
  },

  /**
   * Updates a submission's metadata.
   * @param id - The submission identifier.
   * @param data - The fields to update.
   * @param data.name - Optional new name for the submission.
   * @param data.description - Optional new description for the submission.
   * @returns The updated submission object.
   */
  async update(id: string, data: { name?: string; description?: string }): Promise<Submission> {
    const response = await api.patch<Submission>(`/submissions/${id}`, data)
    return response.data
  },
}
