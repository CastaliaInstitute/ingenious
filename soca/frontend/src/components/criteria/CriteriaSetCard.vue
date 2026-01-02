<script setup lang="ts">
import type { CriteriaSet } from '@/types'

defineProps<{
  criteriaSet: CriteriaSet
}>()

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <div class="flex items-start justify-between mb-3">
      <div>
        <p class="text-sm font-medium text-mine">{{ criteriaSet.name }}</p>
        <p v-if="criteriaSet.description" class="text-xs text-taupe mt-1">{{ criteriaSet.description }}</p>
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
