<script setup lang="ts">
  /**
   * EvaluationCard component for displaying an evaluation summary.
   * Shows status, name, submission count, and timing information.
   */
  import StatusBadge from '@/components/common/StatusBadge.vue'
  import type { Evaluation } from '@/types'

  defineProps<{
    evaluation: Evaluation
  }>()

  defineEmits<{
    click: [evaluation: Evaluation]
    delete: [evaluation: Evaluation]
  }>()

  /**
   * Formats a date string to a human-readable relative time or full date.
   * @param dateString - The ISO date string to format.
   * @returns Formatted time string.
   */
  function formatTime(dateString: string): string {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / (1000 * 60))
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const days = Math.floor(hours / 24)

    if (days > 7) {
      // Show full date with time for older items
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
      })
    } else if (days > 0) {
      return `${days} day${days > 1 ? 's' : ''} ago`
    } else if (hours > 0) {
      return `${hours} hour${hours > 1 ? 's' : ''} ago`
    } else if (minutes > 0) {
      return `${minutes} min${minutes > 1 ? 's' : ''} ago`
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
      <div class="flex items-center gap-3">
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
        <button
          class="p-2 text-taupe hover:text-red-600 transition-colors"
          title="Delete evaluation"
          @click.stop="$emit('delete', evaluation)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
