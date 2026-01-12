<script setup lang="ts">
  /**
   * TestPage component for viewing conversation traces.
   * Displays a paginated list of trace records for the selected revision.
   */
  import { ref, computed, onMounted, watch } from 'vue'
  import { useRevisionsStore } from '@/stores/revisions'
  import { useTracesStore } from '@/stores/traces'
  import Spinner from '@/components/common/Spinner.vue'
  import Pagination from '@/components/common/Pagination.vue'
  import TraceCard from './TraceCard.vue'

  const revisionsStore = useRevisionsStore()
  const tracesStore = useTracesStore()

  // Pagination state
  const currentPage = ref(1)
  const pageSize = ref(10)

  const paginatedTraces = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return tracesStore.traces.slice(start, end)
  })

  const totalTraces = computed(() => tracesStore.traces.length)

  onMounted(async () => {
    await revisionsStore.fetchRevisions()
    if (revisionsStore.activeRevision) {
      tracesStore.fetchTraces(revisionsStore.activeRevision)
    }
  })

  watch(
    () => revisionsStore.activeRevision,
    (newRevision) => {
      tracesStore.fetchTraces(newRevision)
      currentPage.value = 1
    }
  )

  // Reset to first page when total changes and current page is invalid
  watch(totalTraces, (newTotal) => {
    const maxPage = Math.ceil(newTotal / pageSize.value)
    if (currentPage.value > maxPage && maxPage > 0) {
      currentPage.value = maxPage
    }
  })

  /**
   * Handles revision dropdown selection changes.
   * @param event - The change event from the select element.
   */
  function handleRevisionChange(event: Event) {
    const target = event.target as HTMLSelectElement
    revisionsStore.setActiveRevision(target.value)
  }
</script>

<template>
  <div>
    <div class="mb-8">
      <label class="block text-sm font-medium text-taupe mb-2">Revision</label>
      <select
        :value="revisionsStore.activeRevision"
        class="w-64 px-3 py-2 bg-white border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
        @change="handleRevisionChange"
      >
        <option
          v-for="revision in revisionsStore.revisions"
          :key="revision.id"
          :value="revision.id"
        >
          {{ revision.name }}
        </option>
      </select>
    </div>

    <div v-if="tracesStore.loading" class="flex justify-center py-8">
      <Spinner text="Loading traces..." />
    </div>

    <template v-else>
      <div class="space-y-4">
        <TraceCard v-for="trace in paginatedTraces" :key="trace.traceId" :trace="trace" />

        <div v-if="tracesStore.traces.length === 0" class="text-center py-8 text-taupe">
          No test runs found for this revision.
        </div>
      </div>

      <Pagination
        v-if="totalTraces > 0"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total-items="totalTraces"
        class="mt-4 border-t border-gray-100"
      />
    </template>
  </div>
</template>
