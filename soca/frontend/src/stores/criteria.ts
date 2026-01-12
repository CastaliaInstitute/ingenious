import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { CriteriaSet } from '@/types'
import { criteriaService } from '@/services/criteria.service'

/**
 * Pinia store for managing evaluation criteria sets.
 * Handles CRUD operations, templates, and AI-powered generation.
 */
export const useCriteriaStore = defineStore('criteria', () => {
  const criteriaSets = ref<CriteriaSet[]>([])
  const templates = ref<CriteriaSet[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const generating = ref(false)
  const generationError = ref<string | null>(null)

  /**
   * Fetches all user-created criteria sets from the API.
   */
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

  /**
   * Fetches all predefined criteria templates.
   */
  async function fetchTemplates() {
    try {
      templates.value = await criteriaService.listTemplates()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch templates'
    }
  }

  /**
   * Creates a new criteria set.
   * @param data - The criteria set data without id and createdAt.
   * @returns The created criteria set.
   */
  async function createCriteriaSet(data: Omit<CriteriaSet, 'id' | 'createdAt'>) {
    const criteriaSet = await criteriaService.create(data)
    criteriaSets.value.unshift(criteriaSet)
    return criteriaSet
  }

  /**
   * Creates a new criteria set from a template.
   * @param templateId - The template identifier to copy from.
   * @param name - The name for the new criteria set.
   * @returns The created criteria set.
   */
  async function useTemplate(templateId: string, name: string) {
    const template = templates.value.find((t) => t.id === templateId)
    if (!template) throw new Error('Template not found')
    return createCriteriaSet({
      name,
      description: template.description,
      criteria: template.criteria,
    })
  }

  /**
   * Updates an existing criteria set.
   * @param id - The criteria set identifier.
   * @param data - The updated criteria set data.
   * @returns The updated criteria set.
   */
  async function updateCriteriaSet(id: string, data: Omit<CriteriaSet, 'id' | 'createdAt'>) {
    const updated = await criteriaService.update(id, data)
    const index = criteriaSets.value.findIndex((c) => c.id === id)
    if (index !== -1) {
      criteriaSets.value[index] = updated
    }
    return updated
  }

  /**
   * Deletes a criteria set.
   * @param id - The criteria set identifier to delete.
   */
  async function deleteCriteriaSet(id: string) {
    await criteriaService.delete(id)
    criteriaSets.value = criteriaSets.value.filter((c) => c.id !== id)
  }

  /**
   * Retrieves a criteria set by ID from the local store.
   * @param id - The criteria set identifier.
   * @returns The criteria set if found.
   */
  function getCriteriaSet(id: string) {
    return criteriaSets.value.find((c) => c.id === id)
  }

  /**
   * Generates criteria from an uploaded document using AI.
   * @param file - The document file to analyze.
   * @param name - The name for the generated criteria set.
   * @returns The generated criteria set.
   */
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

  /**
   * Generates criteria from text content using AI.
   * @param text - The document text to analyze.
   * @param name - The name for the generated criteria set.
   * @returns The generated criteria set.
   */
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
