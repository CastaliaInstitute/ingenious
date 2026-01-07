import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TabName } from '@/types'

export const useUIStore = defineStore('ui', () => {
  const activeTab = ref<TabName>('evaluations')
  const expandedResultId = ref<string | null>(null)
  const selectedEvaluationId = ref<string | null>(null)

  function setActiveTab(tab: TabName) {
    activeTab.value = tab
    selectedEvaluationId.value = null
  }

  function viewEvaluationResults(evaluationId: string) {
    selectedEvaluationId.value = evaluationId
  }

  function backToEvaluations() {
    selectedEvaluationId.value = null
    expandedResultId.value = null
  }

  function toggleResultExpanded(resultId: string) {
    if (expandedResultId.value === resultId) {
      expandedResultId.value = null
    } else {
      expandedResultId.value = resultId
    }
  }

  return {
    activeTab,
    expandedResultId,
    selectedEvaluationId,
    setActiveTab,
    viewEvaluationResults,
    backToEvaluations,
    toggleResultExpanded,
  }
})
