import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ConversationTrace } from '@/types'
import { tracesService } from '@/services/traces.service'

/**
 * Pinia store for managing conversation traces.
 * Provides state and actions for loading and displaying trace data.
 */
export const useTracesStore = defineStore('traces', () => {
  const traces = ref<ConversationTrace[]>([])
  const loading = ref(false)

  /**
   * Fetches conversation traces for a specific revision.
   * @param revision - The revision identifier to fetch traces for.
   */
  async function fetchTraces(revision: string) {
    loading.value = true
    try {
      traces.value = await tracesService.list(revision)
    } finally {
      loading.value = false
    }
  }

  return {
    traces,
    loading,
    fetchTraces,
  }
})
