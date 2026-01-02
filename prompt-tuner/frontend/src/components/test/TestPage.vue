<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRevisionsStore } from '@/stores/revisions'
import { useTracesStore } from '@/stores/traces'
import TraceCard from './TraceCard.vue'

const revisionsStore = useRevisionsStore()
const tracesStore = useTracesStore()

onMounted(() => {
  tracesStore.fetchTraces(revisionsStore.activeRevision)
})

watch(() => revisionsStore.activeRevision, (newRevision) => {
  tracesStore.fetchTraces(newRevision)
})

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
        @change="handleRevisionChange"
        class="w-64 px-3 py-2 bg-white border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
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

    <div v-if="tracesStore.loading" class="text-center py-8 text-taupe">
      Loading traces...
    </div>

    <div v-else class="space-y-4">
      <TraceCard
        v-for="trace in tracesStore.traces"
        :key="trace.traceId"
        :trace="trace"
      />

      <div v-if="tracesStore.traces.length === 0" class="text-center py-8 text-taupe">
        No test runs found for this revision.
      </div>
    </div>
  </div>
</template>
