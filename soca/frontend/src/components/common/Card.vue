<script setup lang="ts">
defineProps<{
  clickable?: boolean
}>()
</script>

<template>
  <div
    :class="[
      'bg-white rounded-lg border border-gray-200',
      { 'hover:border-shiraz/30 transition-colors cursor-pointer': clickable }
    ]"
  >
    <slot />
  </div>
</template>
