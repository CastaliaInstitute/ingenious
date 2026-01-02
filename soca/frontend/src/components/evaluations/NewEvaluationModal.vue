<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useEvaluationsStore } from '@/stores/evaluations'
  import { useSubmissionsStore } from '@/stores/submissions'
  import { useCriteriaStore } from '@/stores/criteria'
  import Button from '@/components/common/Button.vue'

  const emit = defineEmits<{
    close: []
  }>()

  const evaluationsStore = useEvaluationsStore()
  const submissionsStore = useSubmissionsStore()
  const criteriaStore = useCriteriaStore()

  const name = ref('')
  const selectedSubmissions = ref<string[]>([])
  const selectedCriteriaSet = ref('')
  const creating = ref(false)
  const error = ref<string | null>(null)

  onMounted(() => {
    submissionsStore.fetchSubmissions()
    criteriaStore.fetchCriteriaSets()
  })

  function toggleSubmission(id: string) {
    const index = selectedSubmissions.value.indexOf(id)
    if (index === -1) {
      selectedSubmissions.value.push(id)
    } else {
      selectedSubmissions.value.splice(index, 1)
    }
  }

  async function handleCreate() {
    if (!name.value || selectedSubmissions.value.length === 0 || !selectedCriteriaSet.value) {
      error.value = 'Please fill in all fields'
      return
    }

    creating.value = true
    error.value = null

    try {
      const evaluation = await evaluationsStore.createEvaluation({
        name: name.value,
        submissionIds: selectedSubmissions.value,
        criteriaSetId: selectedCriteriaSet.value,
      })
      await evaluationsStore.runEvaluation(evaluation.id)
      emit('close')
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create evaluation'
    } finally {
      creating.value = false
    }
  }
</script>

<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-lg mx-4">
      <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-mine">New Evaluation</h2>
        <button class="text-taupe hover:text-mine" @click="emit('close')">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <div class="p-6 space-y-4">
        <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-600">
          {{ error }}
        </div>

        <div>
          <label class="block text-sm font-medium text-taupe mb-2">Evaluation Name</label>
          <input
            v-model="name"
            type="text"
            placeholder="e.g., Q4 Grant Proposals Review"
            class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-taupe mb-2">Select Submissions</label>
          <div class="border border-gray-200 rounded-md max-h-40 overflow-y-auto">
            <div
              v-for="submission in submissionsStore.submissions"
              :key="submission.id"
              :class="[
                'px-3 py-2 cursor-pointer border-b border-gray-100 last:border-0 flex items-center gap-2',
                selectedSubmissions.includes(submission.id) ? 'bg-shiraz/5' : 'hover:bg-gray-50',
              ]"
              @click="toggleSubmission(submission.id)"
            >
              <div
                :class="[
                  'w-4 h-4 rounded border flex items-center justify-center',
                  selectedSubmissions.includes(submission.id)
                    ? 'bg-shiraz border-shiraz'
                    : 'border-gray-300',
                ]"
              >
                <svg
                  v-if="selectedSubmissions.includes(submission.id)"
                  class="w-3 h-3 text-white"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <span class="text-sm text-mine">{{ submission.name }}</span>
            </div>
            <div
              v-if="submissionsStore.submissions.length === 0"
              class="px-3 py-4 text-center text-sm text-taupe"
            >
              No submissions available. Upload some first.
            </div>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-taupe mb-2">Criteria Set</label>
          <select
            v-model="selectedCriteriaSet"
            class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
          >
            <option value="">Select a criteria set...</option>
            <option
              v-for="criteriaSet in criteriaStore.criteriaSets"
              :key="criteriaSet.id"
              :value="criteriaSet.id"
            >
              {{ criteriaSet.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="px-6 py-4 border-t border-gray-200 flex justify-end gap-2">
        <Button variant="secondary" @click="emit('close')"> Cancel </Button>
        <Button :disabled="creating" @click="handleCreate">
          {{ creating ? 'Creating...' : 'Create & Run' }}
        </Button>
      </div>
    </div>
  </div>
</template>
