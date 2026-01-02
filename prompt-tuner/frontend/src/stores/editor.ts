import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Prompt } from '@/types'

export const useEditorStore = defineStore('editor', () => {
  const selectedPrompt = ref<Prompt | null>(null)
  const modifiedContent = ref<string | null>(null)

  const hasChanges = computed(() => {
    if (!selectedPrompt.value || modifiedContent.value === null) return false
    return modifiedContent.value !== selectedPrompt.value.content
  })

  function selectPrompt(prompt: Prompt) {
    selectedPrompt.value = prompt
    modifiedContent.value = prompt.content
  }

  function updateContent(content: string) {
    modifiedContent.value = content
  }

  function discardChanges() {
    if (selectedPrompt.value) {
      modifiedContent.value = selectedPrompt.value.content
    }
  }

  function clearSelection() {
    selectedPrompt.value = null
    modifiedContent.value = null
  }

  return {
    selectedPrompt,
    modifiedContent,
    hasChanges,
    selectPrompt,
    updateContent,
    discardChanges,
    clearSelection
  }
})
