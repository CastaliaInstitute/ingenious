<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCriteriaStore } from '@/stores/criteria'
import Button from '@/components/common/Button.vue'
import type { Criterion, CriteriaSet } from '@/types'

const props = defineProps<{
  editingCriteriaSet?: CriteriaSet | null
}>()

const emit = defineEmits<{
  close: []
}>()

const criteriaStore = useCriteriaStore()

const isEditing = computed(() => !!props.editingCriteriaSet)
const name = ref('')
const description = ref('')
const criteria = ref<Omit<Criterion, 'id'>[]>([
  { name: '', description: '', weight: 25, maxScore: 5 }
])
const saving = ref(false)
const error = ref<string | null>(null)

onMounted(() => {
  if (props.editingCriteriaSet) {
    name.value = props.editingCriteriaSet.name
    description.value = props.editingCriteriaSet.description || ''
    criteria.value = props.editingCriteriaSet.criteria.map(c => ({
      name: c.name,
      description: c.description || '',
      weight: c.weight,
      maxScore: c.maxScore
    }))
  }
})

const totalWeight = computed(() =>
  criteria.value.reduce((sum, c) => sum + c.weight, 0)
)

function addCriterion() {
  criteria.value.push({ name: '', description: '', weight: 0, maxScore: 5 })
}

function removeCriterion(index: number) {
  if (criteria.value.length > 1) {
    criteria.value.splice(index, 1)
  }
}

async function handleSave() {
  if (!name.value) {
    error.value = 'Please enter a name'
    return
  }

  if (criteria.value.some(c => !c.name)) {
    error.value = 'Please fill in all criterion names'
    return
  }

  if (totalWeight.value !== 100) {
    error.value = 'Weights must sum to 100%'
    return
  }

  saving.value = true
  error.value = null

  try {
    const criteriaData = {
      name: name.value,
      description: description.value || undefined,
      criteria: criteria.value.map((c, i) => ({
        ...c,
        id: `criterion-${i}`
      }))
    }

    if (isEditing.value && props.editingCriteriaSet) {
      await criteriaStore.updateCriteriaSet(props.editingCriteriaSet.id, criteriaData)
    } else {
      await criteriaStore.createCriteriaSet(criteriaData)
    }
    emit('close')
  } catch (e) {
    error.value = e instanceof Error ? e.message : `Failed to ${isEditing.value ? 'update' : 'create'} criteria set`
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 overflow-y-auto py-8">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4">
      <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-mine">{{ isEditing ? 'Edit Criteria Set' : 'New Criteria Set' }}</h2>
        <button @click="emit('close')" class="text-taupe hover:text-mine">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="p-6 space-y-6 max-h-[70vh] overflow-y-auto">
        <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-600">
          {{ error }}
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-taupe mb-2">Name</label>
            <input
              v-model="name"
              type="text"
              placeholder="e.g., Grant Proposal Evaluation"
              class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-taupe mb-2">Description (optional)</label>
            <input
              v-model="description"
              type="text"
              placeholder="Brief description"
              class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
            />
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-4">
            <label class="text-sm font-medium text-taupe">Criteria</label>
            <div :class="['text-xs', totalWeight === 100 ? 'text-green-600' : 'text-amber-600']">
              Total weight: {{ totalWeight }}%
            </div>
          </div>

          <div class="space-y-4">
            <div
              v-for="(criterion, index) in criteria"
              :key="index"
              class="p-4 bg-gray-50 rounded-lg"
            >
              <div class="flex items-start gap-4">
                <div class="flex-1 grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-xs text-taupe mb-1">Name</label>
                    <input
                      v-model="criterion.name"
                      type="text"
                      placeholder="e.g., Scientific Merit"
                      class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
                    />
                  </div>
                  <div>
                    <label class="block text-xs text-taupe mb-1">Description</label>
                    <input
                      v-model="criterion.description"
                      type="text"
                      placeholder="What to evaluate"
                      class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
                    />
                  </div>
                  <div>
                    <label class="block text-xs text-taupe mb-1">Weight (%)</label>
                    <input
                      v-model.number="criterion.weight"
                      type="range"
                      min="0"
                      max="100"
                      class="w-full"
                    />
                    <div class="text-xs text-center text-mine">{{ criterion.weight }}%</div>
                  </div>
                  <div>
                    <label class="block text-xs text-taupe mb-1">Max Score</label>
                    <select
                      v-model.number="criterion.maxScore"
                      class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
                    >
                      <option :value="5">1-5</option>
                      <option :value="10">1-10</option>
                    </select>
                  </div>
                </div>
                <button
                  v-if="criteria.length > 1"
                  @click="removeCriterion(index)"
                  class="p-2 text-taupe hover:text-red-600"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <button
            @click="addCriterion"
            class="mt-4 w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-sm text-taupe hover:border-shiraz/50 hover:text-shiraz transition-colors"
          >
            + Add Criterion
          </button>
        </div>
      </div>

      <div class="px-6 py-4 border-t border-gray-200 flex justify-end gap-2">
        <Button variant="secondary" @click="emit('close')">Cancel</Button>
        <Button @click="handleSave" :disabled="saving">
          {{ saving ? (isEditing ? 'Saving...' : 'Creating...') : (isEditing ? 'Save' : 'Create') }}
        </Button>
      </div>
    </div>
  </div>
</template>
