import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Revision, Prompt } from '@/types'
import { promptsService } from '@/services/prompts.service'
import api from '@/services/api'

/**
 * Pinia store for managing prompt revisions.
 * Handles revision listing, creation, and associated prompts.
 */
export const useRevisionsStore = defineStore('revisions', () => {
  const revisions = ref<Revision[]>([])
  const activeRevision = ref<string>('')
  const prompts = ref<Prompt[]>([])
  const loading = ref(false)

  /**
   * Fetches all available revisions from the API.
   * Automatically sets the first revision as active if none is selected.
   */
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

  /**
   * Fetches all prompts for the currently active revision.
   */
  async function fetchPrompts() {
    if (!activeRevision.value) return

    loading.value = true
    try {
      prompts.value = await promptsService.list(activeRevision.value)
    } finally {
      loading.value = false
    }
  }

  /**
   * Sets the active revision and loads its prompts.
   * @param revisionId - The revision identifier to activate.
   */
  function setActiveRevision(revisionId: string) {
    activeRevision.value = revisionId
    fetchPrompts()
  }

  /**
   * Creates a new revision, optionally copying prompts from an existing one.
   * @param name - The name for the new revision.
   * @param copyFrom - Optional revision name to copy prompts from.
   * @returns The newly created revision object.
   */
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
