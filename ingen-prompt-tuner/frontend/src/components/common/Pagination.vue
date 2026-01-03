<script setup lang="ts">
  import { computed } from 'vue'

  const props = withDefaults(
    defineProps<{
      totalItems: number
      pageSize: number
      currentPage: number
      pageSizeOptions?: number[]
    }>(),
    {
      pageSizeOptions: () => [5, 10, 20],
    }
  )

  const emit = defineEmits<{
    'update:currentPage': [page: number]
    'update:pageSize': [size: number]
  }>()

  const totalPages = computed(() => Math.ceil(props.totalItems / props.pageSize))

  const startItem = computed(() => {
    if (props.totalItems === 0) return 0
    return (props.currentPage - 1) * props.pageSize + 1
  })

  const endItem = computed(() => {
    return Math.min(props.currentPage * props.pageSize, props.totalItems)
  })

  const canGoPrevious = computed(() => props.currentPage > 1)
  const canGoNext = computed(() => props.currentPage < totalPages.value)

  function goToPrevious() {
    if (canGoPrevious.value) {
      emit('update:currentPage', props.currentPage - 1)
    }
  }

  function goToNext() {
    if (canGoNext.value) {
      emit('update:currentPage', props.currentPage + 1)
    }
  }

  function handlePageSizeChange(event: Event) {
    const target = event.target as HTMLSelectElement
    const newSize = parseInt(target.value, 10)
    emit('update:pageSize', newSize)
    emit('update:currentPage', 1)
  }
</script>

<template>
  <div class="flex items-center justify-between py-3 text-sm text-taupe">
    <div class="flex items-center gap-2">
      <span>Show</span>
      <select
        :value="pageSize"
        class="border border-gray-200 rounded px-2 py-1 text-sm bg-white focus:outline-none focus:border-shiraz"
        @change="handlePageSizeChange"
      >
        <option v-for="size in pageSizeOptions" :key="size" :value="size">
          {{ size }}
        </option>
      </select>
      <span>per page</span>
    </div>

    <div class="flex items-center gap-4">
      <span v-if="totalItems > 0"> {{ startItem }}-{{ endItem }} of {{ totalItems }} </span>
      <span v-else>No items</span>

      <div class="flex gap-1">
        <button
          :disabled="!canGoPrevious"
          :class="[
            'p-1 rounded border transition-colors',
            canGoPrevious
              ? 'border-gray-200 hover:bg-desert text-taupe'
              : 'border-gray-100 text-gray-300 cursor-not-allowed',
          ]"
          title="Previous page"
          @click="goToPrevious"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </button>
        <button
          :disabled="!canGoNext"
          :class="[
            'p-1 rounded border transition-colors',
            canGoNext
              ? 'border-gray-200 hover:bg-desert text-taupe'
              : 'border-gray-100 text-gray-300 cursor-not-allowed',
          ]"
          title="Next page"
          @click="goToNext"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
