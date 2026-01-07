<script setup lang="ts">
  import { ref } from 'vue'

  defineProps<{
    title: string
    defaultOpen?: boolean
  }>()

  const isOpen = ref(false)

  function toggle() {
    isOpen.value = !isOpen.value
  }
</script>

<template>
  <div class="border-t border-gray-100">
    <button
      class="w-full flex items-center gap-2 py-2 text-left text-xs font-medium text-taupe uppercase hover:text-mine transition-colors"
      @click="toggle"
    >
      <svg
        class="w-3 h-3 transition-transform"
        :class="{ 'rotate-90': isOpen }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
      {{ title }}
    </button>
    <div v-show="isOpen" class="pb-3">
      <slot />
    </div>
  </div>
</template>
