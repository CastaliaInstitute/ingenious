<script setup lang="ts">
defineProps<{
  value: string | number
  label: string
  valueClass?: string
}>()
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 p-5">
    <p :class="['text-2xl font-semibold', valueClass || 'text-mine']">{{ value }}</p>
    <p class="text-sm text-taupe">{{ label }}</p>
  </div>
</template>
