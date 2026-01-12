<script setup lang="ts">
  /**
   * TraceCard component for displaying a single conversation trace.
   * Shows trace metadata and expandable agent details.
   */
  import { computed } from 'vue'
  import { useUIStore } from '@/stores/ui'
  import type { ConversationTrace } from '@/types'
  import JsonViewer from './JsonViewer.vue'
  import CollapsibleSection from './CollapsibleSection.vue'

  const props = defineProps<{
    trace: ConversationTrace
  }>()

  const uiStore = useUIStore()

  const expandedAgent = computed(() => {
    if (uiStore.expandedAgent?.traceId !== props.trace.traceId) return null
    return props.trace.agents.find((a) => a.agentName === uiStore.expandedAgent?.agentName)
  })

  /**
   * Formats a timestamp to a human-readable relative time string.
   * @param timestamp - The ISO timestamp string to format.
   * @returns A string like "Just now", "5 minutes ago", or "2 days ago".
   */
  function formatTime(timestamp: string): string {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / (1000 * 60))
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)

    if (days > 0) {
      return `${days} day${days > 1 ? 's' : ''} ago`
    } else if (hours > 0) {
      return `${hours} hour${hours > 1 ? 's' : ''} ago`
    } else if (minutes > 0) {
      return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
    }
    return 'Just now'
  }

  /**
   * Formats token count to a human-readable string.
   * @param tokens - The number of tokens.
   * @returns Formatted string like "1.5k tokens" or "500 tokens".
   */
  function formatTokens(tokens: number): string {
    if (tokens >= 1000) {
      return `${(tokens / 1000).toFixed(1)}k tokens`
    }
    return `${tokens} tokens`
  }

  /**
   * Checks if an agent is currently expanded.
   * @param agentName - The agent name to check.
   * @returns True if the agent is expanded.
   */
  function isAgentActive(agentName: string): boolean {
    return (
      uiStore.expandedAgent?.traceId === props.trace.traceId &&
      uiStore.expandedAgent?.agentName === agentName
    )
  }

  /**
   * Toggles the expanded state of an agent.
   * @param agentName - The agent name to toggle.
   */
  function toggleAgent(agentName: string) {
    uiStore.toggleAgent(props.trace.traceId, agentName)
  }
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <!-- Header: Query and metadata -->
    <div class="mb-3">
      <p class="text-sm font-medium text-mine mb-1 line-clamp-2">
        {{ trace.userQuery }}
      </p>
      <p class="text-xs text-taupe">
        {{ trace.workflow }} &middot; {{ formatTime(trace.timestamp) }} &middot;
        {{ formatTokens(trace.totalTokens) }}
      </p>
    </div>

    <!-- Agent buttons row -->
    <div class="flex flex-wrap gap-2 pb-3 border-b border-gray-100">
      <button
        v-for="agent in trace.agents"
        :key="agent.agentName"
        :class="[
          'px-3 py-1.5 text-xs font-medium rounded transition-colors',
          isAgentActive(agent.agentName)
            ? 'bg-shiraz text-white'
            : 'bg-desert text-taupe hover:bg-gray-200',
        ]"
        @click="toggleAgent(agent.agentName)"
      >
        {{ agent.agentName }}
      </button>
    </div>

    <!-- Expanded agent details -->
    <div v-if="expandedAgent" class="mt-3">
      <!-- Collapsible System Prompt -->
      <CollapsibleSection v-if="expandedAgent.systemPrompt" title="System Prompt">
        <div
          class="bg-desert rounded p-3 text-xs text-mine font-mono whitespace-pre-wrap max-h-64 overflow-auto"
        >
          {{ expandedAgent.systemPrompt }}
        </div>
      </CollapsibleSection>

      <!-- Collapsible User Prompt -->
      <CollapsibleSection v-if="expandedAgent.userPrompt" title="User Prompt">
        <div
          class="bg-desert rounded p-3 text-xs text-mine font-mono whitespace-pre-wrap max-h-64 overflow-auto"
        >
          {{ expandedAgent.userPrompt }}
        </div>
      </CollapsibleSection>

      <!-- Input/Output grid -->
      <div class="grid grid-cols-2 gap-4 mt-3">
        <div>
          <p class="text-xs font-medium text-taupe uppercase mb-2">Input</p>
          <JsonViewer :content="expandedAgent.input" max-height="300px" />
        </div>
        <div>
          <p class="text-xs font-medium text-taupe uppercase mb-2">Output</p>
          <JsonViewer :content="expandedAgent.output" max-height="300px" />
        </div>
      </div>
    </div>
  </div>
</template>
