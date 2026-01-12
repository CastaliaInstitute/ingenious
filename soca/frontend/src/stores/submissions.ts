import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Submission } from '@/types'
import { submissionsService } from '@/services/submissions.service'

/**
 * Pinia store for managing document submissions.
 * Handles upload, listing, update, and deletion operations.
 */
export const useSubmissionsStore = defineStore('submissions', () => {
  const submissions = ref<Submission[]>([])
  const loading = ref(false)
  const uploadProgress = ref<number | null>(null)
  const error = ref<string | null>(null)

  /**
   * Fetches all submissions from the API.
   */
  async function fetchSubmissions() {
    loading.value = true
    error.value = null
    try {
      submissions.value = await submissionsService.list()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch submissions'
    } finally {
      loading.value = false
    }
  }

  /**
   * Uploads a new document submission with progress tracking.
   * @param file - The document file to upload.
   * @param name - Optional name for the submission.
   * @param description - Optional description for the submission.
   * @returns The created submission.
   */
  async function uploadSubmission(file: File, name?: string, description?: string) {
    uploadProgress.value = 0
    try {
      const submission = await submissionsService.upload(file, name, description, (progress) => {
        uploadProgress.value = progress
      })
      submissions.value.unshift(submission)
      return submission
    } finally {
      uploadProgress.value = null
    }
  }

  /**
   * Deletes a submission.
   * @param id - The submission identifier to delete.
   */
  async function deleteSubmission(id: string) {
    await submissionsService.delete(id)
    submissions.value = submissions.value.filter((s) => s.id !== id)
  }

  /**
   * Updates a submission's metadata.
   * @param id - The submission identifier.
   * @param data - The fields to update.
   * @param data.name - Optional new name for the submission.
   * @param data.description - Optional new description for the submission.
   * @returns The updated submission.
   */
  async function updateSubmission(id: string, data: { name?: string; description?: string }) {
    const updated = await submissionsService.update(id, data)
    const index = submissions.value.findIndex((s) => s.id === id)
    if (index !== -1) {
      // eslint-disable-next-line security/detect-object-injection -- index is a validated numeric array index from findIndex
      submissions.value[index] = updated
    }
    return updated
  }

  /**
   * Retrieves a submission by ID from the local store.
   * @param id - The submission identifier.
   * @returns The submission if found.
   */
  function getSubmission(id: string) {
    return submissions.value.find((s) => s.id === id)
  }

  return {
    submissions,
    loading,
    uploadProgress,
    error,
    fetchSubmissions,
    uploadSubmission,
    deleteSubmission,
    updateSubmission,
    getSubmission,
  }
})
