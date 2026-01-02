import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Evaluation } from '@/types'
import { evaluationsService } from '@/services/evaluations.service'

export const useEvaluationsStore = defineStore('evaluations', () => {
  const evaluations = ref<Evaluation[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const completedCount = computed(() =>
    evaluations.value.filter(e => e.status === 'completed').length
  )

  const inProgressCount = computed(() =>
    evaluations.value.filter(e => e.status === 'running').length
  )

  const totalSubmissions = computed(() =>
    evaluations.value.reduce((sum, e) => sum + e.submissionIds.length, 0)
  )

  async function fetchEvaluations() {
    loading.value = true
    error.value = null
    try {
      evaluations.value = await evaluationsService.list()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch evaluations'
    } finally {
      loading.value = false
    }
  }

  async function createEvaluation(data: { name: string; submissionIds: string[]; criteriaSetId: string }) {
    const evaluation = await evaluationsService.create(data)
    evaluations.value.unshift(evaluation)
    return evaluation
  }

  async function runEvaluation(id: string) {
    const evaluation = evaluations.value.find(e => e.id === id)
    if (evaluation) {
      evaluation.status = 'running'
    }
    const updated = await evaluationsService.run(id)
    const index = evaluations.value.findIndex(e => e.id === id)
    if (index !== -1) {
      evaluations.value[index] = updated
    }
    return updated
  }

  function getEvaluation(id: string) {
    return evaluations.value.find(e => e.id === id)
  }

  return {
    evaluations,
    loading,
    error,
    completedCount,
    inProgressCount,
    totalSubmissions,
    fetchEvaluations,
    createEvaluation,
    runEvaluation,
    getEvaluation
  }
})
