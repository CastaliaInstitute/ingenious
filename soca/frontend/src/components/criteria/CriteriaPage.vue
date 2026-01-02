<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useCriteriaStore } from '@/stores/criteria'
import Button from '@/components/common/Button.vue'
import CriteriaSetCard from './CriteriaSetCard.vue'
import TemplateCard from './TemplateCard.vue'
import CriteriaBuilderModal from './CriteriaBuilderModal.vue'
import type { CriteriaSet } from '@/types'

const criteriaStore = useCriteriaStore()
const showBuilder = ref(false)
const editingCriteriaSet = ref<CriteriaSet | null>(null)

onMounted(() => {
  criteriaStore.fetchCriteriaSets()
  criteriaStore.fetchTemplates()
})

function handleUseTemplate(templateId: string) {
  const name = prompt('Enter a name for the new criteria set:')
  if (name) {
    criteriaStore.useTemplate(templateId, name)
  }
}

function handleEdit(criteriaSet: CriteriaSet) {
  editingCriteriaSet.value = criteriaSet
  showBuilder.value = true
}

function handleDelete(id: string) {
  if (confirm('Are you sure you want to delete this criteria set?')) {
    criteriaStore.deleteCriteriaSet(id)
  }
}

function handleCloseBuilder() {
  showBuilder.value = false
  editingCriteriaSet.value = null
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-xl font-semibold text-mine">Criteria</h1>
        <p class="text-sm text-taupe mt-1">Define evaluation criteria sets</p>
      </div>
      <Button @click="showBuilder = true">New Criteria Set</Button>
    </div>

    <div v-if="criteriaStore.criteriaSets.length > 0" class="mb-8">
      <h2 class="text-sm font-medium text-taupe uppercase tracking-wide mb-4">Your Criteria Sets</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <CriteriaSetCard
          v-for="criteriaSet in criteriaStore.criteriaSets"
          :key="criteriaSet.id"
          :criteria-set="criteriaSet"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </div>
    </div>

    <div>
      <h2 class="text-sm font-medium text-taupe uppercase tracking-wide mb-4">Templates</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <TemplateCard
          v-for="template in criteriaStore.templates"
          :key="template.id"
          :template="template"
          @use="handleUseTemplate(template.id)"
        />
      </div>
    </div>

    <CriteriaBuilderModal
      v-if="showBuilder"
      :editing-criteria-set="editingCriteriaSet"
      @close="handleCloseBuilder"
    />
  </div>
</template>
