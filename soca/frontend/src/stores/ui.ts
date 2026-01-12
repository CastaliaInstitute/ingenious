import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TabName } from '@/types'

/**
 * Pinia store for UI state management.
 * Manages active tab, expanded results, and evaluation selection.
 */
export const useUIStore = defineStore('ui', () => {
  const activeTab = ref<TabName>('evaluations')
  const expandedResultId = ref<string | null>(null)
  const selectedEvaluationId = ref<string | null>(null)

  /**
   * Sets the currently active tab in the navigation.
   * @param tab - The tab name to activate.
   */
  function setActiveTab(tab: TabName) {
    activeTab.value = tab
    selectedEvaluationId.value = null
  }

  /**
   * Navigates to view results for a specific evaluation.
   * @param evaluationId - The evaluation identifier to view.
   */
  function viewEvaluationResults(evaluationId: string) {
    selectedEvaluationId.value = evaluationId
  }

  /**
   * Returns to the main evaluations list view.
   */
  function backToEvaluations() {
    selectedEvaluationId.value = null
    expandedResultId.value = null
  }

  /**
   * Toggles the expanded state of a result card.
   * @param resultId - The result identifier to toggle.
   */
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
