<script setup lang="ts">
defineProps<{
  status: 'completed' | 'running' | 'draft' | 'failed'
}>()

const statusStyles = {
  completed: 'bg-green-100 text-green-700',
  running: 'bg-amber-100 text-amber-700',
  draft: 'bg-gray-100 text-gray-700',
  failed: 'bg-red-100 text-red-700'
}

const statusLabels = {
  completed: 'Completed',
  running: 'In Progress',
  draft: 'Draft',
  failed: 'Failed'
}
</script>

<template>
  <span
    :class="[
      'inline-block px-2 py-1 text-xs font-medium rounded',
      statusStyles[status]
    ]"
  >
    {{ statusLabels[status] }}
  </span>
</template>
