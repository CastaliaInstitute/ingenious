<script setup lang="ts">
  import StatusBadge from '@/components/common/StatusBadge.vue'
  import type { Evaluation } from '@/types'

  defineProps<{
    evaluation: Evaluation
  }>()

  defineEmits<{
    click: [evaluation: Evaluation]
  }>()

  function formatTime(dateString: string): string {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const days = Math.floor(hours / 24)

    if (days > 7) {
      return date.toLocaleDateString()
    } else if (days > 0) {
      return `${days} day${days > 1 ? 's' : ''} ago`
    } else if (hours > 0) {
      return `${hours} hour${hours > 1 ? 's' : ''} ago`
    } else {
      return 'Just now'
    }
  }
</script>

<template>
  <div
    class="block bg-white rounded-lg border border-gray-200 p-5 hover:border-shiraz/30 transition-colors cursor-pointer"
    @click="$emit('click', evaluation)"
  >
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm font-medium text-mine mb-1">
          {{ evaluation.name }}
        </p>
        <p class="text-xs text-taupe">
          {{ evaluation.submissionIds.length }} submissions
          <template v-if="evaluation.criteriaSetName">
            &middot; {{ evaluation.criteriaSetName }}
          </template>
        </p>
      </div>
      <div class="flex flex-col items-end gap-1.5">
        <StatusBadge :status="evaluation.status" />
        <p class="text-xs text-taupe">
          <template v-if="evaluation.status === 'running'">
            {{ evaluation.results.length }}/{{ evaluation.submissionIds.length }} evaluated
          </template>
          <template v-else>
            {{ formatTime(evaluation.completedAt || evaluation.createdAt) }}
          </template>
        </p>
      </div>
    </div>
  </div>
</template>
