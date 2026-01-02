<script setup lang="ts">
  import type { CriteriaSet } from '@/types'

  defineProps<{
    criteriaSet: CriteriaSet
  }>()

  defineEmits<{
    edit: [criteriaSet: CriteriaSet]
    delete: [id: string]
  }>()

  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <div class="flex items-start justify-between mb-3">
      <div class="flex-1">
        <p class="text-sm font-medium text-mine">
          {{ criteriaSet.name }}
        </p>
        <p v-if="criteriaSet.description" class="text-xs text-taupe mt-1">
          {{ criteriaSet.description }}
        </p>
      </div>
      <div class="flex gap-1">
        <button
          class="p-1.5 text-taupe hover:text-shiraz rounded transition-colors"
          title="Edit"
          @click="$emit('edit', criteriaSet)"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
            />
          </svg>
        </button>
        <button
          class="p-1.5 text-taupe hover:text-red-600 rounded transition-colors"
          title="Delete"
          @click="$emit('delete', criteriaSet.id)"
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
    <div class="flex items-center gap-2 text-xs text-taupe">
      <span>{{ criteriaSet.criteria.length }} criteria</span>
      <span>&middot;</span>
      <span>Created {{ formatDate(criteriaSet.createdAt) }}</span>
    </div>
    <div class="mt-3 flex flex-wrap gap-1">
      <span
        v-for="criterion in criteriaSet.criteria.slice(0, 3)"
        :key="criterion.id"
        class="px-2 py-0.5 text-xs bg-desert text-taupe rounded"
      >
        {{ criterion.name }} ({{ criterion.weight }}%)
      </span>
      <span
        v-if="criteriaSet.criteria.length > 3"
        class="px-2 py-0.5 text-xs bg-desert text-taupe rounded"
      >
        +{{ criteriaSet.criteria.length - 3 }} more
      </span>
    </div>
  </div>
</template>
