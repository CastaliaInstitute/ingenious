<script setup lang="ts">
import { useUIStore } from '@/stores/ui'
import { useRevisionsStore } from '@/stores/revisions'
import StatCard from '@/components/common/StatCard.vue'

const uiStore = useUIStore()
const revisionsStore = useRevisionsStore()

const recentActivity = [
  { id: '1', title: 'Prompt edited: analyst_prompt.jinja', subtitle: 'quickstart-1', time: '2 hours ago' },
  { id: '2', title: 'New revision created: magical-crystal-51211a8b', subtitle: 'From quickstart-1', time: 'Yesterday' },
  { id: '3', title: 'Test run completed: bike-insights', subtitle: '1,234 tokens', time: '2 days ago' }
]
</script>

<template>
  <div>
    <div class="mb-8">
      <h1 class="text-xl font-semibold text-mine mb-2">Prompt Tuner</h1>
      <p class="text-sm text-taupe">Inspect, edit, and test prompts for your Ingenious workflows.</p>
    </div>

    <div class="grid grid-cols-4 gap-4 mb-8">
      <StatCard :value="revisionsStore.revisions.length" label="Revisions" />
      <StatCard value="12" label="Prompt Files" />
      <StatCard value="47" label="Test Runs" />
      <StatCard value="4" label="Workflows" />
    </div>

    <div class="grid grid-cols-2 gap-4 mb-8">
      <div
        @click="uiStore.setActiveTab('prompts')"
        class="bg-white rounded-lg border border-gray-200 p-5 hover:border-shiraz/30 transition-colors cursor-pointer"
      >
        <p class="text-sm font-medium text-mine mb-1">Edit Prompts</p>
        <p class="text-xs text-taupe">View and modify prompt templates for each revision</p>
      </div>
      <div
        @click="uiStore.setActiveTab('test')"
        class="bg-white rounded-lg border border-gray-200 p-5 hover:border-shiraz/30 transition-colors cursor-pointer"
      >
        <p class="text-sm font-medium text-mine mb-1">View Test Runs</p>
        <p class="text-xs text-taupe">Inspect agent inputs and outputs from past runs</p>
      </div>
    </div>

    <div class="bg-white rounded-lg border border-gray-200">
      <div class="px-5 py-4 border-b border-gray-100">
        <p class="text-sm font-medium text-mine">Recent Activity</p>
      </div>
      <div class="divide-y divide-gray-100">
        <div
          v-for="item in recentActivity"
          :key="item.id"
          class="px-5 py-4 flex items-center justify-between"
        >
          <div>
            <p class="text-sm text-mine">{{ item.title }}</p>
            <p class="text-xs text-taupe">{{ item.subtitle }}</p>
          </div>
          <span class="text-xs text-taupe">{{ item.time }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
