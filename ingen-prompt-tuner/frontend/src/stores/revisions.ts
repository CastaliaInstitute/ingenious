import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Revision, Prompt } from '@/types'
import { promptsService } from '@/services/prompts.service'
import api from '@/services/api'

export const useRevisionsStore = defineStore('revisions', () => {
  const revisions = ref<Revision[]>([])
  const activeRevision = ref<string>('')
  const prompts = ref<Prompt[]>([])
  const loading = ref(false)

  async function fetchRevisions() {
    try {
      const response = await api.get('/revisions')
      revisions.value = response.data
      // Set active revision to first one if not already set
      if (!activeRevision.value && revisions.value.length > 0) {
        activeRevision.value = revisions.value[0].name
        await fetchPrompts()
      }
    } catch (error) {
      console.error('Failed to fetch revisions:', error)
    }
  }

  async function fetchPrompts() {
    if (!activeRevision.value) return

    loading.value = true
    try {
      prompts.value = await promptsService.list(activeRevision.value)
    } finally {
      loading.value = false
    }
  }

  function setActiveRevision(revisionId: string) {
    activeRevision.value = revisionId
    fetchPrompts()
  }

  async function createRevision(name: string, copyFrom?: string) {
    try {
      const response = await api.post('/revisions', {
        name,
        copyFrom: copyFrom || null,
      })
      const revision: Revision = response.data
      revisions.value.unshift(revision)
      // Switch to the new revision
      setActiveRevision(name)
      return revision
    } catch (error) {
      console.error('Failed to create revision:', error)
      throw error
    }
  }

  return {
    revisions,
    activeRevision,
    prompts,
    loading,
    fetchRevisions,
    fetchPrompts,
    setActiveRevision,
    createRevision,
  }
})
