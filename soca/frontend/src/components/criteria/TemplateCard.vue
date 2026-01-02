<script setup lang="ts">
import type { CriteriaSet } from '@/types'
import Button from '@/components/common/Button.vue'

defineProps<{
  template: CriteriaSet
}>()

defineEmits<{
  use: []
}>()
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <div class="flex items-start justify-between mb-3">
      <div>
        <p class="text-sm font-medium text-mine">{{ template.name }}</p>
        <p v-if="template.description" class="text-xs text-taupe mt-1">{{ template.description }}</p>
      </div>
      <Button size="sm" variant="secondary" @click="$emit('use')">Use</Button>
    </div>
    <div class="mt-3 space-y-1">
      <div
        v-for="criterion in template.criteria"
        :key="criterion.id"
        class="flex items-center justify-between text-xs"
      >
        <span class="text-taupe">{{ criterion.name }}</span>
        <span class="text-mine font-medium">{{ criterion.weight }}%</span>
      </div>
    </div>
  </div>
</template>
