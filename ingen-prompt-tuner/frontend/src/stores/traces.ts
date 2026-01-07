import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ConversationTrace } from '@/types'
import { tracesService } from '@/services/traces.service'

export const useTracesStore = defineStore('traces', () => {
  const traces = ref<ConversationTrace[]>([])
  const loading = ref(false)

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
