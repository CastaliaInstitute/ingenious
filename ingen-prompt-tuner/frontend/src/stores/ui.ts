import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TabName } from '@/types'

/**
 * Pinia store for UI state management.
 * Manages active tab navigation and expanded agent details.
 */
export const useUIStore = defineStore('ui', () => {
  const activeTab = ref<TabName>('home')
  const expandedAgent = ref<{ traceId: string; agentName: string } | null>(null)

  /**
   * Sets the currently active tab in the navigation.
   * @param tab - The tab name to activate.
   */
  function setActiveTab(tab: TabName) {
    activeTab.value = tab
  }

  /**
   * Toggles the expanded state of an agent in the trace view.
   * @param traceId - The trace identifier containing the agent.
   * @param agentName - The name of the agent to toggle.
   */
  function toggleAgent(traceId: string, agentName: string) {
    if (expandedAgent.value?.traceId === traceId && expandedAgent.value?.agentName === agentName) {
      expandedAgent.value = null
    } else {
      expandedAgent.value = { traceId, agentName }
    }
  }

  return {
    activeTab,
    expandedAgent,
    setActiveTab,
    toggleAgent,
  }
})
