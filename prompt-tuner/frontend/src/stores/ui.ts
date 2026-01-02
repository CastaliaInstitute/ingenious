import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TabName } from '@/types'

export const useUIStore = defineStore('ui', () => {
  const activeTab = ref<TabName>('home')
  const expandedAgent = ref<{ traceId: string; agentName: string } | null>(null)

  function setActiveTab(tab: TabName) {
    activeTab.value = tab
  }

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
    toggleAgent
  }
})
