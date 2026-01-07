import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { CriteriaSet } from '@/types'
import { criteriaService } from '@/services/criteria.service'

export const useCriteriaStore = defineStore('criteria', () => {
  const criteriaSets = ref<CriteriaSet[]>([])
  const templates = ref<CriteriaSet[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const generating = ref(false)
  const generationError = ref<string | null>(null)

  async function fetchCriteriaSets() {
    loading.value = true
    error.value = null
    try {
      criteriaSets.value = await criteriaService.list()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch criteria sets'
    } finally {
      loading.value = false
    }
  }

  async function fetchTemplates() {
    try {
      templates.value = await criteriaService.listTemplates()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch templates'
    }
  }

  async function createCriteriaSet(data: Omit<CriteriaSet, 'id' | 'createdAt'>) {
    const criteriaSet = await criteriaService.create(data)
    criteriaSets.value.unshift(criteriaSet)
    return criteriaSet
  }

  async function useTemplate(templateId: string, name: string) {
    const template = templates.value.find((t) => t.id === templateId)
    if (!template) throw new Error('Template not found')
    return createCriteriaSet({
      name,
      description: template.description,
      criteria: template.criteria,
    })
  }

  async function updateCriteriaSet(id: string, data: Omit<CriteriaSet, 'id' | 'createdAt'>) {
    const updated = await criteriaService.update(id, data)
    const index = criteriaSets.value.findIndex((c) => c.id === id)
    if (index !== -1) {
      criteriaSets.value[index] = updated
    }
    return updated
  }

  async function deleteCriteriaSet(id: string) {
    await criteriaService.delete(id)
    criteriaSets.value = criteriaSets.value.filter((c) => c.id !== id)
  }

  function getCriteriaSet(id: string) {
    return criteriaSets.value.find((c) => c.id === id)
  }

  async function generateCriteriaFromDocument(file: File, name: string) {
    generating.value = true
    generationError.value = null
    try {
      const criteriaSet = await criteriaService.generateFromDocument(file, name)
      criteriaSets.value.unshift(criteriaSet)
      return criteriaSet
    } catch (e) {
      generationError.value = e instanceof Error ? e.message : 'Failed to generate criteria'
      throw e
    } finally {
      generating.value = false
    }
  }

  async function generateCriteriaFromText(text: string, name: string) {
    generating.value = true
    generationError.value = null
    try {
      const criteriaSet = await criteriaService.generateFromText(text, name)
      criteriaSets.value.unshift(criteriaSet)
      return criteriaSet
    } catch (e) {
      generationError.value = e instanceof Error ? e.message : 'Failed to generate criteria'
      throw e
    } finally {
      generating.value = false
    }
  }

  return {
    criteriaSets,
    templates,
    loading,
    error,
    generating,
    generationError,
    fetchCriteriaSets,
    fetchTemplates,
    createCriteriaSet,
    useTemplate,
    updateCriteriaSet,
    deleteCriteriaSet,
    getCriteriaSet,
    generateCriteriaFromDocument,
    generateCriteriaFromText,
  }
})
