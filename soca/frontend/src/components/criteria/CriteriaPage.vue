<script setup lang="ts">
  /**
   * CriteriaPage component for managing evaluation criteria sets.
   * Displays user criteria sets and templates with CRUD functionality.
   */
  import { onMounted, ref } from 'vue'
  import { useCriteriaStore } from '@/stores/criteria'
  import Button from '@/components/common/Button.vue'
  import CriteriaSetCard from './CriteriaSetCard.vue'
  import TemplateCard from './TemplateCard.vue'
  import CriteriaBuilderModal from './CriteriaBuilderModal.vue'
  import CriteriaGeneratorModal from './CriteriaGeneratorModal.vue'
  import type { CriteriaSet } from '@/types'

  const criteriaStore = useCriteriaStore()
  const showBuilder = ref(false)
  const showGenerator = ref(false)
  const editingCriteriaSet = ref<CriteriaSet | null>(null)

  onMounted(() => {
    criteriaStore.fetchCriteriaSets()
    criteriaStore.fetchTemplates()
  })

  /**
   * Creates a new criteria set from a template.
   * @param templateId - The template identifier to copy from.
   */
  function handleUseTemplate(templateId: string) {
    const name = prompt('Enter a name for the new criteria set:')
    if (name) {
      criteriaStore.useTemplate(templateId, name)
    }
  }

  /**
   * Opens the builder modal to edit a criteria set.
   * @param criteriaSet - The criteria set to edit.
   */
  function handleEdit(criteriaSet: CriteriaSet) {
    editingCriteriaSet.value = criteriaSet
    showBuilder.value = true
  }

  /**
   * Deletes a criteria set after confirmation.
   * @param id - The criteria set identifier to delete.
   */
  function handleDelete(id: string) {
    if (confirm('Are you sure you want to delete this criteria set?')) {
      criteriaStore.deleteCriteriaSet(id)
    }
  }

  /**
   * Closes the builder modal and clears the editing state.
   */
  function handleCloseBuilder() {
    showBuilder.value = false
    editingCriteriaSet.value = null
  }

  /**
   * Closes the generator modal.
   */
  function handleGeneratorClose() {
    showGenerator.value = false
  }

  /**
   * Handles successful criteria generation by opening the result for editing.
   * @param criteriaSetId - The generated criteria set identifier.
   */
  function handleGenerated(criteriaSetId: string) {
    showGenerator.value = false
    // Optionally open the criteria set for editing
    const criteriaSet = criteriaStore.getCriteriaSet(criteriaSetId)
    if (criteriaSet) {
      handleEdit(criteriaSet)
    }
  }
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-xl font-semibold text-mine">Criteria</h1>
        <p class="text-sm text-taupe mt-1">Define evaluation criteria sets</p>
      </div>
      <div class="flex gap-2">
        <Button variant="secondary" @click="showGenerator = true"> Generate from Document </Button>
        <Button @click="showBuilder = true">New Criteria Set</Button>
      </div>
    </div>

    <div v-if="criteriaStore.criteriaSets.length > 0" class="mb-8">
      <h2 class="text-sm font-medium text-taupe uppercase tracking-wide mb-4">
        Your Criteria Sets
      </h2>
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

    <CriteriaGeneratorModal
      v-if="showGenerator"
      @close="handleGeneratorClose"
      @generated="handleGenerated"
    />
  </div>
</template>
