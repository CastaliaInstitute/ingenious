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

  // Extract Jinja2 variables from content dynamically
  const extractedVariables = computed(() => {
    if (!modifiedContent.value) return []

    // Match {{ variable }}, {{ variable.property }}, and similar patterns
    const variablePattern = /\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s*(?:\|[^}]*)?\}\}/g
    const matches = modifiedContent.value.matchAll(variablePattern)

    const variables = new Set<string>()
    for (const match of matches) {
      // Get the base variable name (first part before any dot)
      const baseVar = match[1].split('.')[0]
      variables.add(baseVar)
    }

    // Also extract loop variables from {% for x in y %}
    const forPattern = /\{%\s*for\s+\w+\s+in\s+([a-zA-Z_][a-zA-Z0-9_]*)/g
    const forMatches = modifiedContent.value.matchAll(forPattern)
    for (const match of forMatches) {
      variables.add(match[1])
    }

    return Array.from(variables).sort()
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
    extractedVariables,
    selectPrompt,
    updateContent,
    discardChanges,
    clearSelection
  }
})
