<script setup lang="ts">
  defineProps<{
    variant?: 'primary' | 'secondary'
    size?: 'sm' | 'md' | 'lg'
    disabled?: boolean
  }>()
</script>

<template>
  <button
    :disabled="disabled"
    :class="[
      'font-medium rounded-md transition-colors',
      {
        'bg-shiraz text-white hover:bg-shiraz/90': variant === 'primary' || !variant,
        'bg-desert text-taupe border border-gray-200 hover:bg-gray-100': variant === 'secondary',
        'px-2 py-1 text-xs': size === 'sm',
        'px-4 py-2 text-sm': size === 'md' || !size,
        'px-6 py-3 text-base': size === 'lg',
        'opacity-50 cursor-not-allowed': disabled,
      },
    ]"
  >
    <slot />
  </button>
</template>
