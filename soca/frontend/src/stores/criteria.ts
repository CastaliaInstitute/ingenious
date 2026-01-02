import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { CriteriaSet } from '@/types'
import { criteriaService } from '@/services/criteria.service'

export const useCriteriaStore = defineStore('criteria', () => {
  const criteriaSets = ref<CriteriaSet[]>([])
  const templates = ref<CriteriaSet[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

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
    const template = templates.value.find(t => t.id === templateId)
    if (!template) throw new Error('Template not found')
    return createCriteriaSet({
      name,
      description: template.description,
      criteria: template.criteria
    })
  }

  function getCriteriaSet(id: string) {
    return criteriaSets.value.find(c => c.id === id)
  }

  return {
    criteriaSets,
    templates,
    loading,
    error,
    fetchCriteriaSets,
    fetchTemplates,
    createCriteriaSet,
    useTemplate,
    getCriteriaSet
  }
})
