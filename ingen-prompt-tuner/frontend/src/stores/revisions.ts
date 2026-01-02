import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Revision, Prompt } from '@/types'
import { promptsService } from '@/services/prompts.service'

export const useRevisionsStore = defineStore('revisions', () => {
  const revisions = ref<Revision[]>([
    {
      id: 'quickstart-1',
      name: 'quickstart-1',
      createdAt: new Date().toISOString(),
      promptCount: 4,
    },
    {
      id: 'magical-crystal-51211a8b',
      name: 'magical-crystal-51211a8b',
      createdAt: new Date().toISOString(),
      promptCount: 4,
    },
    {
      id: 'production-v2',
      name: 'production-v2',
      createdAt: new Date().toISOString(),
      promptCount: 4,
    },
  ])
  const activeRevision = ref<string>('quickstart-1')
  const prompts = ref<Prompt[]>([])
  const loading = ref(false)

  async function fetchRevisions() {
    // In production, fetch from API
  }

  async function fetchPrompts() {
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

  async function createRevision(name: string) {
    const revision: Revision = {
      id: name,
      name,
      createdAt: new Date().toISOString(),
      promptCount: prompts.value.length,
    }
    revisions.value.unshift(revision)
    return revision
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
