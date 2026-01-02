<script setup lang="ts">
defineProps<{
  size?: 'sm' | 'md' | 'lg'
  text?: string
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3">
    <div
      :class="[
        'animate-spin rounded-full border-2 border-gray-200',
        size === 'sm' ? 'w-5 h-5' : '',
        size === 'lg' ? 'w-12 h-12' : '',
        (!size || size === 'md') ? 'w-8 h-8' : ''
      ]"
      style="border-top-color: #a91d4b;"
    ></div>
    <p v-if="text" class="text-sm text-taupe">{{ text }}</p>
  </div>
</template>

<style scoped>
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
