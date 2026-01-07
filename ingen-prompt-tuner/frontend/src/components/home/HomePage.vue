<script setup lang="ts">
  import { ref, onMounted, computed } from 'vue'
  import { useUIStore } from '@/stores/ui'
  import { useRevisionsStore } from '@/stores/revisions'
  import { tracesService } from '@/services/traces.service'
  import api from '@/services/api'
  import StatCard from '@/components/common/StatCard.vue'
  import WorkflowDag from './WorkflowDag.vue'
  import type { ConversationTrace } from '@/types'

  const uiStore = useUIStore()
  const revisionsStore = useRevisionsStore()

  const stats = ref({
    revisions: 0,
    promptFiles: 0,
    testRuns: 0,
    workflows: 0,
  })

  const traces = ref<ConversationTrace[]>([])

  const recentActivity = computed(() => {
    return traces.value.slice(0, 5).map((trace) => {
      const timeAgo = getTimeAgo(new Date(trace.timestamp))
      return {
        id: trace.traceId,
        title: `Test run: ${trace.userQuery.slice(0, 40)}${trace.userQuery.length > 40 ? '...' : ''}`,
        subtitle: `${trace.workflow} - ${trace.totalTokens.toLocaleString()} tokens`,
        time: timeAgo,
      }
    })
  })

  function getTimeAgo(date: Date): string {
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins} min ago`
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
    if (diffDays === 1) return 'Yesterday'
    return `${diffDays} days ago`
  }

  onMounted(async () => {
    try {
      const [statsResponse, tracesResponse] = await Promise.all([
        api.get('/stats'),
        tracesService.list(),
      ])
      stats.value = statsResponse.data
      traces.value = tracesResponse
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    }
  })
</script>

<template>
  <div>
    <div class="mb-8">
      <h1 class="text-xl font-semibold text-mine mb-2">Prompt Tuner</h1>
      <p class="text-sm text-taupe">
        Inspect, edit, and test prompts for your Ingenious workflows.
      </p>
    </div>

    <div class="grid grid-cols-4 gap-4 mb-8">
      <StatCard :value="stats.revisions" label="Revisions" />
      <StatCard :value="stats.promptFiles" label="Prompt Files" />
      <StatCard :value="stats.testRuns" label="Test Runs" />
      <StatCard :value="stats.workflows" label="Workflows" />
    </div>

    <div class="mb-8">
      <WorkflowDag />
    </div>

    <div class="grid grid-cols-2 gap-4 mb-8">
      <div
        class="bg-white rounded-lg border border-gray-200 p-5 hover:border-shiraz/30 transition-colors cursor-pointer"
        @click="uiStore.setActiveTab('prompts')"
      >
        <p class="text-sm font-medium text-mine mb-1">Edit Prompts</p>
        <p class="text-xs text-taupe">View and modify prompt templates for each revision</p>
      </div>
      <div
        class="bg-white rounded-lg border border-gray-200 p-5 hover:border-shiraz/30 transition-colors cursor-pointer"
        @click="uiStore.setActiveTab('test')"
      >
        <p class="text-sm font-medium text-mine mb-1">View Test Runs</p>
        <p class="text-xs text-taupe">Inspect agent inputs and outputs from past runs</p>
      </div>
    </div>

    <div class="bg-white rounded-lg border border-gray-200">
      <div class="px-5 py-4 border-b border-gray-100">
        <p class="text-sm font-medium text-mine">Recent Activity</p>
      </div>
      <div v-if="recentActivity.length === 0" class="px-5 py-8 text-center">
        <p class="text-sm text-taupe">No recent activity yet</p>
        <p class="text-xs text-taupe mt-1">Run evaluations in SoCa to see traces here</p>
      </div>
      <div v-else class="divide-y divide-gray-100">
        <div
          v-for="item in recentActivity"
          :key="item.id"
          class="px-5 py-4 flex items-center justify-between"
        >
          <div>
            <p class="text-sm text-mine">
              {{ item.title }}
            </p>
            <p class="text-xs text-taupe">
              {{ item.subtitle }}
            </p>
          </div>
          <span class="text-xs text-taupe">{{ item.time }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
