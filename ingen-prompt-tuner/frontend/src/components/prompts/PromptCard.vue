<script setup lang="ts">
  /**
   * PromptCard component for displaying a prompt file summary.
   * Shows filename, description, size, and tags in a clickable card.
   */
  import type { Prompt } from '@/types'

  defineProps<{
    prompt: Prompt
    selected: boolean
  }>()

  defineEmits<{
    click: []
  }>()

  /**
   * Formats file size in bytes to a human-readable string.
   * @param bytes - The file size in bytes.
   * @returns Formatted size string (e.g., "1.5 KB").
   */
  function formatSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`
    return `${(bytes / 1024).toFixed(1)} KB`
  }
</script>

<template>
  <div
    :class="[
      'bg-white rounded-lg p-5 cursor-pointer transition-colors',
      selected ? 'border-2 border-shiraz' : 'border border-gray-200 hover:border-shiraz/30',
    ]"
    @click="$emit('click')"
  >
    <div class="flex items-start justify-between mb-3">
      <div>
        <p class="text-sm font-medium text-mine">
          {{ prompt.filename }}
        </p>
        <p v-if="prompt.description" class="text-xs text-taupe mt-1">
          {{ prompt.description }}
        </p>
      </div>
      <span class="text-xs text-taupe">{{ formatSize(prompt.size) }}</span>
    </div>
    <div class="flex items-center gap-2">
      <span
        v-for="tag in prompt.tags"
        :key="tag"
        class="px-2 py-0.5 text-xs bg-desert text-taupe rounded"
      >
        {{ tag }}
      </span>
    </div>
  </div>
</template>
