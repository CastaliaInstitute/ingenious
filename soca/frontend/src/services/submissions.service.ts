import api from './api'
import type { Submission } from '@/types'

export const submissionsService = {
  async list(): Promise<Submission[]> {
    const response = await api.get<Submission[]>('/submissions')
    return response.data
  },

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

  async delete(id: string): Promise<void> {
    await api.delete(`/submissions/${id}`)
  },

  async update(id: string, data: { name?: string; description?: string }): Promise<Submission> {
    const response = await api.patch<Submission>(`/submissions/${id}`, data)
    return response.data
  },
}
