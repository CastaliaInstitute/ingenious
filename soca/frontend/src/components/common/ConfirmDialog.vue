<script setup lang="ts">
  defineProps<{
    isOpen: boolean
    title: string
    message: string
    confirmLabel?: string
    cancelLabel?: string
    variant?: 'danger' | 'warning'
  }>()

  defineEmits<{
    confirm: []
    cancel: []
  }>()
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
        @click.self="$emit('cancel')"
      >
        <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
          <h3 class="text-lg font-semibold text-mine mb-2">
            {{ title }}
          </h3>
          <p class="text-sm text-taupe mb-6">
            {{ message }}
          </p>
          <div class="flex justify-end gap-3">
            <button
              class="px-4 py-2 text-sm font-medium text-taupe bg-desert border border-gray-200 rounded-md hover:bg-gray-100 transition-colors"
              @click="$emit('cancel')"
            >
              {{ cancelLabel || 'Cancel' }}
            </button>
            <button
              :class="[
                'px-4 py-2 text-sm font-medium text-white rounded-md transition-colors',
                variant === 'warning'
                  ? 'bg-amber-500 hover:bg-amber-600'
                  : 'bg-red-600 hover:bg-red-700',
              ]"
              @click="$emit('confirm')"
            >
              {{ confirmLabel || 'Confirm' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.2s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
</style>
