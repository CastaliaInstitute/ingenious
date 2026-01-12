<script setup lang="ts">
  import type { Submission } from '@/types'

  defineProps<{
    submission: Submission
    selected?: boolean
  }>()

  defineEmits<{
    delete: []
    click: []
  }>()

  function formatFileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    })
  }
</script>

<template>
  <div
    :class="[
      'bg-white rounded-lg border p-4 flex items-center justify-between cursor-pointer transition-colors',
      selected ? 'border-shiraz bg-desert' : 'border-gray-200 hover:border-gray-300',
    ]"
    @click="$emit('click')"
  >
    <div class="flex items-center gap-4">
      <div class="w-10 h-10 bg-desert rounded flex items-center justify-center">
        <svg class="w-5 h-5 text-taupe" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
      </div>
      <div>
        <p class="text-sm font-medium text-mine">
          {{ submission.name }}
        </p>
        <p class="text-xs text-taupe">
          {{ submission.fileName }} &middot; {{ formatFileSize(submission.fileSize) }} &middot;
          {{ formatDate(submission.uploadedAt) }}
        </p>
      </div>
    </div>
    <button
      class="p-2 text-taupe hover:text-red-600 transition-colors"
      title="Delete submission"
      @click.stop="$emit('delete')"
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
</template>
