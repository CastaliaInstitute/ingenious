<script setup lang="ts">
import { computed, ref } from 'vue'
import { useEvaluationsStore } from '@/stores/evaluations'
import { useUIStore } from '@/stores/ui'
import { useCriteriaStore } from '@/stores/criteria'
import api from '@/services/api'
import StatCard from '@/components/common/StatCard.vue'
import Button from '@/components/common/Button.vue'
import ResultCard from './ResultCard.vue'

const evaluationsStore = useEvaluationsStore()
const criteriaStore = useCriteriaStore()
const uiStore = useUIStore()

const showExportMenu = ref(false)
const exporting = ref(false)

const evaluation = computed(() => {
  if (!uiStore.selectedEvaluationId) return null
  return evaluationsStore.getEvaluation(uiStore.selectedEvaluationId)
})

const criteriaSet = computed(() => {
  if (!evaluation.value) return null
  return criteriaStore.getCriteriaSet(evaluation.value.criteriaSetId)
})

const sortedResults = computed(() => {
  if (!evaluation.value) return []
  return [...evaluation.value.results].sort((a, b) => b.overallScore - a.overallScore)
})

const averageScore = computed(() => {
  if (!sortedResults.value.length) return 0
  const sum = sortedResults.value.reduce((acc, r) => acc + r.overallScore, 0)
  return (sum / sortedResults.value.length).toFixed(1)
})

const highestScore = computed(() => {
  if (!sortedResults.value.length) return 0
  return sortedResults.value[0].overallScore.toFixed(1)
})

function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600'
  if (score >= 60) return 'text-amber-600'
  return 'text-orange-600'
}

function getRankBadge(rank: number): { bg: string; text: string } {
  if (rank === 1) return { bg: 'bg-yellow-100', text: 'text-yellow-700' }
  if (rank === 2) return { bg: 'bg-gray-200', text: 'text-gray-700' }
  if (rank === 3) return { bg: 'bg-amber-100', text: 'text-amber-700' }
  return { bg: 'bg-gray-100', text: 'text-gray-600' }
}

async function exportResults(format: 'json' | 'csv') {
  if (!evaluation.value) return

  exporting.value = true
  showExportMenu.value = false

  try {
    const response = await api.get(`/evaluations/${evaluation.value.id}/export/${format}`, {
      responseType: 'blob'
    })

    // Create download link
    const blob = new Blob([response.data], {
      type: format === 'json' ? 'application/json' : 'text/csv'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${evaluation.value.name}.${format}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Export failed:', error)
  } finally {
    exporting.value = false
  }
}
</script>

<template>
  <div v-if="evaluation">
    <div class="flex items-center justify-between mb-8">
      <div class="flex items-center gap-6">
        <button
          @click="uiStore.backToEvaluations()"
          class="text-sm text-taupe hover:text-mine flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
        <div>
          <p class="text-sm font-medium text-mine">{{ evaluation.name }}</p>
          <p class="text-xs text-taupe">
            {{ evaluation.submissionIds.length }} submissions
            <template v-if="criteriaSet">&middot; {{ criteriaSet.name }}</template>
          </p>
        </div>
      </div>
      <div class="relative">
        <Button
          variant="secondary"
          size="sm"
          :disabled="exporting"
          @click="showExportMenu = !showExportMenu"
        >
          <span v-if="exporting">Exporting...</span>
          <span v-else>Export</span>
          <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </Button>
        <div
          v-if="showExportMenu"
          class="absolute right-0 mt-1 w-40 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-10"
        >
          <button
            @click="exportResults('json')"
            class="w-full px-4 py-2 text-left text-sm text-mine hover:bg-gray-50"
          >
            Export as JSON
          </button>
          <button
            @click="exportResults('csv')"
            class="w-full px-4 py-2 text-left text-sm text-mine hover:bg-gray-50"
          >
            Export as CSV
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-4 mb-8">
      <StatCard :value="averageScore" label="Average Score" />
      <StatCard :value="highestScore" label="Highest Score" value-class="text-green-600" />
      <StatCard value="--" label="Evaluation Time" />
    </div>

    <div class="space-y-3">
      <ResultCard
        v-for="(result, index) in sortedResults"
        :key="result.submissionId"
        :result="result"
        :rank="index + 1"
        :criteria="criteriaSet?.criteria || []"
        :expanded="uiStore.expandedResultId === result.submissionId"
        @toggle="uiStore.toggleResultExpanded(result.submissionId)"
      />
    </div>
  </div>
</template>
