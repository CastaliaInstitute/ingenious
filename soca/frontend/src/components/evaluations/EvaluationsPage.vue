<script setup lang="ts">
  /**
   * EvaluationsPage component for managing evaluations.
   * Displays statistics, evaluation list, and creation interface.
   */
  import { computed, onMounted, ref } from 'vue'
  import { useEvaluationsStore } from '@/stores/evaluations'
  import { useUIStore } from '@/stores/ui'
  import StatCard from '@/components/common/StatCard.vue'
  import Button from '@/components/common/Button.vue'
  import Spinner from '@/components/common/Spinner.vue'
  import Pagination from '@/components/common/Pagination.vue'
  import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
  import EvaluationCard from './EvaluationCard.vue'
  import NewEvaluationModal from './NewEvaluationModal.vue'
  import type { Evaluation } from '@/types'

  const evaluationsStore = useEvaluationsStore()
  const uiStore = useUIStore()
  const showNewModal = ref(false)

  const currentPage = ref(1)
  const pageSize = ref(10)

  const deleteDialogOpen = ref(false)
  const evaluationToDelete = ref<Evaluation | null>(null)

  const paginatedEvaluations = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return evaluationsStore.evaluations.slice(start, end)
  })

  onMounted(() => {
    evaluationsStore.fetchEvaluations()
  })

  /**
   * Navigates to view the results of an evaluation.
   * @param evaluation - The evaluation to view.
   */
  function handleEvaluationClick(evaluation: Evaluation) {
    uiStore.viewEvaluationResults(evaluation.id)
  }

  /**
   * Opens the new evaluation modal.
   */
  function handleNewEvaluation() {
    showNewModal.value = true
  }

  /**
   * Opens the delete confirmation dialog for an evaluation.
   * @param evaluation - The evaluation to delete.
   */
  function handleDeleteClick(evaluation: Evaluation) {
    evaluationToDelete.value = evaluation
    deleteDialogOpen.value = true
  }

  /**
   * Confirms and executes the evaluation deletion.
   */
  async function confirmDelete() {
    if (evaluationToDelete.value) {
      await evaluationsStore.deleteEvaluation(evaluationToDelete.value.id)
      const totalPages = Math.ceil(evaluationsStore.evaluations.length / pageSize.value)
      if (currentPage.value > totalPages && totalPages > 0) {
        currentPage.value = totalPages
      }
    }
    deleteDialogOpen.value = false
    evaluationToDelete.value = null
  }

  /**
   * Cancels the delete operation and closes the dialog.
   */
  function cancelDelete() {
    deleteDialogOpen.value = false
    evaluationToDelete.value = null
  }
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-xl font-semibold text-mine">Evaluations</h1>
      <Button @click="handleNewEvaluation"> New Evaluation </Button>
    </div>

    <div class="grid grid-cols-3 gap-4 mb-8">
      <StatCard :value="evaluationsStore.completedCount" label="Completed" />
      <StatCard :value="evaluationsStore.inProgressCount" label="In Progress" />
      <StatCard :value="evaluationsStore.totalSubmissions" label="Total Submissions" />
    </div>

    <div v-if="evaluationsStore.loading" class="flex justify-center py-8">
      <Spinner text="Loading evaluations..." />
    </div>

    <div v-else-if="evaluationsStore.error" class="text-center py-8 text-red-600">
      {{ evaluationsStore.error }}
    </div>

    <div v-else>
      <div class="space-y-3">
        <EvaluationCard
          v-for="evaluation in paginatedEvaluations"
          :key="evaluation.id"
          :evaluation="evaluation"
          @click="handleEvaluationClick"
          @delete="handleDeleteClick"
        />

        <div v-if="evaluationsStore.evaluations.length === 0" class="text-center py-8 text-taupe">
          No evaluations yet. Create your first evaluation to get started.
        </div>
      </div>

      <Pagination
        v-if="evaluationsStore.evaluations.length > 0"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total-items="evaluationsStore.evaluations.length"
      />
    </div>

    <NewEvaluationModal v-if="showNewModal" @close="showNewModal = false" />

    <ConfirmDialog
      :is-open="deleteDialogOpen"
      title="Delete Evaluation"
      :message="`Are you sure you want to delete '${evaluationToDelete?.name}'? This action cannot be undone.`"
      confirm-label="Delete"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>
