<script setup lang="ts">
  import type { EvaluationResult, Criterion } from '@/types'

  const props = defineProps<{
    result: EvaluationResult
    rank: number
    criteria: Criterion[]
    expanded: boolean
  }>()

  defineEmits<{
    toggle: []
  }>()

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

  function getCriterionName(criterionId: string): string {
    const criterion = props.criteria.find((c) => c.id === criterionId)
    return criterion?.name || criterionId
  }
</script>

<template>
  <div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
    <div class="p-5 flex items-center justify-between cursor-pointer" @click="$emit('toggle')">
      <div class="flex items-center gap-4">
        <span
          :class="[
            'w-8 h-8 flex items-center justify-center rounded-full text-sm font-semibold',
            getRankBadge(rank).bg,
            getRankBadge(rank).text,
          ]"
        >
          {{ rank }}
        </span>
        <div>
          <p class="text-sm font-medium text-mine">
            {{ result.submissionName }}
          </p>
          <p v-if="result.submissionAuthor" class="text-xs text-taupe">
            {{ result.submissionAuthor }}
          </p>
        </div>
      </div>
      <div class="flex items-center gap-6">
        <div class="text-right">
          <p :class="['text-lg font-semibold', getScoreColor(result.overallScore)]">
            {{ result.overallScore.toFixed(1) }}
          </p>
          <p class="text-xs text-taupe">/100</p>
        </div>
        <svg
          :class="['w-5 h-5 text-taupe transition-transform', { 'rotate-180': expanded }]"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </div>
    </div>

    <div v-if="expanded" class="border-t border-gray-100 p-5 bg-gray-50">
      <div
        v-if="result.criterionResults.length"
        class="grid gap-3 mb-4"
        :style="{
          gridTemplateColumns: `repeat(${Math.min(result.criterionResults.length, 6)}, 1fr)`,
        }"
      >
        <div v-for="cr in result.criterionResults" :key="cr.criterionId" class="text-center">
          <p class="text-sm font-semibold text-mine">
            {{ cr.score.toFixed(1) }}
          </p>
          <p class="text-xs text-taupe">
            {{ getCriterionName(cr.criterionId) }}
          </p>
        </div>
      </div>
      <div class="text-sm text-taupe leading-relaxed">
        <p><strong class="text-mine">Summary:</strong> {{ result.summary }}</p>
      </div>
    </div>
  </div>
</template>
