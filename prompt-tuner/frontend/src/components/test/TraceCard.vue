<script setup lang="ts">
import { computed } from 'vue'
import { useUIStore } from '@/stores/ui'
import type { ConversationTrace, AgentTrace } from '@/types'

const props = defineProps<{
  trace: ConversationTrace
}>()

const uiStore = useUIStore()

const expandedAgent = computed(() => {
  if (uiStore.expandedAgent?.traceId !== props.trace.traceId) return null
  return props.trace.agents.find(a => a.agentName === uiStore.expandedAgent?.agentName)
})

function formatTime(timestamp: string): string {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(minutes / 60)

  if (hours > 0) {
    return `${hours} hour${hours > 1 ? 's' : ''} ago`
  } else if (minutes > 0) {
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
  }
  return 'Just now'
}

function formatTokens(tokens: number): string {
  if (tokens >= 1000) {
    return `${(tokens / 1000).toFixed(1)}k tokens`
  }
  return `${tokens} tokens`
}

function isAgentActive(agentName: string): boolean {
  return uiStore.expandedAgent?.traceId === props.trace.traceId &&
         uiStore.expandedAgent?.agentName === agentName
}

function toggleAgent(agentName: string) {
  uiStore.toggleAgent(props.trace.traceId, agentName)
}
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <div class="flex items-start justify-between">
      <div>
        <p class="text-sm font-medium text-mine mb-1">{{ trace.userQuery }}</p>
        <p class="text-xs text-taupe">
          {{ trace.workflow }} &middot; {{ formatTime(trace.timestamp) }} &middot; {{ formatTokens(trace.totalTokens) }}
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button
          v-for="agent in trace.agents"
          :key="agent.agentName"
          @click="toggleAgent(agent.agentName)"
          :class="[
            'px-3 py-1.5 text-xs font-medium rounded transition-colors',
            isAgentActive(agent.agentName)
              ? 'bg-shiraz text-white'
              : 'bg-desert text-taupe hover:bg-gray-200'
          ]"
        >
          {{ agent.agentName }}
        </button>
      </div>
    </div>

    <div v-if="expandedAgent" class="mt-4 pt-4 border-t border-gray-100">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-xs font-medium text-taupe uppercase mb-2">Input</p>
          <div class="bg-desert rounded p-3 text-xs text-mine font-mono whitespace-pre-wrap">{{ expandedAgent.input }}</div>
        </div>
        <div>
          <p class="text-xs font-medium text-taupe uppercase mb-2">Output</p>
          <div class="bg-desert rounded p-3 text-xs text-mine font-mono whitespace-pre-wrap">{{ expandedAgent.output }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
