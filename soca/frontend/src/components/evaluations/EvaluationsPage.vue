<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useEvaluationsStore } from '@/stores/evaluations'
import { useUIStore } from '@/stores/ui'
import StatCard from '@/components/common/StatCard.vue'
import Button from '@/components/common/Button.vue'
import EvaluationCard from './EvaluationCard.vue'
import NewEvaluationModal from './NewEvaluationModal.vue'
import type { Evaluation } from '@/types'

const evaluationsStore = useEvaluationsStore()
const uiStore = useUIStore()
const showNewModal = ref(false)

onMounted(() => {
  evaluationsStore.fetchEvaluations()
})

function handleEvaluationClick(evaluation: Evaluation) {
  uiStore.viewEvaluationResults(evaluation.id)
}

function handleNewEvaluation() {
  showNewModal.value = true
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-xl font-semibold text-mine">Evaluations</h1>
      <Button @click="handleNewEvaluation">New Evaluation</Button>
    </div>

    <div class="grid grid-cols-3 gap-4 mb-8">
      <StatCard
        :value="evaluationsStore.completedCount"
        label="Completed"
      />
      <StatCard
        :value="evaluationsStore.inProgressCount"
        label="In Progress"
      />
      <StatCard
        :value="evaluationsStore.totalSubmissions"
        label="Total Submissions"
      />
    </div>

    <div v-if="evaluationsStore.loading" class="text-center py-8 text-taupe">
      Loading evaluations...
    </div>

    <div v-else-if="evaluationsStore.error" class="text-center py-8 text-red-600">
      {{ evaluationsStore.error }}
    </div>

    <div v-else class="space-y-3">
      <EvaluationCard
        v-for="evaluation in evaluationsStore.evaluations"
        :key="evaluation.id"
        :evaluation="evaluation"
        @click="handleEvaluationClick"
      />

      <div v-if="evaluationsStore.evaluations.length === 0" class="text-center py-8 text-taupe">
        No evaluations yet. Create your first evaluation to get started.
      </div>
    </div>

    <NewEvaluationModal
      v-if="showNewModal"
      @close="showNewModal = false"
    />
  </div>
</template>
