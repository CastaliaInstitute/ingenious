import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Submission } from '@/types'
import { submissionsService } from '@/services/submissions.service'

export const useSubmissionsStore = defineStore('submissions', () => {
  const submissions = ref<Submission[]>([])
  const loading = ref(false)
  const uploadProgress = ref<number | null>(null)
  const error = ref<string | null>(null)

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

  async function deleteSubmission(id: string) {
    await submissionsService.delete(id)
    submissions.value = submissions.value.filter((s) => s.id !== id)
  }

  async function updateSubmission(id: string, data: { name?: string; description?: string }) {
    const updated = await submissionsService.update(id, data)
    const index = submissions.value.findIndex((s) => s.id === id)
    if (index !== -1) {
      submissions.value[index] = updated
    }
    return updated
  }

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
