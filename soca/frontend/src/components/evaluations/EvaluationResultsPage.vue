<script setup lang="ts">
import { computed } from 'vue'
import { useEvaluationsStore } from '@/stores/evaluations'
import { useUIStore } from '@/stores/ui'
import { useCriteriaStore } from '@/stores/criteria'
import StatCard from '@/components/common/StatCard.vue'
import Button from '@/components/common/Button.vue'
import ResultCard from './ResultCard.vue'

const evaluationsStore = useEvaluationsStore()
const criteriaStore = useCriteriaStore()
const uiStore = useUIStore()

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
      <Button variant="secondary" size="sm">Export</Button>
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
