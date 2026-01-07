<script setup lang="ts">
  import { ref, computed } from 'vue'
  import { useCriteriaStore } from '@/stores/criteria'
  import Button from '@/components/common/Button.vue'

  const emit = defineEmits<{
    close: []
    generated: [criteriaSetId: string]
  }>()

  const criteriaStore = useCriteriaStore()

  // State
  const inputMode = ref<'file' | 'text'>('file')
  const selectedFile = ref<File | null>(null)
  const pastedText = ref('')
  const criteriaSetName = ref('')
  const generating = ref(false)
  const error = ref<string | null>(null)

  // File handling
  const fileInput = ref<HTMLInputElement>()
  const isDragging = ref(false)
  const acceptedTypes = '.pdf,.docx,.txt'

  // Computed
  const canGenerate = computed(() => {
    if (!criteriaSetName.value.trim()) return false
    if (inputMode.value === 'file') return !!selectedFile.value
    return pastedText.value.trim().length >= 50
  })

  // Methods
  function handleDragOver(e: DragEvent) {
    e.preventDefault()
    isDragging.value = true
  }

  function handleDragLeave() {
    isDragging.value = false
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault()
    isDragging.value = false

    const files = e.dataTransfer?.files
    if (files && files.length > 0) {
      const file = files[0]
      if (isValidFileType(file)) {
        selectedFile.value = file
        error.value = null
      } else {
        error.value = 'Please upload a PDF, DOCX, or TXT file'
      }
    }
  }

  function isValidFileType(file: File): boolean {
    const validTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain',
    ]
    const validExtensions = ['.pdf', '.docx', '.txt']
    return (
      validTypes.includes(file.type) ||
      validExtensions.some((ext) => file.name.toLowerCase().endsWith(ext))
    )
  }

  function handleFileSelect(e: Event) {
    const target = e.target as HTMLInputElement
    const files = target.files
    if (files && files.length > 0) {
      selectedFile.value = files[0]
      error.value = null
    }
  }

  function clearFile() {
    selectedFile.value = null
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }

  function triggerFileSelect() {
    fileInput.value?.click()
  }

  async function handleGenerate() {
    if (!canGenerate.value) return

    generating.value = true
    error.value = null

    try {
      let criteriaSet
      if (inputMode.value === 'file' && selectedFile.value) {
        criteriaSet = await criteriaStore.generateCriteriaFromDocument(
          selectedFile.value,
          criteriaSetName.value.trim()
        )
      } else {
        criteriaSet = await criteriaStore.generateCriteriaFromText(
          pastedText.value.trim(),
          criteriaSetName.value.trim()
        )
      }
      emit('generated', criteriaSet.id)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to generate criteria'
    } finally {
      generating.value = false
    }
  }
</script>

<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 overflow-y-auto py-8">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-mine">Generate Criteria from Document</h2>
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

      <div class="p-6 space-y-6">
        <!-- Error display -->
        <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-600">
          {{ error }}
        </div>

        <!-- Name input -->
        <div>
          <label class="block text-sm font-medium text-taupe mb-2">Criteria Set Name</label>
          <input
            v-model="criteriaSetName"
            type="text"
            placeholder="e.g., Generated from RFP Document"
            class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz"
          />
        </div>

        <!-- Input mode toggle -->
        <div class="flex gap-2">
          <button
            :class="[
              'px-4 py-2 rounded-md text-sm font-medium transition-colors',
              inputMode === 'file'
                ? 'bg-shiraz text-white'
                : 'bg-gray-100 text-taupe hover:bg-gray-200',
            ]"
            @click="inputMode = 'file'"
          >
            Upload File
          </button>
          <button
            :class="[
              'px-4 py-2 rounded-md text-sm font-medium transition-colors',
              inputMode === 'text'
                ? 'bg-shiraz text-white'
                : 'bg-gray-100 text-taupe hover:bg-gray-200',
            ]"
            @click="inputMode = 'text'"
          >
            Paste Text
          </button>
        </div>

        <!-- File upload mode -->
        <div v-if="inputMode === 'file'">
          <!-- Dropzone -->
          <div
            v-if="!selectedFile"
            :class="[
              'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
              isDragging ? 'border-shiraz bg-shiraz/5' : 'border-gray-300 hover:border-shiraz/50',
            ]"
            @dragover="handleDragOver"
            @dragleave="handleDragLeave"
            @drop="handleDrop"
            @click="triggerFileSelect"
          >
            <input
              ref="fileInput"
              type="file"
              :accept="acceptedTypes"
              class="hidden"
              @change="handleFileSelect"
            />
            <svg
              class="w-12 h-12 mx-auto text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p class="text-sm text-taupe mb-1">Drop your document here, or click to browse</p>
            <p class="text-xs text-gray-400">Supports PDF, DOCX, and TXT files</p>
          </div>

          <!-- Selected file display -->
          <div v-else class="p-4 bg-gray-50 rounded-lg flex items-center justify-between">
            <div class="flex items-center gap-3">
              <svg
                class="w-8 h-8 text-shiraz"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <div>
                <p class="text-sm font-medium text-mine">{{ selectedFile.name }}</p>
                <p class="text-xs text-gray-400">{{ (selectedFile.size / 1024).toFixed(1) }} KB</p>
              </div>
            </div>
            <button class="text-taupe hover:text-red-600 p-2" @click="clearFile">
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
        </div>

        <!-- Text paste mode -->
        <div v-if="inputMode === 'text'">
          <textarea
            v-model="pastedText"
            rows="10"
            placeholder="Paste document text here (minimum 50 characters)..."
            class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-shiraz/20 focus:border-shiraz resize-none"
          />
          <p class="mt-1 text-xs text-gray-400">
            {{ pastedText.length }} characters
            <span v-if="pastedText.length > 0 && pastedText.length < 50" class="text-amber-600">
              (minimum 50 required)
            </span>
          </p>
        </div>

        <!-- Info message -->
        <div class="p-3 bg-blue-50 border border-blue-200 rounded text-sm text-blue-700">
          The AI will analyze your document and extract relevant evaluation criteria. This may take
          a few moments.
        </div>
      </div>

      <!-- Footer -->
      <div class="px-6 py-4 border-t border-gray-200 flex justify-end gap-2">
        <Button variant="secondary" @click="emit('close')">Cancel</Button>
        <Button :disabled="!canGenerate || generating" @click="handleGenerate">
          <template v-if="generating">
            <svg
              class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Generating...
          </template>
          <template v-else>Generate Criteria</template>
        </Button>
      </div>
    </div>
  </div>
</template>
